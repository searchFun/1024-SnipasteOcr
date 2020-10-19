# 存一个缓存图片
from PySide2.QtCore import QFile, QIODevice


def pix2png(pix, file_name):
    tmp_file = QFile(file_name)
    tmp_file.open(QIODevice.WriteOnly)
    pix.save(tmp_file, "PNG")
