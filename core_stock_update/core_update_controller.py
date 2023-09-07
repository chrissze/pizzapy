"""


Core Update Controller further works:
    import upsert_option
    import upsert_zacks
    update button function option
    update button function zacks

I should use some default properties of the SortFilterProxyModel to toggle the filter mode
"""



# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, Generator, List, Optional


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox


# CUSTOM LIBS
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import confirmation_self


# PROGRAM MODULES
from core_stock_update.core_update_view import CoreUpdateView
from database_update.stock_list_model import stock_list_dict
from guru_stock_update.guru_update_database_model import upsert_guru



def closeEvent(self, event: QCloseEvent) -> None:
    """
    IMPORTS: QMessageBox
    USED BY: DailyGuruDialog
    This special named 'closeEvent' method overrides default close() method.
    This methed is called when we call self.close() or users click the X button.
    """
    reply: QMessageBox.StandardButton = QMessageBox.question(
        self, 'Confirmation', 'Do you want to QUIT now?', QMessageBox.Yes | QMessageBox.Cancel)
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()




@confirmation_self
def update_core(self, func) -> None:    
    """
    IMPORTS: QCoreApplication, func(upsert_guru)
    USED BY: CoreUpdateController
    """
    update_stocks_lineedit_string: str = self.update_stocks_lineedit.text()
    stock_list: List[str] = update_stocks_lineedit_string.split()

    stock_list_length = len(stock_list)
    self.progressbar.setRange(0, stock_list_length)
    stockgen = (x for x in stock_list)
    for count, symbol in enumerate(stockgen, start=1):
        s = func(symbol)
        msg = f'{count} / {stock_list_length} {s}'
        self.progressbar.setValue(count)
        self.browser.append(msg)
        self.browser.repaint()
        QCoreApplication.processEvents()   # update the GUI
        print(msg)





@confirmation_self
def update_core_list(self, func) -> None:
    """
    IMPORTS: QCoreApplication, func(upsert_guru), batterypy(int0)
    USED BY: CoreUpdateController

    self.combobox_string, self.full_stock_list, self.full_list_length are defined in self.stock_list_comboxbox_changed() in core_update_view.py
    """
    list_start: int = int0(self.stock_list_starting_number_lineedit.text()) - 1
    valid_starting_number: bool = list_start < self.full_list_length and list_start >= 0
    stock_working_list = stock_list_dict.get(self.combobox_string)[list_start:] if valid_starting_number else self.full_stock_list
    QCoreApplication.processEvents()  # update the GUI

    self.stock_working_list_length = len(stock_working_list)
    self.progressbar.setRange(0, self.stock_working_list_length)
    stockgen = (x for x in stock_working_list)
    for count, symbol in enumerate(stockgen, start=1):
        QCoreApplication.processEvents()   # update the GUI
        s = func(symbol)
        msg = f'{count} / {self.stock_working_list_length} {s}'
        self.progressbar.setValue(count)
        self.browser.append(msg)
        self.browser.repaint()
        QCoreApplication.processEvents()   # update the GUI
        print(msg)






class MakeButtonConnects:
    """
    Buttons' connect functions can only connect to a function with one implicit self argument, 
    however, I can connect it to a wrapper method like below and which points to a function with more arguments.

    When there is no base class, it is more common to omit () after class name, as it is cleaner. 
    Although it is also valid to write a pair of empty parenthesis.
    """
    def __init__(self, parent) -> None:
        parent.update_guru_list_button.clicked.connect(parent.update_guru_list)
        parent.update_zacks_list_button.clicked.connect(parent.update_zacks_list)
        parent.update_option_list_button.clicked.connect(parent.update_option_list)
        parent.update_guru_button.clicked.connect(parent.update_guru)
        parent.update_zacks_button.clicked.connect(parent.update_zacks)
        parent.update_option_button.clicked.connect(parent.update_option)
        parent.clear_button.clicked.connect(parent.browser.clear)
        parent.quit_button.clicked.connect(parent.close)
        

class CoreUpdateController(CoreUpdateView):
    """
    DEPENDS ON: MakeButtonConnects class, closeEvent(),  update_core_list(), update_core()
    IMPORTS: DailyGuruWin, upsert_guru
    """
    def __init__(self) -> None:
        super().__init__() # initialize all DailyGuruWin() variables and methods
        #self.threads: Dict[float, CustomThread] = {}
        MakeButtonConnects(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)
    
    def update_guru_list(self) -> None:
        return update_core_list(self, upsert_guru)
        
    def update_zacks_list(self) -> None:
        return update_core_list(self, upsert_guru)
    
    def update_option_list(self) -> None:
        return update_core_list(self, upsert_guru)
    
    def update_guru(self) -> None:
        return update_core(self, upsert_guru)
        
    def update_zacks(self) -> None:
        return update_core(self, upsert_guru)
    
    def update_option(self) -> None:
        return update_core(self, upsert_guru)
    


def main() -> None:
    app = QApplication(sys.argv)
    win = CoreUpdateController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
