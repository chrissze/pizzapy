
# STANDARD LIBS


from datetime import date
from typing import Tuple


# THIRD PARTY LIBS
from PySide6.QtCore import QDate
from PySide6.QtGui import QCloseEvent

from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)



class MainDockView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Pizza Dock')
        self.resize(250, 300)

        self.central = QWidget()
        self.setCentralWidget(self.central)
        mainbox: QVBoxLayout = QVBoxLayout(self.central)

        self.browser_group_box = QGroupBox('BROWSER')
        self.updater_group_box = QGroupBox('UPDATER')
        self.core_browser_button = QPushButton('Core Browser')
        self.core_updater_button = QPushButton('Core Updater')
        self.price_updater_button = QPushButton('Price Technical Updater')

        self.quit_button = QPushButton('Quit')

        browser_vbox = QVBoxLayout(self.browser_group_box)
        updater_vbox = QVBoxLayout(self.updater_group_box)

        browser_vbox.addWidget(self.core_browser_button)
        updater_vbox.addWidget(self.core_updater_button)
        updater_vbox.addWidget(self.price_updater_button)

        mainbox.addWidget(self.browser_group_box)
        mainbox.addWidget(self.updater_group_box)
        mainbox.addWidget(self.quit_button)




def view() -> None:
    app: QApplication = QApplication(sys.argv)
    win = MainDockView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    view()