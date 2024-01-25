from fastapi import APIRouter, Query, Form, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.classes.txt_document_loader import TxtDocumentLoader
from utils.file_utils import save_file_async
from app.classes.app_context import TxtAppContext

import os

app_context = TxtAppContext()

router = APIRouter()

@router.get("/query_txt")
async def query_txt(query: str = Query(..., title="Query", description="Enter the question")):
    
    if (app_context.chunked_documents == None):
        return JSONResponse(content={"message": "Please upload a txt file to process"}, status_code=400)

    app_context.document_loader.openai_key_environ()
    response = app_context.document_loader.make_query(documents=app_context.chunked_documents, question=query)

    return JSONResponse(content=response, status_code=200)

@router.post("/upload_txt")
async def upload_txt(file: UploadFile = File(...)):
    # Check file format for basic validation
    if not file.filename.endswith(('.txt')):
        raise HTTPException(status_code=400, detail="Invalid file format, please upload a .txt file to process")

    # Create the directory if it doesn't exist
    storage_directory = "file_storage/txt_files"
    os.makedirs(storage_directory, exist_ok=True)

    # Save the file to a temporary file for processing
    await save_file_async(file, storage_directory)

    app_context.document_loader = TxtDocumentLoader(file_path=os.path.join(storage_directory, file.filename))
    app_context.loaded_document = app_context.document_loader.load_document()
    app_context.chunked_documents = app_context.document_loader.text_splitter(documents=app_context.loaded_document)

    return JSONResponse(content={"message": "File uploaded successfully"}, status_code=200)
