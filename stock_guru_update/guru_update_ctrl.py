"""

"""
# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, Generator, Optional


# THIRD PARTY LIBS
from PySide6.QtCore import QThread, QCoreApplication
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QApplication, QMessageBox


# CUSTOM LIBS
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import confirmation_self


# PROGRAM MODULES
from stock_guru_update.guru_update_view import DailyGuruWin
from database_update.stock_list_model import stock_list_dict
from stock_guru_update.guru_update_database_model import upsert_guru



def closeEvent(self, event: QCloseEvent) -> None:
    """
    IMPORTS: QMessageBox
    USED BY: DailyGuruDialog
    This special named 'closeEvent' method overrides default close() method.
    This methed is called when we call self.close() or users click the X button.
    """
    reply: QMessageBox.StandardButton = QMessageBox.question(
        self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
    if reply == QMessageBox.Yes:
        event.accept()
    else:
        event.ignore()




@confirmation_self
def update_core(self, func) -> None:    
    """
    IMPORTS: QCoreApplication, func(upsert_guru)
    USED BY: DailyGuruDialog
    """
    stockstr = self.le.text()
    stocklist = stockstr.split()

    self.l = len(stocklist)
    self.pbar.setRange(0, self.l)
    stockgen = (x for x in stocklist)
    for count, symbol in enumerate(stockgen, start=1):
        s = func(symbol)
        msg = f'{count} / {self.l} {s}'
        self.pbar.setValue(count)
        self.browser.append(msg)
        self.browser.repaint()
        QCoreApplication.processEvents()   # update the GUI
        print(msg)





@confirmation_self
def update_core_list(self, func) -> None:
    """
    IMPORTS: QCoreApplication, func(upsert_guru)
    USED BY: DailyGuruDialog
    """
    list_start: int = int0(self.le_list_start.text())
    stockstr = self.combo.currentText()
    stocklist = stock_list_dict.get(stockstr)[list_start:]
    QCoreApplication.processEvents()  # update the GUI

    self.l = len(stocklist)
    self.pbar.setRange(0, self.l)
    stockgen = (x for x in stocklist)
    for count, symbol in enumerate(stockgen, start=1):
        QCoreApplication.processEvents()   # update the GUI
        s = func(symbol)
        msg = f'{count} / {self.l} {s}'
        self.pbar.setValue(count)
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
        parent.b_list_guru.clicked.connect(parent.update_guru_list)
        parent.b_list_zacks.clicked.connect(parent.update_zacks_list)
        parent.b_list_option.clicked.connect(parent.update_option_list)
        parent.b_le_guru.clicked.connect(parent.update_guru)
        parent.b_le_zacks.clicked.connect(parent.update_zacks)
        parent.b_le_option.clicked.connect(parent.update_option)

        parent.b_clear.clicked.connect(parent.browser.clear)
        parent.b_quit.clicked.connect(parent.close)



class DailyGuruDialog(DailyGuruWin):
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
    win = DailyGuruDialog()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
