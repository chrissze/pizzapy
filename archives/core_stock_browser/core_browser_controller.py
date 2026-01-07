"""
AIM OF THIS MODULE: To create CoreBrowserController class. All other classes and functions are helpers of CoreBrowserController class.

DEPENDS ON: core_browser_view.py, qt_model.py

USED BY: main_dock_controller.py
"""
# STANDARD LIBS

from functools import partial
import re
from typing import Any, List, Tuple


# THIRD PARTY LIBS
from pandas import DataFrame
from PySide6.QtCore import QCoreApplication, QRegularExpression
from PySide6.QtGui import QAction, QCloseEvent
from PySide6.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget



# CUSTOM LIBS
from dimsumpy.qt.dataframemodel import DataFrameModel
from dimsumpy.qt.functions import closeEvent


# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import stock_list_dict
from pizzapy.database_update.postgres_connection_model import execute_pandas_read

from pizzapy.general_update.qt_model import MySortFilterProxyModel 
from pizzapy.core_stock_browser.core_browser_view import CoreBrowserView


def make_dataframe(self) -> None:
    """
        DEPENDS ON: self.symbols_list (property), self.table_list_combobox
        IMPORTS: pandas, execute_pandas_read()
        USED BY: load_stock_table(), load_stock_list_table()
        
        The aim of this function is to create self.df variable on the last line.

        self.df needs to be in self to share its value so that it can be accessed by load_tableview() and load_grid()

        This function depends on self.symbols_list in load_stock_table() and load_stock_list_table().

        When I input only one SYMBOL in the symbols_lineedit, it will becomes ('AMD',) if I convert it to a tuple, this string will have error in SQL query_clause, so I have to get rid of the comma when there is only 1 element.

        If self.symbols_list is empty, this function will just created a empty DataFrame for self.df.

    """
    self.clear()
    self.symbols_tuple_str = str(tuple(self.symbols_list)) if len(self.symbols_list) > 1 else str(tuple(self.symbols_list)).replace(',', '') # replace() is for single tuple
    self.table_name = self.table_list_combobox.currentText()
    query_clause: str = f' WHERE symbol IN {self.symbols_tuple_str} '  # prevent empty LineEdit
    cmd: str = f'SELECT * FROM {self.table_name} {query_clause}'
    self.df = execute_pandas_read(cmd) if self.symbols_list else DataFrame()



def make_tableview(self) -> None:
    """
        DEPENDS ON: make_dataframe()
        IMPORTS: pandas, dimsumpy(DataFrameModel), MySortFilterProxyModel
        USED BY: load_stock_table(), load_stock_list_table()

        This function needs make_dataframe() to prepare self.df property.
    """
    dataframe_model: DataFrameModel = DataFrameModel(self.df)
    self.sort_filter_model = MySortFilterProxyModel()
    self.sort_filter_model.setSourceModel(dataframe_model)
    self.pandas_tableview.setModel(self.sort_filter_model)
    self.statusbar.showMessage(f'{len(self.df)} rows')




def make_grid(self) -> None:
    """
        DEPENDS ON: make_dataframe(), self.on_checkbox_changed(), self.on_floor_lineedit_changed(), self.on_ceiling_lineedit_changed()
        IMPORTS: pandas
        USED BY: load_stock_table(), load_stock_list_table()

        This function needs make_dataframe() to prepare self.df property.
    """
    grid: QGridLayout = QGridLayout()   # If the Grid was created in the view, it will get deleted
    dock_checkboxes: List[QCheckBox] = [QCheckBox(x) for x in self.df.columns]
    for count, checkbox in enumerate(dock_checkboxes):
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(partial(self.on_checkbox_changed, index=count))
        floor_lineedit: QLineEdit = QLineEdit()
        ceiling_lineedit: QLineEdit = QLineEdit()
        floor_lineedit.textChanged.connect(lambda text, col=count: self.on_floor_lineedit_changed(text, col))
        ceiling_lineedit.textChanged.connect(lambda text, col=count: self.on_ceiling_lineedit_changed(text, col))

        grid.addWidget(checkbox, count, 0)
        grid.addWidget(floor_lineedit, count, 1)
        grid.addWidget(ceiling_lineedit, count, 2)
    QWidget().setLayout(self.dockwin.layout()) # get rid of the default layout
    self.dockwin.setLayout(grid)






def load_stock_table(self) -> None:
    """
        DEPENDS ON: make_dataframe(), make_tableview(), make_grid()
        USED BY: CoreBrowserController

        self.symbols_list needs to have self to share its value so that it can be accessed by make_dataframe()
    """
    lineedit_str: str = self.symbols_lineedit.text().upper().strip()
    self.symbols_list: List[str] = re.split(r'[ ,]+', lineedit_str) if lineedit_str else []
    if self.symbols_list:      # prevent empty lineedit string
        make_dataframe(self)
        make_tableview(self)
        make_grid(self) 
    else:
        self.statusbar.showMessage('No SYMBOLS in the lineedit')



