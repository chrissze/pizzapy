import sys;

from shared_model.st_data_model import stock_list_dict

sys.path.append('..')


from datetime import date
from PySide2.QtCore import QDate
from PySide2.QtGui import QCloseEvent
from PySide2.QtWidgets import (QApplication, QCalendarWidget, QComboBox, QGridLayout,
                               QHBoxLayout, QLabel, QLineEdit, QMessageBox,
                               QProgressBar, QPushButton,
                               QTextBrowser, QVBoxLayout, QWidget)


from typing import Tuple


class DailyStockWin(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle('Daily Stock Update')
        self.setGeometry(0, 0, 900, 900)


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
        self.le_start = QLineEdit()
        self.b_prices = QPushButton('Update Y! Prices')
        self.b_prices.setAccessibleName('b_prices')
        self.b_techs = QPushButton('Update Technicals')
        self.b_techs.setAccessibleName('b_techs')

        self.le = QLineEdit()
        self.lb_le = QLabel('Separate symbols by space')
        self.b_price1s = QPushButton('Update Y! 1s')
        self.b_price1s.setAccessibleName('b_price1s')
        self.b_tech1s = QPushButton('Update Technical 1s')
        self.b_tech1s.setAccessibleName('b_tech1s')

        self.browser = QTextBrowser()
        self.browser.setMaximumHeight(400)

        self.pbar = QProgressBar()
        self.b_clear = QPushButton('Clear')
        self.b_quit = QPushButton('Quit')


        mainbox = QVBoxLayout(self)
        grid1 = QGridLayout()
        grid2 = QGridLayout()
        hbox1 = QHBoxLayout()

        mainbox.addLayout(grid1)
        mainbox.addLayout(grid2)
        mainbox.addWidget(self.browser)
        mainbox.addLayout(hbox1)

        # grid (widget, row, column, height, width)

        grid1.addWidget(self.lb_cal1,  0, 0)
        grid1.addWidget(self.b_reset1, 0, 1)
        grid1.addWidget(self.lb_cal2,  0, 2)
        grid1.addWidget(self.b_reset2, 0, 3)

        grid1.addWidget(self.cal1, 1, 0, 2, 2)
        grid1.addWidget(self.cal2, 1, 2, 2, 2)

        grid2.addWidget(self.combo,    0, 0)
        grid2.addWidget(self.le_start,    0, 1)
        grid2.addWidget(self.b_prices, 0, 2)
        grid2.addWidget(self.b_techs,  0, 3)

        grid2.addWidget(self.le,       1, 0)
        grid2.addWidget(self.lb_le,    1, 1)
        grid2.addWidget(self.b_price1s,1, 2)
        grid2.addWidget(self.b_tech1s, 1, 3)

        hbox1.addWidget(self.pbar)
        hbox1.addWidget(self.b_clear)
        hbox1.addWidget(self.b_quit)

        self.b_reset1.clicked.connect(self.calendar_reset)
        self.b_reset2.clicked.connect(self.calendar_reset)
        self.b_reset1.click()
        self.b_reset2.click()

        self.cal1.clicked[QDate].connect(self.calendar_show_date)
        self.cal2.clicked[QDate].connect(self.calendar_show_date)

        self.cal1.currentPageChanged.connect(self.cal1.repaint)
        self.cal2.currentPageChanged.connect(self.cal2.repaint)

        self.b_clear.clicked.connect(self.browser.clear)
        self.b_quit.clicked.connect(self.close)

    def closeEvent(self, event: QCloseEvent) -> None:
        reply: QMessageBox.StandardButton = QMessageBox.question(
            self, 'Confirmation', 'Quit Now?', QMessageBox.Yes | QMessageBox.Cancel)
        print(type(reply))
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()



    def calendar_reset(self) -> None:
        sender: str = self.sender().accessibleName()
        today_: date = date.today()
        qtoday: QDate = QDate.fromString(str(today_), 'yyyy-MM-dd')
        qtodaystr: str = qtoday.toString()
        if sender == 'b_reset1':
            self.cal1.setSelectedDate(qtoday)
            self.cal1.updateCells()
            self.lb_cal1.setText(qtodaystr)
            self.lb_cal1.repaint()
        elif sender == 'b_reset2':
            self.cal2.setSelectedDate(qtoday)
            self.cal2.updateCells()
            self.lb_cal2.setText(qtodaystr)
            self.lb_cal2.repaint()
        else:
            print('no sender')
        QApplication.processEvents()

    def calendar_show_date(self, qdate: QDate) -> None:
        sender: str = self.sender().accessibleName()
        datestr: str = qdate.toString()
        if sender == 'cal1':
            self.lb_cal1.setText(datestr)
            self.lb_cal1.repaint()
            self.cal1.updateCells()
            self.cal1.repaint()
        elif sender == 'cal2':
            self.lb_cal2.setText(datestr)
            self.lb_cal2.repaint()
            self.cal2.updateCells()
            self.cal2.repaint()
        else:
            print('no sender')
        QApplication.processEvents()

    # def calendar_refresh(self, year: int, month: int) -> None:
    #     sender: str = self.sender().accessibleName()
    #     qdate: QDate = QDate(year, month, 1)
    #     qdatestr: str = qdate.toString()
    #     if sender == 'cal1':
    #         self.cal1.setSelectedDate(qdate)
    #         self.cal1.updateCells()
    #         self.lb_cal1.setText(qdatestr)
    #     elif sender == 'cal2':
    #         self.cal2.setSelectedDate(qdate)
    #         self.cal2.updateCells()
    #         self.lb_cal2.setText(qdatestr)


    def calendar_get_dates(self) -> Tuple[date, date]:
        date1: date = self.cal1.selectedDate().toPython()
        date2: date = self.cal2.selectedDate().toPython()
        return date1, date2


def main() -> None:
    app = QApplication(sys.argv)
    w = DailyStockWin()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()