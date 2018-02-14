
path = "Z:\\Tetervak\\skipped_records_20180212_162000.xlsx"

def findReds(xlsx_path: str) -> list:
    from openpyxl import load_workbook
    wb = load_workbook(filename=xlsx_path, read_only=True)
    sheet = wb[wb.get_sheet_names()[0]]
    reds = []
    bad = wb.style_names.index("Плохой")
    for row in sheet.rows:
        for cell in row:
            if cell.value is not None:
                if cell._style_id == bad and str(cell.value)[1:4] == 'rec':
                    reds.append(str(cell.value))
    return reds


print(findReds(path))