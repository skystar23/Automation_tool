import sys,shutil
import os,subprocess
import stat
import json
from pathlib import Path

#sourepages imports
from src.config_ui import Ui_MainWindow as config
from src.fun_login_ui import Ui_login_window
from src.welcome_ui import Ui_MainWindow as welcome
from src.log_ui import Ui_MainWindow  as Ui_log_window
from src.reports_ui import Ui_reports
from src.test_runner_ui import Ui_test_runner
from src.test_data_ui import Ui_MainWindow as test_data
from src.gns3_data_ui import Ui_MainWindow as gns3_data
from src.source_data_ui import Ui_MainWindow as source_data
from src.json_editor_ui import Ui_MainWindow as json_window

#PyQt5 Modules imports
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QComboBox, QTableWidget, QTableWidgetItem,
    QPushButton, QVBoxLayout, QWidget
)
from PyQt5.QtWidgets import QMessageBox



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

class TestdataPage(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = test_data()
        self.ui.setupUi(self)

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
        # self.resize(800,400)
        self.ui=config()
        self.ui.setupUi(self)
        
        
    #     self.stack = QtWidgets.QStackedWidget(self.ui.config_display)  # or self.centralWidget()
    #     self.ui.config_menu = QtWidgets.QVBoxLayout(self.ui.config_menu)
    #     self.ui.config_menu.addWidget(self.stack)

    #     # Pages
    #     self.device_config_page = self.ui.device_config_widget
    #     self.test_data_page = TestdataPage()

    #     # Add pages to stack
    #     self.stack.addWidget(self.device_config_page)
    #     self.stack.addWidget(self.test_data_page)

    #     # Default page
    #     self.stack.setCurrentWidget(self.device_config_page)

    #     # Connect buttons
    #     self.ui.device_config.clicked.connect(self.show_device_config)
    #     self.ui.test_data.clicked.connect(self.show_test_data)

    # def show_device_config(self):
    #     self.stack.setCurrentWidget(self.device_config_page)

    # def show_test_data(self):
    #     self.stack.setCurrentWidget(self.test_data_page)
   

class SourcedataWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=source_data()
        self.ui.setupUi(self)


class JsonWindow(QtWidgets.QMainWindow):
    def __init__(self,JSON_FILE):
        super().__init__()
        self.ui=json_window()
        self.ui.setupUi(self)

        self.JSON_FILE = JSON_FILE
        print(self.JSON_FILE)
        # Load JSON
        with open(self.JSON_FILE, "r") as f:
            self.data = json.load(f)

        # Populate dropdown
        self.ui.comboBox.addItems(self.data.keys())
        self.ui.comboBox.currentTextChanged.connect(self.load_section)

        self.ui.saveButton.clicked.connect(self.save_json)
        self.load_section(self.ui.comboBox.currentText())
    
    def load_section(self, section):
        self.ui.tableWidget.setRowCount(0)
        section_data = self.data[section]

        flat_data = self.flatten_json(section_data)

        self.ui.tableWidget.setRowCount(len(flat_data))
        for row, (key, value) in enumerate(flat_data.items()):
            key_item = QTableWidgetItem(key)
            key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)  # make key read-only
            self.ui.tableWidget.setItem(row, 0, key_item)

            val_item = QTableWidgetItem(str(value))
            self.ui.tableWidget.setItem(row, 1, val_item)

    def flatten_json(self, obj, parent_key=""):
        items = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                items.update(self.flatten_json(v, new_key))
        elif isinstance(obj, list):
            for i, v in enumerate(obj):
                new_key = f"{parent_key}[{i}]"
                items.update(self.flatten_json(v, new_key))
        else:
            items[parent_key] = obj
        return items

    def save_json(self):
        section = self.ui.comboBox.currentText()
        updated = {}
        for row in range(self.ui.tableWidget.rowCount()):
            key = self.ui.tableWidget.item(row, 0).text()
            value = self.ui.tableWidget.item(row, 1).text()
            updated[key] = value

        # Replace section with flat dict (can extend to rebuild nested structure)
        self.data[section] = updated

        with open(self.JSON_FILE, "w") as f:
            json.dump(self.data, f, indent=4)

        print(f"Section {section} saved!")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Saved")
        msg.setText(f"'{section}' has been saved successfully.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

        
        self.close()


class Gns3dataWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui=gns3_data()
        self.ui.setupUi(self)

        # Populate protocol dropdown
        folder_path = Path("/opt/V3_functional_testing/GNS3_data")
        self.ui.gns3_data_proto_dp.addItems([f.name for f in folder_path.iterdir() if f.is_dir()])
        self.ui.gns3_data_proto_dp.currentTextChanged.connect(self.update_file_list)

        # Initialize file list
        self.update_file_list(self.ui.gns3_data_proto_dp.currentText())

        # Connect signals
        self.ui.gns3_data_title_dp.currentTextChanged.connect(self.update_json_file)
        self.ui.gns3_data_open.clicked.connect(self.show_json_window)
    
        

    def update_file_list(self, proto):
        file_path = f"/opt/V3_functional_testing/GNS3_data/{proto}"
        folder_path = Path(file_path)
        self.ui.gns3_data_title_dp.clear()
        self.ui.gns3_data_title_dp.addItems([f.name for f in folder_path.iterdir() if f.is_file()])
        # Update json_file to first item
        self.update_json_file(self.ui.gns3_data_title_dp.currentText())

    def update_json_file(self, filename):
        proto = self.ui.gns3_data_proto_dp.currentText()
        self.json_file = f"/opt/V3_functional_testing/GNS3_data/{proto}/{filename}"
    
    def show_json_window(self):
        # super().__init__()
        # self.ui.setupUi(self)
        self.json = JsonWindow(self.json_file)
        self.json.show()

        



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
        self.test_data_window=TestdataPage()
        self.source_data_window=SourcedataWindow()
        self.gns3_data_window=Gns3dataWindow()

        #Adding pages to stack
        self.stack.addWidget(self.login_window)
        self.stack.addWidget(self.welcome_window)
        self.stack.addWidget(self.config_window)
        self.stack.addWidget(self.log_window)
        self.stack.addWidget(self.reports_window)
        self.stack.addWidget(self.test_runner_window)
        self.stack.addWidget(self.test_data_window)
        self.stack.addWidget(self.source_data_window)
        self.stack.addWidget(self.gns3_data_window)

        self.stack.setCurrentWidget(self.login_window)

        self.login_window.ui.login_button.clicked.connect(self.show_welcome_page)
        self.config()
        self.LOG()
        self.Reports()
        self.Test_Runner()
        self.Test_data()
        self.Source_data()
        self.Device_config()
        self.Gns3_config()

    def config(self):
        self.navi(page="welcome_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="log_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="reports_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="test_runner_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="test_data_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="source_data_window",to_page="self.show_config_window",button="config_btn")
        self.navi(page="gns3_data_window",to_page="self.show_config_window",button="config_btn")

    def LOG(self):
        self.navi(page="welcome_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="config_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="reports_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="test_runner_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="test_data_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="source_data_window",to_page="self.show_log_window",button="log_btn")
        self.navi(page="gns3_data_window",to_page="self.show_log_window",button="log_btn")

    def Reports(self):
        self.navi(page="welcome_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="config_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="log_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="test_runner_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="test_data_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="source_data_window",to_page="self.show_report_window",button="report_btn")
        self.navi(page="gns3_data_window",to_page="self.show_report_window",button="report_btn")
    
    def Test_Runner(self):
        self.navi(page="welcome_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="config_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="reports_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="log_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="test_data_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="source_data_window",to_page="self.show_test_runner_window",button="test_runner_btn")
        self.navi(page="gns3_data_window",to_page="self.show_test_runner_window",button="test_runner_btn")

    def Test_data(self):
        self.navi(page="config_window",to_page="self.show_test_data_window",button="test_data")
        self.navi(page="source_data_window",to_page="self.show_test_data_window",button="test_data")
        self.navi(page="gns3_data_window",to_page="self.show_test_data_window",button="test_data")


    def Source_data(self):
        self.navi(page="config_window",to_page="self.show_source_data_window",button="source_data")
        self.navi(page="test_data_window",to_page="self.show_source_data_window",button="source_data")
        self.navi(page="gns3_data_window",to_page="self.show_source_data_window",button="source_data")
        

    def Gns3_config(self):
        self.navi(page="config_window",to_page="self.show_gns3_data_window",button="gns3_config")
        self.navi(page="test_data_window",to_page="self.show_gns3_data_window",button="gns3_config")
        self.navi(page="source_data_window",to_page="self.show_gns3_data_window",button="gns3_config")
    

    def Device_config(self):
        self.navi(page="test_data_window",to_page="self.show_config_window",button="device_config")
        self.navi(page="source_data_window",to_page="self.show_config_window",button="device_config")
        self.navi(page="gns3_data_window",to_page="self.show_config_window",button="device_config")




    def navi(self,page,to_page,button):
        eval(f"self.{page}.ui.{button}.clicked.connect({to_page})")
      
        
    def show_welcome_page(self):
        self.stack.setCurrentWidget(self.welcome_window)

    def show_config_window(self):
        self.stack.setCurrentWidget(self.config_window)
        
    def show_log_window(self):
        self.stack.setCurrentWidget(self.log_window)
        
    def show_test_runner_window(self):
        self.stack.setCurrentWidget(self.test_runner_window)
    
    def show_report_window(self):
        self.stack.setCurrentWidget(self.reports_window)
    
    def show_test_data_window(self):
        self.stack.setCurrentWidget(self.test_data_window)

    def show_source_data_window(self):
        self.stack.setCurrentWidget(self.source_data_window)

    def show_gns3_data_window(self):
        self.stack.setCurrentWidget(self.gns3_data_window)
    

if __name__ == "__main__":
    app=QtWidgets.QApplication(sys.argv)
    window=Mainwindow()
    window.show()
    sys.exit(app.exec_())



