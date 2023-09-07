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


from PySide6.QtWidgets import (QApplication, QComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict


class StockListRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StockListRow, 'self' is the instance of the calling class CoreUpdateView.
            
            If I have additional methods in this StockListRow class, and those additional methods need to access the parent argument. Then I need to add the following line to __ini__() method:
            ego.self = self
        """
        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())

        self.stock_list_starting_number_lineedit = QLineEdit()
        self.update_guru_list_button = QPushButton('Update Guru List')
        self.update_guru_list_button.setAccessibleName('update_guru_list_button')

        self.update_zacks_list_button = QPushButton('Update Zacks List')
        self.update_zacks_list_button.setAccessibleName('update_zacks_list_button')

        self.update_option_list_button = QPushButton('Update Option List')
        self.update_option_list_button.setAccessibleName('update_option_list_button')
        
        self.stock_list_hbox = QHBoxLayout()
        self.mainbox.addLayout(self.stock_list_hbox)  # stock_list_hbox is defined in StockListRow class
        self.stock_list_hbox.addWidget(self.stock_list_combobox)
        self.stock_list_hbox.addWidget(self.stock_list_starting_number_lineedit)
        self.stock_list_hbox.addWidget(self.update_guru_list_button)
        self.stock_list_hbox.addWidget(self.update_zacks_list_button)
        self.stock_list_hbox.addWidget(self.update_option_list_button)


class StocksRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StocksRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.update_stocks_label = QLabel('Stocks (divided by space):')
        self.update_stocks_lineedit = QLineEdit()
        self.update_guru_button = QPushButton('Update Guru')
        self.update_guru_button.setAccessibleName('update_guru_button')
        self.update_zacks_button = QPushButton('Update Zacks')
        self.update_zacks_button.setAccessibleName('update_zacks_button')
        self.update_option_button = QPushButton('Update Option')
        self.update_option_button.setAccessibleName('update_option_button')

        self.stocks_hbox = QHBoxLayout()
        self.mainbox.addLayout(self.stocks_hbox)
        self.stocks_hbox.addWidget(self.update_stocks_label)
        self.stocks_hbox.addWidget(self.update_stocks_lineedit)
        self.stocks_hbox.addWidget(self.update_guru_button)
        self.stocks_hbox.addWidget(self.update_zacks_button)
        self.stocks_hbox.addWidget(self.update_option_button)

class BrowserRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class BrowserRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.browser = QTextBrowser()
        self.browser.setMaximumHeight(400)

        self.browser_hbox = QHBoxLayout()
        self.mainbox.addLayout(self.browser_hbox)
        self.browser_hbox.addWidget(self.browser)


class QuitRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class QuitRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.progressbar = QProgressBar()
        self.clear_button = QPushButton('Clear Browser')
        self.quit_button = QPushButton('Quit')

        self.quit_hbox = QHBoxLayout()
        self.mainbox.addLayout(self.quit_hbox)
        self.quit_hbox.addWidget(self.progressbar)
        self.quit_hbox.addWidget(self.clear_button)
        self.quit_hbox.addWidget(self.quit_button)



def stock_list_comboxbox_changed(self) -> None:
    """
    This method is about layout appearance change, so I place it in view module.
    """
    self.combobox_string = self.stock_list_combobox.currentText()
    self.full_stock_list = stock_list_dict.get(self.combobox_string)
    self.full_list_length = len(self.full_stock_list)
    self.stock_list_starting_number_lineedit.setPlaceholderText(f'Input 1 to {self.full_list_length} as starting no. (optional)')



class CoreUpdateView(QWidget):
    """
        # self in StockListRow(self) is the DailyGuruWin instance, and this instance becomes the parent of StockListRow instance. During the StockListRow initialization, first argument of StockListRow itself is implicit, no need to write it on instance creation, so the 'self' argument here maps to the 2nd parameter parent.

    """
    def __init__(self) -> None:
        super().__init__()  # initialize all QWidget() variables and methods
        self.setWindowTitle('Core Stock Update')
        self.setGeometry(50, 50, 1000, 600)
        self.initui() # initui() draws the layout

    def initui(self) -> None:
        """
        self instance here represents the parent container of mainbox, Rows must be placed after mainbox because Rows content contain adding widgets for mainbox.
        """
        self.mainbox = QVBoxLayout(self) 
        BrowserRow(self)  
        StockListRow(self)     # Initialized StockListRow widgets
        StocksRow(self)  
        QuitRow(self)        
        self.stock_list_comboxbox_changed() # deliberately run it for the first time to fill in lineedit placeholder text.
        self.stock_list_combobox.currentIndexChanged.connect(self.stock_list_comboxbox_changed)


    def stock_list_comboxbox_changed(self) -> None:
        return stock_list_comboxbox_changed(self)
    


def main() -> None:
    app = QApplication(sys.argv)
    w = CoreUpdateView()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()