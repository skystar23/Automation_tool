import sys
from PyQt5 import QtWidgets,uic
from page_1 import Ui_page_1
from page_2 import Ui_page_2



class Page1(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_page_1()
        self.ui.setupUi(self)


class Page2(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.ui=Ui_page_2()
        self.ui.setupUi(self)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(500,400)
        self.setWindowTitle("StackedWidget Practice")
        
        #Created stacked widget
        self.stack=QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stack)

        #Created pages
        self.page_1=Page1()
        self.page_2=Page2()

        #Adding pages to stack
        self.stack.addWidget(self.page_1)
        self.stack.addWidget(self.page_2)

        #showing page_1 first
        self.stack.setCurrentWidget(self.page_1)

        self.page_1.ui.pushButton.clicked.connect(self.show_page_2)

    def show_page_2(self):
        self.stack.setCurrentWidget(self.page_2)

        

if __name__ =="__main__":
    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())