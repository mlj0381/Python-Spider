from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
import sys
from api.google import GoogleTranslator
from api.baidu import BaiduTranslator
from api.youdao import YoudaoTranslator


if sys.version[0] != "3":
    raise ValueError("请使用 Python 3.x 版本运行")


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        # 定义组件
        self.setWindowTitle("翻译器")
        self.setWindowIcon(QIcon("assests/icon.png"))
        self.setFixedSize(600, 200)
        self.source_label = QLabel("原文")
        self.result_label = QLabel("译文")
        self.source_text = QTextEdit()
        self.result_text = QTextEdit()
        self.translate_button = QPushButton("翻译")
        self.combox = QComboBox()
        self.combox.addItem("谷歌")
        self.combox.addItem("有道")
        self.combox.addItem("百度")
        # 布局
        self.grid = QGridLayout()
        self.grid.addWidget(self.source_label, 1, 0)
        self.grid.addWidget(self.result_label, 2, 0)
        self.grid.addWidget(self.source_text, 1, 1)
        self.grid.addWidget(self.result_text, 2, 1)
        self.grid.addWidget(self.translate_button, 2, 2)
        self.grid.addWidget(self.combox, 1, 2)
        self.setLayout(self.grid)
        self.grid.setSpacing(20)
        # 绑定按钮
        self.translate_button.clicked.connect(self.translate)

    def translate(self):
        # 判断当前选择的翻译引擎
        if self.combox.currentText() == "谷歌":
            api = GoogleTranslator()
        elif self.combox.currentText() == "有道":
            api = YoudaoTranslator()
        elif self.combox.currentText() == "百度":
            api = BaiduTranslator()
        else:
            api = None

        text = self.source_text.toPlainText()
        if text:
            try:
                translated_text = api.get_translation(text)
            except Exception as e:
                # print(e)
                translated_text = "翻译接口调用失败"
        else:
            translated_text = "请输入内容后再翻译"
        self.result_text.setText(translated_text)
        return translated_text


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
