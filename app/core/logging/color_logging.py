# coding=utf-8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import six

import logging
import platform
import sys

__all__ = ['enable_logging']

SP_KEY = '[\x1bANSI_COLOR]'


class ColorFormatter(logging.Formatter):

    def format(self, record):
        """
        Format the specified record as text.

        The record's attribute dictionary is used as the operand to a
        string formatting operation which yields the returned string.
        Before formatting the dictionary, a couple of preparatory steps
        are carried out. The message attribute of the record is computed
        using LogRecord.getMessage(). If the formatting string uses the
        time (as determined by a call to usesTime(), formatTime() is
        called to format the event time. If there is exception information,
        it is formatted using formatException() and appended to the message.
        """
        record.message = record.getMessage()
        if (hasattr(self, 'usesTime()') and self.usesTime()) \
                or self._fmt.find('%(asctime)') >= 0:
            record.asctime = self.formatTime(record, self.datefmt)
        fmt = self._fmt.split(SP_KEY)
        if len(fmt) > 1 and len(fmt) % 2 != 0 \
                and platform.system() != 'Windows':
            color = self._get_color_ansi(record.levelno)
            for i, m in enumerate(fmt):
                if i % 2 == 1:
                    fmt[i] = color % m
        fmt = ''.join(fmt)
        info = record.__dict__.copy()
        info['levelname'] = record.levelname[:1]
        try:
            s = fmt % info
        except UnicodeDecodeError:  # Python2 unicode % str
            for k, v in info.items():
                if isinstance(v, bytes):
                    info[k] = repr(v)
        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            if s[-1:] != "\n":
                s = s + "\n"
            try:
                s = s + record.exc_text
            except UnicodeError:
                # Sometimes filenames have non-ASCII chars, which can lead
                # to errors when s is Unicode and record.exc_text is str
                # See issue 8924.
                # We also use replace for when there are multiple
                # encodings, e.g. UTF-8 for the filesystem and latin-1
                # for a script. See issue 13232.
                s = s + record.exc_text.decode(sys.getfilesystemencoding(),
                                               'replace')
        return s

    def _get_color_ansi(self, levelno):
        if levelno >= 50:
            color = '\x1b[31m'  # red
        elif levelno >= 40:
            color = '\x1b[31m'  # red
        elif levelno >= 30:
            color = '\x1b[33m'  # yellow
        elif levelno >= 20:
            color = '\x1b[32m'  # green
        elif levelno >= 10:
            color = '\x1b[35m'  # pink
        else:
            color = '\x1b[0m'   # normal
        color = '%s%%s\x1b[0m' % color
        return color


DEFAULT_FORMAT = ''.join([
    SP_KEY,
    '[%(asctime)s|%(filename)s:%(lineno)s(%(funcName)s)|%(levelname)s]',
    SP_KEY,
    '%(message)s'])


def enable_logging(name=None, filename=None,
                   format=None, datefmt='%y-%m-%d %H:%M:%S',
                   filemode='a', level=logging.DEBUG, stream=None,
                   enable_color=True, propagate=False, **kwargs):
    if not format:
        format  = format or DEFAULT_FORMAT
    elif isinstance(format, (list, tuple)):
        _format = []
        total = len(format)
        if total == 1:
            format = format[0]
        else:
            b = len(format) % 2
            for i, f in enumerate(format):
                if i or b == 0:
                    _format.append(SP_KEY)
                _format.append(f)
            format = ''.join(_format)

    logging._acquireLock()
    try:
        logger = logging.getLogger(name=name)
        for hdlr in logger.handlers:
            logger.removeHandler(hdlr)
        if filename:
            hdlr = logging.FileHandler(filename, filemode)
            format = format.replace(SP_KEY, '')
            _Fmt = logging.Formatter
        elif enable_color:
            hdlr = logging.StreamHandler(stream)
            _Fmt = ColorFormatter
        else:
            hdlr = logging.StreamHandler(stream)
            format = format.replace(SP_KEY, '')
            _Fmt = logging.Formatter
        fmt = _Fmt(format, datefmt)
        hdlr.setFormatter(fmt)
        logger.addHandler(hdlr)
        logger.propagate = propagate
        if level:
            level = level_by_name(level)
            hdlr.setLevel(level)
            logger.setLevel(level)
    finally:
        logging._releaseLock()


def level_by_name(name):
    if isinstance(name, six.string_types):
        return logging.getLevelName(name.upper())
    return name
