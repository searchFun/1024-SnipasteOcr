import json
import os

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Slot
import sys

import config
from dao.history_dao import select_all, remove_history, get_item_imgurl
from view import WebView, OcrWidget

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
        ocrView.start()

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


if __name__ == '__main__':
    if app is None:
        app = QApplication([])
    if webview is None:
        handler = Handler()
        pageUrl = f"{config.data_dir}/assets/index.html"
        webview = WebView(handler=handler, pageUrl=pageUrl)
        webview.show()
    if ocrView is None:
        ocrView = OcrWidget(ocr_over_callback=ocr_over_callback)
    app.exec_()
