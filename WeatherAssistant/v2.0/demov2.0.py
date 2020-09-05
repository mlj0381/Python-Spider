from PyQt5.QtWidgets import QDialog, QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon, QPixmap
from qtconsole.qt import QtCore
from PyQt5.QtCore import QUrl
from ui.MainWindow import Ui_Form
from api import gw
import sys
import os


def resource_path(relative_path):
    """
    获取正确的文件路径
    :param relative_path: 文件的相对路径
    :return: 文件正确的绝对路径
    """
    if getattr(sys, 'frozen', None):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


class MainDialog(QDialog, Ui_Form):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(resource_path('assets/weather.ico')))
        icon = QIcon()
        icon.addPixmap(QPixmap(resource_path("assets/search.png")), QIcon.Normal, QIcon.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setIconSize(QtCore.QSize(30, 30))
        self.pushButton.setAutoRepeatDelay(200)
        self.flag = 0
        self.pushButton.clicked.connect(self.push_info)

    def push_info(self):
        city_name = self.textEdit.toPlainText().strip()
        if len(city_name) != 0:
            try:
                # 判断查询 1 天还是 7 天的天气情况
                if self.radioButton.isChecked():
                    # 查询 1 天的天气情况
                    city_ip = gw.get_city_ip(city_name)
                    left_info = gw.get_base_weather(city_ip)
                    right_info = gw.get_additional_weather(city_ip)
                    self.textEdit_2.setText(left_info)
                    self.textEdit_3.setText(right_info)
                    gw.plot_1d_weather(city_ip)
                else:
                    # 查询 7 天的天气情况
                    city_ip = gw.get_city_ip(city_name)
                    gw.plot_7d_weather(city_ip)
                    self.textEdit_2.setText("")
                    self.textEdit_3.setText("")
                # 判断第一次查询
                # self.flag = 0 表示第一次查询
                if self.flag:
                    # 删除已有的浏览器控件
                    self.browser.deleteLater()
                    # 重新添加浏览器控件
                    self.browser = QWebEngineView()
                    # url = "file://////" + resource_path("time-temp-curve.html").replace("\\", "/")
                    url = resource_path("time-temp-curve.html").replace("\\", "/")
                    self.browser.load(QUrl(url))
                    self.horizontalLayout.addWidget(self.browser)
                else:
                    self.browser = QWebEngineView()
                    # url = "file://////" + resource_path("time-temp-curve.html").replace("\\", "/")
                    url = resource_path("time-temp-curve.html").replace("\\", "/")
                    self.browser.load(QUrl(url))
                    self.horizontalLayout.addWidget(self.browser)
                    self.flag = 1
            except:
                self.textEdit_2.setText('查询失败！\n\n请检查城市名输入是否正确')
                self.textEdit_3.setText('')
                if self.flag:
                    self.browser.deleteLater()
                    self.flag = 0
        else:
            self.textEdit_2.setText('查询失败！\n\n请输入城市名')
            self.textEdit_3.setText('')
            if self.flag:
                self.browser.deleteLater()
                self.flag = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
