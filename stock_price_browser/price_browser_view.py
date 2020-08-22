import sys;

from shared_model.st_data_model import stock_list_dict

sys.path.append('..')

from datetime import date

from PySide2.QtCore import QCoreApplication, QDate, QObject , QSortFilterProxyModel ,Qt
from PySide2.QtGui import QCloseEvent, QIcon
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox,  QComboBox, QCalendarWidget,
                               QDockWidget, QFileDialog,
                               QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow,
                               QMessageBox, QProgressBar, QPushButton,
                               QTableView, QTextBrowser, QVBoxLayout, QWidget)



from typing import Any, List, Tuple

class StockPriceBrowserWin(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle('Guru Browser')
        self.setGeometry(50, 50, 1000, 1000)

        self.quit_action = QAction('&Quit', self)
        self.quit_action.setShortcut('Ctrl+X')
        self.quit_action.setStatusTip('Leave the app')
        self.quit_action.triggered.connect(self.close)

        self.clear_action = QAction('&Clear', self)
        self.clear_action.setShortcut('Ctrl+0')
        self.clear_action.setStatusTip('Clear Table and Column Dock Cmd+0')
        self.clear_action.triggered.connect(self.clear)


        self.hide_columns_action = QAction('&HideColumns', self)
        self.hide_columns_action.setStatusTip('Hide most Columns')
        self.hide_columns_action.triggered.connect(self.hide_columns)


        self.show_columns_action = QAction('&ShowColumns', self)
        self.show_columns_action.setStatusTip('Show most Columns')
        self.show_columns_action.triggered.connect(self.show_columns)


        self.central = QWidget()
        self.create_central_widget()

        self.initui()

    def initui(self) -> None:
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # For Mac

        filemenu = menubar.addMenu('&File')
        filemenu.addAction(self.clear_action)
        filemenu.addAction(self.show_columns_action)
        filemenu.addAction(self.hide_columns_action)
        filemenu.addAction(self.quit_action)

        toolbar = self.addToolBar('ToolBar1')
        toolbar.addAction(self.clear_action)
        toolbar.addAction(self.show_columns_action)
        toolbar.addAction(self.hide_columns_action)
        toolbar.addAction(self.quit_action)

        self.dock = QDockWidget('Columns      LowerLimit    UpperLimit', self)
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)
        self.dockwin = QWidget(self)
        self.dock.setWidget(self.dockwin)

        self.setCentralWidget(self.central)

        self.statusBar().showMessage('Ready')

    def create_central_widget(self) -> None:
        self.lb_cal1 = QLabel('')
        self.b_reset1 = QPushButton('Reset Calendar 1')
        self.b_reset1.setAccessibleName('b_reset1')
        self.lb_cal2 = QLabel('')
        self.b_reset2 = QPushButton('Reset Calendar 2')
        self.b_reset2.setAccessibleName('b_reset2')

        self.cal1 = QCalendarWidget()
        self.cal1.setAccessibleName('cal1')  # same name as variable
        self.cal2 = QCalendarWidget()
        self.cal2.setAccessibleName('cal2')

        self.combo = QComboBox()
        self.combo.addItems(stock_list_dict.keys())
        self.b_list_price = QPushButton('Load Price DB')
        self.b_list_price.setAccessibleName('b_list_price')
        self.b_list_2 = QPushButton('Load 2 DB')
        self.b_list_2.setAccessibleName('b_list_2')
        self.b_list_option = QPushButton('Load Option DB')
        self.b_list_option.setAccessibleName('b_list_option')

        self.lb_le = QLabel('Stocks (divided by space):')
        self.le = QLineEdit()
        self.b_le_price = QPushButton('Le Price')
        self.b_le_price.setAccessibleName('b_le_price')
        self.b_le_2 = QPushButton('Le 2')
        self.b_le_2.setAccessibleName('b_le_2')
        self.b_le_option = QPushButton('Le Option')
        self.b_le_option.setAccessibleName('b_le_option')

        self.pandasTv = QTableView(self)
        self.pandasTv.setSortingEnabled(True)
        self.pandasTv.setAlternatingRowColors(True)


        mainbox = QVBoxLayout(self.central)
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        mainbox.addLayout(grid1)
        mainbox.addLayout(grid2)
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)

        # grid (widget, row, column, height, width)
        grid1.addWidget(self.lb_cal1,  0, 0)
        grid1.addWidget(self.b_reset1, 0, 1)
        grid1.addWidget(self.lb_cal2,  0, 2)
        grid1.addWidget(self.b_reset2, 0, 3)

        grid1.addWidget(self.cal1, 1, 0, 2, 2)
        grid1.addWidget(self.cal2, 1, 2, 2, 2)


        hbox1.addWidget(self.combo)
        hbox1.addWidget(self.b_list_price)
        hbox1.addWidget(self.b_list_2)
        hbox1.addWidget(self.b_list_option)

        hbox2.addWidget(self.lb_le)
        hbox2.addWidget(self.le)
        hbox2.addWidget(self.b_le_price)
        hbox2.addWidget(self.b_le_2)
        hbox2.addWidget(self.b_le_option)

        hbox3.addWidget(self.pandasTv)

        self.b_reset1.clicked.connect(self.calendar_reset)
        self.b_reset2.clicked.connect(self.calendar_reset)
        self.b_reset1.click()
        self.b_reset2.click()

        self.cal1.clicked[QDate].connect(self.calendar_show_date)
        self.cal2.clicked[QDate].connect(self.calendar_show_date)

        self.cal1.currentPageChanged.connect(self.cal1.repaint)
        self.cal2.currentPageChanged.connect(self.cal2.repaint)


        self.b_le_2.clicked.connect(self.calendar_get_dates)

    def calendar_get_dates(self) -> Tuple[date, date]:
        date1: date = self.cal1.selectedDate().toPython()
        date2: date = self.cal2.selectedDate().toPython()
        return date1, date2

    #
    # def calendar_refresh(self, year: int, month: int) -> None:
    #     sender: str = self.sender().accessibleName()
    #     qdate: QDate = QDate(year, month, 1)
    #     if sender == 'cal1':
    #         self.cal1.setSelectedDate(qdate)
    #         self.cal1.updateCells()
    #         self.lb_cal1.setText(qdate.toString())
    #
    #     elif sender == 'cal2':
    #         self.cal2.setSelectedDate(qdate)
    #         self.cal2.updateCells()
    #         self.lb_cal2.setText(qdate.toString())
    #     QApplication.processEvents()


    def calendar_reset(self) -> None:
        sender: str = self.sender().accessibleName()
        today_: date = date.today()
        qtoday: QDate = QDate.fromString(str(today_), 'yyyy-MM-dd')
        qtodaystr: str = qtoday.toString()
        print('type:', type(qtodaystr))
        if sender == 'b_reset1':
            print('if')
            self.cal1.setSelectedDate(qtoday)
            self.cal1.updateCells()
            self.lb_cal1.setText(qtodaystr)
            self.lb_cal1.repaint()

        elif sender == 'b_reset2':
            print('elif')
            self.cal2.setSelectedDate(qtoday)
            self.cal2.updateCells()
            self.lb_cal2.setText(qtodaystr)
            self.lb_cal2.repaint()
        else:
            print('no sender')
        QApplication.processEvents()


    def calendar_show_date(self, qdate: QDate) -> None:
        sender: str = self.sender().accessibleName()
        if sender == 'cal1':
            self.lb_cal1.setText(qdate.toString())
            self.lb_cal1.repaint()
            self.cal1.updateCells()
        elif sender == 'cal2':
            self.lb_cal2.setText(qdate.toString())
            self.lb_cal2.repaint()
            self.cal2.updateCells()
        else:
            print('no sender')
        QApplication.processEvents()


    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def clear(self) -> None:
        self.pandasTv.setModel(None)
        QWidget().setLayout(self.dockwin.layout()) # re-assign the existing layout
        self.dockwinbox = QVBoxLayout(self.dockwin)

    def hide_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3  # since there are two columns in grid
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i,0).widget().setChecked(False)
                QCoreApplication.processEvents()  # update the GUI
            self.dockwin.layout().itemAtPosition(3,0).widget().setChecked(True)
        else:
            self.setStatusTip('no layout')
            print('no layout')


    def show_columns(self) -> None:
        index: int = 0 if not self.dockwin.layout() else self.dockwin.layout().count() // 3
        if index:
            for i in range(index):
                self.dockwin.layout().itemAtPosition(i, 0).widget().setChecked(True)
                QCoreApplication.processEvents()
        else:
            self.setStatusTip('no layout')
            print('no layout')







def start() -> None:
    app = QApplication(sys.argv)
    w = StockPriceBrowserWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    start()






