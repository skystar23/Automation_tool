import os
import subprocess
import sys
import platform
from PyQt5 import QtWidgets,QtCore
from config import Ui_MainWindow as Ui_config
from fun_login import Ui_login_window as Ui_login

class ConfigWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_config()
        self.ui.setupUi(self)
        self.test_data_widget = QtWidgets.QWidget(self.ui.sideMenuFrame_2)
        self.test_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.test_data_widget.setObjectName("test_data_widget")
        self.source_data_widget = QtWidgets.QWidget(self.ui.sideMenuFrame_2)
        self.source_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.source_data_widget.setObjectName("source_data_widget")
        self.gns3_data_widget = QtWidgets.QWidget(self.ui.sideMenuFrame_2)
        self.gns3_data_widget.setGeometry(QtCore.QRect(0, 40, 961, 471))
        self.gns3_data_widget.setObjectName("gns3_data_widget")
        layout = QtWidgets.QVBoxLayout(self.test_data_widget)
        label = QtWidgets.QLabel("This is the Test Data widget")
        layout.addWidget(label)
        self.test_data_widget.hide()
        self.ui.device_config_widget.hide()
        

    def show_test_data(self):
        self.ui.device_config_widget.hide()
        self.test_data_widget.show()
    
    def show_device_info(self):
        self.ui.device_config_widget.show()
        self.test_data_widget.hide()
    
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_login()
        self.ui.setupUi(self)
        self.ui.login_button.clicked.connect(self.validate_login)

    def validate_login(self):
        if self.ui.Username.text().strip() == "root" and self.ui.Password.text().strip() == "root":
            QtWidgets.QMessageBox.information(self, "Login Success", "Welcome!")
            self.config_window=ConfigWindow()
            self.config_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Invalid credentials")


    
if __name__ =="__main__":
    app=QtWidgets.QApplication(sys.argv)
    login=LoginWindow()
    login.show()
    sys.exit(app.exec_())