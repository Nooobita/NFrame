# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

# from .method_caller import MethodCaller
from app.core.n_api.method_caller import MethodCaller

logger = logging.getLogger(__name__)

_caller = MethodCaller(None)


def init(params):
    global _caller
    _caller = MethodCaller(**params)


def check_project_permission(user_id, proj_id, per_title):
    r = _caller.inner.project_permission(
        user_id=user_id, proj_id=proj_id, per_title=per_title)
    return r and r.ok and r.data.get('has_per') == 1

