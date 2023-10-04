
import sys;

from dimsumpy.qt5.decorators import self_confirmation

sys.path.append('..')

from batterypy.string.read import is_intable, int0, float0

from futures_update.ino_model import ino_upsert_1s, ino_op, ino_calc
from futures_update.fut_update_view import FutUpdateWin
from PySide2.QtWidgets import QApplication, QComboBox, QMessageBox
from PySide2.QtCore import QThread, QCoreApplication

from shared_model.fut_data_model import getfutures, getfutcode

from typing import Any, Dict, Generator, List, Optional

def outer_update_fut(s: str) -> str:
        result: str = ino_upsert_1s(s)  # parallel code MUST run in a outer function, prevent messing with GUI class
        return result


class FutUpdateDialog(FutUpdateWin):
    def __init__(self) -> None:
        super().__init__()
        self.b_list_option.clicked.connect(self.updatefunc)
        self.b_single_option.clicked.connect(self.updatefunc)

    @self_confirmation
    def updatefunc(self) -> None:
        list_start: int = int0(self.symbols_lineedit_list_start.text())
        sender: str = self.sender().accessibleName()
        if sender == 'b_list_option':
            combostr: str = self.stock_list_combobox.currentText()  # if the combobox is empty, '' will be the currentText
            symbols: List[str] = getfutcode(combostr)[list_start:]

        elif sender == 'b_single_option':
            combostr: str = self.stock_list_combobox_individual.currentText()
            symbols: List[str] = [combostr[:2]]
        length: int = len(symbols)
        self.progress_bar.setRange(0, length)
        symbolsgen: Generator[str, None, None] = (x for x in symbols)

        for count, symbol in enumerate(symbolsgen, start=1):
            s: str = outer_update_fut(symbol)
            msg: str = str(count) + ' / ' + str(length) + ' ' + s
            self.progress_bar.setValue(count)
            self.browser.append(msg)
            self.browser.repaint()
            QCoreApplication.processEvents()   # update the GUI
            print(msg)




def main() -> None:
    app: QApplication = QApplication(sys.argv)
    w: FutUpdateDialog = FutUpdateDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
