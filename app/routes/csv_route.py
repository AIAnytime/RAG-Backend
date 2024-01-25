from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse
from app.classes.csv_document_loader import CsvDocumentLoader
from app.classes.app_context import CsvAppContext

csv_app_context = CsvAppContext()

router = APIRouter()

@router.get("/query_csv")
async def query_csv(query: str = Query(..., title="Query", description="Enter the question")):
    
    if (csv_app_context.chunked_documents == None):
        return JSONResponse(content={"message": "Please upload a csv file to process"}, status_code=400)

    csv_app_context.document_loader.openai_key_environ()
    response = csv_app_context.document_loader.make_query(documents=csv_app_context.chunked_documents, question=query)

    return JSONResponse(content=response, status_code=200)

@router.post("/upload_csv")
#async def upload_txt(file: UploadFile = File(...)):
async def upload_csv(file_path: str = Query(..., title="File Path", description="Path to the document file")):
    if (file_path.lower() == "reset"):
        csv_app_context.chunked_documents = None
        return JSONResponse(content= {"message" : "Reset completed successfully"}, status_code=200)

    if not file_path.lower().endswith('.csv'):
        file_extension = list(file_path.split('.'))[-1]
        return JSONResponse(content = {"message" : f"Oops! you're trying to upload {file_extension}, we need .csv file to process"}, status_code=400)
    csv_app_context.document_loader = CsvDocumentLoader(file_path=file_path)
    csv_app_context.loaded_document = csv_app_context.document_loader.load_document()
    csv_app_context.chunked_documents = csv_app_context.document_loader.text_splitter(documents=csv_app_context.loaded_document)
    return JSONResponse(content= {"message" : "File uploaded successfully"}, status_code=200)