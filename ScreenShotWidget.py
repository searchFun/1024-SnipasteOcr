import time

from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QGuiApplication, QPixmap, QBrush, QPainter, QPen, QColor, QIcon
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout

import config
from path_tool import combine_path
from util.img_tool import pix_add_blurry, draw_circle


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
    # 截图结束标识
    endFlag = False

    hasResult = False

    def __init__(self, ocr_over_callback, parent=None, ):
        super(OcrWidget, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = QPalette()
        self.desk = QApplication.desktop()
        self.screen = self.desk.screenGeometry()
        self.set_toolbox()
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

    # 画框
    def paintEvent(self, e):
        if self.startFlag:
            self.draw_rect_image(self.mouse_start_x, self.mouse_start_y,
                                 self.mouse_current_x, self.mouse_current_y)
        if self.endFlag:
            self.draw_rect_image(self.mouse_start_x, self.mouse_start_y,
                                 self.mouse_end_x, self.mouse_end_y)

    def draw_rect_image(self, start_x, start_y, end_x, end_y):
        paint = QPainter(self)
        paint.setPen(QPen(Qt.red, 3, Qt.SolidLine))
        # paint.begin(self)
        # 画边框
        paint.drawRect(min(end_x, start_x),
                       min(end_y, start_y),
                       abs(start_x - end_x),
                       abs(start_y - end_y))
        # 画图像
        paint.drawPixmap(min(end_x, start_x),
                         min(end_y, start_y),
                         abs(start_x - end_x),
                         abs(start_y - end_y), self.part_of_pix(min(end_x, start_x),
                                                                min(end_y, start_y),
                                                                abs(start_x - end_x),
                                                                abs(start_y - end_y)))
        # paint.end()
        draw_circle(5, start_x, start_y, QColor(Qt.white), QColor(Qt.red), self)
        draw_circle(5, start_x, end_y, QColor(Qt.white), QColor(Qt.red), self)
        draw_circle(5, end_x, start_y, QColor(Qt.white), QColor(Qt.red), self)
        draw_circle(5, end_x, end_y, QColor(Qt.white), QColor(Qt.red), self)

    def part_of_pix(self, s_x, s_y, width, height):
        return self.desktop_pix.copy(s_x, s_y, width, height)

    # 鼠标按下事件
    def mousePressEvent(self, e):
        self.mouse_start_x = e.globalX()
        self.mouse_start_y = e.globalY()
        print("start:(%d,%d)" % (self.mouse_start_x, self.mouse_start_y))
        self.startFlag = True
        self.doingFlag = True
        self.endFlag = False

    # 鼠标移动事件
    def mouseMoveEvent(self, e):
        if self.startFlag & self.doingFlag:
            self.mouse_current_x = e.globalX()
            self.mouse_current_y = e.globalY()
            self.update()

    # 鼠标松开
    def mouseReleaseEvent(self, e):
        # 如果已经标记了开始
        if self.startFlag:
            # 开始截图标记置否
            self.startFlag = False
            self.doingFlag = False
            self.endFlag = True
            self.mouse_end_x = e.globalX()
            self.mouse_end_y = e.globalY()

            self.show_toolbox(self.mouse_end_x - 180, self.mouse_end_y + 10)

            # # 获取当前区域选择像素
            # pix = self.get_current_pix()
            # # 保存图片
            # file_name = combine_path(config.tmp_image_dir, get_now_time() + ".png")
            # pix2png(pix, file_name)
            # # 识别结果
            # ocr_str = img_ocr(file_name)
            # # 插入数据库
            # insert_history(ocr_str, file_name)

        # self.hide()

    # 获取当前选择区域pix
    def get_current_pix(self):
        return self.desktop_pix.copy(min(self.mouse_start_x, self.mouse_end_x),
                                     min(self.mouse_start_y, self.mouse_end_y),
                                     abs(self.mouse_end_x - self.mouse_start_x),
                                     abs(self.mouse_end_y - self.mouse_start_y))

    def ok_btn_fun(self):
        ocr_str = '1'
        self.endFlag = False
        self.hasResult = True
        # # 识别完成的回调
        self.ocr_over_callback(ocr_str)
        self.setMouseTracking(False)
        self.tool_box.hide()
        self.hide()

    def cancel_btn_fun(self):
        self.endFlag = False
        self.hasResult = False
        self.tool_box.hide()
        self.hide()

    def set_toolbox(self):
        self.tool_box = QWidget()
        self.tool_box.setWindowFlags(Qt.FramelessWindowHint)
        layout = QHBoxLayout()
        layout.setMargin(0)
        layout.setSpacing(0)
        # ok按钮
        self.ok_btn = QPushButton()
        self.ok_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "ok.png")))
        self.ok_btn.clicked.connect(self.ok_btn_fun)
        layout.addWidget(self.ok_btn)

        # 复制图像
        self.copy_btn = QPushButton()
        self.copy_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "copy.png")))
        layout.addWidget(self.copy_btn)

        # # 固定
        # self.guding_btn = QPushButton()
        # self.guding_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "guding.png")))
        # layout.addWidget(self.guding_btn)

        # 固定
        self.save = QPushButton()
        self.save.setIcon(QIcon(combine_path(config.resource_dir, "img", "save.png")))
        layout.addWidget(self.save)

        # 取消
        self.close_btn = QPushButton()
        self.close_btn.setIcon(QIcon(combine_path(config.resource_dir, "img", "close.png")))
        self.close_btn.clicked.connect(self.cancel_btn_fun)
        layout.addWidget(self.close_btn)
        self.tool_box.setLayout(layout)
        self.tool_box.hide()

    def show_toolbox(self, x, y):
        self.tool_box.move(x, y)
        self.tool_box.show()

    def hide_toolbox(self):
        self.tool_box.hide()
