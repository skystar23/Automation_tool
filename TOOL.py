import sys, os, subprocess
import configparser
from PyQt5 import QtWidgets

INI_FILE = "/opt/V3_functional_testing/Testdata/Load_Balancing_data.ini"   # path to your ini file

# ------------------ Runner Window ------------------
class RunnerWindow(QtWidgets.QMainWindow):
    def __init__(self, ini_file):
        super().__init__()
        self.setWindowTitle("NOMUS")
        self.setGeometry(200, 200, 800, 600)

        self.ini_file = INI_FILE
        self.config = configparser.ConfigParser()
        self.config.read(self.ini_file)

        central = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout()

        #username ,Password ,Device ip
        # Username, Password, Device IP, Mark fields
        
        self.username = QtWidgets.QLineEdit()
        self.username.setPlaceholderText("Username")
        self.layout.addWidget(self.username)

        self.password = QtWidgets.QLineEdit()
        self.password.setPlaceholderText("Password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.layout.addWidget(self.password)

        self.device_ip = QtWidgets.QLineEdit()
        self.device_ip.setPlaceholderText("Device IP")
        self.layout.addWidget(self.device_ip)

        # Dropdown for sections
        self.section_dropdown = QtWidgets.QComboBox()
        self.section_dropdown.addItems(self.config.sections())
        self.section_dropdown.currentTextChanged.connect(self.load_section)
        self.layout.addWidget(self.section_dropdown)

        # Area for key/value fields
        self.fields_layout = QtWidgets.QFormLayout()
        self.layout.addLayout(self.fields_layout)

        # Save button
        save_btn = QtWidgets.QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_changes)
        self.layout.addWidget(save_btn)

        # Run button
        run_btn = QtWidgets.QPushButton("Run Tests")
        run_btn.clicked.connect(self.run_pytest)
        self.layout.addWidget(run_btn)

        # Output box
        self.output_box = QtWidgets.QTextEdit()
        self.output_box.setReadOnly(True)
        self.layout.addWidget(self.output_box)

        central.setLayout(self.layout)
        self.setCentralWidget(central)

        # Load first section initially
        self.load_section(self.section_dropdown.currentText())

    def load_section(self, section):
        # Clear old fields
        while self.fields_layout.count():
            item = self.fields_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.inputs = {}
        for key, value in self.config[section].items():
            line_edit = QtWidgets.QLineEdit(value)
            self.fields_layout.addRow(key, line_edit)
            self.inputs[key] = line_edit

    def save_changes(self):
        section = self.section_dropdown.currentText()
        for key, line_edit in self.inputs.items():
            self.config[section][key] = line_edit.text()

        with open(self.ini_file, "w") as f:
            self.config.write(f)

        QtWidgets.QMessageBox.information(self, "Saved", f"Changes saved to {self.ini_file}")

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
            self.runner = RunnerWindow(INI_FILE)
            self.runner.show()
            self.close()
        else:
            QtWidgets.QMessageBox.critical(self, "Login Failed", "Invalid credentials")


# ------------------ Main ------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = LoginWindow()
    login.show()
    sys.exit(app.exec_())
