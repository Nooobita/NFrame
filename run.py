# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import six
from six.moves.urllib.parse import unquote

import os
import sys

if six.PY2:
    import imp
    imp.reload(sys)
    sys.setdefaultencoding('u8')
    del sys.setdefaultencoding

from flask import url_for

import config
from app.core.logging import logger_util
from app import app

logger_util.init(config.LOGGING_CONFIG)

if config.LIST_ROUTES:

    with app.test_request_context():
        output = []
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith('apilist.'):
                continue

            options = {}
            for arg in rule.arguments:
                options[arg] = '[%s]' % arg

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            output.append((rule.endpoint, unquote(url), methods))

            max_len = [
                (max([len(o[i]) for o in output]) / 4 + 2) * 4 for i in range(3)]
            for (endpoint, url, methods) in sorted(output):
                logger_util.debug('%-{0}s %s'.format(*max_len) %
                                   (endpoint, url))

if __name__ == '__main__':
    svr_cfg = dict(**config.SVR_CONFIG)
    if os.environ.get('SUBLIMETEXT'):
        logger_util.debug('disable flask debug')
        svr_cfg['debug'] = False
    app.run(**svr_cfg)
