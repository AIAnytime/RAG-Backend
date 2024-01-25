from app.classes.csv_document_loader import CsvDocumentLoader
from app.classes.pdf_document_loader import PdfDocumentLoader
from app.classes.txt_document_loader import TxtDocumentLoader

class TxtAppContext:
    def __init__(self):
        self.chunked_documents = None
        self.document_loader = TxtDocumentLoader(file_path=None)

class PdfAppContext:
    def __init__(self):
        self.chunked_documents = None
        self.document_loader = PdfDocumentLoader(file_path=None)

class CsvAppContext:
    def __init__(self):
        self.chunked_documents = None
        self.document_loader = CsvDocumentLoader(file_path=None)