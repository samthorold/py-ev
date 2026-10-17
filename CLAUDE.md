# py-ev

Python discrete event loop. src layout: the package is `src/pyev/`, tests are in `tests/`.

## Tooling

Managed with uv. See the README's Development section for commands.

- Common commands live in `Taskfile.yml`. If `task` isn't installed, run it via `uvx --from go-task-bin task <name>`.
- `uv run pre-commit run --all-files` runs everything: ruff check, ruff format, ty, pytest (including doctests).
- Hooks call `uv run --locked`, so after changing dependencies run `uv lock` or the hooks fail.
- CI (`.github/workflows/ci.yml`) runs the same pre-commit hooks on PRs and pushes to `main`.
- The CI job `pre-commit` is a required status check in the `main` ruleset. Renaming the job breaks merging until the ruleset is updated to the new name.
- Pin GitHub Actions to exact versions. `astral-sh/setup-uv` doesn't publish floating major tags (`@v10` fails).

## Versioning

- Single source: `version` in `pyproject.toml`. Never hard-code it elsewhere. `pyev.__version__` uses `importlib.metadata`.
- Releases happen on merge. `.github/workflows/release.yml` runs on every push to `main`: if `v<version>` isn't tagged yet, it builds, tags and publishes a GitHub Release. On PRs it's a dry run.
- Bump with `task bump -- <part>` (wraps `uv version --bump`) in a PR. Never create or push `v*` tags by hand.
- **Merging a PR that changes the version publishes a release, so ask before merging it.** The squash-merge permission below doesn't cover version bumps.
- A tag created by the workflow's `GITHUB_TOKEN` doesn't trigger other workflows, so release work belongs in `release.yml` itself.

## Workflow

- Work on a branch, open a PR against `main`.
- **PRs with passing CI may always be squash-merged** (`gh pr merge --squash --delete-branch`) without asking first. Confirm CI is green (`gh pr checks <n> --watch`) before merging; never merge with failing or pending checks.
