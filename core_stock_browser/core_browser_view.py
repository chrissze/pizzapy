
# STANDARD LIBS
import sys; sys.path.append('..')


# THIRD PARTY LIBS
from PySide6.QtCore import QCoreApplication, QObject , QSortFilterProxyModel ,Qt
from PySide6.QtGui import QAction, QCloseEvent, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox,  QComboBox, QDockWidget, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar,
                               QMessageBox, QProgressBar, QPushButton,
                               QTableView, QTextBrowser, QToolBar,QVBoxLayout, QWidget)

# PROGRAM MODULES
from database_update.stock_list_model import stock_list_dict





class StockListRow:
    def __init__(ego, self) -> None:
        self.combo = QComboBox()
        self.combo.addItems(stock_list_dict.keys())
        self.b_list_guru = QPushButton('Load G-core DB')
        self.b_list_guru.setAccessibleName('b_list_guru')
        self.b_list_zacks = QPushButton('Load Z-core DB')
        self.b_list_zacks.setAccessibleName('b_list_zacks')
        self.b_list_option = QPushButton('Load Option DB')
        self.b_list_option.setAccessibleName('b_list_option')
        
        self.stock_list_hbox: QHBoxLayout = QHBoxLayout()
        self.mainbox.addLayout(self.stock_list_hbox)
        self.stock_list_hbox.addWidget(self.combo)
        self.stock_list_hbox.addWidget(self.b_list_guru)
        self.stock_list_hbox.addWidget(self.b_list_zacks)
        self.stock_list_hbox.addWidget(self.b_list_option)



class StocksRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StocksRow, 'self' is the instance of the calling class.
        """

        self.lb_le: QLabel = QLabel('Stocks (divided by space):')
        self.le: QLineEdit = QLineEdit()
        self.b_le_guru: QPushButton = QPushButton('Load G-core')
        self.b_le_guru.setAccessibleName('b_le_guru')
        self.b_le_zacks: QPushButton = QPushButton('Load Z-core')
        self.b_le_zacks.setAccessibleName('b_le_zacks')
        self.b_le_option: QPushButton = QPushButton('Load Option')
        self.b_le_option.setAccessibleName('b_le_option')

        self.stocks_hbox: QHBoxLayout = QHBoxLayout()
        self.mainbox.addLayout(self.stocks_hbox)
        self.stocks_hbox.addWidget(self.lb_le)
        self.stocks_hbox.addWidget(self.le)
        self.stocks_hbox.addWidget(self.b_le_guru)
        self.stocks_hbox.addWidget(self.b_le_zacks)
        self.stocks_hbox.addWidget(self.b_le_option)




class TableRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        self.pandasTv: QTableView = QTableView(self)
        self.pandasTv.setSortingEnabled(True)
        self.pandasTv.setAlternatingRowColors(True)
        self.table_hbox: QHBoxLayout = QHBoxLayout()
        self.mainbox.addLayout(self.table_hbox)
        self.table_hbox.addWidget(self.pandasTv)



class MakeActions:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        self.quit_action: QAction = QAction('&Quit', self)
        self.quit_action.setStatusTip('Leave the app')
        self.quit_action.triggered.connect(self.close)
        self.quit_action.setShortcut('Ctrl+X')

        self.clear_action: QAction = QAction('&Clear', self)
        self.clear_action.setStatusTip('Clear Table and Column Dock Cmd+0')
        self.clear_action.triggered.connect(self.clear)
        self.clear_action.setShortcut('Ctrl+0')

        self.hide_columns_action: QAction = QAction('&HideColumns', self)
        self.hide_columns_action.setStatusTip('Hide most Columns')
        self.hide_columns_action.triggered.connect(self.hide_columns)

        self.show_columns_action: QAction = QAction('&ShowColumns', self)
        self.show_columns_action.setStatusTip('Show most Columns')
        self.show_columns_action.triggered.connect(self.show_columns)


class MakeMenuBar:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        menubar: QMenuBar = self.menuBar()
        menubar.setNativeMenuBar(False)  # For Mac
        filemenu: QMenu = menubar.addMenu('&File')
        filemenu.addAction(self.show_columns_action)
        filemenu.addAction(self.hide_columns_action)
        filemenu.addAction(self.clear_action)
        filemenu.addAction(self.quit_action)



class MakeToolBar:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        toolbar: QToolBar = self.addToolBar('ToolBar1')
        toolbar.addAction(self.show_columns_action)
        toolbar.addAction(self.hide_columns_action)
        toolbar.addAction(self.clear_action)
        


class MakeDock:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        self.dock: QDockWidget = QDockWidget('Columns      LowerLimit    UpperLimit', self)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockwin: QWidget = QWidget(self)
        self.dock.setWidget(self.dockwin)





class CoreBrowserView(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Core Browser')
        self.setGeometry(50, 50, 800, 800)

        MakeActions(self)
        MakeMenuBar(self)  # MakeMenuBar must be placed after MakeActions
        MakeToolBar(self)  # MakeToolBar must be placed after MakeActions
        MakeDock(self)
        self.statusBar().showMessage('Ready')
        self.initui()

    def initui(self) -> None:
        # create_central_widget, self.central is the parent container of self.mainbox
        self.central: QWidget = QWidget()  
        self.setCentralWidget(self.central)
        self.mainbox: QVBoxLayout = QVBoxLayout(self.central) 
        StockListRow(self)  # Rows must be placed after mainbox creation
        StocksRow(self)
        TableRow(self)


    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clear(self) -> None:
        self.pandasTv.setModel(None)
        QWidget().setLayout(self.dockwin.layout()) # re-assign the existing layout


    def hide_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3  # since there are two columns in grid
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i,0).widget().setChecked(False)
                QCoreApplication.processEvents()  # update the GUI
            #self.dockwin.layout().itemAtPosition(4,0).widget().setChecked(True)


    def show_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i, 0).widget().setChecked(True)
                QCoreApplication.processEvents()




def test_view() -> None:
    app: QApplication = QApplication(sys.argv)
    win: CoreBrowserView = CoreBrowserView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    test_view()



