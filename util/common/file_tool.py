import os


def copy_file(src: str, dst: str):
    os.system("@copy %s %s" % (src, dst))


def get_file_list(path):
    for root, dirs, files in os.walk(path):
        return files
