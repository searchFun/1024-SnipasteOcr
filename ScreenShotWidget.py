import sys
import time

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import QPalette, QGuiApplication, QPixmap, QBrush, QPainter, QPaintEvent
from PySide2.QtWidgets import QApplication, QWidget

from util.img_tool import pix_add_blurry


class ScreenShotMainWidget(QWidget):
    # 绘画信号
    draw_signal = Signal(QPixmap)
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
    # 截图结束标识
    endFlag = False

    hasResult = False

    show_widget = None

    def __init__(self, parent=None, ):
        super(ScreenShotMainWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = QPalette()
        self.desk = QApplication.desktop()
        self.screen = self.desk.screenGeometry()
        self.show_widget = ScreenShotShowWidget(self)
        self.draw_signal.connect(self.show_widget.loadPix)
        self.screenshot()

    # 按键监听
    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F2:
            self.screenshot()
        if evt.key() == Qt.Key_Escape:
            QApplication.instance().quit()

    # 鼠标按下事件
    def mousePressEvent(self, e):
        self.mouse_start_x = e.globalX()
        self.mouse_start_y = e.globalY()
        self.startFlag = True
        self.doingFlag = True
        self.endFlag = False
        self.show_widget.show()

    # 鼠标移动事件
    def mouseMoveEvent(self, e):
        if self.startFlag & self.doingFlag:
            self.mouse_current_x = e.globalX()
            self.mouse_current_y = e.globalY()
            x = min(self.mouse_start_x, self.mouse_current_x)
            y = min(self.mouse_start_y, self.mouse_current_y)
            width = abs(self.mouse_current_x - self.mouse_start_x)
            height = abs(self.mouse_current_y - self.mouse_start_y)
            print("----------------------------------")
            print("start_x:%d,start_y:%d" % (self.mouse_start_x, self.mouse_start_y))
            print("current_x:%d,current_y:%d" % (self.mouse_current_x, self.mouse_current_y))
            print("x:%d,y:%d,width:%d,height:%d" % (x, y, width, height))
            self.show_widget.setGeometry(x, y, width, height)
            self.draw_signal.emit(self.part_of_pix(x, y, width, height))
            self.show_widget.update()

    # 鼠标松开
    def mouseReleaseEvent(self, e):
        # 如果已经标记了开始
        if self.startFlag:
            # 开始截图标记置否
            self.startFlag = False
            self.doingFlag = False
            self.mouse_end_x = e.globalX()
            self.mouse_end_y = e.globalY()

            # 获取当前区域选择像素
            pix = self.get_current_pix()

            self.endFlag = False
            self.hasResult = True
            # # 识别完成的回调
            # self.setMouseTracking(False)
            # self.hide()

    def screenshot(self):
        self.hasResult = False
        # 对鼠标移动事件进行监听
        self.setMouseTracking(True)
        # 标识开始截图
        self.startFlag = True
        self.endFlag = False
        # 休眠0.3秒
        time.sleep(0.3)
        # 调整窗口大小 用于展示当前页面图
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        # 截全屏
        self.desktop_pix = QPixmap(QGuiApplication.primaryScreen().grabWindow(0))
        self.blurry_pix = pix_add_blurry(self.desktop_pix, 0.3)

        # 设置画笔
        self.palette.setBrush(self.backgroundRole(), QBrush(self.blurry_pix))
        self.setPalette(self.palette)
        # 显示
        self.show()

    # 获取当前选择区域pix
    def get_current_pix(self):
        return self.desktop_pix.copy(min(self.mouse_start_x, self.mouse_end_x),
                                     min(self.mouse_start_y, self.mouse_end_y),
                                     abs(self.mouse_end_x - self.mouse_start_x),
                                     abs(self.mouse_end_y - self.mouse_start_y))

    def part_of_pix(self, s_x, s_y, width, height):
        return self.desktop_pix.copy(s_x, s_y, width, height)


class ScreenShotShowWidget(QWidget):
    main_widget = None
    pixmap = None

    def __init__(self, main_widget):
        super(ScreenShotShowWidget, self).__init__()
        self.main_widget = main_widget
        self.setUi()

        # 按键监听

    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F2:
            self.screenshot()
        if evt.key() == Qt.Key_Escape:
            QApplication.instance().quit()

    def setUi(self):
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        print("hello")

    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.pixmap)

    def loadPix(self, pixmap: QPixmap):
        self.pixmap = pixmap


if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = ScreenShotMainWidget()
    widget.show()
    sys.exit(app.exec_())
