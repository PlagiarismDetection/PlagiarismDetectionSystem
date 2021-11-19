from ..pds.reader.pdf import PDFReader

pdfs = PDFReader.getPDFList('inputs')
print(pdfs[0])
