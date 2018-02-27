from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import threading

from app.core.n_api.api_utils import ApiCaller

logger = logging.getLogger(__name__)
_lock = threading.Lock()


class Method(ApiCaller):
    def __init__(self, prefix, caller_name, method_name):
        self.prefix      = prefix
        self.caller_name = caller_name
        method = 'GET'
        if method_name.endswith('_GET'):
            self.method_name, method = method_name[:-4], 'GET'
        elif method_name.endswith('_POST'):
            self.method_name, method = method_name[:-5], 'POST'
        else:
            self.method_name, method = method_name, 'GET'

        url = os.path.join(prefix, caller_name, self.method_name) + '/' \
            if prefix else None
        super(Method, self).__init__(url, method)


class MethodCaller(object):
    def __init__(self, url_prefix=None, method_klass=Method, **kwargs):
        super(MethodCaller, self).__init__()
        self._caller_name  = None
        self._url_prefix   = url_prefix
        self._method_klass = method_klass
        self._data         = {}

    def __getattribute__(self, name):
        if name.startswith('_'):
            return super(MethodCaller, self).__getattribute__(name)
        if name not in self._data:
            if self._caller_name:
                value = self._method_klass(
                    self._url_prefix, self._caller_name, name)
            else:
                value = MethodCaller(
                    self._url_prefix, self._method_klass)
                value._caller_name = name
            setattr(self, name, value)
        return self._data[name]

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super(MethodCaller, self).__setattr__(name, value)
            return
        with _lock:
            self._data[name] = value

    def __repr__(self):
        if self._caller_name:
            return '<MethodCaller: %s %s>' % (
                self._url_prefix, self._caller_name)
        return '<MethodCaller: %s>' % self._url_prefix