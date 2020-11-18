# 存一个缓存图片
import sys

import PySide2
from PySide2.QtCore import QFile, QIODevice, Qt
from PySide2.QtGui import QPixmap, QPainter, QColor, QPen, QBrush
from PySide2.QtWidgets import QApplication, QWidget


def pix2png(pix, file_name):
    tmp_file = QFile(file_name)
    tmp_file.open(QIODevice.WriteOnly)
    pix.save(tmp_file, "PNG")


def pix_add_blurry(pix, transparency: float):
    temp_pix = QPixmap(pix.size())
    temp_pix.fill(Qt.transparent)
    painter = QPainter(temp_pix)
    painter.setCompositionMode(QPainter.CompositionMode_Source)
    painter.drawPixmap(0, 0, pix)
    painter.setCompositionMode(QPainter.CompositionMode_DestinationIn)
    painter.fillRect(temp_pix.rect(), QColor(0, 0, 0, int(255 * transparency)))
    painter.end()
    return temp_pix


class PainterWidget(QWidget):
    def __init__(self):
        super(PainterWidget, self).__init__()

    def paintEvent(self, event: PySide2.QtGui.QPaintEvent):
        draw_circle(3, 600, 500, QColor("red"),QColor("blue"), self)


def draw_circle(radius, x, y, border_color, fill_color, widget):
    painter = QPainter(widget)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setPen(QPen(border_color, 1.5, Qt.SolidLine))
    painter.setBrush(QBrush(fill_color))
    painter.drawEllipse(x-radius, y-radius, radius * 2, radius * 2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = PainterWidget()
    widget.show()
    app.exec_()
