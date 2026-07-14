PYTHON := 3.12
UV := uv

.PHONY: help install run check clean

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*## "} /^[a-zA-Z_-]+:.*## / {printf "%-12s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install the locked project dependencies
	$(UV) sync --python $(PYTHON) --locked

run: ## Run the salary calculator
	$(UV) run python main.py

check: ## Check that the Python source compiles
	$(UV) run python -m compileall -q main.py salary_calculator

clean: ## Remove generated Python and build artifacts
	rm -rf __pycache__ .pytest_cache .ruff_cache .mypy_cache build dist *.egg-info
	find . -type f -name '*.py[oc]' -delete
