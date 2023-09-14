
import sys
sys.path.append('..')

# new comment

import time
from datetime import date
from functools import partial
from typing import Any, Generator, Dict


import pandas as pd
from PySide2.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget, QFormLayout
from PySide2.QtCore import Qt, QThread, QCoreApplication, QDate, QDateTime ,QRegExp ,QSortFilterProxyModel

from shared_model.sql_model import postgres_engine
from shared_model.st_data_model import MySortFilterProxyModel, stock_list_dict
from stock_price_browser.price_browser_view import StockPriceBrowserWin


from dimsumpy.database.postgres import upsertquery
from dimsumpy.qt5.dataframemodel import DataFrameModel
from batterypy.string.read import is_floatable, readf




class StockPriceBrowserDialog(StockPriceBrowserWin):
    def __init__(self) -> None:
        super().__init__()

        #self.threads: Dict[float, CustomThread] = {}
        self.b_list_price.clicked.connect(self.load_table)
        self.b_le_price.clicked.connect(self.load_table)

        self.b_list_option.clicked.connect(self.load_table)
        self.b_le_option.clicked.connect(self.load_table)





    def load_table(self) -> None:
        self.clear()
        date1, date2 = self.calendar_get_dates()
        fromstr: str = "'" + str(date1) + "'"
        tostr: str = "'" + str(date2) + "'"
        sender = self.sender().accessibleName()
        if sender == 'b_list_price':
            tablename = 'usstock_price'
            stockstr = self.stock_list_combobox.currentText()
            stocklist = stock_list_dict.get(stockstr)
            stockliststr = str(tuple(stocklist))
        elif sender == 'b_le_price':
            tablename = 'usstock_price'
            stockstr = self.symbols_lineedit.text().upper()
            stocklist = stockstr.split()
            stockliststr = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple


        elif sender == 'b_list_option':
            tablename = 'usstock_option'
            stockstr = self.stock_list_combobox.currentText()
            stocklist = stock_list_dict.get(stockstr)
            stockliststr = str(tuple(stocklist))
        elif sender == 'b_le_option':
            tablename = 'usstock_option'
            stockstr = self.symbols_lineedit.text().upper()
            stocklist = stockstr.split()
            stockliststr = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple
        else:
            print('no sender')

        q_clause = '' if not stocklist else ' WHERE symbol IN ' + stockliststr  # prevent empty LineEdit
        date_clause = '' if not stocklist else ' AND td BETWEEN ' + fromstr + ' AND ' + tostr
        q = 'SELECT * FROM ' + tablename + q_clause + date_clause
        print(q)
        df = pd.read_sql(sql=q, con=postgres_engine)
        model = DataFrameModel(df)
        proxy = MySortFilterProxyModel()  # by use proxy instead of self.sort_filter_model, the sorting is faster
        proxy.setSourceModel(model)
        self.pandas_tableview.setModel(proxy)

        grid = QGridLayout()   # If the Grid was created in the view, and this file __init__, it will get deleted
        checkboxes = [QCheckBox(x) for x in df.columns]
        for count, checkbox in enumerate(checkboxes):
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(partial(self.display_column, index=count))
            le1 = QLineEdit()
            le2 = QLineEdit()
            le1.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp), col))
            le2.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString), col))

            grid.addWidget(checkbox, count, 0)
            grid.addWidget(le1, count, 1)
            grid.addWidget(le2, count, 2)

        QWidget().setLayout(self.dockwin.layout()) # get rid of the default layout
        self.dockwin.setLayout(grid)

    def display_column(self, state, index=None) -> None:
        if state == Qt.Checked:
            self.pandas_tableview.setColumnHidden(index, False)
        else:
            self.pandas_tableview.setColumnHidden(index, True)


def main() -> None:
    app = QApplication(sys.argv)
    w = StockPriceBrowserDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
