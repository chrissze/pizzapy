"""
USED BY: guru_update_ctrl.py

This DailyGuruWin class is the Graphical Layout of Guru Update Window without major function implementations. It is the 'View' of Model-View-Controller pattern.

This window has 4 horizontal boxes.

I created the widgets first in __init__() method. Then arrange them in initui() method.

The clear_browser() and closeEvent() method were used by 4th box buttons.


"""

# STANDARD LIBS
import sys; sys.path.append('..')

from typing import Tuple


# THIRD PARTY LIBS
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QCloseEvent

from PySide6.QtWidgets import (QApplication, QComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox, QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict




class Row1:
    def __init__(self, parent):
        """
        If I have additional methods in this Row1 class, and those additional methods need to access the parent argument. Then I need to add the following line to __ini__() method:
        self.parent = parent
        """
        parent.combo = QComboBox()
        parent.combo.addItems(stock_list_dict.keys())

        parent.le_list_start = QLineEdit()
        parent.le_list_start.setPlaceholderText('Optional starting no.')

        parent.b_list_guru = QPushButton('Update Guru')
        parent.b_list_guru.setAccessibleName('b_list_guru')

        parent.b_list_zacks = QPushButton('Update Zacks')
        parent.b_list_zacks.setAccessibleName('b_list_zacks')

        parent.b_list_option = QPushButton('Update Option')
        parent.b_list_option.setAccessibleName('b_list_option')
        
        parent.hbox1 = QHBoxLayout()
        parent.hbox1.addWidget(parent.combo)
        parent.hbox1.addWidget(parent.le_list_start)
        parent.hbox1.addWidget(parent.b_list_guru)
        parent.hbox1.addWidget(parent.b_list_zacks)
        parent.hbox1.addWidget(parent.b_list_option)

class Row2:
    def __init__(self, parent):
        parent.lb_le = QLabel('Stocks (divided by space):')
        parent.le = QLineEdit()
        parent.b_le_guru = QPushButton('Le Guru')
        parent.b_le_guru.setAccessibleName('b_le_guru')
        parent.b_le_zacks = QPushButton('Le Zacks')
        parent.b_le_zacks.setAccessibleName('b_le_zacks')
        parent.b_le_option = QPushButton('Le Option')
        parent.b_le_option.setAccessibleName('b_le_option')

        parent.hbox2 = QHBoxLayout()
        parent.hbox2.addWidget(parent.lb_le)
        parent.hbox2.addWidget(parent.le)
        parent.hbox2.addWidget(parent.b_le_guru)
        parent.hbox2.addWidget(parent.b_le_zacks)
        parent.hbox2.addWidget(parent.b_le_option)

class Row3:
    def __init__(self, parent):
        parent.browser = QTextBrowser()
        parent.browser.setMaximumHeight(400)

        parent.hbox3 = QHBoxLayout()
        parent.hbox3.addWidget(parent.browser)


class Row4:
    def __init__(self, parent):
        parent.pbar = QProgressBar()
        parent.b_clear = QPushButton('Clear Browser')
        parent.b_quit = QPushButton('Quit')

        parent.b_clear.clicked.connect(parent.clear_browser)
        parent.b_quit.clicked.connect(parent.close)

        parent.hbox4 = QHBoxLayout()
        parent.hbox4.addWidget(parent.pbar)
        parent.hbox4.addWidget(parent.b_clear)
        parent.hbox4.addWidget(parent.b_quit)

    
class DailyGuruWin(QWidget):
    """
        # self in Row1(self) is the DailyGuruWin instance, and this instance becomes the parent of Row1 instance. During the Row1 initialization, first argument of Row1 itself is implicit, no need to write it on instance creation, so the 'self' argument here maps to the 2nd parameter parent.

    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Daily Guru Update')
        self.setGeometry(50, 50, 900, 600)
        self.row1 = Row1(self)     # Initialized Row1 widgets
        self.row2 = Row2(self)  
        self.row3 = Row3(self)  
        self.row4 = Row4(self)  
        self.initui() # initui() draws the layout

    def initui(self) -> None:
        
        mainbox = QVBoxLayout(self) # self here represents the parent container of mainbox
        mainbox.addLayout(self.hbox1)  # hbox1 is defined in Row1 class
        mainbox.addLayout(self.hbox2)
        mainbox.addLayout(self.hbox3)
        mainbox.addLayout(self.hbox4)


    def get_le_symbol(self) -> str:
        """ Used by child classes  """
        symbol = self.le.text()
        return symbol

    def clear_browser(self) -> None:
        self.browser.setText('')
        self.browser.clear()
        QCoreApplication.processEvents()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        This special named 'closeEvent' method overrides default close() method.
        This methed is called when we call self.close() or users click the X button.
        """
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
    sys.exit(app.exec())


if __name__ == '__main__':
    main()