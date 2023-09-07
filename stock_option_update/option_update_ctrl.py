
import sys; sys.path.append('..')

from dimsumpy.qt5.decorators import confirmation_self

from typing import Any, Dict, Generator, Optional

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QThread, QCoreApplication

from batterypy.string.read import is_intable, int0, float0

from core_stock_update.core_update_view import DailyGuruWin
from shared_model.st_data_model import stock_list_dict
from core_stock_update.guru_model import guru_upsert_1s
from core_stock_update.zacks_model import zacks_upsert_1s
from core_stock_update.option_model import option_upsert_1s


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
            s = guru_upsert_1s(symbol)
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
            s = zacks_upsert_1s(symbol)
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
            s = option_upsert_1s(symbol)
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
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
