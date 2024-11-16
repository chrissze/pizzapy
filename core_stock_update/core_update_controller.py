"""
DEPENDS ON: core_update_view.py, stock_list_model.py

USED BY: main_dock_controller.py


"""



# STANDARD LIBS

from itertools import dropwhile
import re
import time
from typing import Any, Dict, Generator, List, Optional


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QMessageBox, QProgressBar


# CUSTOM LIBS
from batterypy.control.trys import try_str
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import list_confirmation
from dimsumpy.qt.functions import closeEvent
from dimsumpy.qt.threads import MyThread

# PROGRAM MODULES
from pizzapy.core_stock_update.core_update_view import CoreUpdateView
from pizzapy.database_update.stock_list_model import stock_list_dict, table_function_dict





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







def call_upsert(self, stockgen: Generator[str, None, None], progress_bar, progress_label) -> None:  
    
    """
    * INDEPENDENT *
    IMPORTS: table_function_dict, try_str()
    USED BY: start_thread()
    
    # return type is not None
    This func runs in the QThread
    
    self.browser.repaint() will have error as multiple threads paint at the same time
    self.browser.append(browser_text) will have paint errors.
    
        debug_text: str = f"{i} / {self.list_length} {symbol} {result}"
            #QCoreApplication.processEvents()  # this line will crash the progrom for 2+ active threads
    """
    func = table_function_dict.get(self.table_name) 
    for i, symbol in enumerate(stockgen, start=1): # if the list is too long, program will crash
        print(i, symbol)
        result = try_str(func, symbol)
        progress_bar.setValue(i)
        progress_label.setText(f'{i}  {symbol} ')






