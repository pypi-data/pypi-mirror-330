import os
import re
from typing import NoReturn


def fail(msg) -> NoReturn:
    raise ValueError(msg)


def substr(s, _from, to=None):
    if to:
        return s[_from : _from + to]
    return s[_from:]


def length(a):
    return len(a)


def defined(x):
    return x is not None


def join(sep, lst):
    return sep.join(map(str, lst))


def split(patt, s):
    return re.split(patt, s)


def lc(s: str) -> str:
    # TODO
    return s.lower()


def chomp(s: str) -> str:
    if s.endswith("\n"):
        return s[:-1]
    return s


def ref(obj):
    return type(obj).__name__


def rename(a, b):
    os.rename(a, b)


def die():
    raise ValueError("die")


def bless(params: dict, cls_name: str, context_classes: dict) -> object:
    cls = context_classes[cls_name]
    obj = cls()
    for prop_name, prop_value in params.items():
        if not hasattr(cls, prop_name):
            setattr(obj, prop_name, prop_value)
    return obj


def defstr(s, a, b):
    pass


def mkpath(dir, param):
    os.mkdir(dir, param)


def chdir(path):
    os.chdir(path)


def is_dir(path) -> bool:
    return os.path.isdir(path)


def is_file(path) -> bool:
    return os.path.isfile(path)


class universal_dict_object(dict):
    def __getattr__(self, item):
        return self.get(item, None)

    def __setattr__(self, key, value):
        self[key] = value


def uc(s):
    return s


def reverse(l):
    return list(reversed(l))
