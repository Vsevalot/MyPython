from openpyxl import load_workbook

path2results = "E:\\test\\results.xlsx"

wb = load_workbook(filename=path2results, read_only=True)

ws = wb[wb.get_sheet_names()[0]]
i=0
print(ws.rows)
exit(0)
for row in ws.rows:
    for cell in row:
        print(cell.value)
    i+=1
    if(i==10):
        break