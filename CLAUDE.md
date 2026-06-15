# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single Claude Code skill: **codex-image** — generates images via gpt-image-2 through the Codex/ChatGPT OAuth subscription (no `OPENAI_API_KEY`, no per-image billing).

Tracked files:
- `.claude/skills/codex-image/SKILL.md` — trigger description and usage reference
- `.claude/skills/codex-image/scripts/run.sh` — self-contained launcher (auto-bootstraps a local venv)
- `.claude/skills/codex-image/scripts/codex_image.py` — Python implementation

No build system, no tests, no package manager.

## Running the skill

```bash
~/.claude/skills/codex-image/scripts/run.sh "prompt in English" [quality] [aspect] [ref1.png ... ref5.png]
```

Always invoke via `run.sh`, not `python3 codex_image.py` directly — the script manages its own `.venv` and ensures the `openai` SDK is present.

| Param | Values |
|---|---|
| quality | `low` (~45s) / `medium` (default) / `high` (~2–3min) |
| aspect | `landscape` 1536×1024 / `square` 1024×1024 / `portrait` 1024×1536 |
| refs | up to 5 local png/jpg/webp paths — style/character/logo transfer |

Output: prints path to PNG saved in `~/.codex/cache/images/img_<timestamp>.png`. On macOS the image opens automatically in Preview.

## One-time setup (prerequisite)

```bash
npm install -g @openai/codex   # install Codex CLI
codex login                    # browser auth; use --device-auth on headless servers
```

This writes `~/.codex/auth.json` with the OAuth token. No env vars needed.

## Architecture

The script uses the **Responses API** on the Codex backend (`chatgpt.com/backend-api/codex`), not the standard Images API. Key call pattern:

```python
client.responses.create(
    model="gpt-5.5",           # host model that invokes the image_generation tool
    tools=[{"type": "image_generation", "model": "gpt-image-2", ...}],
    tool_choice={"type": "image_generation"},
    stream=True,   # mandatory
    store=False,   # mandatory
    input=[{"type": "message", "role": "user", "content": [...]}],
)
```

Auth: `tokens.access_token` from `~/.codex/auth.json` is passed as the `api_key`, plus `chatgpt-account-id` and `OpenAI-Beta: responses=experimental` / `originator: codex_cli_rs` headers.

Reference images are embedded as `{"type": "input_image", "image_url": "data:<mime>;base64,...", "detail": "auto"}` content blocks alongside the prompt text — not as separate API calls.

## Hard constraints

Violating any of these causes HTTP 400 or silent wrong-path failures:

1. **Never call `client.images.generate()` / the Images API** — OAuth rejects it.
2. `stream=True` and `store=False` are both **mandatory**.
3. `input` must be a **list** of message objects, not a bare string.
4. Max **5 reference images**; ≤15 MB each; ≤40 MB total; png/jpg/webp only.
5. Auth reads `data["tokens"]["access_token"]` and `data["tokens"]["account_id"]` from `~/.codex/auth.json`.

## When not to use this skill

- Exact typography, brand colors, or precise diagrams → hand-author SVG.
- Seed-based / strictly reproducible pipelines → use a paid image API with seed support.
