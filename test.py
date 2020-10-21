import sys

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QWidget, QButtonGroup, QPushButton, QHBoxLayout

import config
from path_tool import combine_path


class ToolBoxWidget(QWidget):
    def __init__(self):
        super(ToolBoxWidget, self).__init__()
        self.setUi()

    def setUi(self):
        toolbox = QHBoxLayout()
        ok_btn = QPushButton()
        ok_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "ok.png")))
        toolbox.addWidget(ok_btn)

        copy_btn = QPushButton()
        copy_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "copy.png")))
        toolbox.addWidget(copy_btn)

        guding_btn = QPushButton()
        guding_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "guding.png")))
        toolbox.addWidget(guding_btn)

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
