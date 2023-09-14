"""

USED BY: price_update_controller.py

"""
# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date
from typing import Tuple



# THIRD PARTY LIBS
from PySide6.QtCore import QDate
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)

# CUSTOM LIBS
from dimsumpy.qt.functions import closeEvent

# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict



class SetupWindow:
    def __init__(ego, self) -> None:
        self.setWindowTitle('Stock Price Update')
        self.setGeometry(0, 0, 900, 900)
        self.mainbox = QVBoxLayout(self)

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

        self.symbols_lineedit = QLineEdit()
        self.symbols_label = QLabel('Separate symbols by space')
        self.update_price_button = QPushButton('Update Price')
        self.update_price_button.setAccessibleName('update_price_button')
        self.update_technical_button = QPushButton('Update Technical')
        self.update_technical_button.setAccessibleName('update_technical_button')

        update_grid = QGridLayout()
        update_grid.addWidget(self.stock_list_combobox,    0, 0)
        update_grid.addWidget(self.start_lineedit,    0, 1)
        update_grid.addWidget(self.update_price_list_button, 0, 2)
        update_grid.addWidget(self.update_technical_list_button,  0, 3)

        update_grid.addWidget(self.symbols_lineedit,       1, 0)
        update_grid.addWidget(self.symbols_label,    1, 1)
        update_grid.addWidget(self.update_price_button,1, 2)
        update_grid.addWidget(self.update_technical_button, 1, 3)
        self.mainbox.addLayout(update_grid)



class ProgressRow:
    def __init__(ego, self) -> None:

        self.progress_bar = QProgressBar()
        self.progress_label = QLabel(' 0 / 0          ')
        self.clear_button = QPushButton('Clear')
        self.quit_button = QPushButton('Quit')
        hbox = QHBoxLayout()
        hbox.addWidget(self.progress_bar)
        hbox.addWidget(self.progress_label)
        hbox.addWidget(self.clear_button)
        hbox.addWidget(self.quit_button)
        self.mainbox.addLayout(hbox)



def reset_calendar(self) -> None:
    sender: str = self.sender().accessibleName()
    today_: date = date.today()
    qtoday: QDate = QDate.fromString(str(today_), 'yyyy-MM-dd')
    qtodaystr: str = qtoday.toString()
    if sender == 'from_reset_button':
        self.from_calendar.setSelectedDate(qtoday)
        self.from_calendar.updateCells()
        self.from_calendar_label.setText(qtodaystr)
        self.from_calendar_label.repaint()
    elif sender == 'to_reset_button':
        self.to_calendar.setSelectedDate(qtoday)
        self.to_calendar.updateCells()
        self.to_calendar_label.setText(qtodaystr)
        self.to_calendar_label.repaint()
    else:
        print('no sender')
    QApplication.processEvents()



def update_calendar_date(self, qdate: QDate) -> None:
    sender: str = self.sender().accessibleName()
    datestr: str = qdate.toString()
    if sender == 'from_calendar':
        self.from_calendar_label.setText(datestr)
        self.from_calendar_label.repaint()
        self.from_calendar.updateCells()
        self.from_calendar.repaint()
    elif sender == 'to_calendar':
        self.to_calendar_label.setText(datestr)
        self.to_calendar_label.repaint()
        self.to_calendar.updateCells()
        self.to_calendar.repaint()
    else:
        print('no sender')
    QApplication.processEvents()


def clear_interface(self) -> None:
    self.browser.clear
    self.progress_label.setText(' 0 / 0       ')



class MakeConnects:
    """
    I deliberate put MakeConnect class definition after all outer classes just to have a clearer flow.
    """
    def __init__(ego, self) -> None:

        self.from_reset_button.clicked.connect(self.reset_calendar)
        self.to_reset_button.clicked.connect(self.reset_calendar)
        self.from_reset_button.click()
        self.to_reset_button.click()

        self.from_calendar.clicked[QDate].connect(self.update_calendar_date)
        self.to_calendar.clicked[QDate].connect(self.update_calendar_date)

        self.from_calendar.currentPageChanged.connect(self.from_calendar.repaint)
        self.to_calendar.currentPageChanged.connect(self.to_calendar.repaint)

        self.clear_button.clicked.connect(self.clear_interface)
        self.quit_button.clicked.connect(self.close)



class PriceUpdateView(QWidget):
    def __init__(self) -> None:
        super().__init__()
        SetupWindow(self)  # mainbox is in SetupWindow() 
        BrowserRow(self)
        CalendarGrid(self)
        UpdateGrid(self)
        ProgressRow(self)
        MakeConnects(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)

    def reset_calendar(self) -> None:
        return reset_calendar(self)
    
    def update_calendar_date(self, qdate: QDate) -> None:
        return update_calendar_date(self, qdate)
    
    def clear_interface(self) -> None:
        return clear_interface(self)




def main() -> None:
    app = QApplication(sys.argv)
    win = PriceUpdateView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()