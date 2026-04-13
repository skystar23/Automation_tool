import sys
import os
from PyQt5 import QtWidgets
import subprocess

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(400, 200)

        # Dropdown (ComboBox)
        self.combo = QtWidgets.QComboBox(self)
        self.combo.setGeometry(50, 50, 200, 30)

        # Add Word files (you can populate dynamically)
        self.combo.addItem("Load_Balancing_Test_Document_06-04-2026_14-48-16.docx")
        # self.combo.addItem("example2.docx")

        # Button
        self.button = QtWidgets.QPushButton("Open Document", self)
        self.button.setGeometry(50, 100, 200, 30)
        self.button.clicked.connect(self.open_document)

    def open_document(self):
        selected_file = self.combo.currentText()

        # Ensure full path if needed
        file_path = os.path.abspath(selected_file)

        # Cross-platform way to open
        if sys.platform.startswith("win"):
            os.startfile(file_path)  # Windows
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", file_path])  # macOS
        else:
            subprocess.call(["xdg-open", file_path])  # Linux

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
