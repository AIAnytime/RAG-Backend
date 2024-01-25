from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.txt_document_loader import TxtDocumentLoader
from app.classes.app_context import TxtAppContext

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
#async def upload_txt(file: UploadFile = File(...)):
async def upload_txt(file_path: str = Query(..., title="File Path", description="Path to the document file")):
    if (file_path.lower() == "reset"):
        app_context.chunked_documents = None
        return JSONResponse(content= {"message" : "Reset completed successfully"}, status_code=200)

    if not file_path.lower().endswith('.txt'):
        file_extension = list(file_path.split('.'))[-1]
        return JSONResponse(content = {"message" : f"Oops! you're trying to upload {file_extension}, we need .txt file to process"}, status_code=400)
    app_context.document_loader = TxtDocumentLoader(file_path=file_path)
    app_context.loaded_document = app_context.document_loader.load_document()
    app_context.chunked_documents = app_context.document_loader.text_splitter(documents=app_context.loaded_document)
    return JSONResponse(content= {"message" : "File uploaded successfully"}, status_code=200)