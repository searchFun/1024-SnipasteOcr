# 初始化
# 1。创建数据库
# 2. 创建缓存目录

import history_dao
import config
import path_tool

if __name__ == '__main__':
    if path_tool.is_exist(config.database_file) is False:
        history_dao.create_table()
        print("已初始化数据库，数据库文件为:%s" % config.database_file)
    else:
        print("已存在数据库，跳过创建")
    if path_tool.is_exist(config.tmp_image_dir) is False:
        path_tool.mkdir(config.tmp_image_dir)
        print("已初始化图片缓存目录，路径为:%s" % config.tmp_image_dir)
    else:
        print("已创建图片缓存目录，跳过创建")

    print("初始化完成")
