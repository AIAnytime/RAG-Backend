from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.pdf_document_loader import PdfDocumentLoader
from app.classes.app_context import PdfAppContext

pdf_app_context = PdfAppContext()

router = APIRouter()

@router.get("/query_pdf")
async def query_pdf(query: str = Query(..., title="Query", description="Enter the question")):
    
    if (pdf_app_context.chunked_documents == None):
        return JSONResponse(content={"message": "Please upload a pdf file to process"}, status_code=400)

    pdf_app_context.document_loader.openai_key_environ()
    response = pdf_app_context.document_loader.make_query(documents=pdf_app_context.chunked_documents, question=query)

    return JSONResponse(content=response, status_code=200)

@router.post("/upload_pdf")
#async def upload_txt(file: UploadFile = File(...)):
async def upload_pdf(file_path: str = Query(..., title="File Path", description="Path to the document file")):
    if (file_path.lower() == "reset"):
        pdf_app_context.chunked_documents = None
        return JSONResponse(content= {"message" : "Reset completed successfully"}, status_code=200)

    if not file_path.lower().endswith('.pdf'):
        file_extension = list(file_path.split('.'))[-1]
        return JSONResponse(content = {"message" : f"Oops! you're trying to upload {file_extension}, we need .pdf file to process"}, status_code=400)
    pdf_app_context.document_loader = PdfDocumentLoader(file_path=file_path)
    pdf_app_context.loaded_document = pdf_app_context.document_loader.load_document()
    pdf_app_context.chunked_documents = pdf_app_context.document_loader.text_splitter(documents=pdf_app_context.loaded_document)
    return JSONResponse(content= {"message" : "File uploaded successfully"}, status_code=200)