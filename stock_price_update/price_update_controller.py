"""

DEPENDS ON: price_update_view.py

I can click the quit button to stop the current operations.

I can start a 2nd operation when the 1st operation is still running by using threads.


"""


# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date
from itertools import dropwhile
import time
from typing import Any, Dict, Generator, List, Optional, Tuple


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox


# CUSTOM LIBS
from batterypy.control.trys import try_str
from batterypy.string.read import is_floatable, is_intable, int0, float0
from dimsumpy.qt.decorators import self_confirmation


# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict, table_function_dict

from stock_price_update.price_update_view import PriceUpdateView

from stock_price_update.price_update_database_model import upsert_price


class CustomThread(QThread):
    """
    QThread is the base class.
    """
    def __init__(self, func, callback, args=()) -> None:
        super().__init__()
        self.func = func
        self.callback = callback
        self.args = args
        self.finished.connect(self.callitback)

    def __del__(self):
        self.wait()

    def run(self) -> None:
        self.func(*self.args)

    def callitback(self) -> None:
        self.callback()
        print('callitback done') # debug





def thread_finished(self, thread_id: float) -> None:
    """
    this is the callback function of CustomThread class
    """
    print(self.threads_dict, f' thread_finished() {thread_id} starts') # debug
    self.threads_dict.pop(thread_id, None) # None is the default return value to prevent key error, pop means remove the item from dict
    print(self.threads_dict, f' thread_finished() {thread_id} ends') # debug
    thread_message: str = f' thread_finished() {thread_id} ends'
    self.browser.append(thread_message)

def get_calendar_dates(self) -> Tuple[date, date]:
    """
    * INDEPENDENT *
    USED BY: update_price()
    """
    FROM: date = self.from_calendar.selectedDate().toPython()
    TO: date = self.to_calendar.selectedDate().toPython()
    return FROM, TO


def call_upsert(self, FROM: date, TO: date, stockgen: Generator[str, None, None]) -> None:  
    
    """
    IMPORTS: upsert_price()
    USED BY: update_price()
    
    # return type is not None
    This func runs in the QThread
    
    self.browser.repaint() will have error as multiple threads paint at the same time
    self.browser.append(browser_text) will have paint errors.
    """
    for i, symbol in enumerate(stockgen, start=1): # if the list is too long, program will have Segmentation fault
        result = try_str(upsert_price, FROM, TO, symbol)
        browser_text: str = f"{i} / {self.list_length} {symbol} {result}"
        self.progress_bar.setValue(i)
        self.progress_label.setText(f'{i} / {self.list_length} {symbol}       ')
        QCoreApplication.processEvents()  # update the GUI



@self_confirmation
def update_price(self) -> None:
    """
    DEPENDS ON: self.calendar_get_dates(), self.call_upsert(), CustomThread class, self.thread_finished()
    """
    FROM, TO = self.get_calendar_dates()
    sender = self.sender().accessibleName()
    if sender == 'update_price_list_button':
        lineedit_text: str = self.start_lineedit.text()
        stockstr = self.stock_list_combobox.currentText()
        stocklist = stock_list_dict.get(stockstr)
        if lineedit_text in stocklist:
            stocklist = list(dropwhile(lambda x: x != lineedit_text, stocklist))
        else:        
            start_num = max(int0(lineedit_text) - 1, 0)
            stocklist = stocklist[start_num:]

    else:
        stockstr = self.symbols_lineedit.text()
        stocklist = stockstr.split()
    self.list_length = len(stocklist)
    self.progress_bar.setRange(0, self.list_length)
    stockgen = (x for x in stocklist)
    self.thread_id: float = time.time()
    thread: CustomThread = CustomThread(self.call_upsert, lambda tid=self.thread_id: self.thread_finished(tid)
                            , [FROM, TO, stockgen])
    self.threads_dict[self.thread_id] = thread # added this line in 2019
    thread.start()  # start the run() in QThread
    thread.wait(2) # prevent crash
    self.browser.append(f'{self.list_length} stocks')



class MakeUpdateConnects:
    def __init__(ego, self) -> None:
        self.update_price_button.clicked.connect(self.update_price)
        self.update_price_list_button.clicked.connect(self.update_price)  # update prices from a stock list





class PriceUpdateController(PriceUpdateView):
    """
    By using QThread, I can still click the quit button to stop the operation when the update is running.

    A single thread is used for the looping for the whole stock list.
    The key in the threads_dict is a float, this key is created by time.time() in self.update_price()

    self.update_price() is the main function, while get_calendar_dates(), call_upsert() and thread_finished() are helper functions of update_price().
    """
    def __init__(self) -> None:
        super().__init__()
        self.threads_dict: Dict[float, CustomThread] = {}
        MakeUpdateConnects(self)

        
    def get_calendar_dates(self) -> Tuple[date, date]:
        return get_calendar_dates(self)

    def call_upsert(self, FROM: date, TO: date, stockgen: Generator[str, None, None]) -> None:  
        return call_upsert(self, FROM, TO, stockgen)  
        
    def thread_finished(self, thread_id: float) -> None:
        return thread_finished(self, thread_id)

    def update_price(self) -> None:
        return update_price(self)



def main() -> None:
    app = QApplication(sys.argv)
    win = PriceUpdateController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
