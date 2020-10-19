from path_tool import get_current_path, combine_path

app_name = "SnipasteOCR"
tmp_image_dir = "C:\\ProgramData\\SnipasteOcr"
project_dir = get_current_path()
database = combine_path(project_dir, "snipasteocr.db")
icon_img_path = combine_path(project_dir, "assets", "img", "icon.png")
index_file = combine_path(project_dir, "assets", "index.html")
