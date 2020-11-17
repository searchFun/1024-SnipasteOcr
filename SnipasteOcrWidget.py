import json
import os
import sys
import time

from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtGui import Qt, QIcon, QPalette, QPixmap, QGuiApplication, QBrush
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QWidget

import config
from datetime_tool import get_now_time
import history_dao as his_dao
from ocr_tool import img_ocr
from path_tool import combine_path
from util.img_tool import pix2png, pix_add_blurry

app_name = config.app_name

# app_icon = QIcon(config.icon_img_path)
app_icon = config.icon_img_path
app_widget = {
    "width": 700,
    "height": 800
}

web_channel_name = "backend"


class Handler(QObject):
    main_window = None

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    # 最小化
    @Slot()
    def mini(self):
        self.main_window.showMinimized()

    # 退出
    @Slot()
    def quit(self):
        QApplication.instance().quit()

    # 复制结果
    @Slot(str, result=str)
    def copyResult(self, content):
        clipboard = QApplication.clipboard()
        clipboard.clear()
        clipboard.setText(content)
        return json.dumps({
            "code": 200
        }, ensure_ascii=False)

    # ocr
    @Slot(str, result=str)
    def ocr(self, req):
        self.main_window.screenShot()
        return "ff"

    @Slot(str, result=bool)
    def ocr_result(self, req):
        # return ocrView.hasResult
        return "null"

    # 获取所有历史记录
    @Slot(str, result=str)
    def get_all_history(self, request):
        result = his_dao.select_all()
        return json.dumps(result, ensure_ascii=False)

    # 移除一个记录
    @Slot(int, result=str)
    def removeOne(self, id):
        img_url = his_dao.get_item_imgurl(id)
        his_dao.remove_history(id)
        try:
            os.remove(img_url)
        except Exception as e:
            print("没有:%s" % img_url)
        return json.dumps({
            "code": 200
        }, ensure_ascii=False)


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print("WebEnginePage Console: [", message, lineNumber, sourceId, "]")


class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, main_widget):
        super(SystemTrayIcon, self).__init__()
        self.ui = main_widget
        self.setUi()
        self.setFun()

    def setUi(self):
        self.menu_tray = QMenu()
        self.action_show = QAction("显示窗口", self, triggered=self.showWidget)
        self.action_screenshot = QAction("截屏", self, triggered=self.ui.screenShot)
        self.action_quit = QAction("退出", self, triggered=self.quitApp)

        self.menu_tray.addAction(self.action_show)
        self.menu_tray.addAction(self.action_screenshot)
        self.menu_tray.addAction(self.action_quit)

        self.setContextMenu(self.menu_tray)
        self.setIcon(QIcon(app_icon))

    def setFun(self):
        # 图标点击
        self.activated.connect(self.onIconClicked)

    # 启动窗口
    def showWidget(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    # 退出程序
    def quitApp(self):
        QApplication.instance().quit()

    def onIconClicked(self, reason):
        # 1是表示单击右键，2是双击，3是单击左键，4是用鼠标中键点击
        if reason == 2 or reason == 3:
            if self.ui.isMinimized() or not self.ui.isVisible():
                self.showWidget()
            else:
                # 若不是最小化，则最小化
                self.ui.showMinimized()


class SnipasteOcrWidget(QWebEngineView):
    load_page = QUrl.fromLocalFile(config.index_file)

    sc_widget = None

    def __init__(self):
        super(SnipasteOcrWidget, self).__init__()
        self.sc_widget = ScreenShotWidget(self)
        # 设置Ui
        self.setUi()
        # 加载页面
        self.loadPage()

    def setUi(self):
        # 设置无边框模式
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle(app_name)
        self.setWindowIcon(QIcon(app_icon))
        # 调整大小
        self.resize(app_widget["width"], app_widget["height"])
        # 设置系统托盘
        self.system_tray_icon = SystemTrayIcon(self)

    def loadPage(self):
        # channel是页面中可以拿到的,顾名思义,一个通道
        self.web_channel = QWebChannel()
        self.web_channel.registerObject(web_channel_name, Handler(self))

        # Use a custom page that prints console messages to make debugging easier
        self.web_page = WebEnginePage()
        self.web_page.setWebChannel(self.web_channel)
        self.setPage(self.web_page)
        # 加载页面
        self.load(self.load_page)
        self.showManWidget()

    def screenShot(self):
        self.showScWidget()
        self.sc_widget.screenshot()

    def showScWidget(self):
        self.hide()
        # self.sc_widget.show()

    def showManWidget(self):
        # self.sc_widget.hide()
        self.show()


class ScreenShotWidget(QWidget):
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

    def __init__(self, parent_widget, parent=None, ):
        super(ScreenShotWidget, self).__init__(parent)
        self.parent_widget = parent_widget
        self.setUi()

    def setUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = QPalette()
        self.screen = QApplication.primaryScreen()

    # 画图事件
    def paintEvent(self, e):
        if self.startFlag & self.doingFlag:
            self.draw_rect_image(self.mouse_start_x, self.mouse_start_y,
                                 self.mouse_current_x, self.mouse_current_y)

    # 鼠标按下事件
    def mousePressEvent(self, e):
        self.mouse_start_x = e.globalX()
        self.mouse_start_y = e.globalY()
        self.startFlag = True
        self.doingFlag = True

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
            self.mouse_end_x = e.globalX()
            self.mouse_end_y = e.globalY()

            # 获取当前区域选择像素
            pix = self.get_current_pix()
            # 保存图片
            file_name = combine_path(config.tmp_image_dir, str(get_now_time("%Y%m%d%H%M%S")) + ".png")
            pix2png(pix, file_name)
            # 识别结果
            ocr_str = img_ocr(file_name)
            # 插入数据库
            his_dao.insert_history(ocr_str, file_name)
            self.endFlag = False
            self.hasResult = True
            self.setMouseTracking(False)

    def screenshot(self):
        self.hasResult = False
        # 对鼠标移动事件进行监听
        self.setMouseTracking(True)
        # 标识开始截图
        self.startFlag = True
        self.endFlag = False
        # 休眠0.3秒
        time.sleep(0.1)
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


if __name__ == '__main__':
    app = QApplication().instance()
    if app is None:
        app = QApplication(sys.argv)
    widget = SnipasteOcrWidget()
    widget.show()
    app.exec_()
