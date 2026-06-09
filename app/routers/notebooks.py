from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from notebooklm import NotebookLMClient

from app.dependencies import get_client

try:
    from notebooklm import NotebookNotFoundError
except ImportError:
    try:
        from notebooklm.errors import NotebookNotFoundError
    except ImportError:
        NotebookNotFoundError = Exception  # type: ignore[misc,assignment]

router = APIRouter()
templates = Jinja2Templates(directory=str(Path(__file__).resolve().parent.parent / "templates"))


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, client: NotebookLMClient = Depends(get_client)):
    notebooks = await client.notebooks.list()
    return templates.TemplateResponse(request, "index.html", {"notebooks": notebooks})


@router.post("/notebooks")
async def create_notebook(
    title: str = Form(...),
    client: NotebookLMClient = Depends(get_client),
):
    notebook = await client.notebooks.create(title)
    return RedirectResponse(url=f"/notebooks/{notebook.id}", status_code=303)


@router.get("/notebooks/{notebook_id}", response_class=HTMLResponse)
async def notebook_detail(
    notebook_id: str,
    request: Request,
    status: str = "",
    client: NotebookLMClient = Depends(get_client),
):
    try:
        notebook = await client.notebooks.get(notebook_id)
        sources = await client.sources.list(notebook_id)
        artifacts_list = await client.artifacts.list(notebook_id)
    except NotebookNotFoundError:
        raise HTTPException(status_code=404, detail="Notebook not found")
    return templates.TemplateResponse(
        request,
        "notebook.html",
        {
            "notebook": notebook,
            "sources": sources,
            "artifacts": artifacts_list,
            "status": status,
        },
    )


@router.post("/notebooks/{notebook_id}/delete")
async def delete_notebook(
    notebook_id: str,
    client: NotebookLMClient = Depends(get_client),
):
    await client.notebooks.delete(notebook_id)
    return RedirectResponse(url="/", status_code=303)


@router.post("/notebooks/{notebook_id}/rename")
async def rename_notebook(
    notebook_id: str,
    title: str = Form(...),
    client: NotebookLMClient = Depends(get_client),
):
    await client.notebooks.rename(notebook_id, title)
    return RedirectResponse(url=f"/notebooks/{notebook_id}", status_code=303)
