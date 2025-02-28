from typing import Callable, Any, Iterable, Iterator, overload


class StringUtils:

    @staticmethod
    def truncate(func: Callable, data: Iterable[Any]):
        """类似于filter方法，不过遇到第一个不符合条件的数据就会退出循环。"""
        for d in data:
            if func(d):
                break
            yield d

    @staticmethod
    def strip_lines(__val: str, __arg = ' ', *args: str):
        def f(x):
            return x not in {__arg, *args}
        value = StringUtils.remove_empty(__val).splitlines()
        min_size = float('inf')
        for row in value:
            min_size = min(len(list(StringUtils.truncate(f, row))), min_size)
        return '\n'.join(v[min_size:] for v in value)

    @staticmethod
    @overload
    def remove_empty(__val: str) -> str: ...

    @staticmethod
    @overload
    def remove_empty(__val: Iterable[str]) -> Iterator[str]: ...

    @staticmethod
    def remove_empty(__val: str | Iterable[str]):
        if isinstance(__val, str):
            __val = filter(lambda x: x.strip(), __val.splitlines())
            return "\n".join(__val)
        return filter(lambda x: x.strip(), __val)

if __name__ == '__main__':
    print(StringUtils.strip_lines("""
    SELECT * FROM om_customer_order
    where id = 1 
    
    """))
