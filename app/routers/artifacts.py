import tempfile
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from notebooklm import NotebookLMClient

from app.dependencies import get_client

router = APIRouter()

_DOWNLOADS = Path(tempfile.gettempdir()) / "rx_portal_downloads"
_DOWNLOADS.mkdir(exist_ok=True)

# In-memory generation status: notebook_id -> message string
_gen_status: dict[str, str] = {}


async def _run_generation(app, notebook_id: str, kind: str, **kwargs):
    client: NotebookLMClient = app.state.notebooklm
    _gen_status[notebook_id] = f"{kind} generation in progress…"
    try:
        if kind == "flashcards":
            task = await client.artifacts.generate_flashcards(notebook_id, **kwargs)
        elif kind == "study-guide":
            task = await client.artifacts.generate_study_guide(notebook_id)
        elif kind == "audio":
            task = await client.artifacts.generate_audio(notebook_id)
        else:
            _gen_status[notebook_id] = f"Unknown artifact kind: {kind}"
            return
        await client.artifacts.wait_for_completion(notebook_id, task.task_id, timeout=1200.0)
        _gen_status.pop(notebook_id, None)
    except Exception as exc:
        _gen_status[notebook_id] = f"Generation failed: {exc}"


@router.post("/notebooks/{notebook_id}/artifacts/flashcards")
async def generate_flashcards(
    notebook_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    count: int = Form(10),
    client: NotebookLMClient = Depends(get_client),
):
    background_tasks.add_task(_run_generation, request.app, notebook_id, "flashcards", count=count)
    return RedirectResponse(
        url=f"/notebooks/{notebook_id}?status=Flashcard+generation+started.+Refresh+to+check+status.",
        status_code=303,
    )


@router.post("/notebooks/{notebook_id}/artifacts/study-guide")
async def generate_study_guide(
    notebook_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    client: NotebookLMClient = Depends(get_client),
):
    background_tasks.add_task(_run_generation, request.app, notebook_id, "study-guide")
    return RedirectResponse(
        url=f"/notebooks/{notebook_id}?status=Study+guide+generation+started.+Refresh+to+check+status.",
        status_code=303,
    )


@router.post("/notebooks/{notebook_id}/artifacts/audio")
async def generate_audio(
    notebook_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    client: NotebookLMClient = Depends(get_client),
):
    background_tasks.add_task(_run_generation, request.app, notebook_id, "audio")
    return RedirectResponse(
        url=f"/notebooks/{notebook_id}?status=Podcast+generation+started+%28takes+up+to+20+min%29.+Refresh+to+check+status.",
        status_code=303,
    )


@router.get("/notebooks/{notebook_id}/generation-status")
async def generation_status(notebook_id: str):
    return {"status": _gen_status.get(notebook_id)}


@router.get("/notebooks/{notebook_id}/artifacts/audio/download")
async def download_audio(
    notebook_id: str,
    client: NotebookLMClient = Depends(get_client),
):
    out_path = _DOWNLOADS / f"{notebook_id}_podcast.mp3"
    try:
        path = await client.artifacts.download_audio(notebook_id, out_path)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return FileResponse(path=str(path), media_type="audio/mpeg", filename="podcast.mp3")


@router.post("/notebooks/{notebook_id}/artifacts/{artifact_id}/delete")
async def delete_artifact(
    notebook_id: str,
    artifact_id: str,
    client: NotebookLMClient = Depends(get_client),
):
    await client.artifacts.delete(notebook_id, artifact_id)
    return RedirectResponse(url=f"/notebooks/{notebook_id}", status_code=303)
