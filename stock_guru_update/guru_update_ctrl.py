"""

"""
# STANDARD LIBS
import sys; sys.path.append('..')
from typing import Any, Dict, Generator, Optional


# THIRD PARTY LIBS
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread, QCoreApplication

# CUSTOM LIBS
from batterypy.string.read import is_intable, int0, float0
from dimsumpy.qt.decorators import confirmation_self

# PROGRAM MODULES
from stock_guru_update.guru_update_view import DailyGuruWin
from database_update.stock_list_model import stock_list_dict
from stock_guru_update.guru_update_database_model import upsert_guru


class DailyGuruDialog(DailyGuruWin):
    def __init__(self) -> None:
        super().__init__()
        #self.threads: Dict[float, CustomThread] = {}
        self.b_list_guru.clicked.connect(self.guru_func)
        self.b_le_guru.clicked.connect(self.guru_func)
        self.b_list_zacks.clicked.connect(self.zacks_func)
        self.b_le_zacks.clicked.connect(self.zacks_func)
        self.b_list_option.clicked.connect(self.option_func)
        self.b_le_option.clicked.connect(self.option_func)

    @confirmation_self
    def guru_func(self) -> None:
        list_start: int = int0(self.le_list_start.text())
        sender = self.sender().accessibleName()
        if sender == 'b_list_guru':
            stockstr = self.combo.currentText()
            stocklist = stock_list_dict.get(stockstr)[list_start:]
        elif sender == 'b_le_guru':
            stockstr = self.get_le_symbol()
            stocklist = stockstr.split()
        QCoreApplication.processEvents()  # update the GUI

        self.l = len(stocklist)
        self.pbar.setRange(0, self.l)
        stockgen = (x for x in stocklist)
        for count, symbol in enumerate(stockgen, start=1):
            QCoreApplication.processEvents()   # update the GUI
            s = upsert_guru(symbol)
            msg = f'{count} / {self.l} {s}'
            self.pbar.setValue(count)
            self.browser.append(msg)
            self.browser.repaint()
            QCoreApplication.processEvents()   # update the GUI
            print(msg)

    @confirmation_self
    def zacks_func(self) -> None:
        list_start: int = int0(self.le_list_start.text())
        sender = self.sender().accessibleName()
        if sender == 'b_list_zacks':
            stockstr = self.combo.currentText()
            stocklist = stock_list_dict.get(stockstr)[list_start:]

        elif sender == 'b_le_zacks':
            stockstr = self.get_le_symbol()
            stocklist = stockstr.split()

        self.l = len(stocklist)
        self.pbar.setRange(0, self.l)
        stockgen = (x for x in stocklist)
        for count, symbol in enumerate(stockgen, start=1):
            s = upsert_guru(symbol)
            msg = f'{count} / {self.l} {s}'
            self.pbar.setValue(count)
            self.browser.append(msg)
            self.browser.repaint()
            QCoreApplication.processEvents()   # update the GUI
            print(msg)

    @confirmation_self
    def option_func(self) -> None:
        list_start: int = int0(self.le_list_start.text())
        sender = self.sender().accessibleName()
        if sender == 'b_list_option':
            stockstr = self.combo.currentText()
            stocklist = stock_list_dict.get(stockstr)[list_start:]

        elif sender == 'b_le_option':
            stockstr = self.get_le_symbol()
            stocklist = stockstr.split()

        self.l = len(stocklist)
        self.pbar.setRange(0, self.l)
        stockgen = (x for x in stocklist)
        for count, symbol in enumerate(stockgen, start=1):
            s = upsert_guru(symbol)
            msg = f'{count} / {self.l} {s}'
            self.pbar.setValue(count)
            self.browser.append(msg)
            self.browser.repaint()
            QCoreApplication.processEvents()   # update the GUI
            print(msg)


def main() -> None:
    app = QApplication(sys.argv)
    w = DailyGuruDialog()
    w.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
