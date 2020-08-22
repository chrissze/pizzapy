
import sys

from shared_model.st_data_model import stock_list_dict

sys.path.append('..')

from PySide2.QtCore import QCoreApplication, QObject , QSortFilterProxyModel ,Qt
from PySide2.QtGui import QCloseEvent, QIcon
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox,  QComboBox, QDockWidget, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMenu, QMenuBar,
                               QMessageBox, QProgressBar, QPushButton,
                               QTableView, QTextBrowser, QToolBar,QVBoxLayout, QWidget)





class GuruBrowserWin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Core Browser')
        self.setGeometry(50, 50, 800, 800)

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

        self.statusBar().showMessage('Ready')

        # create_central_widget
        self.central: QWidget = QWidget()
        self.setCentralWidget(self.central)

        self.combo: QComboBox = QComboBox()
        self.combo.addItems(stock_list_dict.keys())
        self.b_list_guru = QPushButton('Load G-core DB')
        self.b_list_guru.setAccessibleName('b_list_guru')
        self.b_list_zacks = QPushButton('Load Z-core DB')
        self.b_list_zacks.setAccessibleName('b_list_zacks')
        self.b_list_option = QPushButton('Load Option DB')
        self.b_list_option.setAccessibleName('b_list_option')

        self.lb_le: QLabel = QLabel('Stocks (divided by space):')
        self.le: QLineEdit = QLineEdit()
        self.b_le_guru: QPushButton = QPushButton('Load G-core')
        self.b_le_guru.setAccessibleName('b_le_guru')
        self.b_le_zacks: QPushButton = QPushButton('Load Z-core')
        self.b_le_zacks.setAccessibleName('b_le_zacks')
        self.b_le_option: QPushButton = QPushButton('Load Option')
        self.b_le_option.setAccessibleName('b_le_option')

        self.pandasTv: QTableView = QTableView(self)
        self.pandasTv.setSortingEnabled(True)
        self.pandasTv.setAlternatingRowColors(True)

        self.initui()

    def initui(self) -> None:
        mainbox: QVBoxLayout = QVBoxLayout(self.central)
        hbox1: QHBoxLayout = QHBoxLayout()
        hbox2: QHBoxLayout = QHBoxLayout()
        hbox3: QHBoxLayout = QHBoxLayout()
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)

        hbox1.addWidget(self.combo)
        hbox1.addWidget(self.b_list_guru)
        hbox1.addWidget(self.b_list_zacks)
        hbox1.addWidget(self.b_list_option)

        hbox2.addWidget(self.lb_le)
        hbox2.addWidget(self.le)
        hbox2.addWidget(self.b_le_guru)
        hbox2.addWidget(self.b_le_zacks)
        hbox2.addWidget(self.b_le_option)

        hbox3.addWidget(self.pandasTv)

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
            self.dockwin.layout().itemAtPosition(4,0).widget().setChecked(True)


    def show_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i, 0).widget().setChecked(True)
                QCoreApplication.processEvents()

def start() -> None:
    app: QApplication = QApplication(sys.argv)
    w: GuruBrowserWin = GuruBrowserWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()



