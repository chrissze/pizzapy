"""
AIM OF THIS MODULE:
    To make CoreBrowserView class for core_browser_controller.py to inherit. All other classes are helpers of CoreBrowserView class.

This module in the View of Model-View-Controller. It sets the GUI layout of Core Browser Controller.    

USED BY: core_browser_controller.py

"""
# STANDARD LIBS



# THIRD PARTY LIBS
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (QApplication, QComboBox, QDockWidget,
                               QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar,
                               QPushButton,
                               QScrollArea,
                               QTableView, QToolBar,QVBoxLayout, QWidget)


# PROGRAM MODULES
from pizzapy.database_update.stock_list_model import stock_list_dict
from pizzapy.database_update.postgres_command_model import table_list_dict




class SetupWindow:
    """
    USED BY: CoreBrowserView

    """ 
    def __init__(ego, self) -> None:
        self.setWindowTitle('Core Browser')
        self.resize(1000, 800)
        self.central: QWidget = QWidget()  
        self.setCentralWidget(self.central)
        self.mainbox: QVBoxLayout = QVBoxLayout(self.central) 
        self.statusbar = self.statusBar()  
        self.statusbar.showMessage('Ready')



class TableRow:
    """
    USED BY: CoreBrowserView
    
    """
    def __init__(ego, self):
        self.pandas_tableview: QTableView = QTableView(self)
        self.pandas_tableview.setSortingEnabled(True)
        self.pandas_tableview.setAlternatingRowColors(True)
        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self.pandas_tableview)
        self.mainbox.addLayout(hbox)




class TableListRow:
    """
    USED BY: CoreBrowserView
    """
    def __init__(ego, self) -> None:
        self.table_list_combobox = QComboBox()
        self.table_list_combobox.addItems(table_list_dict.keys())
        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())
        self.load_list_button = QPushButton('Load List')
        
        hbox = QHBoxLayout()
        hbox.addWidget(self.table_list_combobox)
        hbox.addWidget(self.stock_list_combobox)
        hbox.addWidget(self.load_list_button)
        self.mainbox.addLayout(hbox)

        

class SymbolsRow:
    """
    USED BY: CoreBrowserView
    """
    def __init__(ego, self):
        self.symbols_label: QLabel = QLabel(f'SYMBOLS: ')
        self.symbols_lineedit: QLineEdit = QLineEdit()
        self.load_symbols_button: QPushButton = QPushButton('Load SYMBOLS')
        self.load_symbols_button.setAccessibleName('load_symbols_button')

        hbox: QHBoxLayout = QHBoxLayout()
        hbox.addWidget(self.symbols_label)
        hbox.addWidget(self.symbols_lineedit)
        hbox.addWidget(self.load_symbols_button)
        self.mainbox.addLayout(hbox)





class MakeActions:
    """
    USED BY: CoreBrowserView
    """
    def __init__(ego, self):
        self.quit_action: QAction = QAction('&Quit', self)
        self.quit_action.setStatusTip('Leave the app')
        self.quit_action.setShortcut('Ctrl+X')

        self.clear_action: QAction = QAction('&Clear', self)
        self.clear_action.setStatusTip('Clear Table and Column Dock Cmd+0')
        self.clear_action.setShortcut('Ctrl+0')

        self.hide_columns_action: QAction = QAction('&HideColumns', self)
        self.hide_columns_action.setStatusTip('Hide most Columns')

        self.show_columns_action: QAction = QAction('&ShowColumns', self)
        self.show_columns_action.setStatusTip('Show most Columns')



class MakeMenuBar:
    """
    USED BY: CoreBrowserView
    """
    def __init__(ego, self):
        menubar: QMenuBar = self.menuBar()
        menubar.setNativeMenuBar(False)  # For Mac
        filemenu: QMenu = menubar.addMenu('&File')
        filemenu.addAction(self.show_columns_action)
        filemenu.addAction(self.hide_columns_action)
        filemenu.addAction(self.clear_action)
        filemenu.addAction(self.quit_action)



class MakeToolBar:
    """
    USED BY: CoreBrowserView
    """
    def __init__(ego, self):
        toolbar: QToolBar = self.addToolBar('ToolBar1')
        toolbar.addAction(self.show_columns_action)
        toolbar.addAction(self.hide_columns_action)
        toolbar.addAction(self.clear_action)
        toolbar.addAction(self.quit_action)
        


class MakeDock:
    """
    USED BY: CoreBrowserView

    CoreBrowserView (self object) > self.dock > self.scroll > self.dockwin (QWidget) > 

    self.dock's resize method does not work, so I have to use setFixedWidth or setFixedSize.

    Here are the codes that does not have a vertical scroll bar:
        self.dock: QDockWidget = QDockWidget('Columns             LowerLimit    UpperLimit', self)
        self.dock.setFixedWidth(300) 
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockwin: QWidget = QWidget(self)
        self.dock.setWidget(self.dockwin)

    """
    def __init__(ego, self):
        self.dock: QDockWidget = QDockWidget('Columns             LowerLimit    UpperLimit', self)
        self.dock.setFixedWidth(300) 
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.scroll: QScrollArea = QScrollArea()
        self.dockwin: QWidget = QWidget(self)

        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)

        self.dock.setWidget(self.scroll)
        self.scroll.setWidget(self.dockwin)



class CoreBrowserView(QMainWindow):
    """
    DEPENDS ON: SetupWindow, MakeActions, MakeMenuBar, MakeToolBar, MakeDock, TableRow, TableListRow, SymbolsRow
    IMPORTS: QMainWindow
    USED BY: core_browser_controller.py, main()
    """
    def __init__(self) -> None:
        super().__init__() # initialize base class QMainWindow
        SetupWindow(self)
        MakeActions(self)
        MakeMenuBar(self)  # MakeMenuBar must be placed after MakeActions
        MakeToolBar(self)  # MakeToolBar must be placed after MakeActions   
        MakeDock(self)

        TableRow(self)     # Rows must be placed after mainbox creation in SetupWindow
        TableListRow(self)  
        SymbolsRow(self)



def main() -> None:
    app: QApplication = QApplication(sys.argv)
    win: CoreBrowserView = CoreBrowserView()
    win.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()



