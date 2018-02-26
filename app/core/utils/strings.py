# coding=u8

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import six


def is_char_lower(c):
    return 96 < ord(c) < 123


def is_char_upper(c):
    return 64 < ord(c) < 91


def is_char_letter(c):
    return is_char_lower(c) or is_char_upper(c)


def snake_case_name(name):
    assert isinstance(name, six.string_types)
    s = []
    for i, c in enumerate(name):
        if is_char_upper(c):
            if i > 0:
                s.append('_')
            s.append(c.lower())
        else:
            s.append(c)
    return ''.join(s)