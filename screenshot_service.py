import os
import sys
import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from history_dao import get_instance
from util import ocr_tools
from util.date_tool import get_datetime


class ScreenShot(QWidget):
    # 缓存图片文件名称
    tmp_file_name = "tmp.png"

    desktop_pix = None

    # 鼠标点击开始点
    mouse_start_x = 0
    mouse_start_y = 0

    # 鼠标移动点
    mouse_current_x = 0
    mouse_current_y = 0

    # 鼠标释放点
    mouse_end_x = 0
    mouse_end_y = 0

    # 开始截图标识
    startFlag = False
    # 正在截图标识
    doingFlag = False

    def __init__(self, parent=None):
        super(ScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)
        self.palette = QPalette()
        self.desk = QApplication.desktop()
        self.screen = self.desk.screenGeometry()
        # 对鼠标移动事件进行监听
        self.setMouseTracking(True)

    # 按键监听
    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F2:
            self.start()

    def start(self):
        # 标识开始截图
        self.startFlag = 1
        # 休眠0.3秒
        time.sleep(0.3)
        # 调整窗口大小 用于展示当前页面图
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        # 截全屏
        self.desktop_pix = QPixmap(QGuiApplication.primaryScreen().grabWindow(0))
        # 设置画笔
        self.palette.setBrush(self.backgroundRole(), QBrush(self.desktop_pix))
        self.setPalette(self.palette)
        # 显示
        self.show()

    # 画框
    def paintEvent(self, e):
        if self.startFlag & self.doingFlag:
            paint = QPainter(self)
            paint.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            # paint.begin(self)
            paint.drawRect(min(self.mouse_current_y, self.mouse_start_x),
                           min(self.mouse_current_x, self.mouse_start_y),
                           abs(self.mouse_start_x - self.mouse_current_y),
                           abs(self.mouse_start_y - self.mouse_current_x))
            # paint.end()

    # 鼠标按下事件
    def mousePressEvent(self, e):
        if self.startFlag:
            self.mouse_start_x = e.globalX()
            self.mouse_start_y = e.globalY()
            self.doingFlag = True
        else:
            print("未开始截图")

    # 鼠标移动事件
    def mouseMoveEvent(self, e):
        if self.startFlag & self.doingFlag:
            self.mouse_current_y = e.globalX()
            self.mouse_current_x = e.globalY()
            self.update()

    # 鼠标松开
    def mouseReleaseEvent(self, e):
        # 如果已经标记了开始
        if self.startFlag:
            self.doingFlag = False
            self.mouse_end_x = e.globalX()
            self.mouse_end_y = e.globalY()

            # 开始截图标记置否
            self.startFlag = False
            pix = self.get_current_pix()
            result = self.ocr(pix)
            # 插入数据库
            get_instance().Insert_History([result, str(get_datetime())])
            self.hide()
        else:
            print("未开始截图")

    # 获取当前pix
    def get_current_pix(self):
        return self.desktop_pix.copy(min(self.mouse_start_x, self.mouse_end_x),
                                     min(self.mouse_start_y, self.mouse_end_y),
                                     abs(self.mouse_end_x - self.mouse_start_x),
                                     abs(self.mouse_end_y - self.mouse_start_y))

    # 存一个缓存图片
    def save_temp(self, pix):
        tmp_file = QFile(self.tmp_file_name)
        tmp_file.open(QIODevice.WriteOnly)
        pix.save(tmp_file, "PNG")

    # 删除这个缓存图片
    def delete_temp(self):
        os.remove(self.tmp_file_name)

    # ocr
    def ocr(self, pix):
        self.save_temp(pix)
        ocr_str = ocr_tools.img_to_str(self.tmp_file_name)
        self.delete_temp()
        return ocr_str


class ScreenShotService():
    def __init__(self):
        self.app = QApplication.instance()
        if self.app is None:
            self.app = QApplication(sys.argv)
        self.wd = ScreenShot()

    def start(self):
        self.wd.start()

    def end(self):
        self.app.exec_()
