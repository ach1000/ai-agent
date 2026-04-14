.PHONY: sync run test calculator_test calculator_run

sync:
	uv sync

run:
	uv run main.py "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."

test:
	uv run calculator/tests.py
	uv run test_get_files_info.py

calculator_test:
	uv run calculator/tests.py

calculator_run:
	uv run calculator/main.py $(ARGS)
