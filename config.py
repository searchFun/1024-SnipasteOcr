import os
from pathlib import Path

app_name = "SnipasteOCR"
tmp_image_dir = "C:\\ProgramData\\SnipasteOcr"
data_dir = Path(os.path.dirname(__file__))
database = str(data_dir) + "\\snipasteocr.db"
