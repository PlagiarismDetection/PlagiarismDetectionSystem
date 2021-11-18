from pds.reader.docx import DOCXReader
from pds.reader.pdf import PDFReader


def readInputs(folder):
    pdf_data = PDFReader.getPDFList(folder)
    docx_data = DOCXReader.getDOCXList(folder)
    return pdf_data + docx_data
