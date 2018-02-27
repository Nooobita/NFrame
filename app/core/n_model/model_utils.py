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

    @classmethod
    def n_get_by_id(cls, id):
        if cls._meta.primary_key is not False:
            pk_field = cls._meta.primary_key
            condi = pk_field == id
            return cls.select().where(condi).no_deleted().get_or_none()
        else:
            return None

    @classmethod
    def n_search_by_ids(cls, ids):
        if cls._meta.primary_key is not False:
            pk_field = cls._meta.primary_key
            condi = pk_field << ids
            return cls.select().where(condi).no_deleted()
        else:
            return []

    def n_save(self, force_insert=False, only=None):
        pk_value = None
        if self._meta.primary_key is not False:
            pk_value = self.get_id()

        now = datetime.now()
        if pk_value:
            if hasattr(self, 'update_at'):
                self.update_at = now
        else:
            if hasattr(self, 'create_at') and self.create_at is None:
                self.create_at = now
            if hasattr(self, 'update_at') and self.update_at is None:
                self.update_at = now

        return self.save(force_insert, only)

    def n_delete_instance(self):

        return self.n_delete().where(self._pk_expr()).execute()
