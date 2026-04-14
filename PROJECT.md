# PROJECT.md — Agent Knowledge Base

> **Important:** This file should be updated whenever further changes are made to the codebase, so that the next agent has accurate context.

---

## Quick Start

**Setup & Testing:**
```bash
make sync           # Install dependencies (run once)
make test           # Run all 33 unit/schema tests (verify everything works)
make integration_test  # Run 9 integration tests for call_function dispatch
make run            # Try the AI agent with a sample prompt
```

**Available Makefile targets:**
- `make sync` — Install dependencies into `.venv/`
- `make run` — Run the agent with default prompt
- `make test` — Run all 33 unit/schema tests (calculator + 5 agent tool/schema tests)
- `make integration_test` — Run 9 integration tests for call_function dispatch (no network)
- `make calculator_test` — Run just calculator tests
- `make calculator_run ARGS="..."` — Run calculator with expression

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
| `prompts.py` | Contains `system_prompt` — the system instruction passed to Gemini (now a helpful coding agent prompt) |
| `functions/call_function.py` | Defines `available_functions` (`types.Tool`), `function_map` dict, and `call_function(function_call, verbose)` dispatcher — routes LLM `FunctionCall` objects to real functions, injects `working_directory="./calculator"`, and wraps results in `types.Content(role="tool", ...)` |
| `pyproject.toml` | Project metadata and dependency declarations (managed by `uv`) |
| `Makefile` | Convenience targets: `make sync`, `make run`, `make test`, `make calculator_test`, `make calculator_run` |
| `config.py` | Configuration constants (e.g., `MAX_FILE_CHARS`) |
| `.env` | **Not committed.** Must contain `GEMINI_API_KEY=<your key>` |
| `PROJECT.md` | This file — agent knowledge base |
| `calculator/` | **Test project for the AI agent** — a command-line calculator app |
| `calculator/main.py` | CLI entry point for the calculator app |
| `calculator/tests.py` | Unit tests for the calculator (9 tests, all passing) |
| `calculator/lorem.txt` | Lorem ipsum text file (>20k chars) for testing file truncation |
| `calculator/pkg/calculator.py` | Core `Calculator` class with operator precedence evaluation |
| `calculator/pkg/render.py` | JSON output formatting utility |
| `functions/` | **Agent tool functions** — functions the AI agent can call |
| `functions/get_files_info.py` | Lists directory contents with metadata (name, size, is_dir) with path validation; also exports `schema_get_files_info` (`types.FunctionDeclaration`) |
| `functions/get_file_content.py` | Reads file contents with truncation at 10k characters and path validation; also exports `schema_get_file_content` (`types.FunctionDeclaration`) |
| `functions/write_file.py` | Writes/overwrites files with path validation and automatic directory creation; also exports `schema_write_file` (`types.FunctionDeclaration`) |
| `functions/run_python_file.py` | Executes Python files with path validation and 30-second timeout; also exports `schema_run_python_file` (`types.FunctionDeclaration`) |
| `functions/call_function.py` | Defines `available_functions` (`types.Tool`), `function_map` dict, and `call_function(function_call, verbose)` dispatcher — routes LLM `FunctionCall` objects to real functions, injects `working_directory="./calculator"`, and wraps results in `types.Content(role="tool", ...)` |
| `test_get_files_info.py` | Unit tests for the `get_files_info` function (4 tests) |
| `test_get_file_content.py` | Unit tests for the `get_file_content` function (5 tests, creates temporary test files) |
| `test_write_file.py` | Unit tests for the `write_file` function (3 tests, with cleanup) |
| `test_run_python_file.py` | Unit tests for the `run_python_file` function (6 tests) |
| `test_function_schemas.py` | Unit tests for all four `FunctionDeclaration` schemas (6 tests) |
| `integration_test_call_function.py` | Integration tests for `call_function` dispatch — no network calls (9 tests, `make integration_test`) |

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
- `generate_content(client, messages, verbose=False)` — makes the API call with `system_instruction=system_prompt` and `tools=[available_functions]` via `types.GenerateContentConfig`. Validates metadata, prints token usage if `verbose=True`. If `response.function_calls` is non-empty, calls `call_function` for each, validates the returned `Content` (non-empty parts, non-None `function_response` and `.response`), and accumulates `parts[0]` into a `function_results` list. Prints verbose response if enabled. Otherwise prints `response.text`.

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

## Agent Tools

Functions in the `functions/` directory that the AI agent can call to perform actions.

### `get_files_info(working_directory, directory=".")`

