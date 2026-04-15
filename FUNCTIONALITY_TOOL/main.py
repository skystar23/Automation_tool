import sys,shutil
import os,subprocess
from PyQt5 import QtWidgets,QtCore
from src.config_ui import Ui_MainWindow as config
from src.fun_login_ui import Ui_login_window
from src.welcome_ui import Ui_MainWindow as welcome
from src.log_ui import Ui_MainWindow  as Ui_log_window
from src.reports_ui import Ui_reports
from src.test_runner_ui import Ui_test_runner
from src.dummy_ui import Ui_test_data_widget
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
import stat


class LoginWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(600,400)
        self.ui=Ui_login_window()
        self.ui.setupUi(self)


class WelcomeWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,400)
        self.ui=welcome()
        self.ui.setupUi(self)


class LogWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_log_window()
        self.ui.setupUi(self)
        # Path to your log file
        # Create a plain text area
        

        # Make it read-only
        self.ui.logs_display.setReadOnly(True)

        # Always show scrollbars
        # self.ui.logs_display.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.ui.logs_display.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        # Load log file
        self.log_file = "WiZNG.log"
        self.load_logs()
        self.ui.refresh_btn.clicked.connect(self.load_logs)
        self.ui.export_btn.clicked.connect(self.export_log)

    def load_logs(self):
        try:
            with open(self.log_file, "r") as f:
                content = f.read()

            # Show file content exactly as-is
            self.ui.logs_display.setPlainText(content)

            # Move cursor to the end so view starts at bottom
            cursor = self.ui.logs_display.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            self.ui.logs_display.setTextCursor(cursor)
            self.ui.logs_display.ensureCursorVisible()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Could not load log file:\n{e}")

    def export_log(self):
        source_path = os.path.abspath(self.log_file)

        # Ask user where to save
        target_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Document As",
            self.log_file,  # default filename
            "Word Documents (*.txt *.log)"
        )

        if target_path:
            try:
                shutil.copy(source_path, target_path)
                QtWidgets.QMessageBox.information(self, "Success", f"File saved to:\n{target_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")


class TestdataPage(QtWidgets.QWidget,Ui_test_data_widget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # self.ui = Ui_test_data_widget()
        self.setupUi(self)

        

class ReportWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_reports()
        self.ui.setupUi(self)
        self.ui.protocol_dp.addItem("Load_Balancing")
        self.ui.report_dp.addItem("Load_Balancing_Test_Document_06-04-2026_14-48-16.docx")
        self.ui.report_view.clicked.connect(self.open_docx_view_only)
        self.ui.report_export.clicked.connect(self.export_document)

    def open_document(self):
        selected_file = self.ui.report_dp.currentText()

        # Ensure full path if needed
        file_path = os.path.abspath(selected_file)

        # Cross-platform way to open
        if sys.platform.startswith("win"):
            os.startfile(file_path)  # Windows
        elif sys.platform.startswith("darwin"):
            subprocess.run(["open", file_path], check=True)  # macOS
        else:
            subprocess.run(["xdg-open", file_path], check=True)  # Linux

    def open_docx_view_only(self):
        selected_file = self.ui.report_dp.currentText()

        # Ensure full path if needed
        file_path = os.path.abspath(selected_file)
        """
        Opens a .docx file in view/read-only mode using the default application.
        Works on Windows, macOS, and Linux.
        """
        if not os.path.exists(file_path):
            print(f"Error: File not found - {file_path}")
            return

        # Step 1: Make the file read-only at OS level (helps force view mode)
        try:
            current_permissions = os.stat(file_path).st_mode
            # Remove write permissions for user, group, and others
            os.chmod(file_path, current_permissions & ~stat.S_IWUSR & ~stat.S_IWGRP & ~stat.S_IWOTH)
            print(f"File set to read-only: {file_path}")
        except Exception as e:
            print(f"Warning: Could not set read-only permission: {e}")

        # Step 2: Open with default application (cross-platform)
        try:
            system = platform.system()
            
            if system == "Windows":
                # On Windows, os.startfile is simplest and respects default app
                os.startfile(file_path)
                
            elif system == "Darwin":  # macOS
                # 'open' command opens with default app
                subprocess.run(["open", file_path], check=True)
                
            else:  # Linux and other Unix-like
            #    try:
                    subprocess.run(["libreoffice", "--view", file_path], check=True)
                    # print("? Opened in view mode using LibreOffice --view")
                    # return
                # except FileNotFoundError:

                    # Fallback
                    subprocess.run(["xdg-open", file_path], check=True)
            
        except Exception as e:
            print(f"Error opening file: {e}")
            # Fallback: try to open with Python's webbrowser (less reliable for docx)
            import webbrowser
            webbrowser.open(f"file://{os.path.abspath(file_path)}")

    def export_document(self):
        selected_file = self.ui.report_dp.currentText()
        source_path = os.path.abspath(selected_file)

        # Ask user where to save
        target_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Document As",
            selected_file,  # default filename
            "Word Documents (*.docx *.doc)"
        )

        if target_path:
            try:
                shutil.copy(source_path, target_path)
                QtWidgets.QMessageBox.information(self, "Success", f"File saved to:\n{target_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Could not save file:\n{e}")

