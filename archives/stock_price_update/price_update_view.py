"""

USED BY: price_update_controller.py

"""
# STANDARD LIBS

from datetime import date
from typing import Tuple



# THIRD PARTY LIBS
from PySide6.QtCore import QDate
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

# CUSTOM LIBS

# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import stock_list_dict



class SetupWindow:
    def __init__(ego, self) -> None:
        self.setWindowTitle('Stock Price Update')
        self.resize(900, 900)
        self.central = QWidget()  
        self.mainbox = QVBoxLayout(self.central)
        self.setCentralWidget(self.central)
        self.statusbar = self.statusBar()  
        self.statusbar.showMessage('Ready')


class BrowserRow:
    def __init__(ego, self) -> None:

        self.browser = QTextBrowser()
        self.browser.setMaximumHeight(400)
        self.mainbox.addWidget(self.browser)


class CalendarGrid:
    def __init__(ego, self) -> None:

        self.from_calendar_label = QLabel('')
        self.from_reset_button = QPushButton('Reset FROM date')
        self.from_reset_button.setAccessibleName('from_reset_button')
        self.to_calendar_label = QLabel('')
        self.to_reset_button = QPushButton('Reset TO date')
        self.to_reset_button.setAccessibleName('to_reset_button')


        self.from_calendar = QCalendarWidget()
        self.from_calendar.setAccessibleName('from_calendar')  # same name as variable
        self.to_calendar = QCalendarWidget()
        self.to_calendar.setAccessibleName('to_calendar')

        calendar_grid = QGridLayout()
        calendar_grid.addWidget(self.from_calendar_label,  0, 0)
        calendar_grid.addWidget(self.from_reset_button, 0, 1)
        calendar_grid.addWidget(self.to_calendar_label,  0, 2)
        calendar_grid.addWidget(self.to_reset_button, 0, 3)

        # grid (widget, row, column, height, width)
        calendar_grid.addWidget(self.from_calendar, 1, 0, 2, 2)
        calendar_grid.addWidget(self.to_calendar, 1, 2, 2, 2)
        self.mainbox.addLayout(calendar_grid)


class UpdateGrid:
    def __init__(ego, self) -> None:

        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())
        self.start_lineedit = QLineEdit()
        self.start_lineedit.setPlaceholderText('Input a number from 1 OR a SYMBOL in the list to start')
        self.update_price_list_button = QPushButton('Update Price List')
        self.update_price_list_button.setAccessibleName('update_price_list_button')
        self.update_technical_list_button = QPushButton('Update Technical List')
        self.update_technical_list_button.setAccessibleName('update_technical_list_button')

        self.symbols_label = QLabel('SYMBOLS: ')
        self.symbols_lineedit = QLineEdit()
        self.symbols_lineedit.setPlaceholderText('separated by spaces or commas')
        self.update_price_button = QPushButton('Update Price')
        self.update_price_button.setAccessibleName('update_price_button')
        self.update_technical_button = QPushButton('Update Technical')
        self.update_technical_button.setAccessibleName('update_technical_button')

        self.clear_button = QPushButton('Clear')
        self.quit_button = QPushButton('Quit')

        update_grid = QGridLayout()
        update_grid.addWidget(self.stock_list_combobox,    0, 0)
        update_grid.addWidget(self.start_lineedit,    0, 1)
        update_grid.addWidget(self.update_price_list_button, 0, 2)
        update_grid.addWidget(self.update_technical_list_button,  0, 3)

        update_grid.addWidget(self.symbols_label,    1, 0)
        update_grid.addWidget(self.symbols_lineedit,       1, 1)
        update_grid.addWidget(self.update_price_button,1, 2)
        update_grid.addWidget(self.update_technical_button, 1, 3)
        
        update_grid.addWidget(self.clear_button, 2, 2)
        update_grid.addWidget(self.quit_button,  2, 3)

        self.mainbox.addLayout(update_grid)



class ProgressRow:
    def __init__(ego, self) -> None:
        self.progress_box = QVBoxLayout()
        self.mainbox.addLayout(self.progress_box)





class PriceUpdateView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        SetupWindow(self)  # mainbox is in SetupWindow() 
        BrowserRow(self)
        CalendarGrid(self)
        UpdateGrid(self)
        ProgressRow(self)




def main() -> None:
    app = QApplication(sys.argv)
    win = PriceUpdateView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()