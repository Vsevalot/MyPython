import PyPDF2

if __name__ == "__main__":
    path_to_book = "e:\\Users\\sevamunger\\Downloads\\Murphy R. English Grammar in Use. 2012 4-ed..pdf"
    inputpdf = PyPDF2.PdfFileReader(open(path_to_book, "rb"))

    path_to_answers = "e:\\Users\\sevamunger\\Downloads\\additional_answers.pdf"
    output = PyPDF2.PdfFileWriter()
    for i in range(378, 382, 1):
        output.addPage(inputpdf.getPage(i))

    outputStream = open(path_to_answers, "wb")
    output.write(outputStream)
    outputStream.close()