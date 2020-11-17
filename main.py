import ctypes
import os
import sys

import history_dao
import config
import path_tool

from PySide2.QtWidgets import QApplication
from SnipasteOcrMainWidget import SnipasteOcrMainWidget


# 初始化必要的文件
def initMustFile():
    exist_fix_init = False
    # 判断数据库文件是否存在 不存在则创建
    if path_tool.is_exist(config.database_file) is False:
        history_dao.create_table()
        print("已初始化数据库，数据库文件为:%s" % config.database_file)
        exist_fix_init = True
    # 判断文件缓存目录是否存在 不存在则创建
    if path_tool.is_exist(config.tmp_image_dir) is False:
        path_tool.mkdir(config.tmp_image_dir)
        print("已初始化图片缓存目录，路径为:%s" % config.tmp_image_dir)
        exist_fix_init = True
    if path_tool.is_exist(path_tool.combine_path(config.tesseract_path, "chi_sim.traineddata")) is False:
        raise FileNotFoundError("请检查tesseract训练文件是否存在哦~")
    if exist_fix_init:
        print("初始化完成")


# 初始化必要的环境
def initMustEnvironments():
    # 标志程序为单独程序 非python程序，作用是显示任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.app_name)
    # 设置Tesseract环境变量
    os.environ['TESSDATA_PREFIX'] = config.tesseract_path


# 初始化
# 1.初始化必要文件
# 2.初始化必要环境
def init():
    initMustFile()
    initMustEnvironments()


if __name__ == '__main__':
    # 初始化
    init()
    # 创建唯一QtApplication
    app = QApplication().instance()
    if app is None:
        app = QApplication(sys.argv)
    widget = SnipasteOcrMainWidget()
    widget.show()
    sys.exit(app.exec_())
