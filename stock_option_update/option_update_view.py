
import sys
sys.path.append('..')

from typing import Tuple
from PySide2.QtCore import QCoreApplication
from PySide2.QtGui import QCloseEvent

from PySide2.QtWidgets import (QApplication, QComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

from shared_model.st_data_model import stock_list_dict


class DailyGuruWin(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Daily Guru Update')
        self.setGeometry(50, 50, 900, 600)

        self.combo = QComboBox()
        self.combo.addItems(stock_list_dict.keys())
        self.load_list_button = QPushButton('Update Guru')
        self.load_list_button.setAccessibleName('load_list_button')
        self.b_list_zacks = QPushButton('Update Zacks')
        self.b_list_zacks.setAccessibleName('b_list_zacks')
        self.b_list_option = QPushButton('Update Option')
        self.b_list_option.setAccessibleName('b_list_option')

        self.symbols_label = QLabel('Stocks (divided by space):')
        self.le = QLineEdit()
        self.le_list_start = QLineEdit()
        self.le_list_start.setPlaceholderText('Optional starting no.')
        self.load_symbols_button = QPushButton('Le Guru')
        self.load_symbols_button.setAccessibleName('load_symbols_button')
        self.b_le_zacks = QPushButton('Le Zacks')
        self.b_le_zacks.setAccessibleName('b_le_zacks')
        self.b_le_option = QPushButton('Le Option')
        self.b_le_option.setAccessibleName('b_le_option')

        self.browser = QTextBrowser()
        self.browser.setMaximumHeight(400)

        self.pbar = QProgressBar()
        self.b_clear = QPushButton('Clear Browser')
        self.b_quit = QPushButton('Quit')

        self.b_clear.clicked.connect(self.clear_browser)
        self.b_quit.clicked.connect(self.close)

        self.initui() # initui() draws the layout

    def initui(self) -> None:
        mainbox = QVBoxLayout(self)
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        hbox4 = QHBoxLayout()
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)
        mainbox.addLayout(hbox4)

        hbox1.addWidget(self.combo)
        hbox1.addWidget(self.le_list_start)
        hbox1.addWidget(self.load_list_button)
        hbox1.addWidget(self.b_list_zacks)
        hbox1.addWidget(self.b_list_option)

        hbox2.addWidget(self.symbols_label)
        hbox2.addWidget(self.le)
        hbox2.addWidget(self.load_symbols_button)
        hbox2.addWidget(self.b_le_zacks)
        hbox2.addWidget(self.b_le_option)

        hbox3.addWidget(self.browser)

        hbox4.addWidget(self.pbar)
        hbox4.addWidget(self.b_clear)
        hbox4.addWidget(self.b_quit)



    def get_le_symbol(self) -> str:
        symbol = self.le.text()
        return symbol

    def clear_browser(self) -> None:
        self.browser.setText('')
        self.browser.clear()
        QCoreApplication.processEvents()

    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main() -> None:
    app = QApplication(sys.argv)
    w = DailyGuruWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()