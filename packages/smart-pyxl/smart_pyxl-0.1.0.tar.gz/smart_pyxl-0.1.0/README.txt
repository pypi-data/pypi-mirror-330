smart-pyxl
========

smart-pyxl is a Python library to help get merged cells. It is based on top of openpyxl

============

Sample code::

    from openpyxl import Workbook
    wb = Workbook()

    # grab the active worksheet
    ws = wb.active

    # Data can be assigned directly to cells
    ws['A1'] = 42

    # Rows can also be appended
    ws.append([1, 2, 3])

    # Python types will automatically be converted
    import datetime
    ws['A2'] = datetime.datetime.now()

    # Save the file
    wb.save("sample.xlsx")
