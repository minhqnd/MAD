# Repository Guidelines

## Project Structure & Module Organization
The repo currently contains `debai.txt`, which records the assignment brief; leave it untouched so reviewers can trace the requirements. Place executable code under `src/` (for example, `src/trees/expr_tree.py` with the `ExpressionTree` class plus traversal helpers) and keep any command-line entry point in `src/main.py`. Put fixtures and sample expressions from the brief into `tests/data/` so they can be reused across test cases, and add supporting notes or design sketches in `docs/` if needed.

## Build, Test, and Development Commands
Run `python -m venv .venv && source .venv/bin/activate` before installing dependencies. Use `python -m pip install -r requirements.txt` to sync tooling (formatters, pytest). Launch the CLI or demo runner with `python -m src.main --expr "(1+2)*(3+4)"`, which should print traversals plus evaluations. Execute the test suite and linters in one go with `pytest && ruff check src tests`, or run `pytest tests/test_traversals.py -k prefix` while iterating on a specific scenario.

## Coding Style & Naming Conventions
Follow Python 3.11 conventions: 4-space indentation, type hints on all public functions, and docstrings summarizing traversal behavior. Favor descriptive names such as `build_expression_tree`, `evaluate_postfix`, and `TraversalResult`. Keep modules narrow in scope (e.g., `parsers.py`, `evaluator.py`). Format code with `black .` and enforce import order with `ruff check --select I`; run these before every commit.

## Testing Guidelines
Use `pytest` with files named `test_*.py`; within each file mirror the module name (`test_evaluator.py`, etc.). Cover all tree construction and evaluation steps: one test per formula from `debai.txt`, plus property-style tests that assert prefix/postfix round-trips. Aim for ≥90 % branch coverage (`pytest --cov=src --cov-report=term-missing`). Store reusable arithmetic examples as JSON or plain text under `tests/data/expressions.json`.

## Commit & Pull Request Guidelines
Write commits in the imperative mood (`Add post-order evaluator`, `Refactor tree builder`). Keep diffs focused; batch unrelated cleanups separately. Pull requests must include a short summary, a checklist of commands run (`pytest`, `ruff`, etc.), links to any tracking issues, and screenshots or console excerpts showing sample CLI output. Highlight any new dependencies or deviations from the “no external traversal libraries” rule noted in `debai.txt`.
