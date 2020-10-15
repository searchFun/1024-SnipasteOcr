import os
import threading
import time

from PySide2.QtCore import Qt, QUrl, QFile, QIODevice
from PySide2.QtGui import QPalette, QGuiApplication, QPixmap, QBrush, QPainter, QPen, QIcon, QColor
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QApplication, QWidget

import config
from dao.history_dao import insert_history
from util import img_utils
from util.date_tool import get_datetime
from util.img_utils import save_temp


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print("WebEnginePage Console: [", message, lineNumber, sourceId, "]")


class WebView(QWebEngineView):
    def __init__(self, handler, pageUrl):
        super(WebView, self).__init__()
        # 设置为无边框窗口
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle('SnipasteOcr')
        self.setWindowIcon(QIcon(f"{config.data_dir}/assets/img/icon.png"))
        # 调整大小
        self.resize(700, 800)

        # channel是页面中可以拿到的,顾名思义,一个通道
        self.channel = QWebChannel()
        # Make the handler object available, naming it "backend"
        self.channel.registerObject("backend", handler)

        # Use a custom page that prints console messages to make debugging easier
        self.page = WebEnginePage()
        self.page.setWebChannel(self.channel)
        self.setPage(self.page)

        # Finally, load our file in the view
        # url = QUrl.fromLocalFile(f"{data_dir}/screenshotUi/index.html")
        url = QUrl.fromLocalFile(pageUrl)
        self.load(url)


class OcrWidget(QWidget):
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

    hasResult = False

    def __init__(self, ocr_over_callback, parent=None, ):
        super(OcrWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = QPalette()
        self.desk = QApplication.desktop()
        self.screen = self.desk.screenGeometry()
        self.ocr_over_callback = ocr_over_callback

    # 按键监听
    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F2:
            self.start()

    def start(self):
        self.hasResult = False
        # 对鼠标移动事件进行监听
        self.setMouseTracking(True)
        # 标识开始截图
        self.startFlag = 1
        # 休眠0.3秒
        time.sleep(0.3)
        # 调整窗口大小 用于展示当前页面图
        self.setGeometry(0, 0, self.screen.width(), self.screen.height())
        # 截全屏
        self.desktop_pix = QPixmap(QGuiApplication.primaryScreen().grabWindow(0))
        self.blurry_pix = self.add_blurry(self.desktop_pix)

        # 设置画笔
        self.palette.setBrush(self.backgroundRole(), QBrush(self.blurry_pix))
        self.setPalette(self.palette)
        # 显示
        self.show()

    def add_blurry(self, pix):
        temp = QPixmap(pix.size())
        temp.fill(Qt.transparent)
        p1 = QPainter(temp)
        p1.setCompositionMode(QPainter.CompositionMode_Source)
        p1.drawPixmap(0, 0, pix)
        p1.setCompositionMode(QPainter.CompositionMode_DestinationIn)
        p1.fillRect(temp.rect(), QColor(100, 100, 100, 100))
        p1.end()
        return temp

    # 画框
    def paintEvent(self, e):
        if self.startFlag & self.doingFlag:
            paint = QPainter(self)
            paint.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            # paint.begin(self)
            # 画边框
            paint.drawRect(min(self.mouse_current_y, self.mouse_start_x),
                           min(self.mouse_current_x, self.mouse_start_y),
                           abs(self.mouse_start_x - self.mouse_current_y),
                           abs(self.mouse_start_y - self.mouse_current_x))
            paint.drawPixmap(min(self.mouse_current_y, self.mouse_start_x),
                             min(self.mouse_current_x, self.mouse_start_y),
                             abs(self.mouse_start_x - self.mouse_current_y),
                             abs(self.mouse_start_y - self.mouse_current_x),
                             self.part_of_pix(min(self.mouse_current_y, self.mouse_start_x),
                                              min(self.mouse_current_x, self.mouse_start_y),
                                              abs(self.mouse_start_x - self.mouse_current_y),
                                              abs(self.mouse_start_y - self.mouse_current_x)))
            # paint.end()

    def part_of_pix(self, s_x, s_y, width, height):
        return self.desktop_pix.copy(s_x, s_y, width, height)

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
            # 获取当前区域选择像素
            pix = self.get_current_pix()
            # 保存图片
            file_name = config.tmp_image_dir + "\\" + get_datetime() + ".png"
            save_temp(pix, file_name)
            # 识别结果
            ocr_str = img_utils.img_ocr(file_name)
            # 插入数据库
            insert_history(ocr_str, file_name)
            self.hasResult = True
            # # 识别完成的回调
            self.ocr_over_callback(ocr_str)

        self.hide()
        self.setMouseTracking(False)

    # 获取当前选择区域pix
    def get_current_pix(self):
        return self.desktop_pix.copy(min(self.mouse_start_x, self.mouse_end_x),
                                     min(self.mouse_start_y, self.mouse_end_y),
                                     abs(self.mouse_end_x - self.mouse_start_x),
                                     abs(self.mouse_end_y - self.mouse_start_y))