.PHONY: sync run

sync:
	uv sync

run:
	uv run main.py "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
