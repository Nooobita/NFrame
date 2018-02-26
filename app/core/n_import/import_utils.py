# coding=u8

__all__ = ['load_contents', 'TypeFilter', 'InstaneFielter', 'import_types']


def load_contents(root_path, file_suffix, package, obj_filter, locals_dict, all_list, decorators=[]):
    import os
    import importlib

    for src_file in os.listdir(root_path or '.'):
        if not src_file.endswith(file_suffix + '.py'):
            continue


        m = importlib.import_module(
            '.' + src_file[:-3],
            package=package
        )

        for key in dir(m):
            obj = getattr(m, key)
            if obj_filter(obj):
                for decorator in decorators:
                    obj = decorator(obj)

                locals_dict[key] = obj
                all_list.append(key)


def _import(file_suffix, filter, decorators, stack, package=None):
    import os.path as osp
    target_obj, caller_path = stack
    if not '__all__' in target_obj.f_locals:
        target_obj.f_locals['__all__'] = []
    load_contents(
        root_path=osp.dirname(caller_path),
        file_suffix=file_suffix,
        package=package or target_obj.f_locals['__package__'],
        obj_filter=filter,
        locals_dict=target_obj.f_locals,
        all_list=target_obj.f_locals['__all__'],
        decorators=decorators
    )


class TypeFilter(object):

    def __init__(self, type_):
        self._type = type_

    def __call__(self, obj):
        return isinstance(obj, type) and issubclass(obj, self._type) and obj != self._type


class InstanceFilter(object):

    def __init__(self, type_):
        self._type = type_

    def __call__(self, obj):
        return isinstance(obj, self._type)


def import_types(file_suffix, target_type, decorators=None, package=None):
    import inspect
    _import(file_suffix, TypeFilter(target_type), decorators or [], inspect.stack()[1][0:2], package)


def import_instances(file_suffix, target_type, decorators=None, package=None):
    import inspect
    _import(file_suffix, InstanceFilter(target_type), decorators or [], inspect.stack()[1][0:2], package)


