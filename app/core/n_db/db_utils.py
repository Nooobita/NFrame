# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six

import logging

from playhouse import pool

logger = logging.getLogger(__name__)


class DbCfg(object):
    def __init__(self, name, db_cfg):
        super(DbCfg, self).__init__()
        db_cfg = db_cfg[name]
        self.name = name
        self.engine = db_cfg['engine']
        self.database = db_cfg['database']
        self.params = dict(
            stale_timeout = 60 * 60,
            timeout = 10,
            autorollback= True
        )
        self.params.update(**db_cfg.get('pool', {}))
        self.params.update(db_cfg['params'])

    def init_db(self, app=None):
        if self.engine == 'mysql':
            db = pool.PooledMySQLDatabase(self.database, **self.params)

            if app:
                @app.before_request
                def _db_connect():
                    if db.is_closed():
                        logger.info('db %s connect' % self.name)
                        db.connect()

                @app.teardown_request
                def _db_close(exec):
                    if not db.is_closed():
                        logger.info('db %s close' % self.name)
                        db.close()
            return db
        raise Exception('Unknown engine "%s"' % self.engine)
