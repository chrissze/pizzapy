"""
DEPENDS ON: core_update_view.py, stock_list_model.py


"""



# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, Generator, List, Optional


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox


# CUSTOM LIBS
from batterypy.control.trys import try_str
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import confirmation_self
from dimsumpy.qt.functions import closeEvent


# PROGRAM MODULES
from core_stock_update.core_update_view import CoreUpdateView
from database_update.stock_list_model import stock_list_dict, table_function_dict






@confirmation_self
def update_core(self) -> None:    
    """
    IMPORTS: QCoreApplication, func(upsert_guru)
    USED BY: CoreUpdateController
    """
    symbols_lineedit_string: str = self.symbols_lineedit.text()
    stock_list: List[str] = symbols_lineedit_string.split()

    stock_list_length = len(stock_list)
    self.progress_bar.setRange(0, stock_list_length)
    stockgen = (x for x in stock_list)
    func = table_function_dict.get(self.table_name)   
    # self.table_name is defined in core_update_view.py
    for count, symbol in enumerate(stockgen, start=1):
        s = try_str(func, symbol)
        msg = f'{count} / {stock_list_length} {s}'
        self.progress_bar.setValue(count)
        self.progress_label.setText(f'{count} / {stock_list_length} {symbol}          ')
        self.browser.append(msg)
        self.browser.repaint()
        QCoreApplication.processEvents()   # update the GUI
        print(msg)





@confirmation_self
def update_core_list(self) -> None:
    """
    IMPORTS: QCoreApplication, func(upsert_guru), batterypy(int0)
    USED BY: CoreUpdateController

    self.stock_list_combobox_text, self.full_stock_list, self.full_list_length are defined in self.stock_list_combobox_changed() in core_update_view.py
    """
    starting_number: int = int0(self.starting_lineedit.text()) - 1
    valid_starting_number: bool = starting_number < self.full_list_length and starting_number >= 0
    stock_working_list = stock_list_dict.get(self.stock_list_combobox_text)[starting_number:] if valid_starting_number else self.full_stock_list
    QCoreApplication.processEvents()  # update the GUI

    self.stock_working_list_length = len(stock_working_list)
    self.progress_bar.setRange(0, self.stock_working_list_length)
    stockgen = (x for x in stock_working_list)
    func = table_function_dict.get(self.table_name)
    # self.table_name is defined in core_update_view.py
    for count, symbol in enumerate(stockgen, start=1):
        QCoreApplication.processEvents()   # update the GUI
        s = try_str(func, symbol)
        msg = f'{count} / {self.stock_working_list_length} {s}'
        self.progress_bar.setValue(count)
        self.progress_label.setText(f'{count} / {self.stock_working_list_length} {symbol}          ')
        self.browser.append(msg)
        self.browser.repaint()
        QCoreApplication.processEvents()   # update the GUI
        print(msg)




def table_list_combobox_changed(self) -> None:
    """
    This method is about layout appearance change, so I place it in view module.
    """
    self.table_name = self.table_list_combobox.currentText()
    self.symbols_label.setText(f'{self.table_name} SYMBOLS (divided by space): ')


def stock_list_combobox_changed(self) -> None:
    """
    This method is about layout appearance change, so I place it in view module.
    """
    self.stock_list_combobox_text = self.stock_list_combobox.currentText()
    self.full_stock_list = stock_list_dict.get(self.stock_list_combobox_text)
    self.full_list_length = len(self.full_stock_list)
    self.starting_lineedit.setPlaceholderText(f'Input 1 to {self.full_list_length} as starting no. (optional)')



def clear(self) -> None:
    """
    IMPORTS: 
    USED BY: CoreUpdateController
    """
    self.browser.clear()
    self.progress_label.setText(' 0 / 0          ')


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
        self.table_list_combobox_changed() 
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
        MakeConnects(self)
        
    def clear(self) -> None:
        return clear(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)

    def stock_list_combobox_changed(self) -> None:
        return stock_list_combobox_changed(self)
    
    def table_list_combobox_changed(self) -> None:
        return table_list_combobox_changed(self)
    
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
