.PHONY: sync run test calculator_test calculator_run

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

calculator_test:
	uv run calculator/tests.py

calculator_run:
	uv run calculator/main.py $(ARGS)
