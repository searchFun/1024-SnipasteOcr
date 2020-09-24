import json
import multiprocessing
import time

from PySide2.QtWidgets import QApplication

from history_dao import get_instance

from flask import Flask

from screenshot_service import ScreenShotService, ScreenShot

app = Flask(__name__)

overFlag = False


def shot():
    application = QApplication()
    wd = ScreenShot()
    wd.start()
    application.exec()


@app.route('/')
def hello_world():
    return 'Hello Flask!'


@app.route('/screenshot')
def screenshot():
    # pool = multiprocessing.Pool(processes=8)
    # pool.apply(shot)
    # pool.close()
    # pool.join()
    # print("ffff")
    return json.dumps(get_instance().select("select * from history", [])).encode('utf-8').decode('unicode_escape')


if __name__ == '__main__':
    app.run()
