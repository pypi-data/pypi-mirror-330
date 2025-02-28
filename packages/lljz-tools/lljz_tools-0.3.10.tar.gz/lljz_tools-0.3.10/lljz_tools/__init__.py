# coding=utf-8

__version__ = '0.3.10'

from .log_manager import LogManager
from .models import Model, ReadOnlyModel
from .random_tools import RandomTools


logger = LogManager('my-tools', console_level='DEBUG').get_logger()


__all__ = [
    'Model', 'ReadOnlyModel',
    'LogManager',
    'logger', 
    'RandomTools'
]
if __name__ == '__main__':
    logger.debug('debug')
    pass
