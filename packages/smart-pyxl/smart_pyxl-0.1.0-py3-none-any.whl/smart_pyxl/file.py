from typing import List
from .sheet import Sheet
from openpyxl import Workbook, load_workbook


class File:
    def __init__(self, book: Workbook):
        self.book = book
    
    @classmethod
    def from_path(cls, path: str):
        wb = load_workbook(path)
        return File(wb)
    
    def get_sheets_len(self) -> int:
        return len(self.book.worksheets)
    
    def get_sheets(self) -> List[Sheet]:
        res = []
        for i in self.book:
            res.append(Sheet(i))
        
        return res
