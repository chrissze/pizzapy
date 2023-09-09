"""

Custom Sort Filter Example:
https://doc.qt.io/qtforpython-6/overviews/qtwidgets-itemviews-customsortfiltermodel-example.html


"""
# STANDARD LIBS
import sys;sys.path.append('..')
from typing import Any, Dict, List, Set, Union

# THIRD PARTY LIBS
import pandas as pd
from PySide6.QtCore import (Qt, QModelIndex, QRegularExpression ,QSortFilterProxyModel)

# CUSTOM LIBS
from batterypy.string.read import is_floatable, readf, float0



class MySortFilterProxyModel(QSortFilterProxyModel):
    """
    This is for Pyside6
    """
    def __init__(self) -> None:
        super().__init__()
        self.filters_dict: Dict[Union[int, str], QRegularExpression] = {}


    def setFilterByColumn(self, regex: QRegularExpression, column: int) -> None:
        """
            I need to figure out why I have to convert column key to a key when the regex is invalid.

            Since there are TWO lineedits in the dock for a single column filter, floor_lineedit and ceiling_lineedit, I deliberately add a '+' sign before ceiling_lineedit text to make its regular expression text invalid.

            So for each column, there will be TWO filters in the filters_dict, if I use column int as the key for ceiling_lineedit filter, then this second filter will overwrite the first filter of floor_lineedit, as key is unique in python dictionaries. So I have to convert the column key to str to avoid overwrite the first floor regular expression. 

            Due to the str type of ceiling filter key, so I have to convert the key back to int in filterAcceptsRow else-clause.

            In PySide2 older version, I deliberately made the regular expression of the ceiling_lineedit (le2) into another another type to distinguish it without adding the '+' sign, and test the regex type in setFilterByColumn by checking equality of QRegExp.RegExp enum: 
                le1.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp), col))
                
                le2.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString), col))

        """
        if regex.isValid():
            self.filters_dict[column] = regex  # use int as dictionary key
        else:
            self.filters_dict[str(column)] = regex # use str as dictionary key
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        I use two lineedits to input lower limits and upper limits to filter QTableView results. 
        In order to distinguish if it is a lower limit or upper limit, I add a '+' string to the upper limit number to make it an invalid regular expression. So it will fall to the else clause when I test regex.isValid().

        In seFilterByColumn() method, I set the column key into a string when the regex is invalid, so I need to use int(key) to convert the key back to an int in the else clause in the for loop below. 

        'key, regex' is the key value pairs in self.filters_dict dictionary, that defined earlier.
        
        True means SHOWING

        when the regex_text or cell_text is not floatable, the filter will change to string comparison.
        regex_text == cell_text is for symbol string comparison, if I want to get rid of of a particular symbol, just input the symbol in the lineedit
        """
        for key, regex in self.filters_dict.items():

            regex_text: str = regex.pattern().upper()  # convert regex_text to upper for symbol mapping
            if regex.isValid():
                # self is the ProxyModel instance
                model_index: QModelIndex = self.sourceModel().index(source_row, key, source_parent) 
                cell_text: str = self.sourceModel().data(model_index)

                if model_index.isValid():
                    result: bool = float(regex_text) > float(cell_text) if is_floatable(cell_text) \
                        and is_floatable(regex_text) else regex_text == cell_text
                        # above line end need to be False, so lineedit text deletion will restore rows.
                    if result:
                        return False

            else:
                # else clause runs here because regex is invalid
                model_index: QModelIndex = self.sourceModel().index(source_row, int(key), source_parent)
                cell_text: str = self.sourceModel().data(model_index)

                if model_index.isValid():
                    result: bool = readf(regex_text[1:]) < float(cell_text) if is_floatable(cell_text) and is_floatable(regex_text[1:]) else regex_text[1:] == cell_text
                    if result:
                        return False
                    

        return True   # The row is shown by default value True.

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        leftstr: str = left.data()
        rightstr: str = right.data()
        leftdat: Union[str, float] = leftstr if not is_floatable(leftstr) else float(leftstr)
        rightdat: Union[str, float] = rightstr if not is_floatable(rightstr) else float(rightstr)
        return leftdat < rightdat


if __name__ == '__main__':
    x = MySortFilterProxyModel()
    print('done')