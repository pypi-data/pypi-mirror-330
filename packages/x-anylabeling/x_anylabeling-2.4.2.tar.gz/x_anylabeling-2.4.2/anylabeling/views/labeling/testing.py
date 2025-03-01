import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    progress = pyqtSignal(int)  # 用于传递进度值
    send_signal = pyqtSignal(str)  # 用于传递状态信息

    def __init__(self, url, token, form_data):
        super().__init__()
        self.url = url
        self.token = token
        self.form_data = form_data

    def run(self):
        headers = {
            'Authorization': self.token
        }
        response = requests.get(self.url, headers=headers,params=self.form_data)
        print(response.text)
        # 由于是表单数据，通常不会有content-length，所以不显示进度条
        self.send_signal.emit("Request complete")


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('HTTP Request Progress Example')
        layout = QVBoxLayout()

        self.start_button = QPushButton('Start Request')
        self.start_button.clicked.connect(self.start_processing)
        layout.addWidget(self.start_button)

        self.progress_bar = QProgressBar(self)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel(self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def start_processing(self):
        url = 'http://localhost:8092/images'  # 替换为实际的URL
        # token = singleton.Config.get_token()  # 替换为你的Token
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjUsImlzX2FkbWluaXN0cmF0b3JzIjp0cnVlLCJleHAiOjE3MzIwMjgxOTcsImlhdCI6MTczMjAyNDU5N30.S3dRu5cHlbZGYwT_g0frqlximQFt7hTP02VnoAFyiP8'
        params = {
            'size': -1,
            'type': 2,
            'own':1
        }
        # 可以选择文件作为表单数据的一部分
        # options = QFileDialog.Options()
        # # file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
        # #                                            "All Files (*);;Python Files (*.py)", options=options)
        # # if file_name:
        # #     self.form_data['file'] = (file_name, open(file_name, 'rb'), 'application/octet-stream')
        try:
            self.thread = Worker(url, token, params)
            self.thread.send_signal.connect(self.update_status)
            self.thread.start()
        except Exception as e:
            print(e)
    def update_status(self, message):
        self.status_label.setText(message)

from dataclasses import dataclass
from typing import Optional


@dataclass
class Request:
    own: Optional[str] = 1
    size: Optional[str] = -1
    type: Optional[str] = 2
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())