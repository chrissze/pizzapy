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
    def __init__(self, filter_mode) -> None:
        super().__init__()
        self.filters: Dict[Union[int, str], QRegularExpression] = {}


    def setFilterByColumn(self, regex: QRegularExpression, column: int) -> None:
        
        
        if regex.isValid():
            self.filters[column] = regex  # use int as dictionary key
        else:
            self.filters[str(column)] = regex # use str as dictionary key
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        """
        'key, regex' is the key value pairs in self.filters dictionary, that defined earlier. 
        """
        for key, regex in self.filters.items():
            
            if regex.isValid():
                print('regex is Valid')
                regextext: str = regex.pattern()
                ix: QModelIndex = self.sourceModel().index(source_row, key, source_parent) # self is the ProxyModel instance
                celltext: str = self.sourceModel().data(ix)
                print(f'celltext is {celltext}')
                print(f'regextext is {regextext}')
                
                
                if ix.isValid() and is_floatable(celltext):
                    print(f'ix {ix} is_valid ')

                    result: bool = float(regextext) > float(celltext) if is_floatable(celltext) \
                        and is_floatable(regextext) else False #regex.indexIn(celltext)
                        # above line end need to be False, so lineedit text deletion will restore rows.
                    print(f'result 60 is {result} \n\n')
                    if result:
                        return False
                    
            else:
                print('regex is NOT Valid')
                regextext: str = regex.pattern()
                print(f'regextext is {regextext}')
                ix: QModelIndex = self.sourceModel().index(source_row, int(key), source_parent)
                celltext: str = self.sourceModel().data(ix)
                print(f'celltext is {celltext}')

                if ix.isValid() and is_floatable(celltext):
                    print(f'ix {ix} is_valid')
                    print(f'regextext {regextext[1:]} is_floatable: {is_floatable(regextext[1:])}')
                    result: bool = readf(regextext[1:]) < float(celltext) if is_floatable(celltext) and is_floatable(regextext[1:]) else False # regex.indexIn(celltext)
                    print(f'result 82 is {result} \n\n')
                    if result:
                        return False
                
                    

        return True

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        leftstr: str = left.data()
        rightstr: str = right.data()
        leftdat: Union[str, float] = leftstr if not is_floatable(leftstr) else float(leftstr)
        rightdat: Union[str, float] = rightstr if not is_floatable(rightstr) else float(rightstr)
        return leftdat < rightdat


if __name__ == '__main__':
    x = MySortFilterProxyModel()
    print('done')