# BloomFlow

BloomFlow is a CrewAI-based multi-agent workflow project designed to transform user input into a refined result through coordinated research, analysis, generation, and review stages. Each specialized agent is intended to contribute to the final output, while the workflow coordinates sequence and consistency.

The name reflects the intended progression: a simple input moves through specialized stages and develops into a complete result. The design leaves room for future research, writing, review, and fact-checking agents.

This repository is a standalone workspace for building and refining that AI workflow outside a FastAPI application. The intended package boundary is named `ai_workflow`: broad enough to hold CrewAI orchestration, memory, persistence, repositories, and supporting services without coupling them to an API project's dependencies or release cycle.

This repository is intended first as a practical reference for its maintainer and also as a public learning resource. When a design is stable, it can be adapted into a separate FastAPI project; this repository is not currently connected to that application.

## Why keep it separate?

AI workflows often change quickly: agents and prompts are revised, features are tried or removed, and supporting infrastructure evolves. Keeping this work in its own project makes it easier to experiment without disrupting an API backend or duplicating that backend's Redis and repository implementation prematurely.

The intended boundary is:

- **This project (`ai_workflow`):** The independent AI subsystem—CrewAI logic and its supporting memory, persistence, repositories, and services. Its future `application/` directory belongs to this AI subsystem; it is not the FastAPI application's `app/` directory.
- **A future FastAPI project:** The API and its routers. A router can import and use the AI application class from `ai_workflow` while the API remains a separate host project.

The projects are deliberately independent for now. There is no FastAPI integration or shared runtime configured here. When integrating later, bring in the AI workflow source and the dependencies it needs—not its local virtual environment (`.venv`) or the FastAPI project's API layer. Any sharing of infrastructure, such as Redis, can be decided deliberately during that integration.

## Current status

This is an early scaffold, not yet a complete CrewAI template or a working multi-agent workflow. CrewAI is a dependency, but the repository does not currently define CrewAI agents, tasks, tools, or a crew kickoff flow. Research, analysis, generation, and review describe the intended direction; they are not implemented stages yet. The current `main.py` only prints a greeting.

The codebase also includes an initial Redis message-storage and Mem0 configuration scaffold. These pieces are not assembled into a working end-to-end agent workflow yet. Treat the setup and commands below as a way to install and inspect the scaffold, not as instructions for running a finished AI service.

## Current project structure

The existing scaffold is currently named `agentic_workflow/`. `ai_workflow` is the broader package name planned for the evolving design; the source package has not yet been renamed or reorganized.

```text
.
├── agentic_workflow/
│   ├── core/
│   │   └── config.py                 # Environment-based configuration
│   ├── repositories/
│   │   ├── base_repository.py        # Redis lifecycle and Mem0 configuration
│   │   └── message_repository.py     # Redis key/value operations
│   └── services/
│       └── message_service.py        # JSON message-history operations
├── main.py                           # Current greeting-only entry point
├── pyproject.toml                    # Project metadata and dependencies
├── uv.lock                           # Locked dependency versions
└── .python-version                   # Python 3.12
```

## Requirements

- Python 3.12 or newer (the project is configured for Python 3.12)
- [uv](https://docs.astral.sh/uv/) for dependency management
- Redis at `127.0.0.1:6379` if you run code that uses the Redis repository
- Provider and vector-store credentials if you use the Mem0 configuration

## Setup

Clone the repository, then install its locked dependencies:

```bash
uv sync
```

The current entry point can be run with:

```bash
uv run python main.py
```

At this stage, that command only prints a greeting. It does not start Redis, initialize Mem0, or run a CrewAI workflow. No automated test suite is currently configured.

## Configuration

Configuration is loaded from environment variables, with `.env` loaded when the configuration module is used. Create a local `.env` file for credentials; do not commit real secrets.

| Variable | Purpose | Default |
| --- | --- | --- |
| `GROQ_API_KEY` | Groq credential for the Mem0 LLM configuration | None |
| `COHERE_API_KEY` | Cohere credential for embeddings | None |
| `MILVUS_URI` | Milvus vector-store URI | None |
| `MILVUS_TOKEN` | Milvus credential | None |
| `MEM_ZERO_COLLECTION_NAME` | Mem0/Milvus collection name | `mem_zero_collection` |
| `COHERE_EMBEDDING_MODEL_NAME` | Cohere embedding model | `embed-v4.0` |
| `MEM_ZERO_LLM_MODEL_NAME` | Mem0 LLM model identifier | `openai/gpt-oss-120b` |

The Mem0 setup currently selects Milvus as its vector store, Groq as its LLM provider, and Cohere for embeddings. Redis is configured in the repository code with the local URL `redis://127.0.0.1:6379`; a configurable Redis URL and service orchestration have not been added yet. These settings are relevant only when using those scaffold components, not when running the greeting-only entry point.

## Development direction

The project is expected to grow through small experiments and refactors. Possible next steps include:

- Build a working CrewAI example with explicit agents, tasks, tools, and a kickoff flow.
- Clarify and test the boundaries between workflow logic, repositories, and services.
- Make Redis and external provider configuration explicit and easy to run locally.
- Add examples and tests for message persistence and memory.
- Document the FastAPI integration after that integration has been implemented and its interface is clear.
- Add project guidance for AI coding tools (for example, a root `AGENTS.md` plus tool-specific instructions where needed). The guidance should explain the architecture, conventions, and verification steps so coding agents can make changes without casually breaking project boundaries.

These are intentions, not existing features. Instructions for coding agents should complement code review and tests rather than replace them.

## Reuse and publishing

BloomFlow is currently a reference and experimental workspace, not a packaged service with a stable public API. If you plan to invite others to reuse its code, add an appropriate license and document which parts are stable first.
