"""

"""


# STANDARD LIBS
import sys; sys.path.append('..')
from datetime import date
import time
from typing import Any, Dict, Generator, List, Optional


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox


# CUSTOM LIBS
from batterypy.control.trys import try_str
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import confirmation_self


# PROGRAM MODULES
from core_stock_update.core_update_view import CoreUpdateView
from database_update.stock_list_model import stock_list_dict, table_function_dict

from stock_price_update.price_update_view import PriceUpdateView

from stock_price_update.price_update_database_model import upsert_price


class CustomThread(QThread):
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
        print('callback 35') # debug


class PriceUpdateController(PriceUpdateView):
    def __init__(self) -> None:
        super().__init__()
        self.threads: Dict[float, CustomThread] = {}
        self.b_price1s.clicked.connect(self.yahooupsert)
        self.b_prices.clicked.connect(self.yahooupsert)  # update prices from a stock list

    def threadfinished(self, thread_id: float) -> None:
        print(self.threads, ' finished 46') # debug
        self.threads.pop(thread_id, None) # None is the default return value to prevent key error, pop means remove the item from dict
        print(self.threads, ' finished 48') # debug

    def yahooupsertfunc(self, date1: date, date2: date, stockgen: Generator[str, None, None]) -> None:  # return type is not None
        """This func runs in the QThread"""
        for count, symbol in enumerate(stockgen, start=1): # if the list is too long, program will have Segmentation fault
            s = upsert_price(date1, date2, symbol)
            msg: str = f"{count} / {self.l}  {s}"
            self.pbar.setValue(count)
            self.browser.append(msg)
            print(msg)
            QCoreApplication.processEvents()  # update the GUI
            #self.browser.repaint() # this line will have error as multiple threads paint at the same time



    @confirmation_self
    def yahooupsert(self) -> None:
        date1, date2 = self.calendar_get_dates()
        sender = self.sender().accessibleName()
        if sender == 'b_prices':
            stockstr = self.combo.currentText()
            start_num = int0(self.le_start.text())
            stocklist = stock_list_dict.get(stockstr)[start_num:]
        else:
            stockstr = self.le.text()
            stocklist = stockstr.split()
        self.l = len(stocklist)
        self.pbar.setRange(0, self.l)
        stockgen = (x for x in stocklist)
        thread_id: float = time.time()
        thread: CustomThread = CustomThread(self.yahooupsertfunc, lambda tid=thread_id: self.threadfinished(tid)
                              , [date1, date2, stockgen])
        self.threads[thread_id] = thread # added this line in 2019
        thread.start()  # start the run() in QThread
        thread.wait(2) # prevent crash
        self.browser.append(str(self.l) + ' stocks')



def main() -> None:
    app = QApplication(sys.argv)
    win = PriceUpdateController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
