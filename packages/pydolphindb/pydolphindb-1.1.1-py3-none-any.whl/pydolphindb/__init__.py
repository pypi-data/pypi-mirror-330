from .connection import Connection as connect
from .exceptions import Error
from .sqlalchemy import DolphinDBDialect

# from .enginespec import DolphinDBEngineSpec

__all__ = [
    connect,
    Error,
    DolphinDBDialect,
]

__version__ = "1.1.1"  # pydolphindb version

apilevel = "2.0"  # DBapi2.0
threadsafety = 0  # thread safety level, need to check & modify
paramstyle = "format"  # param style for Engine URL
