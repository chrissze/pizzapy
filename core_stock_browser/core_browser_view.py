
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
from database_update.postgres_command_model import table_list_dict




class TableListRow:
    def __init__(ego, self) -> None:
        self.table_list_combobox = QComboBox()
        self.table_list_combobox.addItems(table_list_dict.keys())
        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())
        self.load_list_button = QPushButton('Load List')
        
        self.table_list_hbox = QHBoxLayout()
        self.mainbox.addLayout(self.table_list_hbox)
        self.table_list_hbox.addWidget(self.table_list_combobox)
        self.table_list_hbox.addWidget(self.stock_list_combobox)
        self.table_list_hbox.addWidget(self.load_list_button)


class SymbolsRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class StocksRow, 'self' is the instance of the calling class.
        """

        self.table_name: str = self.table_list_combobox.currentText()
        self.symbols_label: QLabel = QLabel(f'SYMBOLS (divided by space):')
        self.symbols_lineedit: QLineEdit = QLineEdit()
        self.load_symbols_button: QPushButton = QPushButton('Load SYMBOLS')
        self.load_symbols_button.setAccessibleName('load_symbols_button')

        self.stocks_hbox: QHBoxLayout = QHBoxLayout()
        self.mainbox.addLayout(self.stocks_hbox)
        self.stocks_hbox.addWidget(self.symbols_label)
        self.stocks_hbox.addWidget(self.symbols_lineedit)
        self.stocks_hbox.addWidget(self.load_symbols_button)




class TableRow:
    def __init__(ego, self):
        """
            'ego' is the instance of the current class, 'self' is the instance of the calling class.
        """
        self.pandas_tableview: QTableView = QTableView(self)
        self.pandas_tableview.setSortingEnabled(True)
        self.pandas_tableview.setAlternatingRowColors(True)
        self.table_hbox: QHBoxLayout = QHBoxLayout()
        self.mainbox.addLayout(self.table_hbox)
        self.table_hbox.addWidget(self.pandas_tableview)





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
            self.dock is the parent container of self.dockwin
        """
        self.dock: QDockWidget = QDockWidget('Columns      LowerLimit    UpperLimit', self)
        self.dock.setFixedWidth(300) # resize method does not work, alternatively I can use setFixedSize
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockwin: QWidget = QWidget(self)
        self.dock.setWidget(self.dockwin)





class CoreBrowserView(QMainWindow):
    """
    super().__init__() is called because this class has a base class QMainWindow.
    
    """
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Core Browser')
        self.resize(1000, 800)

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
        TableRow(self)
        TableListRow(self)  # Rows must be placed after mainbox creation
        SymbolsRow(self)

    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clear(self) -> None:
        self.pandas_tableview.setModel(None)
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



