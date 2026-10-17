# py-ev

Python discrete event loop. src layout: the package is `src/pyev/`, tests are in `tests/`.

## Tooling

Managed with uv. See the README's Development section for commands.

- Common commands live in `Taskfile.yml`. If `task` isn't installed, run it via `uvx --from go-task-bin task <name>`.
- `uv run pre-commit run --all-files` runs everything: ruff check, ruff format, ty, pytest (including doctests).
- Hooks call `uv run --locked`, so after changing dependencies run `uv lock` or the hooks fail.
- CI (`.github/workflows/ci.yml`) runs the same pre-commit hooks on PRs. On `main` it only runs when `uv.lock` changes, to refresh the uv cache that PRs restore from.
- The CI job `pre-commit` is a required status check in the `main` ruleset. Renaming the job breaks merging until the ruleset is updated to the new name.
- Workflows and shell scripts aren't covered by the hooks. Lint them by hand after changes: `uvx --from actionlint-py actionlint .github/workflows/*.yml` and `uvx --from shellcheck-py shellcheck .github/scripts/*.sh`.
- Pin GitHub Actions to exact versions. `astral-sh/setup-uv` doesn't publish floating major tags (`@v10` fails).

## Versioning

- Single source: `version` in `pyproject.toml`. Never hard-code it elsewhere. `pyev.__version__` uses `importlib.metadata`.
- Releases happen on merge. `.github/workflows/release.yml` runs on every push to `main`: if `v<version>` isn't tagged yet, it builds, tags and publishes a GitHub Release. On PRs it's a dry run.
- **Feature PRs never change the version.** A release is its own PR that only bumps the version (`task bump -- <part>`, which wraps `uv version --bump`) and releases whatever is on `main`. Never create or push `v*` tags by hand.
- On PRs, the Release workflow fails if the PR changes the version to one that's already tagged. Otherwise that bump would be silently skipped after merge. Its logic is in `.github/scripts/release-check.sh`.
- Hotfixes: fix forward. Merge the fix, then a patch-bump PR, which keeps `main` releasable. Release branches (`release/X.Y` from a tag, with the fix merged to `main` first and then cherry-picked with `git cherry-pick -x`) are the agreed fallback but aren't set up yet. They'd need the release workflow and ruleset extended to `release/**`, plus `--latest=false` and `--notes-start-tag` handling.
- **Merging a PR that changes the version publishes a release, so ask before merging it.** The squash-merge permission below doesn't cover version bumps.
- A tag created by the workflow's `GITHUB_TOKEN` doesn't trigger other workflows, so release work belongs in `release.yml` itself.

## Workflow

- Work on a branch, open a PR against `main`.
- **PRs with passing CI may always be squash-merged** (`gh pr merge --squash --delete-branch`) without asking first. Confirm CI is green (`gh pr checks <n> --watch`) before merging; never merge with failing or pending checks.
- The `main` ruleset requires PRs to be up to date. If a PR falls behind after another merge, run `gh pr update-branch <n>` and wait for CI again.
