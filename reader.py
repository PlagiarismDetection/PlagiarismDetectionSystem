from Reader.PDFReader import PDFReader

pdfs = PDFReader.getPDFList('inputs')
for pdf in pdfs:
    title = pdf.getDate()
    print(title)
