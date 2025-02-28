from os import PathLike
from typing import Iterable, Optional
from io import BytesIO

from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet

class ExcelWriter:

    def __init__(self, excel_filename: str | PathLike | BytesIO):
        self._file = excel_filename
        self._sheets: dict[str, Worksheet] = {}
        self._excel = self._get_excel()
    
    def _get_excel(self):
        return Workbook(write_only=True)

    @staticmethod
    def __write_sheet(sheet: Worksheet, data: dict | list):
        if isinstance(data, dict):
            sheet.append(tuple(data.values()))
        else:
            sheet.append(data)

    def write(self, data: Iterable[list | dict], /, *, sheet_name: Optional[str] = None) -> Worksheet:
        sheet_name = str(sheet_name) or f'Sheet{len(self._sheets) + 1}'
        if sheet_name not in self._sheets:
            self._sheets[sheet_name] = self._excel.create_sheet(title=sheet_name)
        if not data:
            return self._sheets[sheet_name]

        data = iter(data)
        first = next(data)
        if isinstance(first, dict):
            self._sheets[sheet_name].append(tuple(first.keys()))  # write_title
        self.__write_sheet(self._sheets[sheet_name], first)
        for r in data:
            self.__write_sheet(self._sheets[sheet_name], r)
        return self._sheets[sheet_name]

    def save(self):
        self._excel.save(self._file)

    def close(self):
        self._excel.close()
