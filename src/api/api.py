from contextlib import asynccontextmanager

from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import asyncio as aioredis

from .endpoints import data_science, csv_file


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis_client = None
    try:
        redis_client = aioredis.from_url("redis://localhost:6379")
        FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache")
        print("Cache initialized successfully.")

        await FastAPILimiter.init(redis_client)
        print("Limiter initialized successfully.")

        yield
    except Exception as e:
        print(f"Error setting up Redis caching: {e}")
        yield
    finally:
        try:
            if FastAPICache.get_backend():
                await FastAPICache.clear()
                print("Cache cleared during shutdown.")
                await FastAPILimiter.close()
                print("Limiter cleared during shutdown.")
        except Exception as e:
            print(f"Error clearing cache: {e}")
        finally:
            if redis_client:
                await redis_client.close()
                print("Redis connection closed.")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(data_science.router, prefix="/data_science", tags=["Data Science"])
app.include_router(csv_file.router, prefix="/csv_file", tags=["CSV File"])


@app.get("/", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def read_root():
    return {
        "program_name": "ML Platform",
        "version": "1.0"
    }


@app.get("/health", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def health_check():
    return {
        "status": "healthy",
        "message": "API is running successfully",
    }


@app.get("/help", status_code=status.HTTP_200_OK, dependencies=[Depends(RateLimiter(times=50, seconds=60))])
async def help():
    return {
        "message": "API is working properly!"
    }
