from fastapi import APIRouter, Depends, Form, HTTPException
from notebooklm import NotebookLMClient

from app.dependencies import get_client

router = APIRouter()


@router.post("/notebooks/{notebook_id}/chat")
async def chat(
    notebook_id: str,
    message: str = Form(...),
    client: NotebookLMClient = Depends(get_client),
):
    try:
        response = await client.chat.ask(notebook_id, message)
        return {"answer": response.answer}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
