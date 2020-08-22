
import sys; sys.path.append('..')

from shared_model.st_data_model import stock_list_dict


from dimsumpy.qt5.decorators import confirmation_self

import time
from datetime import date
from typing import Any, Generator, Dict

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread, QCoreApplication

from batterypy.string.read import int0


from stock_price_update.st_price_update_view import DailyStockWin
from stock_price_update.st_price_update_model import ya_px_upsert_1s


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


class StockPriceUpdateDialog(DailyStockWin):
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
            s = ya_px_upsert_1s(date1, date2, symbol)
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
    w = StockPriceUpdateDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
