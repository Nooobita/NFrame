# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import peewee

from app.core.n_import.import_utils import import_types

from app import db_n

from app.core.n_model.model_utils import ModelAppendId, SnakeNameModel


class BaseModel(SnakeNameModel, ModelAppendId):
    class Meta:
        database = db_n


def _append_model(model):
    globals()[model.__name__] = model
    return model


import_types(
    file_suffix='_models',
    target_type=peewee.Model,
    decorators=[_append_model]
)