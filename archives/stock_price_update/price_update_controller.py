"""
AIM:
The aim of this module is to create self.update_list() and self.update_symbols_lineedit() for 4 update buttons. 

DEPENDS ON: price_update_view.py

USED BY: main_dock_controller.py

I can click the quit button to stop the current operations.

I can start a 2nd operation when the 1st operation is still running by using threads.


"""


# STANDARD LIBS

from datetime import date
from itertools import dropwhile
import re
import time
from typing import Any, Dict, Generator, List, Optional, Tuple


# THIRD PARTY LIBS
from PySide6.QtCore import QDate, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMessageBox, QProgressBar

# CUSTOM LIBS
from batterypy.control.trys import try_str
from batterypy.string.read import is_floatable, is_intable, int0, float0

from dimsumpy.qt.decorators import list_confirmation
from dimsumpy.qt.functions import closeEvent
from dimsumpy.qt.threads import MyThread


# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import stock_list_dict

from pizzapy.stock_price_update.price_update_view import PriceUpdateView

from pizzapy.stock_price_update.price_update_database_model import upsert_price

from pizzapy.stock_price_update.technical_update_database_model import upsert_technical






def thread_finished(self, tid: float, box) -> None:
    """
    * INDEPENDENT *
    USED BY: start_thread()
    this is the callback function of MyThread class

    Qt is event-driven, when we delete a widget, it might still doing something, so we cannot delete it immediately. deleteLater() is a safer way to delete widgets, we let Qt handles the deletion. 
    """    
    while box.count() > 0:
        widget = box.itemAt(0).widget()
        box.removeWidget(widget)
        widget.deleteLater()

    self.progress_box.removeItem(box)
    box.deleteLater()

    self.threads_dict.pop(tid, None) # None is the default return value to prevent key error, pop means remove the item from dict
    job_id: str = str(tid)[-3:]  
    thread_message: str = f'JOB {job_id} FINISHED \n'
    self.browser.append(thread_message)
    self.statusbar.showMessage(thread_message)



def get_calendar_dates(self) -> Tuple[date, date]:
    """
    * INDEPENDENT *
    USED BY: start_thread()
    """
    FROM: date = self.from_calendar.selectedDate().toPython()
    TO: date = self.to_calendar.selectedDate().toPython()
    return FROM, TO


def call_upsert(self, FROM: date, TO: date, stockgen: Generator[str, None, None], progress_bar, progress_label) -> None:  
    
    """
    * INDEPENDENT *
    IMPORTS: upsert_price(), upsert_technical(), try_str()
    USED BY: start_thread()
    
    # return type is not None
    This func runs in the QThread
    
    self.browser.repaint() will have error as multiple threads paint at the same time
    self.browser.append(browser_text) will have paint errors.
    
        debug_text: str = f"{i} / {self.list_length} {symbol} {result}"
            #QCoreApplication.processEvents()  # this line will crash the progrom for 2+ active threads
    """
    sender = self.sender().accessibleName()
    if sender == 'update_price_list_button' or sender == 'update_price_button':
        func = upsert_price
    elif sender == 'update_technical_list_button' or sender == 'update_technical_button':
        func = upsert_technical
    else:
        print(f'INVALID SENDER: {sender}')
        return
    
    for i, symbol in enumerate(stockgen, start=1): # if the list is too long, program will have Segmentation fault
        result = try_str(func, FROM, TO, symbol)
        progress_bar.setValue(i)
        progress_label.setText(f'{i}  {symbol} ')






