# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals


import collections
import inspect

from app.core.n_constant.constant_utils import ConstGroup
from app.core.n_constant.constant_utils import Item


class Error(Exception):
    code    = 0
    message = ''

    def __init__(self, message=None):
        message = '%s|%s' % (self.message, message) \
            if message else self.message
        super(Error, self).__init__(self.code, message)
        self.code = self.code
        self.message = message

    @classmethod
    def cls(cls, name, code, message):
        new_cls = type(str(name), (cls,), dict(code=code, message=message))
        return new_cls

    @classmethod
    def clsf(cls, code, message):
        return ErrorDef(cls, code, message)

    @classmethod
    def _enum_item(cls, name, code, message):
        return Item(code, cls.cls(name, code, message))

    def __str__(self):
        s = '<Error[%s]%s>' % (self.code, self.message)
        return str(s)

    def to_dict(self):
        return dict(code=self.code, message=self.message)


class ErrorDef(object):
    def __init__(self, error_cls, code, message):
        self.error_cls = error_cls
        self.code      = code
        self.message   = message

    def get_error(self, name):
        return type(str(name), (self.error_cls,),
                    dict(code=self.code, message=self.message))


class ErrorNum(ConstGroup):
    UN_KNOWN        = Error.clsf(-9999, '未定义错误')
    MUST_BE_STRING  = Error.clsf(1201, '必须是字符串')
    PARAMS_REQUIRED = Error.clsf(2101, '缺乏必填参数')

    # 内部API调用类异常
    ApiCallerFailed = Error.clsf(3001, '内部API调用失败')

    @classmethod
    def _get_code_map(cls):
        if not hasattr(cls, '__code_map__'):
            cls._init_cls()
        return cls.__code_map__

    @classmethod
    def get_error(cls, code, message=None):
        e = cls._get_code_map().get(code, cls.UN_KNOWN)
        if e == cls.UN_KNOWN:
            return e(message) if message else e
        message = (message or '').split('|', 1)
        return e(message[1]) if len(message) > 1 else e

    @classmethod
    def _init_cls(cls):
        code_map = collections.OrderedDict()
        for field_name, _ in inspect.getmembers(cls):
            field_value = getattr(cls, field_name, None)
            if isinstance(field_value, ErrorDef):
                field_value = field_value.get_error(field_name)
                setattr(cls, field_name, field_value)
            if not (isinstance(field_value, type) and
                    issubclass(field_value, Error)):
                continue
            if field_value.code in code_map:
                raise ValueError('Duplicated error code %d in %s' % (
                    field_value.code, cls.__name__))
            code_map[field_value.code] = field_value
        cls.__code_map__ = code_map


ErrorNum._init_cls()
