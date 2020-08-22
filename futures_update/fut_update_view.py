import sys;

from dimsumpy.qt5.decorators import confirmation_self

sys.path.append('..')

from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QCloseEvent

from PySide2.QtWidgets import (QApplication, QComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

from shared_model.fut_data_model import fut_type_list, getfutures
from typing import List, Tuple


class FutUpdateWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Daily Futures Update')
        self.setGeometry(50, 50, 900, 600)

        self.combo: QComboBox = QComboBox()
        self.combo.addItems(fut_type_list)
        self.combo.activated[str].connect(self.refresh_combo_individual)
        self.combo_individual: QComboBox = QComboBox()
        self.refresh_combo_individual(self.combo.currentText())

        self.b_list_option: QPushButton = QPushButton('Update List Option')
        self.b_list_option.setAccessibleName('b_list_option')

        self.le_list_start: QLineEdit = QLineEdit('Enter an alternative no. to start the list')
        self.b_single_option: QPushButton = QPushButton('Update Single Option')
        self.b_single_option.setAccessibleName('b_single_option')

        self.browser: QTextBrowser = QTextBrowser()
        self.browser.setMaximumHeight(400)

        self.pbar: QProgressBar = QProgressBar()
        self.b_clear: QPushButton = QPushButton('Clear Browser')
        self.b_quit: QPushButton = QPushButton('Quit')

        self.b_clear.clicked.connect(self.clear_browser)
        self.b_quit.clicked.connect(self.close)

        self.initui()

    def initui(self) -> None:
        mainbox: QVBoxLayout = QVBoxLayout(self)
        hbox1: QHBoxLayout = QHBoxLayout()
        hbox2: QHBoxLayout = QHBoxLayout()
        hbox3: QHBoxLayout = QHBoxLayout()
        hbox4: QHBoxLayout = QHBoxLayout()
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)
        mainbox.addLayout(hbox4)

        hbox1.addWidget(self.combo)
        hbox1.addWidget(self.le_list_start)
        hbox1.addWidget(self.b_list_option)

        hbox2.addWidget(self.combo_individual)
        hbox2.addWidget(self.b_single_option)

        hbox3.addWidget(self.browser)

        hbox4.addWidget(self.pbar)
        hbox4.addWidget(self.b_clear)
        hbox4.addWidget(self.b_quit)

    @confirmation_self
    def clear_browser(self) -> None:
        self.browser.clear()
        self.browser.repaint()
        QCoreApplication.processEvents()


    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def refresh_combo_individual(self, text: str) -> None:
        codes: List[str] = getfutures(text)
        self.combo_individual.clear()
        self.combo_individual.addItems(codes)


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    w: FutUpdateWin = FutUpdateWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()