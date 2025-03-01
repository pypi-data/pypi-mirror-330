from PyQt5.QtCore import QSettings, QUrl, QTimer, QCoreApplication, pyqtSignal

class LoginAccountSingleton(QSettings):
    # 定义一个信号，当登录账号发生变化时发出
    login_account_changed = pyqtSignal(str)

    def __init__(self, application):
        super().__init__(application)
        # 读取已保存的登录账号信息
        self.read_account_info()

    def read_account_info(self):
        # 从QSettings中读取登录账号信息
        self.account = self.value("login_account", "")
        # 发出信号通知登录账号发生变化
        self.login_account_changed.emit(self.account)

    def set_account(self, account):
        # 设置登录账号信息
        self.account = account
        # 保存到QSettings中
        self.setValue("login_account", account)
        # 发出信号通知登录账号发生变化
        self.login_account_changed.emit(account)

    def get_account(self):
        # 获取登录账号信息
        return self.account


login_account_singleton = LoginAccountSingleton(QCoreApplication.instance())
