# coding=u8


from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging
import os
import os.path as osp
import sys
import yaml


APP_NAME = 'n'

# 屏蔽登录请求！！！
LOGIN_IGNORE = True

# 项目根目录
PROJECT_ROOT = osp.dirname(osp.abspath(__file__))
STATIC_FOLDER = 'static'

# 需要加入到sys.path的目录列表
EXTENTIONS_DIRECTORIES = [
    '../pycomm',
    '../zhijian_server_pyutils',
]

# WEB服务器配置
SVR_CONFIG = dict(
    host='0.0.0.0',
    port=8888,
    debug=True,
)

# Flask的额外配置
# 参考：http://flask.pocoo.org/docs/0.12/config/#builtin-configuration-values
SVR_FLASK_CONFIG = dict()

# session信息配置
SESSION = dict(
    name      = 'zjsess',  # 客户端cookie名
    key_pairs = 'helloworld',  # cookie校验密钥
    prefix    = 'session_',  # redis保存前缀
    tmp_age   = 3600,  # 默认cookie保存时间
    max_age   = 3600 * 24 * 7,  # 默认cookie最大保存时间
    redis     = None,
)

# redis配置
REDIS = None

# 数据库配置
DATABASES = dict(
    zj3 = dict(
        engine = 'mysql',
        database = 'zhijian2',
        params = dict(
            host = '127.0.0.1', port = 3306, user = 'root', password = ''),
        pool = dict(),
    ),
    zj3user = dict(
        engine = 'mysql',
        database = 'zhijian_user',
        params = dict(
            host = '127.0.0.1', port = 3306, user = 'root', password = ''),
    )
)

# 日志配置，default为zjutils.logger默认使用的日志名称
LOGGING_CONFIG = {
    'default': 'app',
    'app': dict(
        level        = logging.DEBUG,
        datefmt      = '%Y-%m-%d %H:%M:%S',
        enable_color = True,
        format       = [
            '[',
            '%(name)s',
            '|%(asctime)s|%(filename)s:%(lineno)s(%(funcName)s)|',
            '%(levelname)s',
            ']%(message)s',
        ],
    ),
}

# apilist路径，默认不开启
APILIST_PATH = None
# 请求远端api服务的地址，仅在APILIST_PATH已设置的情况下有效
REMOTE_APILIST_PATH = None

# 显示路由信息
LIST_ROUTES = True

INNER_API = {}

# 登录路径
LOGIN_PATH = '/login'

FILE_STORE_PATH = '/data/zhijian/'

CTX_ID = '__ctx_id__'


def _load_config():

    global _custom_cfgs
    config_file = os.environ.get('CONFIG_FILE', None)
    argv = sys.argv[1:]
    argv_len = len(argv)

    for i, arg in enumerate(argv):
        if arg == '-c' and i + 1 <= argv_len:
            config_file = argv[i + 1]
            break
        if arg.startswith('--config_file='):
            config_file = arg.split('=', 1)[1]
            break
    if config_file:
        print('>>>>>>> load config file', config_file)
        with open(config_file, 'rb') as fr:
            cfg = yaml.load(fr)
        for k, v in cfg.items():
            _custom_cfgs[k.upper()] = v


_custom_cfgs = {}
_load_config()
globals().update(_custom_cfgs)
del _custom_cfgs

for index, directory in enumerate(EXTENTIONS_DIRECTORIES):
    sys.path.insert(index + 1, directory)