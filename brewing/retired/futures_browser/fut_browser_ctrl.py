

from dimsumpy.qt5.dataframemodel import DataFrameModel
from functools import partial
from futures_browser.fut_browser_view import FutBrowserWin

import pandas as pd
from pandas.core.frame import DataFrame
from PySide2.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget, QFormLayout
from PySide2.QtCore import Qt, QThread, QCoreApplication, QDateTime ,QRegExp ,QSortFilterProxyModel

from shared_model.sql_model import cnx,  postgres_engine
from shared_model.st_data_model import MySortFilterProxyModel
from shared_model.fut_data_model import getfutures, getfutcode
from typing import Any, Dict, Generator, List


class FutBrowserDialog(FutBrowserWin):
    def __init__(self) -> None:
        super().__init__()
        self.b_list_option.clicked.connect(self.load_table)
        self.b_single_option.clicked.connect(self.load_table)

    def load_table(self) -> None:
        self.clear()
        sender: str = self.sender().accessibleName()

        if sender == 'b_list_option':
            tablename: str = 'fut_option'
            stockstr: str = self.stock_list_combobox.currentText()
            stocklist: List[str] = getfutcode(stockstr)
            stockliststr: str = str(tuple(stocklist))
        elif sender == 'b_single_option':
            tablename: str = 'fut_option'
            stockstr: str = self.stock_list_combobox_individual.currentText()[:2]
            stocklist: List[str] = [stockstr]
            stockliststr: str = "('" + stockstr + "')"  # for single tuple
        else:
            print('no sender')
        q_clause: str = '' if not stocklist else ' WHERE symbol IN ' + stockliststr  # prevent empty LineEdit
        q: str = 'SELECT * FROM ' + tablename + q_clause
        print(q)
        df: DataFrame = pd.read_sql(sql=q, con=postgres_engine)
        model: DataFrameModel = DataFrameModel(df)
        proxy: MySortFilterProxyModel = MySortFilterProxyModel(self)
        proxy.setSourceModel(model)
        self.pandas_tableview.setModel(proxy)

        grid: QGridLayout = QGridLayout()   # If the Grid was created in the view, it will get deleted
        checkboxes: List[QCheckBox] = [QCheckBox(x) for x in df.columns]
        for count, checkbox in enumerate(checkboxes):
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(partial(self.display_column, index=count))
            le1: QLineEdit = QLineEdit()
            le2: QLineEdit = QLineEdit()
            le1.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp), col))
            le2.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString), col))

            grid.addWidget(checkbox, count, 0)
            grid.addWidget(le1, count, 1)
            grid.addWidget(le2, count, 2)

        QWidget().setLayout(self.dockwin.layout()) # get rid of the default layout
        self.dockwin.setLayout(grid)

    def display_column(self, state: int, index: int) -> None:  # state: checked 2 ; unchecked 0
        if state == Qt.Checked:
            self.pandas_tableview.setColumnHidden(index, False)
        else:
            self.pandas_tableview.setColumnHidden(index, True)


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    w: FutBrowserDialog = FutBrowserDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
