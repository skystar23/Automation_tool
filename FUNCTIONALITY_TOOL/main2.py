import sys
from PyQt5 import QtWidgets
from config import Ui_MainWindow as config
from fun_login import Ui_login_window
from welcome import Ui_MainWindow as welcome
from test_data import Ui_MainWindow as test_data
# from log import Ui_log_window as Ui_log_window
from log1 import Ui_MainWindow as Ui_log_window


class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_login_window()
        self.ui.setupUi(self)


class WelcomePage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = welcome()
        self.ui.setupUi(self)


class LogPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_log_window()
        self.ui.setupUi(self)


class ConfigPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = config()
        self.ui.setupUi(self)

        # self.log_page = QtWidgets.QWidget(self.ui.config_display)
        # self.log_page.hide()
        # self.ui.device_config_widget.show()

        self.ui.device_config.clicked.connect(self.show_device_config)
        # self.ui.log_btn.clicked.connect(self.show_log_page)

    def hide_all(self):
        self.ui.device_config_widget.hide()
        self.ui.config_menu.hide()
        # self.log_page.hide()

    def show_device_config(self):
        self.hide_all()
        self.ui.device_config_widget.show()

    # def show_log_page(self):
    #     self.hide_all()
    #     self.ui.device_config_widget.hide()
    #     self.log_page.show()


class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1200, 800)  # Control the outer window size here

        # Stack widget
        self.stack = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        # Pages
        self.login_page = LoginPage()
        self.welcome_page = WelcomePage()
        self.config_page = ConfigPage()
        self.log_page=LogPage()
        # Add pages to stack
        self.stack.addWidget(self.login_page)
        self.stack.addWidget(self.welcome_page)
        self.stack.addWidget(self.config_page)
        self.stack.addWidget(self.log_page)

        # Start with login
        self.stack.setCurrentWidget(self.login_page)

        self.navi(page="login_page",to_page="self.show_welcome_page",button="login_button")
        self.config()
        self.LOG()
        # Navigation
        # self.login_page.ui.login_button.clicked.connect(self.show_welcome_page)
        # self.welcome_page.ui.config_btn.clicked.connect(self.show_config_page)
        # self.config_page.ui.log_btn.clicked.connect(self.show_log_page)
        # self.welcome_page.ui.log_btn.clicked.connect(self.show_log_page)
        # self.log_page.ui.config_btn.clicked.connect(self.show_config_page)
    
    def config(self):
        self.navi(page="welcome_page",to_page="self.show_config_page",button="config_btn")
        self.navi(page="log_page",to_page="self.show_config_page",button="config_btn")
    
    def LOG(self):
        self.navi(page="welcome_page",to_page="self.show_log_page",button="log_btn")
        self.navi(page="config_page",to_page="self.show_log_page",button="log_btn")
    


    def navi(self,page,to_page,button):
        # self.login_page.ui.login_button.clicked.connect(self.show_welcome_page)
        # self
        eval(f"self.{page}.ui.{button}.clicked.connect({to_page})")
        

    def show_welcome_page(self):
        self.stack.setCurrentWidget(self.welcome_page)

    def show_config_page(self):
        self.stack.setCurrentWidget(self.config_page)
        self.config_page.ui.config_display.show()
        self.config_page.hide_all()

    def show_log_page(self):
        self.stack.setCurrentWidget(self.log_page)
        # self.config_page.ui.config_menu.hide()
        # self.config_page.ui.device_config_widget.hide()
        # self.log_page.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Mainwindow()
    window.show()
    sys.exit(app.exec_())
