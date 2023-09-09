

"""
QRegularExpression patters are enums, Qt designs use  '|' (bitwise OR) operator to combine them.

Ref:
https://doc.qt.io/qtforpython-6/PySide6/QtCore/QRegularExpression.html#PySide6.QtCore.PySide6.QtCore.QRegularExpression.patternOptions



"""
# STANDARD LIBS


# THIRD PARTY LIBS

from PySide6.QtCore import Qt, QThread, QCoreApplication, QDateTime ,QRegularExpression ,QSortFilterProxyModel




myopt = QRegularExpression.CaseInsensitiveOption | QRegularExpression.MultilineOption

r1 = QRegularExpression('123', QRegularExpression.CaseInsensitiveOption)
r2 = QRegularExpression('123', QRegularExpression.MultilineOption)
r3 = QRegularExpression('123', myopt )

case_insensitive_enum = QRegularExpression.CaseInsensitiveOption.value
verbose_case_insensitive_enum = QRegularExpression.PatternOption.CaseInsensitiveOption.value

enum1 = r1.patternOptions().value        # 1
enum2 = r2.patternOptions().value        # 4
enum3 = r3.patternOptions().value        # 5

def test_enum() -> None:
    print(enum1)
    print(enum2)
    print(enum3)


def test_pattern_options() -> None:
    print(r1.patternOptions())
    print(r2.patternOptions())
    print(r3.patternOptions())


def test_equality() -> None:
    if  r3.patternOptions() == QRegularExpression.MultilineOption:
        print('they are equal')
    else:
        print('they are NOT equal')


if __name__ == '__main__':
    test_enum()
    test_pattern_options()
    test_equality()

    