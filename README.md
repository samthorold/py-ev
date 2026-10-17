# py-ev

Python discrete event loop.

## Development

Tooling is managed with [uv](https://docs.astral.sh/uv/): ruff (lint + format),
ty (type checking) and pytest (tests + doctests). Common commands are in
`Taskfile.yml`, run with [Task](https://taskfile.dev) (`brew install go-task`).

```sh
uv sync                     # create .venv with dev tools
uv run pre-commit install   # install git hooks
task                        # list tasks
task test                   # uv run pytest (extra args: task test -- -k name)
task lint                   # ruff check, ruff format --check, ty check
task fmt                    # ruff fix + format
```

## Releasing

The version lives in `pyproject.toml` only; `pyev.__version__` reads it from the
installed package metadata.

1. On a branch: `task bump -- patch|minor|major`, then open a PR and merge it.
2. On an up-to-date `main`: `task tag` creates and pushes `vX.Y.Z`.

The Release workflow fails if the tag doesn't match the `pyproject.toml` version.
