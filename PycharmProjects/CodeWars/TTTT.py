def readXLSX(xlsx_path:str)->list:
    from openpyxl import load_workbook
    wb = load_workbook(filename=xlsx_path, read_only=True)
    ws = wb[wb.get_sheet_names()[0]]
    lines = []
    for row in ws.rows:
        line = []
        for cell in row:
            if cell.value is not None:
                line.append(str(cell.value))
            else:
                line.append('')
        lines.append(line)

    x=lines[-3:]
    return [[line[i] for line in lines if line[i] is not None] for i in range(len(lines[0]))]

a="Z:\\Tetervak\\13_data14_4_30sec_20171031_122700.xlsx"

b=readXLSX(a)[0][:5]

print(b)