'''
path2docx="E:\\test\\Багин\\rec300_20.02.14.docx"
from docx import Document
document = Document(path2docx)
table = document.tables[0]
for row in table.rows:
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            print(paragraph.text)
exit(0)
'''
import os

path2reports = "E:\\test\\Багин"
reportsList = [ f for f in os.listdir(path2reports) if
               os.path.isfile(os.path.join(path2reports, f))]

for i in range(len(reportsList)):
    f=open(path2reports+'\\'+reportsList[i][:6]+'_'+reportsList[i][-12:-10]+reportsList[i][-9:-7]+reportsList[i][-6:-4]+".csv",'w')
    f.close()

exit(0)
import win32com.client as win32

path2doc="E:\\test\\Багин\\rec300_20.02.14.doc"

word = win32.Dispatch("Word.Application")
word.Visible = 0
word.Documents.Open(path2doc)
doc = word.ActiveDocument
table = doc.Tables(1)


text=str(doc.Content).split()

columns=[]
for i in range(len(table.columns)):
    columns.append(table.Cell(Row =1, Column =i+1).Range.Text.split()[0])

report={columns[i]:[] for i in range(len(columns))}

for i in range(2,len(table.rows),1):
    for k in range(len(table.columns)):
        report[columns[k]].append(''.join(table.Cell(Row =i+1, Column =k+1).Range.Text.split()[:-1]))

def stageReader(stage:str):
    stage=stage.split('/')



for column in report:
    print(report[column])