Lists the contents of a directory with metadata (file name, size in bytes, and whether it's a directory).

**Security feature:** The `working_directory` parameter restricts the agent's view. Any attempt to escape outside this directory (e.g., using `../` or absolute paths like `/bin`) returns an error. This prevents the agent from accessing sensitive files or locations.

**Returns:** A formatted string with one line per entry:
```
- filename: file_size=1234 bytes, is_dir=False
- dirname: file_size=5678 bytes, is_dir=True
```

Or an error string if the target directory is invalid or outside the working directory.

**Test:** Run `uv run test_get_files_info.py` to verify the function.

### `get_file_content(working_directory, file_path)`

Reads and returns the contents of a file relative to a working_directory.

**Security features:**
- The `working_directory` parameter restricts file access. Absolute paths or paths that escape the working directory (e.g., `../../../etc/passwd`) are blocked.
- Files are read with a maximum character limit (`MAX_FILE_CHARS = 10000`) to prevent token exhaustion when sending large files to the LLM.
- If a file is larger than the limit, it is truncated with a message indicating the truncation point.

**Returns:** The file contents as a string (up to 10,000 characters), or an error string if the file is outside the working directory, doesn't exist, or is not a regular file.

**Example output:**
```
# For a small file:
import sys
...

# For a large file:
Lorem ipsum dolor sit amet...
[...File "lorem.txt" truncated at 10000 characters]
```

**Test:** Run `uv run test_get_file_content.py` to verify the function.

### `write_file(working_directory, file_path, content)`

Writes content to a file relative to a working_directory. Creates parent directories automatically if needed.

**Security features:**
- The `working_directory` parameter restricts where files can be written. Absolute paths or paths that escape the working directory are blocked.
- Cannot write to existing directories (only to files).
- Returns success/error feedback for the LLM to confirm the action.

**Parameters:**
- `working_directory`: Base directory to restrict access to
- `file_path`: Relative path to the file to write
- `content`: The text content to write

**Returns:** A success message with the character count written, or an error string if validation fails or writing fails.

**Example output:**
```
Successfully wrote to "pkg/morelorem.txt" (26 characters written)
```

**Test:** Run `uv run test_write_file.py` to verify the function.

### `run_python_file(working_directory, file_path, args=None)`

Executes a Python file within a working_directory with optional command-line arguments.

**Security features:**
- The `working_directory` parameter restricts code execution. Only Python files within this directory can be executed.
- Only `.py` files can be executed (prevents accidental execution of non-Python files).
- **30-second timeout** to prevent infinite execution or resource exhaustion.
- Returns stdout/stderr separately so the LLM can see both output and errors.

**⚠️  SECURITY WARNING:** This function allows arbitrary Python code execution within the working directory. This is intentionally limited for educational purposes. **Do NOT use this in production or with untrusted inputs.** The LLM could potentially:
- Read/write files outside the working directory (if you're not careful with isolation)
- Consume resources
- Call external commands
- Access network connections

**Parameters:**
- `working_directory`: Base directory to restrict execution to
- `file_path`: Relative path to the Python file to execute
- `args`: Optional list of command-line arguments to pass to the script

**Returns:** 
- On success: Combined output string with optional exit code and STDOUT/STDERR labels
- On error: Error string describing why execution failed

**Example output:**
```
STDOUT:
{
  "expression": "3 + 5",
  "result": 8
}
```

**Test:** Run `uv run test_run_python_file.py` to verify the function.

---

## Configuration

| File | Purpose |
|---|---|
| `config.py` | Configuration constants (e.g., `MAX_FILE_CHARS = 10000` for file truncation limit) |

---

## Assumptions & Known Constraints

- The program is stateless — no conversation history is maintained between runs.
- The prompt is supplied as a required positional CLI argument; running without one will print usage help and exit.
- Error handling covers two cases: missing `GEMINI_API_KEY` environment variable, and a `None` `usage_metadata` on the response (which would indicate a failed API request).

---

## Next Steps for Agent Development

**Phase 1: Tool Integration (Immediate)**
- Integrate the four agent tools with the Gemini API using tool/function calling
- Parse tool responses from the LLM and execute corresponding functions
- Return tool results back to the model for iterative reasoning

**Phase 2: Conversation Loop (Important)**
- Implement multi-turn conversation with message history
- Allow the agent to reason through tasks over multiple turns
- Test with the calculator project as a workflow example

**Phase 3: Extended Capabilities (Future)**
- Add error recovery and retry logic for failed tool calls
- Implement cost/token budgeting to manage API usage
- Add support for additional tools (file deletion, directory creation, etc.)
- Persistent session state if needed

**Phase 4: Production Hardening (Later)**
- Comprehensive input validation and sanitization
- Rate limiting and request throttling
- Audit logging of agent actions
- Formal security review for production use
