import json
import os

from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Slot
import sys

import config
from core.WebEngine import WebView
from history_dao import select_all, remove_history, get_item_imgurl
from ScreenShotWidget import OcrWidget, MySystemTrayIcon

import ctypes


app = None
webview = None
ocrView = None


def ocr_over_callback(ocr_result):
    webview.show()


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


# 部分初始化
def init():
    # 标志程序为单独程序 非python程序，作用是显示任务栏图标
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(config.app_name)
    # 设置环境变量
    os.environ['TESSDATA_PREFIX'] = config.tesseract_path


if __name__ == '__main__':
    init()
    if app is None:
        app = QApplication([])
    if webview is None:
        handler = Handler()
        webview = WebView(handler=handler,
                          load_url=config.index_file,
                          window_title=config.app_name,
                          window_icon=QIcon(config.icon_img_path))
        webview.show()
        ti = MySystemTrayIcon(webview)
        ti.show()
    if ocrView is None:
        ocrView = OcrWidget(ocr_over_callback=ocr_over_callback)
    app.exec_()
