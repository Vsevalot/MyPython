
def readXLSX(path2xlsx:str)->list:
    from openpyxl import load_workbook
    wb = load_workbook(filename=path2xlsx, read_only=True)
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
    return [[line[i] for line in lines if line[i] is not None] for i in range(len(lines[0]))]

def sergey2lavrov(matName:str)->str:
    return ''.join([v+'_' for v in matName.split('_')][:3])[:-1]+".mat("+str(int(int(matName.split('_')[-2])/30))+")'"

def write2csv(some2Dlist:list, path2save:str):
    if type(some2Dlist[0])!=list:
        print("You should give a list of lists to write it for csv")
        exit(0)
    try:
        with open(path2save, 'w') as file:
            for k in range(max([len(l) for l in some2Dlist])):
                line=''
                for column in some2Dlist:
                    if k>=len(column):
                        line+=';'
                    else:
                        line+=column[k]+';'
                file.write(line[:-1]+'\n')
            file.close()
        print("Saved : "+path2save)
        return True
    except:
        return False


path2results="Z:\\Tetervak\\9_data14_3_30sec_all_20171027_172800.xlsx"
results=readXLSX(path2results)
converted=[[] for column in results]
for i, group in enumerate(results):
    for fileName in group:
        if len(fileName.split('_'))==6 or fileName=='':
            continue
        converted[i].append(sergey2lavrov(fileName))

write2csv(converted, "Z:\\Tetervak\\Test.csv")
