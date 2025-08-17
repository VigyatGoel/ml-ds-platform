from fastapi import FastAPI, status, Request
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from .routes import data_science, csv_file, machine_learning, data_summary
# from ..service.database.database_service import DatabaseService, engine

# db_service = DatabaseService()


# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     await db_service.init_db()
#     yield
#     await engine.dispose()


app = FastAPI()
limiter = Limiter(key_func=get_remote_address)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware removed (backend only accessed internally by Streamlit)

app.include_router(data_science.router, prefix="/data_science", tags=["Data Science"])
app.include_router(csv_file.router, prefix="/csv_file", tags=["CSV File"])
app.include_router(
    machine_learning.router, prefix="/machine_learning", tags=["Machine Learning"]
)
app.include_router(data_summary.router, prefix="/data_summary", tags=["Data Summary"])
# app.include_router(api_key.router, prefix="/api", tags=["API Key"])


@app.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def read_root(request: Request):
    return {"program_name": "ML Platform", "version": "1.0"}


@app.get("/health", status_code=status.HTTP_200_OK)
@limiter.limit("20/minute")
async def health_check(request: Request):
    return {"status": "healthy"}
