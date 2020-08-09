from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from ui.MainWindow import Ui_Form
import sys
from api.google import GoogleTranslator
from api.baidu import BaiduTranslator
from api.youdao import YoudaoTranslator


if sys.version[0] != "3":
    raise ValueError("请使用 Python 3.x 版本运行")


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("简易翻译器")
        self.setWindowIcon(QIcon("assests/icon.png"))
        self.pushButton.clicked.connect(self.translate)

    def translate(self):
        # 判断当前选择的翻译引擎
        if self.comboBox.currentText() == "谷歌":
            api = GoogleTranslator()
        elif self.comboBox.currentText() == "有道":
            api = YoudaoTranslator()
        else:
            api = BaiduTranslator()

        text = self.textEdit.toPlainText()
        if text:
            try:
                translated_text = api.get_translation(text)
            except Exception as e:
                print(e)
                translated_text = "翻译接口调用失败"
        else:
            translated_text = "请输入内容后再翻译"
        self.textEdit_2.setText(translated_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
