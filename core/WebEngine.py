from PySide2.QtCore import Qt, QUrl
from PySide2.QtGui import QIcon
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print("WebEnginePage Console: [", message, lineNumber, sourceId, "]")


class WebView(QWebEngineView):
    def __init__(self, handler, load_url: str, window_title: str, window_icon: QIcon,
                 window_flag=Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint):
        super(WebView, self).__init__()
        # 设置为无边框窗口
        # self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlags(window_flag)
        self.setWindowTitle(window_title)
        self.setWindowIcon(window_icon)
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
        url = QUrl.fromLocalFile(load_url)
        self.load(url)
