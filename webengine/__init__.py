import json
import os
from pathlib import Path

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Slot
import sys

from dao.history_dao import select_all, remove_history
from webengine.view import WebView, OcrWidget

data_dir = Path(os.path.dirname(os.path.dirname(__file__)))

app = None
webview = None
ocrView = None


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
        webview.show()
        return json.dumps({
            "code": 200
        }, ensure_ascii=False)

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
        remove_history(id)
        print("remove:%d" % id)
        return json.dumps({
            "code": 200
        }, ensure_ascii=False)


if __name__ == '__main__':
    if app is None:
        app = QApplication([])
    if webview is None:
        handler = Handler()
        webview = WebView(handler=handler, pageUrl=f"{data_dir}/screenshotUi/dist/index.html")
        webview.show()
    if ocrView is None:
        ocrView = OcrWidget()
    app.exec_()
