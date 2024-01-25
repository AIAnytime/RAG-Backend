from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.txt_route import router as txt_router
from app.routes.pdf_route import router as pdf_router
from app.routes.csv_route import router as csv_router

app = FastAPI(swagger_ui_parameters={"syntaxHighlight": False})

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(txt_router)
app.include_router(pdf_router)
app.include_router(csv_router)

# if __name__ == "__main__":
#     uvicorn.run(app, host='0.0.0.0', port=8000)
