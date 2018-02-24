# coding=u8

__all__ = ['load_contents', 'TypeFilter', 'InstaneFielter', 'import_types']


def load_contents(root_path, file_suffix, package, obj_filter, locals_dict, all_list, decorators=[]):
    import os
    import importlib
    