@list_confirmation
def start_thread(self, stock_list: List[str]) -> None:
    """
    DEPENDS ON: self.calendar_get_dates(), self.call_upsert(), self.thread_finished()
    IMPORTS: MyThread, list_confiramtion()
    USED BY: update_core(), update_core_list()

    [stockgen] is the arguments for self.call_upsert in MyThread

    thread_id should NOT be self.thread_id as I may have multiple threads. If I use self.thread_id, it will overwrite the previous one.

    MyThread 2nd argument callback function cannot be shorted to self.thread_finished, as I need to include thread_id and hbox.

    Keep those variables local, do not add self: list_length, progress_bar, progress_label, hbox, stockgen, thread_id, thread

    The hbox, progress_bar and progress_label will be deleted on thread_finished() call back function.

    For empty line_edit, the stock_list will be ['']
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

    stockgen = (x for x in stock_list)
    thread: MyThread = MyThread(self.call_upsert, lambda tid=thread_id, box=hbox: self.thread_finished(tid, box), [stockgen, progress_bar, progress_label])
    self.threads_dict[thread_id] = thread
    thread.start()  # start the run() in QThread
    thread.wait(2) # prevent crash
    message = f'JOB {job_id}: Update {list_length} stocks ({self.table_name}) \n'
    self.browser.append(message)
    self.statusbar.showMessage(message)




def update_core(self) -> None:    
    """
    DEPENDS ON: start_thread()
    USED BY: CoreUpdateController

    I use stock_list as a start_thread second argument so that list decorator will work, 
    if I don't use decorator for upsert_core, I could simply make stock_list as self.stock_list, no second argument will be needed.
    
    In the stock_list line, I need to check lineedit_string by 'if lineedit_string', otherwise, re.split() will return ['']
    """
    lineedit_string: str = self.symbols_lineedit.text().strip()
    stock_list: List[str] = re.split(r'[ ,]+', lineedit_string) if lineedit_string else []
    if stock_list:   # prevent empty lineedit
        start_thread(self, stock_list) 
    else:
        self.statusbar.showMessage('No SYMBOLS in the lineedit')



def update_core_list(self) -> None:
    """
    DEPENDS ON: start_thread()
    IMPORTS: batterypy(int0)
    USED BY: CoreUpdateController

    self.stock_list_combobox_text, self.full_stock_list, self.full_list_length are defined in self.stock_list_combobox_changed() in core_update_view.py
    """
    lineedit_text: str = self.starting_lineedit.text()
    stock_list_name = self.stock_list_combobox.currentText()
    stock_list = stock_list_dict.get(stock_list_name)
    if lineedit_text in stock_list:
        stock_list = list(dropwhile(lambda x: x != lineedit_text, stock_list))
    else:        
        starting_number = max(int0(lineedit_text) - 1, 0)
        valid_starting_number: bool = starting_number < self.full_list_length
        stock_list = stock_list[starting_number:] if valid_starting_number else []
    
    if stock_list:
        start_thread(self, stock_list)
    else:
        self.statusbar.showMessage('Empty List')




def table_list_combobox_changed(self) -> None:
    """
    """
    self.table_name = self.table_list_combobox.currentText()
    self.symbols_lineedit.setPlaceholderText(f'input SYMBOLS for {self.table_name}, separated by spaces or commas')


def stock_list_combobox_changed(self) -> None:
    """
    """
    self.stock_list_combobox_text = self.stock_list_combobox.currentText()
    self.full_stock_list = stock_list_dict.get(self.stock_list_combobox_text)
    self.full_list_length = len(self.full_stock_list)
    self.starting_lineedit.setPlaceholderText(f'Input 1 to {self.full_list_length} OR a SYMBOL in the list to start')



def clear(self) -> None:
    """
    IMPORTS: 
    USED BY: CoreUpdateController
    """
    self.browser.clear()
    self.statusbar.showMessage('Ready')



class MakeConnects:
    """
    Buttons' connect functions can only connect to a function with one implicit self argument, 
    however, I can connect it to a wrapper method like below and which points to a function with more arguments.

    When there is no base class, it is more common to omit () after class name, as it is cleaner. 
    Although it is also valid to write a pair of empty selfhesis.

    deliberately run combobox changes for the first time to fill in label and lineedit text. I put the staring_lineedit.setPlaceholderText in the change function because I just need to edit once if I want to make further changes.
    """
    def __init__(ego, self) -> None:
        self.table_list_combobox.currentIndexChanged.connect(self.table_list_combobox_changed)
        self.stock_list_combobox.currentIndexChanged.connect(self.stock_list_combobox_changed)
        self.table_list_combobox_changed()   # this line sets self.table_name
        self.stock_list_combobox_changed() 
        
        self.update_list_button.clicked.connect(self.update_core_list)
        self.update_symbols_button.clicked.connect(self.update_core)
        
        self.clear_button.clicked.connect(self.clear)
        self.quit_button.clicked.connect(self.close)
        
    
class CoreUpdateController(CoreUpdateView):
    """
    DEPENDS ON: MakeConnects class, closeEvent(),  update_core_list(), update_core()
    IMPORTS: CoreUpdateView, closeEvent()
    """
    def __init__(self) -> None:
        super().__init__() # initialize all base class variables and methods
        self.threads_dict: Dict[float, MyThread] = {}
        MakeConnects(self)
        
    def clear(self) -> None:
        return clear(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)

    def stock_list_combobox_changed(self) -> None:
        return stock_list_combobox_changed(self)
    
    def table_list_combobox_changed(self) -> None:
        return table_list_combobox_changed(self)
        
    def thread_finished(self, thread_id: float, box) -> None:
        return thread_finished(self, thread_id, box)


    def call_upsert(self, stockgen: Generator[str, None, None], progress_bar, progress_label) -> None:  
        return call_upsert(self, stockgen, progress_bar, progress_label)  


    def update_core(self) -> None:
        return update_core(self)

    def update_core_list(self) -> None:
        return update_core_list(self)
        

def main() -> None:
    app = QApplication(sys.argv)
    win = CoreUpdateController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
