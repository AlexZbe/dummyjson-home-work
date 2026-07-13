from concurrent.futures import ThreadPoolExecutor
from contextlib import asynccontextmanager
import sys
from pathlib import Path

sourse_path = Path(__file__).parent.parent
sys.path.append(str(sourse_path))

from fastapi import FastAPI
from src.api.v1.api_v1 import router as router_v1


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.thread_pool = ThreadPoolExecutor(max_workers=5)
    yield
    app.state.thread_pool.shutdown(wait=True)


app = FastAPI(lifespan=lifespan)

app.include_router(router_v1)
