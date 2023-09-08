
# STANDARD LIBS
import sys; sys.path.append('..')
from functools import partial

# THIRD PARTY LIBS
import pandas
from pandas import DataFrame
from PySide6.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget
from PySide6.QtCore import Qt, QRegularExpression

# CUSTOM LIBS
from dimsumpy.qt.dataframemodel import DataFrameModel

# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict
from database_update.postgres_connection_model import execute_pandas_read

from general_update.qt_model import MySortFilterProxyModel 
from core_stock_browser.core_browser_view import CoreBrowserView
from typing import Any, List, Tuple




def load_tableview(self, df: DataFrame) -> None:
    """
        IMPORTS: pandas, dimsumpy(DataFrameModel), MySortFilterProxyModel
        USED BY: load_stock_list_table()
    """
   
    model: DataFrameModel = DataFrameModel(df)
    self.proxy: MySortFilterProxyModel = MySortFilterProxyModel()
    self.proxy.setSourceModel(model)
    self.pandasTv.setModel(self.proxy)



def load_grid(self, df: DataFrame) -> None:
    """
        DEPENDS ON: self.on_checkbox_changed()
        IMPORTS: pandas
        USED BY: load_stock_list_table()
    """
    grid: QGridLayout = QGridLayout()   # If the Grid was created in the view, it will get deleted
    checkboxes: List[QCheckBox] = [QCheckBox(x) for x in df.columns]
    for count, checkbox in enumerate(checkboxes):
        checkbox.setChecked(True)
        checkbox.stateChanged.connect(partial(self.on_checkbox_changed, index=count))
        le1: QLineEdit = QLineEdit()
        le2: QLineEdit = QLineEdit()
        le1.textChanged.connect(lambda text, col=count: self.on_text_lower(text, col))
        le2.textChanged.connect(lambda text, col=count: self.on_text_changed(text, col))

        grid.addWidget(checkbox, count, 0)
        grid.addWidget(le1, count, 1)
        grid.addWidget(le2, count, 2)

    QWidget().setLayout(self.dockwin.layout()) # get rid of the default layout
    self.dockwin.setLayout(grid)



def load_stock_table(self, tablename: str) -> None:
    """
    DEPENDS ON: load_tableview(), load_grid()
    IMPORTS:  execute_pandas_read(), pandas
    USED BY: CoreBrowserController
    """
    self.clear()
    stockstr: str = self.le.text().upper()
    stocklist: List[str] = stockstr.split()
    stockliststr: str = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple

    q_clause: str = '' if not stocklist else f' WHERE symbol IN {stockliststr} '  # prevent empty LineEdit
    cmd: str = f'SELECT * FROM {tablename} {q_clause}'
    df: DataFrame = execute_pandas_read(cmd)
    load_tableview(self, df)
    load_grid(self, df)   


def load_stock_list_table(self, tablename: str) -> None:
    """
    DEPENDS ON: load_tableview(), load_grid()
    IMPORTS:  execute_pandas_read(), pandas
    USED BY: CoreBrowserController
    """
    self.clear()
    stockstr: str = self.combo.currentText()
    stocklist: List[str] = stock_list_dict.get(stockstr)
    stockliststr: str = str(tuple(stocklist))

    q_clause: str = '' if not stocklist else f' WHERE symbol IN {stockliststr} '  # prevent empty LineEdit
    q: str = f'SELECT * FROM {tablename} {q_clause}'
    df: DataFrame = execute_pandas_read(q)
    load_tableview(self, df)
    load_grid(self, df)    



class MakeConnects:
    def __init__(ego, self) -> None:
        super().__init__()
        self.b_list_guru.clicked.connect(self.load_guru_list_table)
        self.b_list_zacks.clicked.connect(self.load_zacks_list_table)
        self.b_list_option.clicked.connect(self.load_option_list_table)

        self.b_le_guru.clicked.connect(self.load_guru_table)
        self.b_le_zacks.clicked.connect(self.load_zacks_table)
        self.b_le_option.clicked.connect(self.load_option_table)




class CoreBrowserController(CoreBrowserView):
    """
    DEPENDS ON: MakeConnects, load_stock_list_table(),  load_stock_table()
    """
    def __init__(self) -> None:
        super().__init__()

        MakeConnects(self)

    def load_guru_list_table(self) -> None:
        return load_stock_list_table(self, 'stock_guru')

    def load_zacks_list_table(self) -> None:
        return load_stock_list_table(self, 'stock_guru')

    def load_option_list_table(self) -> None:
        return load_stock_list_table(self, 'stock_guru')

    def load_guru_table(self) -> None:
        return load_stock_table(self, 'stock_guru')

    def load_zacks_table(self) -> None:
        return load_stock_table(self, 'stock_guru')

    def load_option_table(self) -> None:
        return load_stock_table(self, 'stock_guru')


    def on_checkbox_changed(self, value: int, index: int) -> None:
        if value == 2:
            self.pandasTv.setColumnHidden(index, False)
        else:
            self.pandasTv.setColumnHidden(index, True)


    def on_text_lower(self, text, col):
        self.proxy.setFilterByColumn(
                QRegularExpression(text, QRegularExpression.CaseInsensitiveOption), col)

    def on_text_changed(self, text, col):
        revised_text:str = f'+{text}'
        self.proxy.setFilterByColumn(
                QRegularExpression(revised_text, QRegularExpression.CaseInsensitiveOption), col)

def main() -> None:
    app: QApplication = QApplication(sys.argv)
    win: CoreBrowserController = CoreBrowserController()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
