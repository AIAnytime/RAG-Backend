from fastapi import APIRouter, Query, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from utils.file_utils import save_file_async
from app.classes.pdf_document_loader import PdfDocumentLoader
from app.classes.app_context import PdfAppContext
import os

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
async def upload_pdf(file: UploadFile = File(...)):
    # Check file format for basic validation
    if not file.filename.endswith(('.pdf')):
        raise HTTPException(status_code=400, detail="Invalid file format, please upload a .pdf file to process")

    # Create the directory if it doesn't exist
    storage_directory = "file_storage/pdf_files"
    os.makedirs(storage_directory, exist_ok=True)

    # Save the file to a temporary file for processing
    await save_file_async(file, storage_directory)

    pdf_app_context.document_loader = PdfDocumentLoader(file_path=os.path.join(storage_directory, file.filename))
    pdf_app_context.loaded_document = pdf_app_context.document_loader.load_document()
    pdf_app_context.chunked_documents = pdf_app_context.document_loader.text_splitter(documents=pdf_app_context.loaded_document)

    return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
