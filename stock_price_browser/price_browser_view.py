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
        self.from_calendar_label = QLabel('')
        self.from_reset_button = QPushButton('Reset Calendar 1')
        self.from_reset_button.setAccessibleName('from_reset_button')
        self.to_calendar_label = QLabel('')
        self.to_reset_button = QPushButton('Reset Calendar 2')
        self.to_reset_button.setAccessibleName('to_reset_button')

        self.from_calendar = QCalendarWidget()
        self.from_calendar.setAccessibleName('from_calendar')  # same name as variable
        self.to_calendar = QCalendarWidget()
        self.to_calendar.setAccessibleName('to_calendar')

        self.stock_list_combobox = QComboBox()
        self.stock_list_combobox.addItems(stock_list_dict.keys())
        self.b_list_price = QPushButton('Load Price DB')
        self.b_list_price.setAccessibleName('b_list_price')
        self.b_list_2 = QPushButton('Load 2 DB')
        self.b_list_2.setAccessibleName('b_list_2')
        self.b_list_option = QPushButton('Load Option DB')
        self.b_list_option.setAccessibleName('b_list_option')

        self.symbols_label = QLabel('Stocks (divided by space):')
        self.symbols_lineedit = QLineEdit()
        self.b_le_price = QPushButton('Le Price')
        self.b_le_price.setAccessibleName('b_le_price')
        self.b_le_2 = QPushButton('Le 2')
        self.b_le_2.setAccessibleName('b_le_2')
        self.b_le_option = QPushButton('Le Option')
        self.b_le_option.setAccessibleName('b_le_option')

        self.pandas_tableview = QTableView(self)
        self.pandas_tableview.setSortingEnabled(True)
        self.pandas_tableview.setAlternatingRowColors(True)


        mainbox = QVBoxLayout(self.central)
        calendar_grid = QGridLayout()
        update_grid = QGridLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()
        hbox3 = QHBoxLayout()
        mainbox.addLayout(calendar_grid)
        mainbox.addLayout(update_grid)
        mainbox.addLayout(hbox1)
        mainbox.addLayout(hbox2)
        mainbox.addLayout(hbox3)

        # grid (widget, row, column, height, width)
        calendar_grid.addWidget(self.from_calendar_label,  0, 0)
        calendar_grid.addWidget(self.from_reset_button, 0, 1)
        calendar_grid.addWidget(self.to_calendar_label,  0, 2)
        calendar_grid.addWidget(self.to_reset_button, 0, 3)

        calendar_grid.addWidget(self.from_calendar, 1, 0, 2, 2)
        calendar_grid.addWidget(self.to_calendar, 1, 2, 2, 2)


        hbox1.addWidget(self.stock_list_combobox)
        hbox1.addWidget(self.b_list_price)
        hbox1.addWidget(self.b_list_2)
        hbox1.addWidget(self.b_list_option)

        hbox2.addWidget(self.symbols_label)
        hbox2.addWidget(self.symbols_lineedit)
        hbox2.addWidget(self.b_le_price)
        hbox2.addWidget(self.b_le_2)
        hbox2.addWidget(self.b_le_option)

        hbox3.addWidget(self.pandas_tableview)

        self.from_reset_button.clicked.connect(self.calendar_reset)
        self.to_reset_button.clicked.connect(self.calendar_reset)
        self.from_reset_button.click()
        self.to_reset_button.click()

        self.from_calendar.clicked[QDate].connect(self.calendar_show_date)
        self.to_calendar.clicked[QDate].connect(self.calendar_show_date)

        self.from_calendar.currentPageChanged.connect(self.from_calendar.repaint)
        self.to_calendar.currentPageChanged.connect(self.to_calendar.repaint)


        self.b_le_2.clicked.connect(self.calendar_get_dates)

    def calendar_get_dates(self) -> Tuple[date, date]:
        date1: date = self.from_calendar.selectedDate().toPython()
        date2: date = self.to_calendar.selectedDate().toPython()
        return date1, date2

    #
    # def calendar_refresh(self, year: int, month: int) -> None:
    #     sender: str = self.sender().accessibleName()
    #     qdate: QDate = QDate(year, month, 1)
    #     if sender == 'from_calendar':
    #         self.from_calendar.setSelectedDate(qdate)
    #         self.from_calendar.updateCells()
    #         self.from_calendar_label.setText(qdate.toString())
    #
    #     elif sender == 'to_calendar':
    #         self.to_calendar.setSelectedDate(qdate)
    #         self.to_calendar.updateCells()
    #         self.to_calendar_label.setText(qdate.toString())
    #     QApplication.processEvents()


    def calendar_reset(self) -> None:
        sender: str = self.sender().accessibleName()
        today_: date = date.today()
        qtoday: QDate = QDate.fromString(str(today_), 'yyyy-MM-dd')
        qtodaystr: str = qtoday.toString()
        print('type:', type(qtodaystr))
        if sender == 'from_reset_button':
            print('if')
            self.from_calendar.setSelectedDate(qtoday)
            self.from_calendar.updateCells()
            self.from_calendar_label.setText(qtodaystr)
            self.from_calendar_label.repaint()

        elif sender == 'to_reset_button':
            print('elif')
            self.to_calendar.setSelectedDate(qtoday)
            self.to_calendar.updateCells()
            self.to_calendar_label.setText(qtodaystr)
            self.to_calendar_label.repaint()
        else:
            print('no sender')
        QApplication.processEvents()


    def calendar_show_date(self, qdate: QDate) -> None:
        sender: str = self.sender().accessibleName()
        if sender == 'from_calendar':
            self.from_calendar_label.setText(qdate.toString())
            self.from_calendar_label.repaint()
            self.from_calendar.updateCells()
        elif sender == 'to_calendar':
            self.to_calendar_label.setText(qdate.toString())
            self.to_calendar_label.repaint()
            self.to_calendar.updateCells()
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
        self.pandas_tableview.setModel(None)
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






