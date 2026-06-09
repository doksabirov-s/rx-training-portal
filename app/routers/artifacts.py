import copy
import tempfile
from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, Form, HTTPException, Request
from fastapi.responses import FileResponse, RedirectResponse
from notebooklm import NotebookLMClient, SlideDeckFormat

from app.dependencies import get_client

router = APIRouter()

_DOWNLOADS = Path(tempfile.gettempdir()) / "rx_portal_downloads"
_DOWNLOADS.mkdir(exist_ok=True)

# In-memory generation status: notebook_id -> message string
_gen_status: dict[str, str] = {}


def _merge_pptx(files: list[Path]) -> Path:
    """Merge multiple PPTX files into one by copying slide XML."""
    from pptx import Presentation
    from pptx.oxml.ns import qn

    base = Presentation(str(files[0]))

    for src_path in files[1:]:
        src = Presentation(str(src_path))
        # Copy slide layouts/masters mapping isn't needed for simple copy
        for slide in src.slides:
            # Add a blank slide using the first layout of base
            layout = base.slide_layouts[0]
            new_slide = base.slides.add_slide(layout)
            # Remove placeholder shapes from the blank slide
            sp_tree = new_slide.shapes._spTree
            for ph in sp_tree.findall(qn("p:sp")):
                sp_tree.remove(ph)
            # Copy all shapes from source slide
            for el in slide.shapes._spTree:
                sp_tree.append(copy.deepcopy(el))

    out = _DOWNLOADS / f"{files[0].stem}_merged.pptx"
    base.save(str(out))
    return out


async def _run_extended_slides(app, notebook_id: str, parts: int, topic: str = ""):
    """Generate `parts` slide decks and merge them into one PPTX."""
    client: NotebookLMClient = app.state.notebooklm
    _gen_status[notebook_id] = f"Extended slides: generating part 1 of {parts}…"

    topic_prefix = f"Topic: {topic}. " if topic.strip() else ""

    part_suffixes = [
        "Focus on introduction, key definitions, and main concepts.",
        "Focus on detailed analysis, data, mechanisms, and supporting evidence.",
        "Focus on clinical applications, case studies, and practical recommendations.",
        "Focus on conclusions, future directions, and supplementary information.",
    ]

    pptx_files: list[Path] = []
    try:
        for i in range(parts):
            _gen_status[notebook_id] = f"Extended slides: generating part {i + 1} of {parts}…"
            instructions = topic_prefix + part_suffixes[i % len(part_suffixes)]
            task = await client.artifacts.generate_slide_deck(
                notebook_id,
                instructions=instructions,
                slide_format=SlideDeckFormat.DETAILED_DECK,
            )
            await client.artifacts.wait_for_completion(notebook_id, task.task_id, timeout=600.0)

            out = _DOWNLOADS / f"{notebook_id}_slides_part{i + 1}.pptx"
            await client.artifacts.download_slide_deck(notebook_id, out, format="pptx")
            pptx_files.append(out)

        _gen_status[notebook_id] = "Extended slides: merging files…"
        merged = _merge_pptx(pptx_files)
        _gen_status[notebook_id] = f"__slides_ready__{merged}"
    except Exception as exc:
        _gen_status[notebook_id] = f"Generation failed: {exc}"


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


@router.post("/notebooks/{notebook_id}/artifacts/slides")
async def generate_extended_slides(
    notebook_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    parts: int = Form(2),
    topic: str = Form(""),
    client: NotebookLMClient = Depends(get_client),
):
    parts = max(1, min(parts, 4))  # clamp 1–4
    background_tasks.add_task(_run_extended_slides, request.app, notebook_id, parts, topic)
    slides = parts * 16
    return RedirectResponse(
        url=f"/notebooks/{notebook_id}?status=Generating+{slides}+slides+in+{parts}+parts.+Refresh+to+check+status.",
        status_code=303,
    )


@router.get("/notebooks/{notebook_id}/artifacts/slides/download")
async def download_extended_slides(notebook_id: str):
    status = _gen_status.get(notebook_id, "")
    if status.startswith("__slides_ready__"):
        path = Path(status.removeprefix("__slides_ready__"))
        if path.exists():
            return FileResponse(
                path=str(path),
                media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                filename="presentation.pptx",
            )
    raise HTTPException(status_code=404, detail="Slides not ready yet. Please wait and refresh.")


@router.get("/notebooks/{notebook_id}/generation-status")
async def generation_status(notebook_id: str):
    status = _gen_status.get(notebook_id)
    if status and status.startswith("__slides_ready__"):
        return {"status": None, "slides_ready": True}
    return {"status": status, "slides_ready": False}


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
