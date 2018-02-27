# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import requests
import json

from app.core.n_error.error_utils import ErrorNum

logger = logging.getLogger(__name__)


class ApiResult(object):
    def __init__(self, result=-9999, data=None, message='', **kwargs):
        self.result    = result
        self.data      = data
        self.message   = message
        self.extra_msg = kwargs
        self.ok        = result == 0

    def to_dict(self):
        return dict(
            ok        = self.ok,
            result    = self.result,
            data      = self.data,
            message   = self.message,
            extra_msg = self.extra_msg,
        )

    @property
    def correct_data(self):
        '''正确时的请求结果，失败的话会抛出'''
        if not self.ok:
            logger.debug(self.__dict__)
            raise ErrorNum.get_error(self.result, message=self.message)
        return self.data


class ApiCaller(object):
    def __init__(self,url, method='GET'):
        super(ApiCaller, self).__init__()

        self.url = url
        self.method = method
        self.result = None
        self.err = None

    def __call__(self, **params):
        if self.method == 'POST':
            return self.post(data=params)
        return self.get(params=params)

    def call(self, **kwargs):
        if self.method == 'POST':
            return self.post(**kwargs)
        return self.get(**kwargs)

    def get(self, **kwargs):
        return self._do(requests.get, **kwargs)

    def post(self, **kwargs):
        return self._do(requests.post, **kwargs)

    def _do(self, req, *args, **kwargs):
        self.result = None
        self.err = None
        if not self.url:
            return None
        try:
            logger.debug(self.url)
            self.result = r = req(self.url, *args, **kwargs)
            r.raise_for_status()
            data = r.json()
            result = ApiResult(**data)
            if not result.ok:
                logger.error('错误[%d]：%s %s\n%s' % (
                    result.result, result.message, self.url, result.extra_msg))
            return result
        except requests.RequestException as err:
            self.err = err
            logger.error('请求失败')
            if 'r' in locals():
                logger.debug(r.text)
            raise ErrorNum.ApiCallerFailed
        except json.JSONDecodeError as err:
            self.err = err
            logger.error('响应解码失败')
            logger.debug(r.text)
            raise ErrorNum.ApiCallerFailed

    def __repr__(self):
        return '<ApiCaller[%s]: %s>' % (
            self.method, self.url)
