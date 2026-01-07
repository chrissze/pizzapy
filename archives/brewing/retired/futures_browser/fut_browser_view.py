

from PySide2.QtCore import QCoreApplication, QObject , QSortFilterProxyModel ,Qt
from PySide2.QtGui import QCloseEvent, QIcon
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox,  QComboBox, QDockWidget, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar,
                               QMessageBox, QProgressBar, QPushButton,
                               QTableView, QTextBrowser, QToolBar, QVBoxLayout, QWidget)

from shared_model.fut_data_model import fut_type_list, getfutcode, getfutures
from typing import List


class FutBrowserWin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Futures Browser')
        self.setGeometry(50, 50, 800, 800)

        self.quit_action: QAction = QAction('&Quit', self)
        self.quit_action.setShortcut('Ctrl+X')
        self.quit_action.setStatusTip('Leave the app')
        self.quit_action.triggered.connect(self.close)

        self.clear_action: QAction = QAction('&Clear', self)
        self.clear_action.setShortcut('Ctrl+0')
        self.clear_action.setStatusTip('Clear Table and Column Dock Cmd+0')
        self.clear_action.triggered.connect(self.clear)

        self.hide_columns_action: QAction = QAction('&HideColumns', self)
        self.hide_columns_action.setStatusTip('Hide most Columns')
        self.hide_columns_action.triggered.connect(self.hide_columns)

        self.show_columns_action: QAction = QAction('&ShowColumns', self)
        self.show_columns_action.setStatusTip('Show most Columns')
        self.show_columns_action.triggered.connect(self.show_columns)

        menubar: QMenuBar = self.menuBar()
        menubar.setNativeMenuBar(False)  # For Mac

        filemenu: QMenu = menubar.addMenu('&File')
        filemenu.addAction(self.clear_action)
        filemenu.addAction(self.show_columns_action)
        filemenu.addAction(self.hide_columns_action)
        filemenu.addAction(self.quit_action)

        toolbar: QToolBar = self.addToolBar('ToolBar1')
        toolbar.addAction(self.clear_action)
        toolbar.addAction(self.show_columns_action)
        toolbar.addAction(self.hide_columns_action)
        toolbar.addAction(self.quit_action)

        self.dock: QDockWidget = QDockWidget('Columns      LowerLimit    UpperLimit', self)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockwin: QWidget = QWidget(self)
        self.dock.setWidget(self.dockwin)

        # Create Central Widget:
        self.central: QWidget = QWidget()
        self.setCentralWidget(self.central)
        self.stock_list_combobox: QComboBox = QComboBox()
        self.stock_list_combobox.addItems(fut_type_list)
        self.stock_list_combobox.activated[str].connect(self.refresh_combo_individual)
        self.stock_list_combobox_individual: QComboBox = QComboBox()
        self.refresh_combo_individual(self.stock_list_combobox.currentText())

        self.b_list_option: QPushButton = QPushButton('Load Option DB')
        self.b_list_option.setAccessibleName('b_list_option')

        self.b_single_option: QPushButton = QPushButton('Load single Option')
        self.b_single_option.setAccessibleName('b_single_option')

        self.pandas_tableview: QTableView = QTableView(self)
        self.pandas_tableview.setSortingEnabled(True)
        self.pandas_tableview.setAlternatingRowColors(True)

        self.statusBar().showMessage('Ready')
        self.initui()

    def initui(self) -> None:
        mainbox: QVBoxLayout = QVBoxLayout(self.central)
        hbox1: QHBoxLayout = QHBoxLayout()
        hbox2: QHBoxLayout = QHBoxLayout()
        hbox3: QHBoxLayout = QHBoxLayout()
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)

        hbox1.addWidget(self.stock_list_combobox)
        hbox1.addWidget(self.b_list_option)
        hbox2.addWidget(self.stock_list_combobox_individual)
        hbox2.addWidget(self.b_single_option)
        hbox3.addWidget(self.pandas_tableview)

    def clear(self) -> None:
        self.pandas_tableview.setModel(None)
        QWidget().setLayout(self.dockwin.layout()) # re-assign the existing layout

    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def hide_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3  # since there are two columns in grid
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i,0).widget().setChecked(False)
                QCoreApplication.processEvents()  # update the GUI
            self.dockwin.layout().itemAtPosition(3,0).widget().setChecked(True)

    def refresh_combo_individual(self, text: str) -> None:
        codes: List[str] = getfutures(text)
        self.stock_list_combobox_individual.clear()
        self.stock_list_combobox_individual.addItems(codes)


    def show_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i, 0).widget().setChecked(True)
                QCoreApplication.processEvents()


def start() -> None:
    app: QApplication = QApplication(sys.argv)
    w: FutBrowserWin = FutBrowserWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()




