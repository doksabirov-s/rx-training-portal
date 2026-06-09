from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from notebooklm import NotebookLMClient

from app.routers import notebooks, sources, artifacts, chat

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with NotebookLMClient.from_storage(keepalive=300.0) as client:
        app.state.notebooklm = client
        yield


app = FastAPI(title="RX Training Portal", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(notebooks.router)
app.include_router(sources.router)
app.include_router(artifacts.router)
app.include_router(chat.router)
