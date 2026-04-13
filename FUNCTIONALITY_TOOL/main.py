import os
import subprocess
import sys
import platform
from PyQt5 import QtWidgets,QtCore,uic
from config import Ui_MainWindow as Ui_config
from fun_login import Ui_login_window as Ui_login
from welcome import Ui_MainWindow as Ui_welcome
from test_data import Ui_MainWindow as Ui_test

class ConfigWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_config()
        self.ui.setupUi(self)

        # Create extra widgets
        self.test_data_widget = QtWidgets.QWidget(self.ui.config_menu)
        self.test_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.test_data_widget.setObjectName("test_data_widget")

        layout = QtWidgets.QVBoxLayout(self.test_data_widget)
        label = QtWidgets.QLabel("This is the Test Data widget")
        layout.addWidget(label)

        self.source_data_widget = QtWidgets.QWidget(self.ui.config_menu)
        self.source_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.source_data_widget.setObjectName("source_data_widget")

        self.gns3_data_widget = QtWidgets.QWidget(self.ui.config_menu)
        self.gns3_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.gns3_data_widget.setObjectName("gns3_data_widget")

       

    
        self.test_data_widget.hide()
        self.source_data_widget.hide()
        self.gns3_data_widget.hide()
        self.ui.device_config_widget.show()

    
        self.ui.test_data.clicked.connect(self.show_test_data)
        self.ui.device_config.clicked.connect(self.show_device_info)
       
       

    def hide_all_content(self):
        """Helper to hide all content widgets"""
        self.ui.device_config_widget.hide()
        self.test_data_widget.hide()
        self.source_data_widget.hide()
        self.gns3_data_widget.hide()

    def show_test_data(self):
        self.hide_all_content()
        self.test_data_widget.show()

    def show_device_info(self):
        self.hide_all_content()
        self.ui.device_config_widget.show()
    

    def hide_all_content(self):
        """Helper to hide all content widgets"""
        self.ui.device_config_widget.hide()
        self.test_data_widget.hide()
        self.source_data_widget.hide()
        self.gns3_data_widget.hide()

    def show_test_data(self):
        self.hide_all_content()
        self.test_data_widget.show()

    def show_device_info(self):
        self.hide_all_content()
        self.ui.device_config_widget.show()

class Sidemenu(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_welcome()
        self.ui.setupUi(self)

        self.config_page=ConfigWindow()
        self.config_page.setParent(self)
        self.config_page.hide()
        self.ui.config_btn.clicked.connect(self.config_window)
        
    
    def config_window(self):
        self.ui.centralwidget.hide()  
        self.config_page.show()
                

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500,400)
        self.ui=Ui_login()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.validate_login)
    
    

    def validate_login(self):
        if self.ui.Username.text().strip() == "root" and self.ui.Password.text().strip() == "root":
            self.welcome_window=Sidemenu()
            self.welcome_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Invalid credentials")


    
if __name__ =="__main__":
    app=QtWidgets.QApplication(sys.argv)
    login=LoginWindow()
    login.show()
    sys.exit(app.exec_())