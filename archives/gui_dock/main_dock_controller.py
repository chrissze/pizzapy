"""

USED BY: main.py
"""

# STANDARD LIBS
import sys
from typing import Any, List


# THIRD PARTY LIBS
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QCloseEvent


# CUSTOM LIBS
from dimsumpy.qt.functions import closeEvent

# PROGRAM MODULES
from pizzapy.gui_dock.main_dock_view import MainDockView

from pizzapy.core_stock_update.core_update_controller import CoreUpdateController

from pizzapy.core_stock_browser.core_browser_controller import CoreBrowserController

from pizzapy.stock_price_update.price_update_controller import PriceUpdateController




def open_external_window(window_list: List[Any], controller) -> None:
    """
    I need to have a collection structure to hold the controller window, otherwise it is not shown.
    """
    window = controller()
    window_list.append(window)
    window.show()



class MakeConnects:
    """

    """
    def __init__(ego, self) -> None:        
        self.core_browser_button.clicked.connect(lambda: open_external_window(self.windows, CoreBrowserController))
        self.core_updater_button.clicked.connect(lambda: open_external_window(self.windows, CoreUpdateController))
        self.price_updater_button.clicked.connect(lambda: open_external_window(self.windows, PriceUpdateController))
        self.quit_button.clicked.connect(self.close)        


class MainDockController(MainDockView):
    def __init__(self) -> None:
        super().__init__()
        self.windows: List[Any] = list()
        MakeConnects(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)




def main() -> None:
    app: QApplication = QApplication(sys.argv)
    win: MainDockController = MainDockController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
