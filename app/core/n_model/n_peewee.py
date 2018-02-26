# coding=u8

import peewee
from app.core.utils.bin_utils import bin_or

from playhouse.shortcuts import *


def _get_or_none(self):
    try:
        return self.get()
    except peewee.DoesNotExist as e:
        return None


def _no_deleted(q, field_name='delete_at'):
    model_class = q.model_class
    field = getattr(model_class, field_name, None)
    if not field:
        return q
    condi = []
    if isinstance(field, (peewee.FloatField, peewee.IntegerField)):
        condi.append(field == 0)
    elif isinstance(field, peewee.DateField):
        condi.append(field == '0001-01-01')
    elif isinstance(field, peewee.DateTimeField):
        condi.append(field == '0001-01-01 00:00:00')
    if field.null:
        condi.append(field >> None)
    if not condi:
        return q
    return q.filter(bin_or(condi))


peewee.SelectQuery.get_or_none = _get_or_none
peewee.Query.no_deleted = _no_deleted()


class NBaseModel(peewee.Model):

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def from_dict(cls, data, ignore_unknown=True):
        return dict_to_model(cls, data, ignore_unknown=ignore_unknown)
