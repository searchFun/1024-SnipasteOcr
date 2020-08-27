import os
import time

from datasource.history_dao import HistoryTemplate
from util import ocr_tools
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from util.date_tool import get_datetime


class Widget(QWidget):
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

    # 窗口位置
    widget = {
        'x': 100,
        'y': 200,
        'width': 200,
        'height': 200,
    }
    # 截图按钮
    screenShootBtn = {
        'text': "开始截屏",
        'x': 100,
        'y': 100,
        'width': 100,
        'height': 20
    }

    # 开始截图标识
    startFlag = False
    # 正在截图标识
    doingFlag = False

    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)

        # 图片展示标签
        self.picture_label = QLabel()
        self.setGeometry(self.widget['x'],
                         self.widget['y'],
                         self.widget['width'],
                         self.widget['height'])

        # 设置截图按钮
        self.screen_btn = QPushButton(self.screenShootBtn['text'], self)
        self.screen_btn.setGeometry(self.screenShootBtn['x'],
                                    self.screenShootBtn['y'],
                                    self.screenShootBtn['width'],
                                    self.screenShootBtn['height'])
        self.screen_btn.clicked.connect(self.start)

        # 设置截图按钮
        self.text_label = QPushButton("", self)
        self.text_label.setGeometry(200,
                                    200,
                                    self.screenShootBtn['width'],
                                    self.screenShootBtn['height'])

        # 水平布局
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.screen_btn)
        # self.layout2 = QHBoxLayout()
        # self.layout2.addWidget(self.picture_label)
        # self.layout2.addWidget(self.text_label)
        # self.layout.addChildLayout(self.layout2)
        self.layout.addWidget(self.text_label)
        self.setLayout(self.layout)

        self.text_label.clicked.connect(self.copy_ocr_text)
        # 设置背景色
        self.palette = QPalette()
        # self.palette.setColor(QPalette.Window, Qt.lightGray)
        # self.setPalette(self.palette)

        self.desk = QApplication.desktop()
        self.qrect = self.desk.screenGeometry()

        # 对鼠标移动事件进行监听
        self.setMouseTracking(True)

        # self.label2.setTextInteractionFlags(Qt.TextSelectableByMouse)

    # 按键监听
    def keyPressEvent(self, evt):
        if evt.key() == Qt.Key_F2:
            self.start()

    def start(self):
        # 标识开始截图
        self.startFlag = 1
        # 隐藏自己
        self.hide()
        # 调整窗口大小 为桌面触发paintEvent
        self.setGeometry(0, 0, self.qrect.width(), self.qrect.height())
        # 休眠0.3秒
        time.sleep(0.3)
        screen = QGuiApplication.primaryScreen()

        self.desktopPixmap = QPixmap(screen.grabWindow(0))

        self.palette.setBrush(self.backgroundRole(), QBrush(self.desktopPixmap))
        self.setPalette(self.palette)

        self.show()
        self.screen_btn.hide()
        # self.picture_label.hide()
        self.text_label.hide()

    def copy_ocr_text(self):
        if self.text_label.text() is not "" and self.text_label.text() is not None:
            self.put_into_clipboard('text', self.text_label.text())

    def put_into_clipboard(self, type, content):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        if type == 'pixmap':
            clipboard.setPixmap(content)
        elif type == 'text':
            clipboard.setText(content)

    # 画框
    def paintEvent(self, e):
        if self.startFlag & self.doingFlag:
            paint = QPainter(self)
            paint.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            paint.begin(self)
            paint.drawRect(min(self.mouse_current_y, self.mouse_start_x),
                           min(self.mouse_current_x, self.mouse_start_y),
                           abs(self.mouse_start_x - self.mouse_current_y),
                           abs(self.mouse_start_y - self.mouse_current_x))
            paint.end()

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

            # 保存到剪切板
            self.put_into_clipboard('pixmap', self.get_current_pix())
            # 开始截图标记置否
            self.startFlag = False
            # 再次显示截图按钮
            self.palette.setColor(QPalette.Window, Qt.lightGray)
            self.setPalette(self.palette)
            self.screen_btn.show()

            pix = self.get_current_pix()
            self.picture_label.setPixmap(pix)
            self.text_label.setText(self.ocr(pix))
            # self.picture_label.show()
            self.text_label.show()
            self.setGeometry(self.widget['x'], self.widget['y'],
                             abs(self.mouse_end_x - self.mouse_start_x),
                             abs(self.mouse_end_y - self.mouse_start_y))
        else:
            print("未开始截图")

    # 获取当前pix
    def get_current_pix(self):
        return self.desktopPixmap.copy(min(self.mouse_start_x, self.mouse_end_x),
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

        # try:
        #     ocr_str = ocr_tools.img_to_str1(self.tmpFileName)
        # except Exception:
        ocr_str = ocr_tools.img_to_str(self.tmp_file_name)
        # 插入数据库snipasteocr中表history
        # pdbc = HistoryTemplate("snipasteocr.db")
        # pdbc.insert([ocr_str, get_datetime()])
        # pdbc.Close()
        self.delete_temp()
        return ocr_str
