

"""
QRegularExpression patters are enums, Qt designs use  '|' (bitwise OR) operator to combine them.

Ref:
https://doc.qt.io/qtforpython-6/PySide6/QtCore/QRegularExpression.html#PySide6.QtCore.PySide6.QtCore.QRegularExpression.patternOptions



"""
# STANDARD LIBS

from datetime import date
from typing import List, Tuple


# THIRD PARTY LIBS
import pandas

from PySide6.QtCore import Qt, QThread, QCoreApplication, QDateTime ,QRegularExpression ,QSortFilterProxyModel



def make_date_ranges(FROM: date, TO: date, years: int) -> List[Tuple[date, date]]:    
    """
    This function returns a list of tuples. 'years' parameter is the maximum time length of each tuple.
    'years' parameter can be 1 or more. 

        FROM = date(2019, 7, 1)
        TO = date(2023, 9, 30)
        xs = make_date_ranges(FROM, TO, 2)

        # xs will be [(datetime.date(2019, 7, 1), datetime.date(2020, 12, 31)), (datetime.date(2021, 1, 1), datetime.date(2022, 12, 31)), (datetime.date(2023, 1, 1), datetime.date(2023, 9, 30))]
    """
    if years < 1 or TO < FROM:
        return []

    ranges = []
    range_start = FROM
    range_end = date(FROM.year + (years - 1), 12, 31)

    while range_end < TO:
        date_tuple = (range_start, range_end)
        ranges.append(date_tuple)
        range_start = date(range_end.year + 1, 1, 1)
        range_end = date(range_end.year + years, 12, 31)
    else:
        date_tuple = (range_start, TO)
        ranges.append(date_tuple)

    return ranges


# Create a sample DataFrame

def test() -> None:
    FROM = date(2019, 7, 1)
    TO = date(2023, 9, 30)
    x = make_date_ranges(FROM, TO, 2)
    print(x)

if __name__ == '__main__':
    test()
    