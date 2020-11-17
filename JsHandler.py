import json
import os

import history_dao as his_dao

from PySide2.QtCore import QObject, Slot
from PySide2.QtWidgets import QApplication


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
        except FileNotFoundError:
            print("没有:%s" % img_url)
        return json.dumps({
            "code": 200
        }, ensure_ascii=False)
