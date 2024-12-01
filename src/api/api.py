from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .endpoints import data_science, csv_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_science.router, prefix="/data_science", tags=["Data Science"])
app.include_router(csv_file.router, prefix="/csv_file", tags=["CSV File"])


@app.get("/")
async def read_root():
    return {
        "program_name": "ML Platform",
        "version": "1.0"
    }


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully",
    }


@app.get("/help", status_code=status.HTTP_200_OK)
async def help():
    return {
        "message": "API is working properly!"
    }
