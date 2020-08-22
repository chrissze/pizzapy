
# http://www.dayofthenewdan.com/2013/02/09/Qt_QSortFilterProxyModel.html

import sys
sys.path.append('..')

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime,
                           QObject , QRegExp ,QSortFilterProxyModel ,Qt, QTime )
from PySide2.QtGui import QCloseEvent, QIcon, QStandardItemModel
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox,  QComboBox, QDockWidget, QFileDialog,
                               QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QMessageBox, QProgressBar, QPushButton,
                               QTableView, QTextBrowser, QTreeView, QVBoxLayout, QWidget)



class CustomSortFilterProxyModel(QSortFilterProxyModel):

    def __init__(self):
        super().__init__()
        self.filterString = ''
        self.filterFunctions = {}

    def setFilterString(self, text):
        self.filterString = text.lower()
        self.invalidateFilter()

    def addFilterFunction(self, name, new_func):

        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def removeFilterFunction(self, name):

        if name in self.filterFunctions.keys():
            del self.filterFunctions[name]
            self.invalidateFilter()

    def filterAcceptsRow(self, row_num, parent):
        model = self.sourceModel()
        tests = [func(model.row(row_num), self.filterString)
                 for func in self.filterFunctions.values()]
        return False not in tests
