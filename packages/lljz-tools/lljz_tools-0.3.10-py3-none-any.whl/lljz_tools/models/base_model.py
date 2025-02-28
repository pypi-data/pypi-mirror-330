import re
import types
from itertools import cycle
from typing import Any, Mapping, Self, Sequence, TypedDict, Union, get_origin, get_args, overload
from collections.abc import Iterable


class ModelConfig(TypedDict, total=False):
    """
    是否允许额外字段，默认True
    设置允许后，会自动将额外字段添加到模型中
    """
    allow_extra: bool

    """
    是否允许缺失字段，默认True
    设置允许后，缺失的字段默认被设置为None
    """
    allow_missing: bool

    """
    是否只读，默认False
    设置只读后，模型中的字段将无法被修改
    """
    readonly: bool

class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        annotations = {}
        defaults = {}
        config = {}
        
        
        # 从基类继承注解和默认值
        for base in bases:
            if hasattr(base, '__annotations__'):
                annotations.update(base.__annotations__)
            if hasattr(base, '__default__'):
                defaults.update(base.__default__)
            if hasattr(base, '__config__'):
                config.update(base.__config__)
        # 更新当前类的注解和默认值
        if '__annotations__' in attrs:
            annotations.update(attrs['__annotations__'])
        if '__default__' in attrs:
            defaults.update(attrs['__default__'])
        if '__config__' in attrs:
            config.update(attrs['__config__'])
        

        remove_keys = []
        
        for key in attrs.keys():
            if key.startswith('__'):
                continue
            if key in annotations:
                defaults[key] = attrs[key]
                remove_keys.append(key)
        
        for key in remove_keys:
            attrs.pop(key)
        
        # 设置类属性
        attrs['__annotations__'] = annotations
        attrs['__annotations__'].pop('__show__', None)
        attrs['__annotations__'].pop('__config__', None)
        attrs['__default__'] = defaults
        attrs['__config__'] = config
        attrs['__config__'].update(kwargs)
        
        return super().__new__(cls, name, bases, attrs)
    
def is_namedtuple(cls):
    """判断一个类是否为namedtuple"""
    return (
        isinstance(cls, tuple.__class__) and  # type: ignore
        hasattr(cls, '_fields')
    )

