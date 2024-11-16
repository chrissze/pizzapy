
# STANDARD LIBS

from functools import partial

# THIRD PARTY LIBS
import pandas
from pandas import DataFrame
from PySide6.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget
from PySide6.QtCore import Qt, QRegularExpression

# CUSTOM LIBS
from dimsumpy.qt.dataframemodel import DataFrameModel

# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import stock_list_dict
from pizzapy.database_update.postgres_connection_model import execute_pandas_read

from pizzapy.general_update.qt_model import MySortFilterProxyModel 
from pizzapy.core_stock_browser.core_browser_view import CoreBrowserView
from typing import Any, List, Tuple





def make_dataframe(self) -> None:
    """
        DEPENDS ON: 
        IMPORTS: pandas, execute_pandas_read()
        USED BY: load_stock_table(), load_stock_list_table()
        self.df needs to be in self to share its value so that it can be accessed by load_tableview() and load_grid()

    """
    self.clear()
    self.symbols_tuple_str = str(tuple(self.symbols_list))  # for single tuple
    self.table_name = self.table_list_combobox.currentText()
    query_clause: str = '' if not self.symbols_list else f' WHERE symbol IN {self.symbols_tuple_str} '  # prevent empty LineEdit
    cmd: str = f'SELECT * FROM {self.table_name} {query_clause}'
    self.df = execute_pandas_read(cmd)



def make_tableview(self) -> None:
    """
        IMPORTS: pandas, dimsumpy(DataFrameModel), MySortFilterProxyModel
        USED BY: load_stock_table(), load_stock_list_table()
    """
    dataframe_model: DataFrameModel = DataFrameModel(self.df)
    self.sort_filter_model = MySortFilterProxyModel()
    self.sort_filter_model.setSourceModel(dataframe_model)
    self.pandas_tableview.setModel(self.sort_filter_model)



def make_grid(self) -> None:
    """
        DEPENDS ON: self.on_checkbox_changed(), self.on_text_changed_floor(), self.on_text_changed_ceiling()
        IMPORTS: pandas
        USED BY: load_stock_table(), load_stock_list_table()
    """
    grid: QGridLayout = QGridLayout()   # If the Grid was created in the view, it will get deleted
    dock_checkboxes: List[QCheckBox] = [QCheckBox(x) for x in self.df.columns]
    for count, checkbox in enumerate(dock_checkboxes):
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(partial(self.on_checkbox_changed, index=count))
        floor_lineedit: QLineEdit = QLineEdit()
        ceiling_lineedit: QLineEdit = QLineEdit()
        floor_lineedit.textChanged.connect(lambda text, col=count: self.on_text_changed_floor(text, col))
        ceiling_lineedit.textChanged.connect(lambda text, col=count: self.on_text_changed_ceiling(text, col))

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
    symbols_str: str = self.symbols_lineedit.text().upper()
    self.symbols_list: List[str] = symbols_str.split()
    make_dataframe(self)
    make_tableview(self)
    make_grid(self)   


def load_list_table(self) -> None:
    """
    DEPENDS ON: make_dataframe(), make_tableview(), make_grid()
    IMPORTS: stock_list_dict
    USED BY: CoreBrowserController
    """
    list_name_str: str = self.stock_list_combobox.currentText()
    self.symbols_list: List[str] = stock_list_dict.get(list_name_str)
    make_dataframe(self)
    make_tableview(self)
    make_grid(self)    



class MakeConnects:
    """self in this class is the instance of the calling class CoreBrowserController"""
    def __init__(ego, self) -> None:
        self.load_list_button.clicked.connect(self.load_list_table)
        self.load_symbols_button.clicked.connect(self.load_stock_table)



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
        """ USED BY: make_grid() """
        if value == 2:    # value is 2 for checked state
            self.pandas_tableview.setColumnHidden(index, False)
        else:
            self.pandas_tableview.setColumnHidden(index, True)

    def on_text_changed_floor(self, text, col):
        """ USED BY: make_grid() """
        self.sort_filter_model.setFilterByColumn(
            QRegularExpression(text, QRegularExpression.CaseInsensitiveOption), col)

    def on_text_changed_ceiling(self, text, col):
        """ USED BY: make_grid() """
        revised_text:str = f'+{text}'
        self.sort_filter_model.setFilterByColumn(
            QRegularExpression(revised_text, QRegularExpression.CaseInsensitiveOption), col)


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    win: CoreBrowserController = CoreBrowserController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
