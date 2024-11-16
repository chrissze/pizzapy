"""
AIM OF THIS MODULE: To create a CoreUpdateView class for core_update_controller to inherit. All other classes are helpers of CoreUpdateView class.
 
USED BY: core_update_controller.py

This class is the Graphical Layout of Core Update Controller without major function implementations. It is the 'View' of Model-View-Controller pattern.

This window has 4 horizontal boxes. These 4 boxes' sequence can be changed freely.

"""

# STANDARD LIBS

from typing import Tuple


# THIRD PARTY LIBS
from PySide6.QtWidgets import (QApplication, QComboBox,
                               QHBoxLayout, QLabel, QLineEdit, QMainWindow, QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

# PROGRAM MODULES
from pizzapy.database_update.postgres_command_model import table_list_dict
from pizzapy.database_update.stock_list_model import stock_list_dict


class SetupWindow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class CoreUpdateView.
            This class has self.mainbox, it has to be the first in CoreUpdateView.

            Rows must be placed after mainbox because Rows content contain adding widgets for mainbox.

            I created self.statusbar property, if I don't create it, every time I want to update the status bar, I need to make function call to the self.statusBar()
        """
        self.setWindowTitle('Core Stock Update')
        self.resize(500, 500)
        self.central = QWidget()  
        self.mainbox = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)
        self.statusbar = self.statusBar()  
        self.statusbar.showMessage('Ready')


class BrowserRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class BrowserRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.browser = QTextBrowser()
        hbox = QHBoxLayout()
        hbox.addWidget(self.browser)
        self.mainbox.addLayout(hbox)


class StockListRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StockListRow, 'self' is the instance of the calling class CoreUpdateView.
            
            If I have additional methods in this StockListRow class, and those additional methods need to access the parent argument. Then I need to add the following line to __ini__() method:
            ego.self = self
        """
        self.table_list_combobox = QComboBox()
        self.table_list_combobox.addItems(table_list_dict.keys())
        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())

        self.starting_lineedit = QLineEdit()
        self.update_list_button = QPushButton('Update List')
        self.update_list_button.setAccessibleName('update_list_button')

        hbox = QHBoxLayout()
        hbox.addWidget(self.table_list_combobox)
        hbox.addWidget(self.stock_list_combobox)
        hbox.addWidget(self.starting_lineedit)
        hbox.addWidget(self.update_list_button)
        self.mainbox.addLayout(hbox) 


class StocksRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StocksRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.symbols_label = QLabel('SYMBOLS: ')
        self.symbols_lineedit = QLineEdit()
        self.update_symbols_button = QPushButton('Update SYMBOLS')
        self.update_symbols_button.setAccessibleName('update_symbols_button')
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.symbols_label)
        self.hbox.addWidget(self.symbols_lineedit)
        self.hbox.addWidget(self.update_symbols_button)
        self.mainbox.addLayout(self.hbox)



class QuitRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class QuitRow, 'self' is the instance of the calling class CoreUpdateView.
        """
        self.clear_button = QPushButton('Clear Browser')
        self.clear_button.setMaximumWidth(200)
        self.quit_button = QPushButton('Quit')
        self.quit_button.setMaximumWidth(200)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.clear_button)
        self.hbox.addWidget(self.quit_button)
        self.mainbox.addLayout(self.hbox)


class ProgressRow:
    def __init__(ego, self) -> None:
        self.progress_box = QVBoxLayout()
        self.mainbox.addLayout(self.progress_box)


class CoreUpdateView(QMainWindow):
    """
    DEPENDS ON: SetupWindow, BrowserRow, StockListRow, StocksRow, QuitRow
    IMPORTS: QWidget
    USED BY: core_update_controller.py, main()

        # self in StockListRow(self) is the CoreUpdateView instance, and this instance becomes the parent of StockListRow instance. During the StockListRow initialization, first argument of StockListRow itself is implicit, no need to write it on instance creation, so the 'self' argument here maps to the 2nd parameter.

    """
    def __init__(self) -> None:
        super().__init__()  # initialized all base class QWidget() variables and methods
        SetupWindow(self)   # initialized mainbox
        BrowserRow(self)  
        StockListRow(self)
        StocksRow(self)  
        QuitRow(self)        
        ProgressRow(self)        
    
        


def view() -> None:
    app = QApplication(sys.argv)
    win = CoreUpdateView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    view()