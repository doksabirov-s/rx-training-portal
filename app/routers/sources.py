import tempfile
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import RedirectResponse
from notebooklm import NotebookLMClient

from app.dependencies import get_client

router = APIRouter()


@router.post("/notebooks/{notebook_id}/sources/url")
async def add_url_source(
    notebook_id: str,
    url: str = Form(...),
    client: NotebookLMClient = Depends(get_client),
):
    try:
        await client.sources.add_url(notebook_id, url, wait=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return RedirectResponse(url=f"/notebooks/{notebook_id}", status_code=303)


@router.post("/notebooks/{notebook_id}/sources/file")
async def add_file_source(
    notebook_id: str,
    file: UploadFile = File(...),
    client: NotebookLMClient = Depends(get_client),
):
    suffix = Path(file.filename or "upload").suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = Path(tmp.name)
    try:
        await client.sources.add_file(notebook_id, tmp_path, title=file.filename, wait=True)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        tmp_path.unlink(missing_ok=True)
    return RedirectResponse(url=f"/notebooks/{notebook_id}", status_code=303)


@router.post("/notebooks/{notebook_id}/sources/{source_id}/delete")
async def delete_source(
    notebook_id: str,
    source_id: str,
    client: NotebookLMClient = Depends(get_client),
):
    await client.sources.delete(notebook_id, source_id)
    return RedirectResponse(url=f"/notebooks/{notebook_id}", status_code=303)
