# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from datetime import datetime

from app.core.utils import strings
from .n_peewee import NBaseModel


class ModelAppendId(object):

    @property
    def _id(self):
        return getattr(self, 'id', 0)


def snake_model_name(m):
    return strings.snake_case_name(m.__name__)


class SnakeNameModel(NBaseModel):

    class Meta:
        db_table_func = snake_model_name

    @classmethod
    def n_delete(cls):
        if hasattr(cls, 'delete_at'):
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            update_kw = dict(delete_at=now)
            return cls.update(**update_kw).filter(
                (cls.delete_at.is_null(True)) |
                (cls.delete_at == '0001-01-01 00:00:00'))

        else:
            return cls.delete()

