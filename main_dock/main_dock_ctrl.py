
import sys; sys.path.append('..')


from datetime import date
from futures_update.fut_update_ctrl import FutUpdateDialog
from futures_browser.fut_browser_ctrl import FutBrowserDialog
from main_dock.main_dock_view import MainDockWin

from PySide2.QtWidgets import QApplication, QWidget
from core_stock_update.core_update_ctrl import DailyGuruDialog
from stock_core_browser.core_browser_ctrl import GuruBrowserDialog

from stock_price_browser.price_browser_ctrl import StockPriceBrowserDialog
from stock_price_update.st_price_update_ctrl import StockPriceUpdateDialog
from typing import Any, Dict,  Generator, List


def outer_open_dialog(sharedlist: List[Any], sender: str) -> None:
    if sender == 'b1_1':
        dialog = StockPriceBrowserDialog()
    if sender == 'b1_2':
        dialog = StockPriceUpdateDialog()
    elif sender == 'b2_1':
        dialog = FutBrowserDialog()
    elif sender == 'b2_2':
        dialog = FutUpdateDialog()
    else:
        print('no sender')
    sharedlist.append(dialog)
    dialog.show()


class MainDockDialog(MainDockWin):
    def __init__(self) -> None:
        super().__init__()
        self.dialogs: List[Any] = list()
        self.b1_1.clicked.connect(lambda: outer_open_dialog(self.dialogs, 'b1_1'))
        self.b1_2.clicked.connect(lambda: outer_open_dialog(self.dialogs, 'b1_2'))
        self.b2_1.clicked.connect(lambda: outer_open_dialog(self.dialogs, 'b2_1'))
        self.b2_2.clicked.connect(lambda: outer_open_dialog(self.dialogs, 'b2_2'))
        self.b3_1.clicked.connect(self.opendialog)
        self.b3_2.clicked.connect(self.opendialog)

    def opendialog(self) -> None:
        sender: str = self.sender().accessibleName()
        if sender == 'b3_1':
            dialog = GuruBrowserDialog()
        elif sender == 'b3_2':
            dialog = DailyGuruDialog()
        else:
            print('no sender')
        self.dialogs.append(dialog)
        dialog.show()



def main() -> None:
    app: QApplication = QApplication(sys.argv)
    w: MainDockDialog = MainDockDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