def load_list_table(self) -> None:
    """
    DEPENDS ON: make_dataframe(), make_tableview(), make_grid()
    IMPORTS: stock_list_dict
    USED BY: CoreBrowserController
    """
    list_name: str = self.stock_list_combobox.currentText()
    self.symbols_list: List[str] = stock_list_dict.get(list_name)
    make_dataframe(self)
    make_tableview(self)
    make_grid(self)    


def clear(self) -> None:
    self.pandas_tableview.setModel(None)
    QWidget().setLayout(self.dockwin.layout()) # re-assign the existing layout


def hide_columns(self) -> None:
    index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3  # since there are two columns in grid
    if index:
        for i in range(index):
            self.dockwin.layout().itemAtPosition(i,0).widget().setChecked(False)
            QCoreApplication.processEvents()  # update the GUI


def show_columns(self) -> None:
    index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3
    if index:
        for i in range(index):
            self.dockwin.layout().itemAtPosition(i, 0).widget().setChecked(True)
            QCoreApplication.processEvents()


def table_list_combobox_changed(self) -> None:
    """

    """
    self.table_name = self.table_list_combobox.currentText()
    self.symbols_lineedit.setPlaceholderText(f'input SYMBOLS for {self.table_name}, separated by spaces or commas')


def on_checkbox_changed(self, value: int, index: int) -> None:
    """ 
    USED BY: make_grid() 
    """
    if value == 2:    # value is 2 for checked state
        self.pandas_tableview.setColumnHidden(index, False)
    else:
        self.pandas_tableview.setColumnHidden(index, True)


def on_floor_lineedit_changed(self, text, col) -> None:
    """ 
    USED BY: make_grid() 

    I deliberately add CaseInsensitiveOption to the floor filter's QRegualarExpression, so that I can have two streams in MySortFilterProxyModel's filterAcceptsRow() built-in virtual function.

    the floor_lineedit is for input a number so as to filter out all numbers below that threshold. For example, I want to get rid of all stocks that have a earn_pc lower that 5%, I can input 5 to floor_lineedit.

    In string columns like 'symbol', when the symbol is matched, the row will be hidden. 
    """
    self.sort_filter_model.setFilterByColumn(
        QRegularExpression(text, QRegularExpression.CaseInsensitiveOption), col)


def on_ceiling_lineedit_changed(self, text, col) -> None:
    """ 
    USED BY: make_grid() 

    As this method's Regular Expression does not have CaseInsensitiveOption, so it will fall into the else-clause in MySortFilterProxyModel's filterAcceptsRow() built-in virtual function.
    """
    self.sort_filter_model.setFilterByColumn(
        QRegularExpression(text), col)




class MakeConnects:
    """
    USED BY: CoreBrowserController

    Run self.table_list_combobox_changed() once for filling placeholder text.
    """
    def __init__(ego, self) -> None:
        self.table_list_combobox.currentIndexChanged.connect(self.table_list_combobox_changed)
        self.table_list_combobox_changed()

        self.load_list_button.clicked.connect(self.load_list_table)
        self.load_symbols_button.clicked.connect(self.load_stock_table)

        self.show_columns_action.triggered.connect(self.show_columns)
        self.hide_columns_action.triggered.connect(self.hide_columns)
        self.clear_action.triggered.connect(self.clear)
        self.quit_action.triggered.connect(self.close) # defined in closeEvent()




class CoreBrowserController(CoreBrowserView):
    """
    DEPENDS ON: MakeConnects, load_stock_list_table(), load_stock_table()
    IMPORTS: CoreBrowserView

    wrapper methods like self.load_list_table are necessary redundancies. I cannot skip them and directly call outer functions.
    
    super().__init__() is called because this class has a base class CoreBrowserView.
    """
    def __init__(self) -> None:
        super().__init__()
        MakeConnects(self)

    def load_list_table(self) -> None:
        return load_list_table(self)

    def load_stock_table(self) -> None:
        return load_stock_table(self)

    def on_checkbox_changed(self, value: int, index: int) -> None:
        return on_checkbox_changed(self, value, index)
    
    def on_floor_lineedit_changed(self, text, col) -> None:
        return on_floor_lineedit_changed(self, text, col)

    def on_ceiling_lineedit_changed(self, text, col) -> None:
        return on_ceiling_lineedit_changed(self, text, col)    

    def table_list_combobox_changed(self) -> None:
        return table_list_combobox_changed(self)

    def clear(self) -> None:
        return clear(self)

    def hide_columns(self) -> None:
        return hide_columns(self)

    def show_columns(self) -> None:
        return show_columns(self)
        
    def closeEvent(self, event: QCloseEvent) -> None:
        return closeEvent(self, event)
    




def main() -> None:
    app: QApplication = QApplication(sys.argv)
    win: CoreBrowserController = CoreBrowserController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
