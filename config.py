from util.common.path_tool import get_current_path, combine_path

# 程序名称
app_name = "SnipasteOCR"
# 缓存目录
tmp_image_dir = "C:\\ProgramData\\SnipasteOcr"
# 当前目录
project_dir = get_current_path()

# 页面文件目录
page_dir = combine_path(project_dir, "assets", "page")
# 首页文件
index_file = combine_path(page_dir, "index.html")

# 其他资源目录
resources_dir = combine_path(project_dir, "assets", "other")
# 数据库文件
database_file = combine_path(resources_dir, "snipasteocr.db")
# icon
icon_img_path = combine_path(resources_dir, "icon.png")
# tesseract 训练后的文件
tesseract_path = resources_dir
