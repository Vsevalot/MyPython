import win32com.client as win32

path2doc="E:\\test\\Багин\\rec300_20.02.14.doc"

word = win32.Dispatch("Word.Application")
word.Visible = 0
word.Documents.Open(path2doc)
doc = word.ActiveDocument
table = doc.Tables(1)

text=str(doc.Content).split()
print(text)
exit(0)
for i in range(len(table.rows)):
    print(table.Cell(Row =i+1, Column =1).Range.Text.split())