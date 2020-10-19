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
        # 如果路径参数不是最后一个，判断是否是目录
        if index < paths_len:
            if is_dir(os.path.join(tmp_path, path)) is False:
                raise ValueError("%s不是一个目录" % path)
            index += 1
        tmp_path = os.path.join(tmp_path, path)

    return tmp_path


def is_exist(path: str):
    return os.path.exists(path)


def mkdir(path: str):
    os.mkdir(path)
