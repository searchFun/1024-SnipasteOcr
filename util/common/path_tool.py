import os


# 获取当前路径
def get_current_path():
    return os.path.abspath(".")


# 是否目录
def is_dir(path: str):
    return os.path.isdir(path)


# 是否文件
def is_file(path: str):
    return os.path.isfile(path)


# 路径拼接
def combine_path(base_path, *paths):
    tmp_path = base_path
    paths_len = len(paths)
    index = 1
    for path in paths:
        # 如果路径参数不是最后一个，判断是否是目录
        if index < paths_len:
            tpath = os.path.join(tmp_path, path)
            if is_dir(tpath) is False:
                raise ValueError("%s不是一个目录" % tpath)
            index += 1
        tmp_path = os.path.join(tmp_path, path)

    return tmp_path


# 路径是否存在
def is_exist(path: str):
    return os.path.exists(path)


# 创建目录
def mkdir(path: str):
    os.mkdir(path)


# 复制文件
def copy_file(src: str, dst: str):
    os.system("@copy %s %s" % (src, dst))


# 获取目录文件列表
def get_file_list(path):
    for root, dirs, files in os.walk(path):
        return files
