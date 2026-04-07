import sys
import subprocess
import platform
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
from PyQt5 import QtWidgets
from PING_CHECK import Ui_PING_CHECK


class PingApp(QtWidgets.QMainWindow,Ui_PING_CHECK):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.PING.clicked.connect(self.run_ping)
    

    def run_ping(self):
        ip = self.IP_address.text().strip()
        if not ip:
            self.statusbar.showMessage("Please enter an IP address")
            return

        self.statusbar.showMessage(f"Pinging {ip}...")

        # Choose correct ping parameter based on OS
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '4', ip]

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True)

            # Show result in the output window
            if result.returncode == 0:
                self.output_window.setPlainText(result.stdout)
            else:
                self.output_window.setPlainText(result.stderr)

            self.statusbar.showMessage("Ping Completed", 3000)

        except Exception as e:
            self.statusbar.showMessage(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = PingApp()
    window.show()
    sys.exit(app.exec_())