import sys
import subprocess
import platform
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import configparser
from PyQt5 import QtWidgets,QtCore
from login_window import Ui_MainWindow as Ui_Login
from Device_login import Ui_NOMUS as Ui_Device
from PING_CHECK import Ui_PING_CHECK as Ui_Ping

class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        self.ui.Login.clicked.connect(self.validate_login)

    def validate_login(self):
        if self.ui.Username.text().strip() == "root" and self.ui.Password.text().strip() == "root":
            QtWidgets.QMessageBox.information(self, "Login Success", "Welcome!")
            self.device_window = PingWindow()
            self.device_window.show()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Invalid credentials")

class DeviceLoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Device()
        self.ui.setupUi(self)
        self.ui.select_dropdown.hide()
        self.ui.Select_ini_file.hide()
        self.ui.edit_ini_checkbox.stateChanged.connect(self.toggle_dropdown)

    def toggle_dropdown(self, state):
        if state == QtCore.Qt.Checked:
            self.ui.select_dropdown.show()
            self.ui.Select_ini_file.show()
        else:
            self.ui.select_dropdown.hide()
            self.ui.Select_ini_file.hide()
        self.ui.Run.clicked.connect(self.run_pytest)

    # def run_tests(self):
    #     print("Running automation...")  
    def run_pytest(self):
        # Example: run pytest with selected section name as marker
        section = self.section_dropdown.currentText()
        test_file = "/opt/V3_functional_testing/Testcases/test_Load_Balancing_1.py"  # your test file

        cmd = ["pytest", "-v", "-s",test_file]
        result = subprocess.run(cmd, capture_output=True, text=True)

        self.output_box.clear()
        self.output_box.append(result.stdout)
        if result.stderr:
            self.output_box.append("\nErrors:\n" + result.stderr)

class PingWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=Ui_Ping()
        self.ui.setupUi(self)
        self.ui.PING.clicked.connect(self.run_ping)
    
    def run_ping(self):
        ip = self.ui.IP_address.text().strip()
        if not ip:
            self.ui.statusbar.showMessage("Please enter an IP address")
            return
        self.ui.statusbar.showMessage(f"Pinging {ip}...")
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', ip]
        try:
            result = subprocess.run(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)
            if result.returncode == 0:
                self.ui.output_window.setPlainText(result.stdout)
            else:
                self.ui.output_window.setPlainText(result.stderr)
            self.ui.statusbar.showMessage("Ping Completed", 3000)
        except Exception as e:
            self.ui.statusbar.showMessage(f"Error: {str(e)}")
        self.devicewindow=DeviceLoginWindow()
        self.devicewindow.show()
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
