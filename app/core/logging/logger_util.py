# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import logging

from .color_logging import enable_logging

__all__ = ['log', 'debug', 'info', 'warn', 'warning', 'error',
           'critical', 'exception']


class Logger(logging.Logger):

    def get_ctx_id(self):
        return None

    def _log(self, level, msg, args, exc_info=None, extra=None, stack_info=False):
        _ctx_id = self.get_ctx_id()
        _extra = dict(ctx_id='|%s' % _ctx_id if _ctx_id else '')
        if extra is None:
            extra = _extra
        elif hasattr(self, '_extra'):
            extra.update(self._extra)
        super(Logger, self)._log(level, msg, args, exc_info=exc_info, extra=extra)


LOGGER_NAME = 'app'
_logger     = None
debug       = None
info        = None
warn        = None
warning     = None
error       = None
critical    = None
log         = None
exception   = None


logging.Logger.manager.setLoggerClass(Logger)


def init(logging_config):
    global LOGGER_NAME
    global _logger, debug, info, warn, warning, error, critical, log, exception
    if logging_config:
        if 'default' in logging_config:
            LOGGER_NAME = logging_config['default']

        tcfg = logging_config.get(None, None)

        if not isinstance(tcfg, dict):
            tcfg = logging_config.get(LOGGER_NAME, None)
        if not isinstance(tcfg, dict):
            tcfg = dict(enable_color=False)
        if None not in logging_config:
            logging_config[None] = tcfg

        for name, cfg in logging_config.items():
            if name == 'default':
                continue
            if not cfg:
                continue
            if isinstance(cfg, dict):
                kwargs = cfg
            else:
                kwargs = tcfg.copy()
                kwargs['level'] = cfg
            enable_logging(name=name, **kwargs)

    _logger   = logging.getLogger(LOGGER_NAME)
    debug     = logging.debug     = _logger.debug
    info      = logging.info      = _logger.info
    warn      = logging.warn      = _logger.warning
    warning   = logging.warning   = _logger.warning
    error     = logging.error     = _logger.error
    critical  = logging.critical  = _logger.critical
    log       = logging.log       = _logger.log
    exception = logging.exception = _logger.exception

