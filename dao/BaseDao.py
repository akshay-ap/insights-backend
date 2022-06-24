import abc


class BaseDao(metaclass=abc.ABCMeta):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BaseDao, cls).__new__(cls, *args, **kwargs)
        return cls._instance
