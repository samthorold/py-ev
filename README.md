# py-ev

Python discrete event loop.

## Development

Tooling is managed with [uv](https://docs.astral.sh/uv/): ruff (lint + format),
ty (type checking) and pytest (tests + doctests).

```sh
uv sync                     # create .venv with dev tools
uv run pre-commit install   # install git hooks
make test                   # uv run pytest
make lint                   # ruff check, ruff format --check, ty check
make fmt                    # ruff fix + format
```