@list_confirmation
def start_thread(self, stock_list: List[str]) -> None:
    """
    DEPENDS ON: self.calendar_get_dates(), self.call_upsert(), self.thread_finished()
    IMPORTS: MyThread, list_confiramtion()
    USED BY: update_symbols_lineedit(), update_price_list()

    [FROM, TO, stockgen] is the arguments for self.call_upsert in MyThread

    thread_id should NOT be self.thread_id as I may have multiple threads. If I use self.thread_id, it will overwrite the previous one.

    MyThread 2nd argument callback function cannot be shorted to self.thread_finished, as I need to include thread_id and hbox.

    Keep those variables local, do not add self: list_length, progress_bar, progress_label, hbox, stockgen, thread_id, thread

    The hbox, progress_bar and progress_label will be deleted on thread_finished() call back function.
    """
    thread_id: float = time.time()
    job_id: str = str(thread_id)[-3:]  
    list_length = len(stock_list)
    progress_bar = QProgressBar()
    progress_bar.setRange(0, list_length)
    progress_job_label = QLabel(f'JOB {job_id}: ')
    progress_label = QLabel('               ')
    hbox = QHBoxLayout()

    hbox.addWidget(progress_bar)
    hbox.addWidget(progress_job_label)
    hbox.addWidget(progress_label)
    self.progress_box.addLayout(hbox)

    FROM, TO = self.get_calendar_dates()
    stockgen = (x for x in stock_list)
    thread: MyThread = MyThread(self.call_upsert, lambda tid=thread_id, box=hbox: self.thread_finished(tid, box), [FROM, TO, stockgen, progress_bar, progress_label])
    self.threads_dict[thread_id] = thread # added this line in 2019
    thread.start()  # start the run() in QThread
    thread.wait(2) # prevent crash
    message = f'JOB {job_id}: Updating {list_length} stocks, {FROM} to {TO} ({self.sender().accessibleName()}) \n'
    self.browser.append(message)
    self.statusbar.showMessage(message)




def update_symbols_lineedit(self) -> None:
    """
    DEPENDS ON: start_thread()
    """
    lineedit_str = self.symbols_lineedit.text().strip()
    stock_list = re.split(r'[ ,]+', lineedit_str) if lineedit_str else []
    if stock_list:
        self.statusbar.showMessage(f'Updating {len(stock_list)} stocks')
        start_thread(self, stock_list)
    else:
        self.statusbar.showMessage('No SYMBOLS in the lineedit')



def update_list(self) -> None:
    """
    DEPENDS ON: start_thread()
    """
    
    lineedit_text: str = self.start_lineedit.text()
    stockstr = self.stock_list_combobox.currentText()
    stock_list = stock_list_dict.get(stockstr)
    if lineedit_text in stock_list:
        stock_list = list(dropwhile(lambda x: x != lineedit_text, stock_list))
    else:        
        start_num = max(int0(lineedit_text) - 1, 0)
        stock_list = stock_list[start_num:]
    start_thread(self, stock_list)



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
        print('INVALID SENDER for reset_calendar()')
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
        print('INVALID SENDER for update_calendar_date()')
    QApplication.processEvents()


def clear(self) -> None:
    """
    
    """
    self.browser.clear()
    self.statusbar.showMessage('Clear')



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

        self.clear_button.clicked.connect(self.clear)
        self.quit_button.clicked.connect(self.close)





class MakeUpdateConnects:
    def __init__(ego, self) -> None:
        self.update_price_list_button.clicked.connect(self.update_list)  # update prices from a stock list
        self.update_technical_list_button.clicked.connect(self.update_list)  # update prices from a stock list
        
        self.update_price_button.clicked.connect(self.update_symbols_lineedit)
        self.update_technical_button.clicked.connect(self.update_symbols_lineedit)
        





class PriceUpdateController(PriceUpdateView):
    """
    By using QThread, I can still click the quit button to stop the operation when the update is running.

    A single thread is used for the looping for the whole stock list.
    The key in the threads_dict is a float, this key is created by time.time() in self.update_price()

    """
    def __init__(self) -> None:
        super().__init__()
        self.threads_dict: Dict[float, MyThread] = {}

        MakeConnects(self)

        MakeUpdateConnects(self)


    def reset_calendar(self) -> None:
        return reset_calendar(self)
    
    def update_calendar_date(self, qdate: QDate) -> None:
        return update_calendar_date(self, qdate)
    


    def clear(self) -> None:
        return clear(self)
    
    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)



    def get_calendar_dates(self) -> Tuple[date, date]:
        return get_calendar_dates(self)

    def call_upsert(self, FROM: date, TO: date, stockgen: Generator[str, None, None], progress_bar, progress_label) -> None:  
        return call_upsert(self, FROM, TO, stockgen, progress_bar, progress_label)  
        
    def thread_finished(self, thread_id: float, box) -> None:
        return thread_finished(self, thread_id, box)

    def update_symbols_lineedit(self) -> None:
        return update_symbols_lineedit(self)

    def update_list(self) -> None:
        return update_list(self)



def main() -> None:
    app = QApplication(sys.argv)
    win = PriceUpdateController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
