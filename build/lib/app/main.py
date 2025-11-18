from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.documents import router as documents_router

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]


app = FastAPI(title="TDD Workshop API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # o ["*"] para permitir todos (no recomendado en prod)
    allow_credentials=True,
    allow_methods=["*"],         # GET, POST, PUT, DELETE...
    allow_headers=["*"],
)

app.include_router(documents_router, prefix="/documents", tags=["documents"])
