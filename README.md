# AI Agent Project

An educational AI agent built with Google's Gemini API that can read, write, and execute code. This is a learning project demonstrating how to build an agent with tool-calling capabilities and safety guardrails.

## Overview

This project is a scaffold for building an AI agent using the Gemini API. The agent can currently:

- **Read directories** — List files and their metadata
- **Read files** — Display file contents (with truncation at 10k characters)
- **Write files** — Create and modify files with path validation
- **Execute code** — Run Python scripts safely with a 30-second timeout

All operations are restricted to a designated working directory for safety.

## Quick Start

### Prerequisites
- Python ≥ 3.13
- Google Gemini API key (from [Google AI Studio](https://aistudio.google.com))

### Setup

1. **Install dependencies:**
   ```bash
   make sync
   ```

2. **Create a `.env` file** with your API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

3. **Run tests** to verify everything works:
   ```bash
   make test
   ```

4. **Try the agent:**
   ```bash
   make run
   ```

## Project Structure

```
├── calculator/              # Test project - a calculator app
│   ├── main.py
│   ├── tests.py            # 9 unit tests
│   ├── lorem_ipsum.txt     # Test data
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── functions/              # Agent tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── main.py                 # Entry point
├── config.py               # Configuration constants
├── Makefile                # Build targets
├── PROJECT.md               # Technical documentation (for next agent)
└── README.md               # This file
```

## Available Commands

| Command | Purpose |
|---------|---------|
| `make sync` | Install dependencies |
| `make run` | Run the agent with a sample prompt |
| `make test` | Run all 27 unit tests |
| `make calculator_test` | Run calculator tests only |
| `make calculator_run ARGS="3 + 5"` | Test the calculator directly |

## Agent Tools

The agent has access to four tools:

### 1. `get_files_info(working_directory, directory)`
Lists directory contents with file metadata (size, type).

```
- main.py: file_size=719 bytes, is_dir=False
- pkg: file_size=5992 bytes, is_dir=True
```

### 2. `get_file_content(working_directory, file_path)`
Reads file contents. Large files are truncated at 10,000 characters.

### 3. `write_file(working_directory, file_path, content)`
Writes or overwrites files. Creates parent directories automatically.

### 4. `run_python_file(working_directory, file_path, args)`
Executes Python scripts with optional arguments. 30-second timeout enforced.

## Test Project: Calculator

A command-line calculator app is included to demonstrate agent capabilities:

```bash
# Run the calculator directly
uv run calculator/main.py "3 + 5"
# Output: {"expression": "3 + 5", "result": 8}

# Run calculator tests
uv run calculator/tests.py
# All 9 tests pass
```

The calculator supports `+`, `-`, `*`, `/` with proper operator precedence.

## Testing

The project includes comprehensive unit tests across five test modules:

| Module | Tests | Purpose |
|--------|-------|---------|
| `calculator/tests.py` | 9 | Calculator functionality |
| `test_get_files_info.py` | 4 | Directory listing |
| `test_get_file_content.py` | 5 | File reading with truncation |
| `test_write_file.py` | 3 | File writing |
| `test_run_python_file.py` | 6 | Python execution |

**Total: 27 tests, all passing** ✓

Run all tests with:
```bash
make test
```

## Security Notes

⚠️ **Important:** This is an educational project, not production-ready.

**Safety features implemented:**
- Path validation prevents access outside working directory
- File size limits prevent token exhaustion
- Execution timeout prevents infinite loops
- Python file validation prevents arbitrary code execution
- Error strings returned instead of exceptions for LLM resilience

**Known limitations:**
- No authentication or authorization
- No rate limiting or API quota management
- Minimal input sanitization
- The LLM can run arbitrary code within the working directory

**Do NOT use this with untrusted inputs or in production.** It's designed for learning purposes only.

## Architecture

The current implementation is a minimal scaffold:

1. **User provides a prompt** via CLI
2. **Agent calls Gemini API** with the prompt
3. **Model generates a response** and returns it
4. **Output is printed** to the user

The next phase will add:
- Tool calling integration (LLM invokes functions)
- Multi-turn conversation
- Message history
- Iterative task completion

See [PROJECT.md](PROJECT.md) for detailed technical documentation and development roadmap.

## Dependencies

- `google-genai` — Gemini API client
- `python-dotenv` — Environment variable management
- `uv` — Package manager (not pip)

## License

Educational project for learning purposes.
