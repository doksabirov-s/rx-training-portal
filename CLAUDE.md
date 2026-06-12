# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**RX Training Portal** is a FastAPI web application that wraps the [NotebookLM](https://notebooklm.google.com/) service to generate pharmaceutical training materials — slide decks, flashcards, study guides, and podcasts — via the `notebooklm-py` Python client. The UI is server-rendered with Jinja2 and Bootstrap 5. There is no database; all persistent data lives inside NotebookLM, with generated artifacts cached in `/tmp/rx_portal_downloads/`.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Start dev server (auto-reload enabled, http://localhost:8000)
python run.py
```

There are no test suites, linters, or build steps configured in this project.

## Architecture

### NotebookLM Client Lifecycle

A single `NotebookLMClient` is created at startup via the lifespan context manager in `app/main.py` and stored in `app.state.notebooklm`. It is shared across all requests. The `get_client` dependency in `app/dependencies.py` retrieves it from `request.app.state`. The client holds a 300-second keepalive session; if the server restarts, the client session resets.

### Router Structure

Four routers under `app/routers/` cover the full feature surface:

| Router | Prefix | Responsibility |
|---|---|---|
| `notebooks.py` | `/notebooks` | CRUD for NotebookLM notebooks (training modules) |
| `sources.py` | `/notebooks/{id}/sources` | Add/delete URL and file sources |
| `artifacts.py` | `/notebooks/{id}/artifacts` | Generate and download all content types |
| `chat.py` | `/notebooks/{id}/chat` | Q&A endpoint, returns JSON |

### Background Task Pattern

Long-running operations (slide generation, audio, flashcards) are dispatched via FastAPI `BackgroundTasks`. Their progress is tracked in the module-level `_gen_status: dict[str, str]` dict in `artifacts.py`, keyed by `notebook_id`. The frontend polls `GET /notebooks/{id}/generation-status` every 10 seconds. Completed slides signal readiness with the sentinel prefix `__slides_ready__<path>`.

### Extended Slide Generation

The core feature. `_run_extended_slides()` in `artifacts.py`:
1. Optionally runs a web research import via `client.research` (up to 300 s)
2. Calls `client.artifacts.generate_slide_deck()` once per part (1–4 parts, 16 slides each), using explicit Russian-language instructions that are strictly non-overlapping across parts to avoid repetition
3. Merges the resulting PPTX files via `_merge_pptx()`, which operates at the ZIP level (not the python-pptx object model) to avoid memory and compatibility issues
4. Saves a record to `slides_history.json` in `/tmp/rx_portal_downloads/`

### Form-Based Routes

All POST routes accept `application/x-www-form-urlencoded` (or multipart for file upload) and redirect with HTTP 303. Only `POST /notebooks/{id}/chat` returns JSON. There is no REST/JSON API otherwise.

### Template Layer

Templates in `app/templates/` extend `base.html`. The notebook detail page (`notebook.html`) is the most complex — it contains substantial inline JavaScript for:
- Polling the generation-status endpoint
- Rendering chat message bubbles
- Loading slide history via `GET /artifacts/slides/history`

### State and Persistence

| What | Where | Lifetime |
|---|---|---|
| Notebooks & sources | NotebookLM (remote) | Permanent |
| In-progress generation status | `_gen_status` dict in memory | Until server restart |
| Generated PPTX / MP3 files | `/tmp/rx_portal_downloads/` | Until OS clears `/tmp` |
| Slide history index | `/tmp/rx_portal_downloads/slides_history.json` | Until OS clears `/tmp` |

The app is single-user and single-process with no auth, no multi-tenancy, and no persistent local storage beyond `/tmp`.
