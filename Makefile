default: help

.PHONY: help
help:
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done

.PHONY: sync
.SILENT: sync
sync: # Sync all packages
	uv sync --all-packages

.PHONY: lint
.SILENT: lint
lint: # Run the linter
	uv run mypy .
	uv run ruff check .
	uv run ruff format . --check

.PHONY: format
.SILENT: format
format: # Format the code
	uv run ruff check . --fix
	uv run ruff format .
