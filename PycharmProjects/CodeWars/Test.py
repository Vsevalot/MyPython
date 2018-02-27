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
                    value = str(cell.value)
                    if cell.value[0] == "'" and cell.value[-1] == "'":
                        value = value[1:-1]
                    reds.append(value)
    return reds

def readCSV(csv_path: str) -> list:  # read any CSV file and return it like list of columns
    with open(csv_path, 'r') as file:
        lines = [line.split(';') for line in
                 file.readlines()]  # reading all lines in the file with rows as elements of the list
        for line in range(len(lines)):
            if lines[line][-1][-1] == '\n':
                lines[line][-1] = lines[line][-1][:-1]

        if lines==[]:
            return []
        data = [[value[i] for value in lines] for i in
                range(len(lines[0]))]  # transpose the list to make columns elements of the list
        return data

skipped_path = "Z:\\Tetervak\\skipped_records_20180212_162000.xlsx"

def ignoreList(path_to_skipped):
    ignored_fragments = readCSV("Z:/Tetervak/Ignored_fragments.csv")
    to_ignore = findReds(path_to_skipped)
    with open ("Z:/Tetervak/Ignored_fragments.csv", 'a') as file:
        for record in to_ignore:
            if record not in ignored_fragments:
                file.write("{}\n".format(record))
                ignored_fragments.append(record)
        file.close()
    return ignored_fragments