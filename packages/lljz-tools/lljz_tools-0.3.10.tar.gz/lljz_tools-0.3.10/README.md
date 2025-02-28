## 简介
包含了一些常用方法的封装，安装方法
```
pip install lljz_tools
```
内含
- 控制台表格
- 常用装饰器
- 彩色日志
- 内置print猴子补丁
- 属性字典
- requirements.txt生成工具
- 快速的Excel读写操作
- 随机数工具
- 支持连接池管理的数据库连接、MongoDB连接
- 更易用的HTTPClient，适用于自动化测试
- 

更多功能正在开发中...
## 控制台表格
目前已有的控制台表格大部分都不支持中文，本表格能完美支持中文（PS：请使用等宽字符，否则效果不完美）
```python
from my_tools.console_table import ConsoleTable

# 数据必须满足list[dict]格式
table = ConsoleTable([{"name": "Tom", "age": 13}])
table.show()
# print(table)  # 直接打印
```
输出结果
```
   name    |      b    
=======================
    Tom    |      2    
   Lucy    |      4 
```
## 常用装饰器

```python
import logging
from lljz_tools.decorators import catch_exception, time_cache, debug, timer 


# catch_exception用于自动捕获异常，并支持传入指定logger来记录日志, 支持自动重试
@catch_exception
def f():
    raise ValueError


logger = logging.getLogger()

@catch_exception(logger)  # 如果不指定logger，将会自动采用默认logger记录异常堆栈
def f1():
    raise ValueError


@catch_exception(retry=3, interval=0.5)  # 如果失败，重试3次，每次重试间隔0.5s   
def f1():
    raise ValueError


@time_cache(3)   # 缓存结果，最多缓存3秒
def f1(n):
   for _ in range(n):
        pass 

@debug    # 在控制台中将函数运行日志、运行结果、运行耗时等数据自动用logger输出
def f1():
    pass 

@timer   # 自动统计函数运行耗时
def f1():  
    pass
```

## 彩色日志
```python
from lljz_tools.log_manager import LogManager

# 自动打印彩色日志，自动添加文件handler，日志文件自动按天分割
logger = LogManager("your logger name").get_logger()


logger.info("info")
logger.debug("debug")
logger.error("info")
```

# print猴子补丁
添加猴子补丁之后，print自动变更为日志格式，且会显示print代码所在的行数

```python
from my_tools.track_print import patch_print

patch_print()  # 给print添加猴子补丁
```

# 属性字典
属性字典支持用`.`的格式访问数据，支持只读模式
```python
from lljz_tools import Model
# IgnoreCaseAttributeDict支持忽略大小写来访问数据

class Book(Model):
    name: str 
    author: str 
    price: float = 0.1  

    __show__ = 'name author'

book = Book(name='python', author='guido', price=0.1)
assert isinstance(book, dict)
print(book)
print(book.name)


class User(Model, readonly=True):
    # __config__ = {'readonly': True}  # 配置的另一种写法
    
    name: str 
    age: int 
    books: list[Book]
    
    __show__ = ('name', 'book')  # __show__参数决定在print时展示的字段，默认为全部字段

user = User(name='Tom', age=1, books=[{'name': 'python', 'author': 'guido', 'price': 0.1}]) # OK
print(user)
user.name = 'Hic'  # error, User is readonly
user.books[0].name = 'java'  # ok, book is not readonly
```

