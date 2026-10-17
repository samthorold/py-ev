# py-ev

Python discrete event loop (`pyev/`).

## Tooling

Managed with uv. See the README's Development section for commands.

- Common commands live in `Taskfile.yml`. If `task` isn't installed, run it via `uvx --from go-task-bin task <name>`.
- `uv run pre-commit run --all-files` runs everything: ruff check, ruff format, ty, pytest (including doctests).
- Hooks call `uv run --locked`, so after changing dependencies run `uv lock` or the hooks fail.
- CI (`.github/workflows/ci.yml`) runs the same pre-commit hooks on PRs and pushes to `main`.
- The CI job `pre-commit` is a required status check in the `main` ruleset. Renaming the job breaks merging until the ruleset is updated to the new name.
- Pin GitHub Actions to exact versions. `astral-sh/setup-uv` doesn't publish floating major tags (`@v10` fails).

## Workflow

- Work on a branch, open a PR against `main`.
- **PRs with passing CI may always be squash-merged** (`gh pr merge --squash --delete-branch`) without asking first. Confirm CI is green (`gh pr checks <n> --watch`) before merging; never merge with failing or pending checks.
