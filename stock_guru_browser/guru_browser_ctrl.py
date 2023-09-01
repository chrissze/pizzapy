import sys; sys.path.append('..')

from dimsumpy.qt5.dataframemodel import DataFrameModel
from functools import partial
import pandas
from pandas.core.frame import DataFrame
from PySide2.QtWidgets import QApplication, QCheckBox ,QGridLayout, QLineEdit ,QWidget
from PySide2.QtCore import Qt, QRegExp

from shared_model.sql_model import cnx
from shared_model.st_data_model import MySortFilterProxyModel, stock_list_dict
from stock_core_browser.core_browser_view import GuruBrowserWin
from typing import Any, List, Tuple


class GuruBrowserDialog(GuruBrowserWin):
    def __init__(self) -> None:
        super().__init__()
        self.b_list_guru.clicked.connect(self.load_table)
        self.b_le_guru.clicked.connect(self.load_table)

        self.b_list_zacks.clicked.connect(self.load_table)
        self.b_le_zacks.clicked.connect(self.load_table)
        self.b_list_option.clicked.connect(self.load_table)
        self.b_le_option.clicked.connect(self.load_table)

    def load_table(self) -> None:
        self.clear()
        sender: str = self.sender().accessibleName()
        if sender == 'b_list_guru':
            tablename: str = 'usstock_g'
            stockstr: str = self.combo.currentText()
            stocklist: List[str] = stock_list_dict.get(stockstr)
            stockliststr: str = str(tuple(stocklist))
        elif sender == 'b_le_guru':
            tablename: str = 'usstock_g'
            stockstr: str = self.le.text().upper()
            stocklist: List[str] = stockstr.split()
            stockliststr: str = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple

        elif sender == 'b_list_zacks':
            tablename: str = 'usstock_z'
            stockstr: str = self.combo.currentText()
            stocklist: List[str] = stock_list_dict.get(stockstr)
            stockliststr: str = str(tuple(stocklist))
        elif sender == 'b_le_zacks':
            tablename: str = 'usstock_z'
            stockstr: str = self.le.text().upper()
            stocklist: List[str] = stockstr.split()
            stockliststr: str = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple

        elif sender == 'b_list_option':
            tablename: str = 'usstock_option'
            stockstr: str = self.combo.currentText()
            stocklist: List[str] = stock_list_dict.get(stockstr)
            stockliststr: str = str(tuple(stocklist))
        elif sender == 'b_le_option':
            tablename: str = 'usstock_option'
            stockstr: str = self.le.text().upper()
            stocklist: List[str] = stockstr.split()
            stockliststr: str = str(stocklist).replace('[', '(').replace(']', ')')  # for single tuple

        q_clause: str = '' if not stocklist else ' WHERE symbol IN ' + stockliststr  # prevent empty LineEdit
        q: str = 'SELECT * FROM ' + tablename + q_clause
        print(q)
        df: DataFrame = pandas.read_sql(sql=q, con=cnx)
        model: DataFrameModel = DataFrameModel(df)
        proxy: MySortFilterProxyModel = MySortFilterProxyModel(self)
        proxy.setSourceModel(model)
        self.pandasTv.setModel(proxy)

        grid: QGridLayout = QGridLayout()   # If the Grid was created in the view, it will get deleted
        checkboxes: List[QCheckBox] = [QCheckBox(x) for x in df.columns]
        for count, checkbox in enumerate(checkboxes):
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(partial(self.display_column, index=count))
            le1: QLineEdit = QLineEdit()
            le2: QLineEdit = QLineEdit()
            le1.textChanged.connect(lambda text, col=count: proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp), col))
            le2.textChanged.connect(lambda text, col=count: proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString), col))

            grid.addWidget(checkbox, count, 0)
            grid.addWidget(le1, count, 1)
            grid.addWidget(le2, count, 2)

        QWidget().setLayout(self.dockwin.layout()) # get rid of the default layout
        self.dockwin.setLayout(grid)

    def display_column(self, state: int, index: int) -> None:
        if state == Qt.Checked:
            self.pandasTv.setColumnHidden(index, False)
        else:
            self.pandasTv.setColumnHidden(index, True)


def main() -> None:
    app: QApplication = QApplication(sys.argv)
    w: GuruBrowserDialog = GuruBrowserDialog()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