class TestRunnerWindow(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_test_runner()
        self.ui.setupUi(self)
        self.ui.mark_label.hide()
        self.ui.mark_str.hide()

        self.ui.protocol_dp.addItems(["Bgp","Ospf2","Ospf3","Ipsec"])
        
            
        self.ui.run_btn.clicked.connect(self.run_command)

    def run_command(self):
          # replace with your command
        if not self.ui.add_mark.isChecked():
            self.command = f"pytest -v -s ./Testcases/test_{self.ui.protocol_dp.currentText()}.py"
        else:
            self.command = f"pytest -v -s ./Testcases/test_{self.ui.protocol_dp.currentText()}.py -m {self.ui.mark_str.text()}"
        
        QtWidgets.QMessageBox.information(self, "Success",f"{self.command}")
        if sys.platform.startswith("win"):
            # Windows: run command and close terminal after completion
            subprocess.Popen(["cmd", "/c", self.command])
        elif sys.platform.startswith("darwin"):
            # macOS: open Terminal and run command, then close
            subprocess.Popen(["osascript", "-e",
                f'tell application "Terminal" to do script "{self.command}; exit"'])
        else:
            # Linux: run command in gnome-terminal and close after completion
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{self.command}"])

class ConfigWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800,400)
        self.ui=config()
        self.ui.setupUi(self)
        
        
        self.stack = QtWidgets.QStackedWidget(self.ui.config_display)  # or self.centralWidget()
        self.ui.config_menu = QtWidgets.QVBoxLayout(self.ui.config_menu)
        self.ui.config_menu.addWidget(self.stack)

        # Pages
        self.device_config_page = self.ui.device_config_widget
        self.test_data_page = TestdataPage()

        # Add pages to stack
        self.stack.addWidget(self.device_config_page)
        self.stack.addWidget(self.test_data_page)

        # Default page
        self.stack.setCurrentWidget(self.device_config_page)

        # Connect buttons
        self.ui.device_config.clicked.connect(self.show_device_config)
        self.ui.test_data.clicked.connect(self.show_test_data)

    def show_device_config(self):
        self.stack.setCurrentWidget(self.device_config_page)

    def show_test_data(self):
        self.stack.setCurrentWidget(self.test_data_page)
   
        




class Mainwindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        #Created stack widget
        self.resize(1200,800)
        self.stack=QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)
        #Creating pages
        self.login_window=LoginWindow()
        self.welcome_window=WelcomeWindow()
        self.config_window=ConfigWindow()
        self.log_window=LogWindow()
        self.reports_window=ReportWindow()
        self.test_runner_window=TestRunnerWindow()
        # self.test_data_window=test_data()
        #Adding pages to stack
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.welcome_window)
        self.stack.addWidget(self.config_window)
        self.stack.addWidget(self.log_window)
        self.stack.addWidget(self.reports_window)
        self.stack.addWidget(self.test_runner_window)
        # self.stack.addWidget(self.test_data_window)

        self.stack.setCurrentWidget(self.login_window)

        self.login_window.ui.login_button.clicked.connect(self.show_welcome_page)
        self.config()
        self.LOG()
        self.Reports()
        self.Test_Runner()

    def config(self):
        self.navi(page="welcome_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="log_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="reports_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="test_runner_window",to_page="self.show_config_window",button="config_btn")
        

    def LOG(self):
        self.navi(page="welcome_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="config_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="reports_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="test_runner_window",to_page="self.show_log_window",button="log_btn")
    
    def Reports(self):
        self.navi(page="welcome_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="config_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="log_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="test_runner_window",to_page="self.show_report_window",button="report_btn")

    def Test_Runner(self):
        self.navi(page="welcome_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="config_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="reports_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="log_window",to_page="self.show_test_runner_window",button="test_runner_btn")



    def navi(self,page,to_page,button):
        eval(f"self.{page}.ui.{button}.clicked.connect({to_page})")
      
        
    def show_welcome_page(self):
        self.stack.setCurrentWidget(self.welcome_window)

    def show_config_window(self):
        self.stack.setCurrentWidget(self.config_window)
        # self.config_window.ui.config_display.show()
        # self.config_window.hide_all()
    
    def show_log_window(self):
        self.stack.setCurrentWidget(self.log_window)
        
    def show_test_runner_window(self):
        self.stack.setCurrentWidget(self.test_runner_window)
    
    def show_report_window(self):
        self.stack.setCurrentWidget(self.reports_window)
    


if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    window=Mainwindow()
    window.show()
    sys.exit(app.exec_())



