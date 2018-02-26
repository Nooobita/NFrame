# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from app.core.n_import.import_utils import import_types

# 赖加载


class _ServiceMgr(object):

    _servs = dict()

    def __getattr__(self, name):
        return self._servs[name]

    @classmethod
    def reg_service(cls, target_cls):
        name = target_cls.__name__
        if not name.endswith('Service'):
            return target_cls
        name = name[:-len('Service')]
        import re
        name = '_'.join([part.lower() for part in re.findall('[A-Z][a-z]*', name)])
        cls._servs[name] = target_cls()
        return target_cls


class ServiceCaller(object):

    _servs = _ServiceMgr()

    @property
    def servs(self):
        return self._servs


class BaseService(ServiceCaller):
    pass


import_types(
    file_suffix='_services',
    target_type=BaseService,
    decorators=[
        _ServiceMgr.reg_service
    ]
)





