from openpyxl.worksheet.worksheet import Worksheet
from typing import List
from openpyxl.cell import MergedCell


class MergedCellRanges:
    def __init__(self, value, row_start, row_end, col_start, col_end):
        self.value = value
        self.rstart = row_start - 1
        self.rend = row_end - 1
        self.cstart = col_start - 1
        self.cend = col_end - 1

class Sheet:
    def __init__(self, sheet: Worksheet):
        self.sheet = sheet

    def get_name(self) -> str:
        return self.sheet.title

    def get_merged_cells(self) -> List[MergedCellRanges]:
        results = []
        for mc in self.sheet.merged_cells.ranges:
            value = self.sheet.cell(row=mc.min_row, column=mc.min_col).value
            results.append(MergedCellRanges(value, mc.min_row, mc.max_row, mc.min_col, mc.max_col))
        return results

    def __str__(self):
        return f"Sheet: {self.name}, data: {self.data}"