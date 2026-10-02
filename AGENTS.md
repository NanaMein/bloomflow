# Repository guidance

- Use Python 3.12 and `uv`: install with `uv sync`; run the current entry point with `uv run python main.py`.
- `main.py` only prints a greeting. CrewAI is a dependency, but there are no implemented agents, tasks, crew kickoff, or FastAPI integration yet; do not assume these scaffolds are connected.
- The current import package is `agentic_workflow/`. `ai_workflow` is the README's planned name, not an existing package.
- Existing code is grouped under `agentic_workflow/core` (environment config), `repositories` (Redis and Mem0 setup/storage), and `services` (message-history operations). The Redis repository uses `redis://127.0.0.1:6379`; repository use requires Redis, while `main.py` does not.
- `core/config.py` loads `.env` when imported. Mem0 setup additionally expects the provider/vector-store settings documented in `README.md`; these are not prerequisites for running `main.py`.
- No automated tests, CI, or test/type-check commands are configured. Ruff is a dev dependency; a basic lint check is `uv run ruff check .`.
