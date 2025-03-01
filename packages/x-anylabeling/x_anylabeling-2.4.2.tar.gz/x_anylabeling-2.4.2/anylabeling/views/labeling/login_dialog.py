
import requests
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QLabel, QVBoxLayout, QMessageBox
from humanfriendly.terminal import message
from anylabeling.views.labeling.utils.url import URLProvider
from .config import token  # 导入token变量
from .singleton import Config
from .utils.LoginAccountSingleton import login_account_singleton

class LoginDialog(QDialog):
    def get_login_info(self):
        return self.logged_in, self.login_info
    def __init__(self, parent=None):
        self.logged_in = False
        self.login_info = {}
        super().__init__(parent)
        self.setWindowTitle('Login')
        self.setFixedSize(500, 300)

        self.username_label = QLabel('Username:', self)
        self.username_input = QLineEdit(self)

        self.password_label = QLabel('Password:', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.login_button.clicked.connect(self.send_login_request)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def send_login_request(self):
        username = self.username_input.text()
        password = self.password_input.text()
        # username = "lin"
        # password = "password"
        data = {
            'username': username,
            'password': password
        }
        response = self.post_login_data(data)
        print(token)
        if response:
            QMessageBox.information(self, 'Success', 'Login successful!')
            login_account_singleton.set_account(username)
            print(login_account_singleton.get_account())
            self.accept()
        else:
            QMessageBox.critical(self, 'Error', 'Login failed!')

    def post_login_data(self, data):
        # Replace with your Java backend URL
        url = URLProvider.get_url()+'/user/login'
        # global token  # 声明token为全局变量
        try:
            response = requests.post(url, json=data)

            status=response.json()["status"]

            if status == 200:
                print("Login successful.")
                print("Response data:", response.json())
                response_data = response.json()
                self.logged_in=True
                self.login_info=response_data.get('data',{})
                token = response_data.get('data', {}).get('token')
                config=Config()
                config.set_token(token)
                print(config.get_token())
                if token:
                    print("Token updated successfully.")
                    return True
                else:
                    print("Token not found in response.")
                    return False
                # return response.json()
            else:
                print("Login failed.")
                return None
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, 'Error', str(e))
            return None
