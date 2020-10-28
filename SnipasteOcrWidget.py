from typing import Union

from PySide2.QtCore import QObject, Slot, QUrl
from PySide2.QtGui import Qt, QIcon, QPalette
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
from PySide2.QtWidgets import QSystemTrayIcon, QMenu, QAction, QApplication, QWidget

import config

app_name = config.app_name

app_icon = QIcon(config.icon_img_path)

app_widget = {
    "width": 700,
    "height": 800
}

web_channel_name = "backend"


class Handler(QObject):

    @Slot(str, result=str)
    def demo(self, content):
        return content

    # 最小化
    @Slot()
    def mini(self):
        webview.showMinimized()

    # 退出
    @Slot()
    def quit(self):
        sys.exit()

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
        webview.hide()
        ocrView.screenshot()

    @Slot(str, result=bool)
    def ocr_result(self, req):
        return ocrView.hasResult

    # 获取所有历史记录
    @Slot(str, result=str)
    def get_all_history(self, request):
        result = select_all()
        return json.dumps(result, ensure_ascii=False)

    # 移除一个记录
    @Slot(int, result=str)
    def removeOne(self, id):
        img_url = get_item_imgurl(id)
        remove_history(id)
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
        self.action_screenshot = QAction("截屏", self, triggered=self.screenShot)
        self.action_quit = QAction("退出", self, triggered=self.quitApp)

        self.menu_tray.addAction(self.action_show)
        self.menu_tray.addAction(self.action_screenshot)
        self.menu_tray.addAction(self.action_quit)

        self.setContextMenu(self.menu_tray)
        self.setIcon(app_icon)

    def setFun(self):
        # 图标点击
        self.activated.connect(self.onIconClicked)

    # 启动窗口
    def showWidget(self):
        # 若是最小化，则先正常显示窗口，再变为活动窗口（暂时显示在最前面）
        self.ui.showNormal()
        self.ui.activateWindow()

    # 截图
    def screenShot(self):
        print("doNothing")

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

    def __init__(self):
        super(SnipasteOcrWidget, self).__init__()
        # 设置Ui
        self.setUi()
        # 加载页面
        self.loadPage()

    def setUi(self):
        # 设置无边框模式
        self.setWindowFlags(Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.setWindowTitle(app_name)
        self.setWindowIcon(app_icon)
        # 调整大小
        self.resize(app_widget["width"], app_widget["height"])
        # 设置系统托盘
        self.system_tray_icon = SystemTrayIcon(self)

    def loadPage(self):
        # channel是页面中可以拿到的,顾名思义,一个通道
        self.web_channel = QWebChannel()
        self.web_channel.registerObject(web_channel_name, Handler())

        # Use a custom page that prints console messages to make debugging easier
        self.web_page = WebEnginePage()
        self.web_page.setWebChannel(self.web_channel)
        self.setPage(self.web_page)
        # 加载页面
        self.load(self.load_page)


class ScreenShotWidget(QWidget):
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
        self.setUi()

    def setUi(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.palette = QPalette()
        self.desk = QApplication.desktop()
        self.screen = self.desk.screenGeometry()