class Model(dict, metaclass=ModelMetaclass):
    __show__: str | Sequence[str] | None = None
    __config__: ModelConfig = {'allow_extra': True, 'allow_missing': True, 'readonly': False}

    @staticmethod
    def __init_value(cls_, value: Any, readonly: bool = False):
        if readonly:
            M = ReadOnlyModel
        else:
            M = Model
        if value is None:
            return None
        if cls_ is None:
            if isinstance(value, dict):
                return M(value)
            elif isinstance(value, list):
                return [M.__init_value(None, v, readonly) for v in value]
            elif isinstance(value, tuple):
                return tuple(M.__init_value(None, v, readonly) for v in value)
            elif isinstance(value, set):
                return set(M.__init_value(None, v, readonly) for v in value)
            else:
                return value
        if cls_ is dict:
            cls_ = M
        elif cls_ is Model:
            cls_ = M
        try:
            if get_origin(cls_) is Union:
                return M.__init_value(get_args(cls_)[0], value, readonly)
            elif type(cls_) is types.UnionType:
                args = getattr(cls_, '__args__', [])
                return M.__init_value(args[0], value, readonly)
            elif type(cls_) is types.GenericAlias:
                origin = getattr(cls_, '__origin__', list)
                args = getattr(cls_, '__args__', [])
                if origin is dict:
                    return M({M.__init_value(args[0], k, readonly): M.__init_value(args[1], v, readonly) for k, v in value.items()})
                else:
                    return origin((M.__init_value(c, v, readonly) for c, v in zip(cycle(args), value)))
            elif is_namedtuple(cls_):
                return cls_(*value)
            elif cls_ in (list, tuple, set):
                return cls_(value)
            else:
                return cls_(**value)
        except:
            return value

    def __init__(self, __mapper: Mapping[str, Any] | None = None, **kwargs):
        # 直接保存所有字段，包括额外字段
        all_values = {}
        if __mapper:
            kwargs.update(__mapper)
        for key, value in kwargs.items():
            cls = self.__annotations__.get(key, None)
            all_values[key] = self.__init_value(cls, value, readonly=self.__config__.get('readonly', False))
            
        for key, value in self.__default__.items():
            if key not in all_values:
                all_values[key] = value
        if not self.__config__.get('allow_extra', True):
            for key in kwargs.keys():
                if key not in self.__annotations__.keys():
                    raise ValueError(f"{self.__class__.__name__} not allow extra field '{key}'!")
         
        if self.__config__.get('allow_missing', False):
            for key in self.__annotations__.keys():
                if key not in all_values:
                    all_values[key] = None
        super().__init__(all_values)
    
    @classmethod
    def from_dict(cls, data: dict) -> Self:
        """将字典转换为模型对象"""
        if not isinstance(data, dict):
            raise ValueError(f"Expected dict, got {type(data)}")
            
        converted_data = {}
        for key, value in data.items():
            # 递归处理嵌套的数据结构
            if isinstance(value, dict):
                converted_data[key] = cls.from_dict(value)
            elif isinstance(value, list):
                converted_data[key] = cls.from_list(value)
            else:
                converted_data[key] = value
        return cls(**converted_data)
    
    @classmethod
    def from_list(cls, data: list[dict]) -> list[Self]:
        """将列表转换为模型对象列表"""
        if not isinstance(data, list):
            raise ValueError(f"Expected list, got {type(data)}")
            
        return [
            cls.from_dict(item) if isinstance(item, dict) else (cls.from_list(item) if isinstance(item, list) else item) for item in data
        ]  # type: ignore
    
    @classmethod
    @overload
    def from_object(cls, obj: dict) -> Self:
        ...
    @classmethod
    @overload
    def from_object(cls, obj: list[dict]) -> list[Self]:
        ...

    @classmethod
    @overload
    def from_object[T](cls, obj: T) -> T:
        ...
    

    @classmethod
    def from_object[V](cls, obj: dict[str, V] | list[V] | V):
        if isinstance(obj, dict):
            return cls.from_dict({k: cls.from_object(v) for k, v in obj.items()})
        elif isinstance(obj, Iterable):
            return [cls.from_object(item) for item in obj]
        else:
            return obj

    def __getitem__(self, key: Any) -> Any:
        if not self.__config__.get('allow_missing', False):
            return super().__getitem__(key)
        elif key not in self:
            return None
        return super().__getitem__(key)
    
    def __getattr__(self, key: str) -> Any:
        """支持通过属性方式访问字段"""
        try:
            return self.__getitem__(key)
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{key}'")
    
    def __setattr__(self, key: str, value: Any) -> None:
        if key.startswith('__'):
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)
    
    def __setitem__(self, key: Any, value: Any) -> None:
        if self.__config__.get('readonly', False):
            raise AttributeError(f"'{self.__class__.__name__}' object is readonly!")
        super().__setitem__(key, value)

    def __str__(self):
        show = self.__show__
        if not show:
            if self.__class__.__name__ in ('Model', 'ReadOnlyModel'):
                show = list(self.keys())
            else:
                show = list(self.__annotations__.keys())  # 显示所有字段
        if isinstance(show, str):
            show = re.split(r'[,\s]+', show.strip())
        val = ', '.join(f"{key}={self[key]!r}" for key in show if key in self)
        return f'{self.__class__.__name__}({val})'

    __repr__ = __str__

class ReadOnlyModel(Model, readonly=True):
    pass

if __name__ == "__main__":
    data = [{"id": "12321", "name": "abc"}]
    model = Model.from_list(data)
    print(model)
    print(model[0].id)
    print(model[0].name)
    # print(model.age)
    pass