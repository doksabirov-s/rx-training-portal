from fastapi import Request
from notebooklm import NotebookLMClient


def get_client(request: Request) -> NotebookLMClient:
    return request.app.state.notebooklm
