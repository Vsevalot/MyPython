import win32com.client as win32

path2docx="E:\\test\\Багин\\rec300_20.02.14.docx"

from docx import Document

document = Document(path2docx)
table = document.tables[0]
print(document.paragraphs[0].run())
exit(0)




for row in table.rows:
    for cell in row.cells:
        for paragraph in cell.paragraphs:
            print(paragraph.text)
exit(0)
