# coding=u8

from flask import Flask

import os.path as osp
import config

from app.core.n_db.db_utils import DbCfg


app = Flask(
    __name__,
    static_url_path='/%s/static' % config.APP_NAME,
    static_folder=osp.join(config.PROJECT_ROOT, config.STATIC_FOLDER)

)

app.config.update(**(config.SVR_FLASK_CONFIG or {}))


db_n = DbCfg('zj3', config.DATABASES).init_db(app)