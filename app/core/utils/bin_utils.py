# coding=u8


def bin_and(arg, *args):
    if not args and arg and isinstance(arg, (list, tuple)):
        arg, args = arg[0], arg[1:]
    arg, args = _filter_args(arg, *args)
    for _arg in args:
        arg &= _arg
    return arg


def _filter_args(*args):
    args = [_arg for _arg in args if _arg is not None]
    if not args:
        return None, []
    return args[0], args[1:]


def bin_or(arg, *args):
    if not args and arg and isinstance(arg, (list, tuple)):
        arg, args = arg[0], arg[1:]
    arg, args = _filter_args(arg, *args)
    for _arg in args:
        arg |= _arg
    return arg