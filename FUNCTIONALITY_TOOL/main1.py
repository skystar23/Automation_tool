import sys
from PyQt5 import QtWidgets,QtCore
from config import Ui_MainWindow as config
from fun_login import Ui_login_window
from welcome import Ui_MainWindow as welcome
from test_data import Ui_MainWindow as test_data
from log import Ui_log_window as Ui_log_window

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_login_window()
        self.ui.setupUi(self)


class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=welcome()
        self.ui.setupUi(self)


class LogWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_log_window()
        self.ui.setupUi(self)





class ConfigWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=config()
        self.ui.setupUi(self)
        
        self.log_window=LogWindow(self.ui.config_display)      
        self.log_window.hide()
        self.ui.device_config_widget.show()

  
        self.ui.device_config.clicked.connect(self.show_device_config)
        self.ui.log_btn.clicked.connect(self.show_log_window)
        

    def hide_all(self):
        self.ui.device_config_widget.hide()
        self.log_window.hide()
    
    def show_device_config(self):
        self.hide_all()
        self.ui.device_config_widget.show()

    def show_log_window(self):
        self.hide_all()
        self.ui.device_config_widget.hide()
        self.log_window.show()




class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #Created stack widget
        self.stack=QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        #Creating pages
        self.login_window=LoginWindow()
        self.welcome_window=WelcomeWindow()
        self.config_window=ConfigWindow()
        # self.log_window=LogWindow()
   
        #Adding pages to stack
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.welcome_window)
        self.stack.addWidget(self.config_window)
        # self.stack.addWidget(self.log_window)

        self.stack.setCurrentWidget(self.login_window)

        self.login_window.ui.login_button.clicked.connect(self.show_welcome_page)
        self.welcome_window.ui.config_btn.clicked.connect(self.show_config_window)
      
        

    def show_welcome_page(self):
        self.stack.setCurrentWidget(self.welcome_window)

    def show_config_window(self):
        self.stack.setCurrentWidget(self.config_window)
        self.config_window.ui.config_display.show()
        self.config_window.hide_all()
    
    def show_log_window(self):
        self.stack.setCurrentWidget(self.log_window)
        

    
    


if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    window=Mainwindow()
    window.show()
    sys.exit(app.exec_())



