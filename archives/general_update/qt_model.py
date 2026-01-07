"""

USED BY: core_browser_controller.py

QSortFilterProxyModel API:
    https://doc.qt.io/qtforpython-6/PySide6/QtCore/QSortFilterProxyModel.html

Custom Sort Filter Example:
    https://doc.qt.io/qtforpython-6/overviews/qtwidgets-itemviews-customsortfiltermodel-example.html


"""
# STANDARD LIBS
import sys;sys.path.append('..')
from typing import Any, Dict, List, Set, Union


# THIRD PARTY LIBS
from PySide6.QtCore import (QModelIndex, QRegularExpression ,QSortFilterProxyModel)


# CUSTOM LIBS
from batterypy.string.read import is_floatable



class MySortFilterProxyModel(QSortFilterProxyModel):
    """
    USED BY: core_browser_controller.py

    filterAcceptsRow() provides filtering capabilities for dock on the left.
    lessThan() provides sorting capability for the TableView
    """
    def __init__(self) -> None:
        super().__init__()
        self.filters_dict: Dict[Union[int, str], QRegularExpression] = {}

    def setFilterByColumn(self, regex: QRegularExpression, column: int) -> None:
        """
        USED BY: core_browser_controller.py

            This setFilterByColumn method is NOT a built-in method, I can use whatever name I like.

            The aim of this method is to fill up self.filters_dict, which is used by filterAcceptsRow() builtin virtual function.

            Since there are TWO lineedits in the dock for a single column filter, floor_lineedit and ceiling_lineedit, I deliberately add CaseInsensitiveOption to floor filter to distinguish it.            

            So for each column, there will be TWO filters in the filters_dict, if I use column int as the key for ceiling_lineedit filter, then this second filter will overwrite the first filter of floor_lineedit, as key is unique in python dictionaries. So I have to convert the column key to str to avoid overwrite the first floor regular expression. 

            Due to the str type of ceiling filter key, so I have to convert the key back to int in filterAcceptsRow else-clause.

            In PySide2 older version, I deliberately made the regular expression of the ceiling_lineedit (le2) into another another type to distinguish it, and test the regex type in setFilterByColumn by checking equality of QRegExp.RegExp enum: 
                le1.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.RegExp), col))
                
                le2.textChanged.connect(lambda text, col=count:proxy.setFilterByColumn(
                QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString), col))

            
            Alternatively,  I can add a '+' sign before ceiling_lineedit text to make its regular expression text invalid and test regex.isValid() in PySide6.
        """
        is_floor_filter: bool = regex.patternOptions() == QRegularExpression.CaseInsensitiveOption
        if is_floor_filter:
            self.filters_dict[column] = regex  # use int as dictionary key
        else:
            self.filters_dict[str(column)] = regex # use str as dictionary key
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        This filterAcceptsRow() method is a built-in virtual function, I override it here, the name cannot be changed.

        This method determines if a particular row in the TableView will be shown. If this method return True, the row will be shown, if this method return False, the row will be hidden.

        I use two lineedits to input lower limits and upper limits to filter QTableView results. 
        In order to distinguish if it is a lower limit or upper limit, I add CaseInsensitveOption to the floor_lineedit regular expression,
         
        In setFilterByColumn() method, I set the column key into a string when the regex is_floor_filter, so I need to use int(key) to convert the key back to an int in the else clause in the for loop below. 

        'key, regex' is the key value pairs in self.filters_dict dictionary, defined in the custom class.
        
        True means SHOWING

        when the regex_text or cell_text is not floatable, the filter will change to string comparison.
        regex_text == cell_text is for symbol string comparison, if I want to get rid of of a particular symbol, just input the symbol in the lineedit

        
        """
        for key, regex in self.filters_dict.items():
            is_floor_filter: bool = regex.patternOptions() == QRegularExpression.CaseInsensitiveOption
            regex_text: str = regex.pattern() #.upper()  # I should not convert the regex_text to upper, otherwise I cannot hide nan values. Since nan values are lowercase.
            
            if is_floor_filter:
                # self is the ProxyModel instance
                model_index: QModelIndex = self.sourceModel().index(source_row, key, source_parent) 
                cell_text: str = self.sourceModel().data(model_index)

                if model_index.isValid():
                    result: bool = float(regex_text) > float(cell_text) if is_floatable(cell_text) \
                        and is_floatable(regex_text) else regex_text == cell_text
                        # above line end need to be False, so lineedit text deletion will restore rows.
                    #print(f'{regex_text} {cell_text} {result}')
                    if result:
                        return False

            else:
                # else clause runs here because regex is invalid
                model_index: QModelIndex = self.sourceModel().index(source_row, int(key), source_parent)
                cell_text: str = self.sourceModel().data(model_index)

                if model_index.isValid():
                    result: bool = float(regex_text) < float(cell_text) if is_floatable(cell_text) and is_floatable(regex_text) else regex_text == cell_text
                    #print(f' {result} {regex_text} {cell_text}')
                    if result:
                        return False
        return True   # The row is shown by default value True.

    def lessThan(self, source_left: QModelIndex, source_right: QModelIndex) -> bool:
        """
        lessThan is a built-in method.
        
        When I click the column header text, this function will be triggered.
        """
        left_str: str = source_left.data()
        right_str: str = source_right.data()

        if is_floatable(left_str) and is_floatable(right_str):
            return float(left_str) < float(right_str) 
        else:
            return left_str < right_str





if __name__ == '__main__':
    x = MySortFilterProxyModel()
    print('done')