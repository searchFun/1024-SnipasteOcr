from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, QUrl, Slot, Qt
from PySide2.QtWebChannel import QWebChannel
from PySide2.QtWebEngineWidgets import QWebEngineView, QWebEnginePage
import sys


class Handler(QObject):
    # Slot，中文网络上大多称其为槽。作用是接收网页发起的信号
    @Slot(str, result=str)
    def print(self, content):
        print('输出文本：', content)  # 对接收到的内容进行处理，比如调用打印机进行打印等等。此处略去，只在bash中显示接收到的消息
        return content

    @Slot()
    def exit(self):
        sys.exit()

    @Slot()
    def min(self):
        

class WebEnginePage(QWebEnginePage):
    def __init__(self, *args, **kwargs):
        super(WebEnginePage, self).__init__(*args, **kwargs)

    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceId):
        print("WebEnginePage Console: ", level, message, lineNumber, sourceId)


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationDisplayName("Greetings from the other side")

    # Use a webengine view
    view = QWebEngineView()
    view.setWindowFlags(Qt.FramelessWindowHint)
    view.resize(700, 800)

    # Set up backend communication via web channel
    handler = Handler()
    # channel是页面中可以拿到的,顾名思义,一个通道
    channel = QWebChannel()
    # Make the handler object available, naming it "backend"
    channel.registerObject("backend", handler)

    # Use a custom page that prints console messages to make debugging easier
    page = WebEnginePage()
    page.setWebChannel(channel)
    view.setPage(page)

    # Finally, load our file in the view
    url = QUrl.fromLocalFile("C:/Users/hjc/Desktop/screenShotUI/index.html")
    view.load(url)
    view.show()

    app.exec_()
