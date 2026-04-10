import sys, os, subprocess
from PyQt5 import QtWidgets, QtGui

# ------------------ Runner Window ------------------
class RunnerWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pytest Runner")
        self.setGeometry(200, 200, 800, 600)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        # Test file
        self.file_path = QtWidgets.QLineEdit()
        self.file_path.setPlaceholderText("Select test file...")
        browse_btn = QtWidgets.QPushButton("Browse Test File")
        browse_btn.clicked.connect(self.browse_file)

        # Device IP, Username, Password, Mark
        self.device_ip = QtWidgets.QLineEdit()
        self.device_ip.setPlaceholderText("Device IP")

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        self.mark = QtWidgets.QLineEdit()
        self.mark.setPlaceholderText("Mark")

        # Run button
        run_btn = QtWidgets.QPushButton("Run Tests")
        run_btn.clicked.connect(self.run_pytest)

        # Output box
        self.output_box = QtWidgets.QTextEdit()
        self.output_box.setReadOnly(True)

        # Add widgets
        layout.addWidget(self.file_path)
        layout.addWidget(browse_btn)
        layout.addWidget(self.device_ip)
        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(self.mark)
        layout.addWidget(run_btn)
        layout.addWidget(self.output_box)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def browse_file(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a pytest file", "./Testcases", "Python Files (*.py)"
        )
        if filename:
            self.file_path.setText(filename)

    def run_pytest(self):
        test_file = self.file_path.text().strip()
        device_ip = self.device_ip.text().strip()
        username = self.username.text().strip()
        password = self.password.text().strip()
        mark = self.mark.text().strip()

        if not test_file or not os.path.isfile(test_file):
            QtWidgets.QMessageBox.critical(self, "Error", "Please select a valid test file")
            return

        if not device_ip or not username or not password:
            QtWidgets.QMessageBox.critical(self, "Error", "Please fill in device IP, username, and password")
            return

        cmd = ["pytest", "-v", "-s", test_file,
               f"--deviceip={device_ip}",
               f"--username={username}",
               f"--password={password}"]
        if mark:
            cmd.extend(["-m", mark])

        result = subprocess.run(cmd, capture_output=True, text=True)
        self.output_box.clear()
        self.output_box.append(result.stdout)
        if result.stderr:
            self.output_box.append("\nErrors:\n" + result.stderr)


# ------------------ Login Window ------------------
class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 400, 200)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()

        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("Username")

        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)

        login_btn = QtWidgets.QPushButton("Login")
        login_btn.clicked.connect(self.validate_login)

        layout.addWidget(self.username)
        layout.addWidget(self.password)
        layout.addWidget(login_btn)

        central.setLayout(layout)
        self.setCentralWidget(central)

    def validate_login(self):
        if self.username.text().strip() == "root" and self.password.text().strip() == "root":
            QtWidgets.QMessageBox.information(self, "Login Success", "Welcome!")
            self.runner = RunnerWindow()
            self.runner.show()
            self.close()  # close login window
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Invalid credentials")


# ------------------ Main ------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
