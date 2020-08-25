from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPixmap
from qtconsole.qt import QtCore
import sys
import os
import time
from ui.MainWindow import Ui_Form
from api import gw
from PyQt5 import sip
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib
matplotlib.use('Qt5Agg')


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


class PlotFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PlotFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
        self.axes = self.fig.add_subplot(111)

    def plot(self, data: list):
        self.axes.cla()
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        time = data[0]
        temp = data[1]
        self.axes.plot(time, temp, 's-', color='#f68227', linewidth=2.5)
        # self.draw()
        self.fig.canvas.draw()


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
        self.gridLayout = QGridLayout(self.groupBox)
        self.pushButton.clicked.connect(self.push_info)

    def push_info(self):
        city_name = self.textEdit.toPlainText()
        if len(city_name) != 0:
            try:
                city_ip = gw.get_city_ip(city_name)
                left_info = gw.get_base_weather(city_ip)
                right_info = gw.get_additional_weather(city_ip)
                curve_data = gw.get_1d_weather(city_ip)
                self.textEdit_2.setText(left_info)
                self.textEdit_3.setText(right_info)

                if self.flag == 0:
                    self.F = PlotFigure(width=3, height=2, dpi=80)
                    self.F.plot(curve_data)
                    self.gridLayout.addWidget(self.F, 0, 1)
                    self.flag += 1
                else:
                    sip.delete(self.F)  # 删除画布
                    self.F = PlotFigure(width=3, height=2, dpi=80)
                    self.F.plot(curve_data)
                    self.gridLayout.addWidget(self.F, 0, 1)
            except:
                self.textEdit_2.setText('查询失败！\n\n请检查城市名输入是否正确')
                self.textEdit_3.setText('')
                if self.flag:
                    sip.delete(self.F)
        else:
            self.textEdit_2.setText('查询失败！\n\n请输入城市名')
            self.textEdit_3.setText('')
            if self.flag:
                sip.delete(self.F)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainDialog()
    main.show()
    sys.exit(app.exec_())
