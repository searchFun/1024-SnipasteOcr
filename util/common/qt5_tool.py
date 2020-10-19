# 创建一个可以打开文件夹并选定文件的消息提示
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QMessageBox, QWidget


def create_openfile_message(title, message, file_path):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

    buttonY = message_box.button(QMessageBox.Yes)
    buttonY.setText("打开文件夹")
    buttonC = message_box.button(QMessageBox.Cancel)
    buttonC.setText("取消")
    message_box.exec_()
    # 打开文件夹
    if message_box.clickedButton() == buttonY:
        cmd = 'explorer /select, %s' % file_path
        import subprocess
        subprocess.Popen(cmd)
    elif message_box.clickedButton() == buttonC:
        message_box.hide()


# 创建一个报错的消息提示
def create_error_message(title, message):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStandardButtons(QMessageBox.Accepted)

    buttonA = message_box.button(QMessageBox.Yes)
    buttonA.setText("我知道了~")
    message_box.exec_()

    if message_box.clickedButton() == buttonA:
        message_box.hide()


def drawRect(widget: QWidget, painter: QPainter, start_x, start_y, end_x, end_y):
    painter.begin(widget)
    painter.drawRect(start_x, start_y, end_x, end_y)
    painter.end()
