# PROJECT.md — Agent Knowledge Base

> **Important:** This file should be updated whenever further changes are made to the codebase, so that the next agent has accurate context.

---

## Purpose

This is a learning project implementing an AI agent using Google's Gemini API. The current state is a minimal working scaffold — a single-prompt, single-response call to a Gemini model.

---

## How the Program Works

1. `main.py` is the sole entry point.
2. On startup, it loads environment variables from a `.env` file using `python-dotenv`.
3. It reads `GEMINI_API_KEY` from the environment and raises a `RuntimeError` if it is missing.
4. It parses a required positional CLI argument `user_prompt` using `argparse`.
5. It instantiates a `google.genai.Client`, wraps the prompt in a `types.Content(role="user", ...)` message list, and calls `generate_content(client, messages)`.
6. `generate_content()` calls the Gemini API, checks that `response.usage_metadata` is not `None` (raises `RuntimeError` if so), prints prompt and response token counts, then prints the response text.

---

## Project Structure

| File/Dir | Purpose |
|---|---|
| `main.py` | Entry point and all application logic |
| `pyproject.toml` | Project metadata and dependency declarations (managed by `uv`) |
| `Makefile` | Convenience targets: `make sync` (install deps) and `make run` (run the program) |
| `.env` | **Not committed.** Must contain `GEMINI_API_KEY=<your key>` |
| `PROJECT.md` | This file — agent knowledge base |

---

## Dependencies

| Package | Version | Role |
|---|---|---|
| `google-genai` | 1.12.1 | Google Gemini API client |
| `python-dotenv` | 1.1.0 | Loads `.env` into `os.environ` |

Python ≥ 3.13 is required.

---

## Environment & Tooling

- **Package manager:** `uv` (not pip). Use `uv sync` to install deps, `uv run main.py` to execute.
- **Virtual environment:** `.venv/` in the project root (standard `uv` layout).
- **API key:** Stored in `.env` as `GEMINI_API_KEY`. Never commit this file.

---

## Code Structure

- `main()` — entry point: parses args, loads env, builds client and message list, calls `generate_content()`.
- `generate_content(client, messages)` — makes the API call, validates metadata, and prints token usage and response text.

---

## Model

- Currently uses `gemini-2.5-flash`.
- The prompt is supplied at runtime as a positional CLI argument (e.g. `uv run main.py "Your question here"`).
- `make run` passes a default prompt for convenience.
- There is no conversation loop, tool use, or persistent state yet — this is the starting scaffold for an agent that will likely grow to include those features.

---

## Assumptions & Known Constraints

- The program is stateless — no conversation history is maintained between runs.
- The prompt is supplied as a required positional CLI argument; running without one will print usage help and exit.
- Error handling covers two cases: missing `GEMINI_API_KEY` environment variable, and a `None` `usage_metadata` on the response (which would indicate a failed API request).
