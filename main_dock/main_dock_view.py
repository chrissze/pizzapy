import sys; sys.path.append('..')

from datetime import date
from PySide2.QtCore import QDate
from PySide2.QtGui import QCloseEvent

from PySide2.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)
from typing import Tuple


class MainDockWin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Pizza Dock')
        self.setGeometry(50, 50, 1000, 750)

        self.central = QWidget()
        self.setCentralWidget(self.central)

        self.gbox1 = QGroupBox('Daily Stock')
        self.gbox1.setCheckable(True)
        self.gbox2 = QGroupBox('Daily Future')
        self.gbox3 = QGroupBox('US Stock GZ')
        self.gbox4 = QGroupBox('GBox4')

        self.b1_1 = QPushButton('b1_1 US Stock Browser')
        self.b1_1.setAccessibleName('b1_1')
        self.b1_2 = QPushButton('b1_2 US Stock Price Update')
        self.b1_2.setAccessibleName('b1_2')
        self.b1_3 = QPushButton('b1_3')
        self.b1_3.setAccessibleName('b1_3')


        self.b2_1 = QPushButton('b2_1 Futures Browser')
        self.b2_1.setAccessibleName('b2_1')
        self.b2_2 = QPushButton('b2_2 Futures Option Update')
        self.b2_2.setAccessibleName('b2_2')
        self.b2_3 = QPushButton('b2_3')
        self.b2_3.setAccessibleName('b2_3')


        self.b3_1 = QPushButton('b3_1 US Stock Core Browser')
        self.b3_1.setAccessibleName('b3_1')
        self.b3_2 = QPushButton('b3_2 Core Update')
        self.b3_2.setAccessibleName('b3_2')
        self.b3_3 = QPushButton('b3_3')
        self.b3_3.setAccessibleName('b3_3')


        self.b4_1 = QPushButton('b4_1')
        self.b4_1.setAccessibleName('b4_1')
        self.b4_2 = QPushButton('b4_2')
        self.b4_2.setAccessibleName('b4_2')
        self.b4_3 = QPushButton('b4_3')
        self.b4_3.setAccessibleName('b4_3')

        self.lb_info = QLabel('Info Label')
        self.lb_info.setText(str(self.gbox1.isChecked()))
        self.quit_button = QPushButton('Quit')



        self.quit_button.clicked.connect(self.close)
        self.gbox1.toggled.connect(self.fun)

        self.initui()

    def initui(self) -> None:
        mainbox: QVBoxLayout = QVBoxLayout(self.central)

        mainbox.addWidget(self.gbox1)
        mainbox.addWidget(self.gbox2)
        mainbox.addWidget(self.gbox3)
        mainbox.addWidget(self.gbox4)
        mainbox.addWidget(self.lb_info)
        mainbox.addWidget(self.quit_button)

        hbox1 = QHBoxLayout(self.gbox1)
        hbox2 = QHBoxLayout(self.gbox2)
        hbox3 = QHBoxLayout(self.gbox3)
        hbox4 = QHBoxLayout(self.gbox4)


        hbox1.addWidget(self.b1_1)
        hbox1.addWidget(self.b1_2)
        hbox1.addWidget(self.b1_3)

        hbox2.addWidget(self.b2_1)
        hbox2.addWidget(self.b2_2)
        hbox2.addWidget(self.b2_3)

        hbox3.addWidget(self.b3_1)
        hbox3.addWidget(self.b3_2)
        hbox3.addWidget(self.b3_3)

        hbox4.addWidget(self.b4_1)
        hbox4.addWidget(self.b4_2)
        hbox4.addWidget(self.b4_3)




    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def fun(self) -> None:
        self.gbox4.setVisible(self.gbox1.isChecked())
        self.lb_info.setText('GBox1 set to ' + str(self.gbox1.isChecked()))



def maindock() -> None:
    app: QApplication = QApplication(sys.argv)
    w: MainDockWin = MainDockWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    maindock()