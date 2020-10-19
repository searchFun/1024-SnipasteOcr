import os

def get_current_path():
    return os.path.abspath(".")


def is_dir(path: str):
    return os.path.isdir(path)


def is_file(path: str):
    return os.path.isfile(path)


def combine_path(base_path, *paths):
    tmp_path = base_path
    paths_len = len(paths)
    index = 1
    for path in paths:
        if index < paths_len:
            if is_dir(path) is False:
                raise ValueError("%s不是一个目录" % path)
        tmp_path = os.path.join(tmp_path, path)

    return tmp_path


def is_exist(path: str):
    return os.path.exists(path)


def mkdir(path: str):
    os.mkdir(path)