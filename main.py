from fastapi import FastAPI
from app.routes.txt_route import router as txt_router
from app.routes.pdf_route import router as pdf_router
from app.routes.csv_route import router as csv_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

app.include_router(txt_router)
app.include_router(pdf_router)
app.include_router(csv_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host='0.0.0.0', port=8000)