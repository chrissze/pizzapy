

"""
QRegularExpression patters are enums, Qt designs use  '|' (bitwise OR) operator to combine them.

Ref:
https://doc.qt.io/qtforpython-6/PySide6/QtCore/QRegularExpression.html#PySide6.QtCore.PySide6.QtCore.QRegularExpression.patternOptions



"""
# STANDARD LIBS


# THIRD PARTY LIBS
import pandas

from PySide6.QtCore import Qt, QThread, QCoreApplication, QDateTime ,QRegularExpression ,QSortFilterProxyModel



def format_int_with_commas(x):
    """
    Formats an integer with commas as thousand separators.
    """
    return f"{x:,}"


# Create a sample DataFrame

def test() -> None:
    df = pandas.DataFrame({
        'A': [1000, 2000000, 300000000],
        'B': [4000, 5000000, 600000000],
        'C': [7000, 8000000, 900000000]
    })
    df = df.applymap(format_int_with_commas)

    print(df)

if __name__ == '__main__':
    test()
    