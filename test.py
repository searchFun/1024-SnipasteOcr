import sys

import PySide2
from PySide2.QtCore import QRect
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QWidget, QButtonGroup, QPushButton, QHBoxLayout, QVBoxLayout

import config
from path_tool import combine_path


class ToolBoxWidget(QWidget):
    def __init__(self):
        super(ToolBoxWidget, self).__init__()
        self.setUi()

    def resizeEvent(self, event:PySide2.QtGui.QResizeEvent):
        print(self.width())

    def setUi(self):
        toolbox = QHBoxLayout()
        toolbox.setMargin(1)
        toolbox.setSpacing(1)
        ok_btn = QPushButton()
        ok_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "ok.png")))
        toolbox.addWidget(ok_btn)

        copy_btn = QPushButton()
        copy_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "copy.png")))
        toolbox.addWidget(copy_btn)

        # guding_btn = QPushButton()
        # guding_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "guding.png")))
        # toolbox.addWidget(guding_btn)

        save = QPushButton()
        save.setIcon(QIcon(combine_path(config.resource_dir, "img", "save.png")))
        toolbox.addWidget(save)

        close_btn = QPushButton()
        close_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "close.png")))
        toolbox.addWidget(close_btn)
        self.setLayout(toolbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ToolBoxWidget()
    widget.show()
    app.exec_()
