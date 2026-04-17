.PHONY: sync run test integration_test functional_test calculator_test calculator_run clean

sync:
	uv sync

run:
	uv run main.py "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

test:
	uv run calculator/tests.py
	uv run test_get_files_info.py
	uv run test_get_file_content.py
	uv run test_write_file.py
	uv run test_run_python_file.py
	uv run test_function_schemas.py

integration_test:
	uv run integration_test_call_function.py

functional_test:
	uv run main.py "how does the calculator render results to the console?"

calculator_test:
	uv run calculator/tests.py

calculator_run:
	uv run calculator/main.py $(ARGS)

clean:
	find . -path './.venv' -prune -o -type d \( -name '__pycache__' -o -name '.pytest_cache' -o -name '.mypy_cache' -o -name '.ruff_cache' -o -name 'htmlcov' \) -exec rm -rf {} +
	find . -type f ! -path './.venv/*' \( -name '*.pyc' -o -name '*.pyo' -o -name '.coverage' -o -name '.coverage.*' \) -delete
	rm -f calculator/pkg/morelorem.txt
