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
5. It instantiates a `google.genai.Client`, wraps the prompt in a `types.Content(role="user", ...)` message list, optionally prints `User prompt: ...` if `--verbose`, and calls `generate_content(client, messages, verbose=args.verbose)`.
6. `generate_content()` calls the Gemini API, checks that `response.usage_metadata` is not `None` (raises `RuntimeError` if so), prints prompt and response token counts if `verbose=True`, then prints the response text.

---

## Project Structure

| File/Dir | Purpose |
|---|---|
| `main.py` | Entry point and all application logic for the AI agent |
| `pyproject.toml` | Project metadata and dependency declarations (managed by `uv`) |
| `Makefile` | Convenience targets: `make sync` (install deps) and `make run` (run the program) |
| `.env` | **Not committed.** Must contain `GEMINI_API_KEY=<your key>` |
| `PROJECT.md` | This file — agent knowledge base |
| `calculator/` | **Test project for the AI agent** — a command-line calculator app |
| `calculator/main.py` | CLI entry point for the calculator app |
| `calculator/tests.py` | Unit tests for the calculator (9 tests, all passing) |
| `calculator/pkg/calculator.py` | Core `Calculator` class with operator precedence evaluation |
| `calculator/pkg/render.py` | JSON output formatting utility |

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

- `main()` — entry point: parses args (positional `user_prompt` and optional `--verbose`), loads env, builds client and message list, calls `generate_content()`.
- `generate_content(client, messages, verbose=False)` — makes the API call, validates metadata, prints token usage (only when `verbose=True`), and prints the response text.

---

## Model

- Currently uses `gemini-2.5-flash`.
- The prompt is supplied at runtime as a positional CLI argument (e.g. `uv run main.py "Your question here"`).
- `make run` passes a default prompt for convenience.
- There is no conversation loop, tool use, or persistent state yet — this is the starting scaffold for an agent that will likely grow to include those features.

---

## Test Project: Calculator App

A command-line calculator app is included as a test project for the AI agent to read, modify, and execute. This serves as a sandbox for agent capabilities.

**Running the calculator:**
```bash
uv run calculator/main.py "3 + 5"          # Output: {"expression": "3 + 5", "result": 8}
uv run calculator/tests.py                 # All 9 tests pass
```

**Calculator features:**
- Supports `+`, `-`, `*`, `/` operators
- Proper operator precedence (multiplication/division before addition/subtraction)
- Infix notation evaluation using stack-based operator precedence algorithm
- JSON output formatting for results
- Comprehensive error handling (invalid tokens, insufficient operands, etc.)

---

## Assumptions & Known Constraints

- The program is stateless — no conversation history is maintained between runs.
- The prompt is supplied as a required positional CLI argument; running without one will print usage help and exit.
- Error handling covers two cases: missing `GEMINI_API_KEY` environment variable, and a `None` `usage_metadata` on the response (which would indicate a failed API request).
