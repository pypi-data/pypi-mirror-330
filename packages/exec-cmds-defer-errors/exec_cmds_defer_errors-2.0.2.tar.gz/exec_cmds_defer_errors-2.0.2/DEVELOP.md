# Develop!

This document is targeted at project developers. It helps people to make their
first steps. It also serves as a general entry to development documentation like
tooling configuration and usage.

The environment is expected to be Unix-like.

For core development activities, [uv](https://docs.astral.sh/uv/) is sufficient.
Other stuff just comes on top and is in any case handled by GitHub Actions. For
a complete development environment (Git hooks, Markdown formatting, etc.), the
following tools are required:

- [Copier](https://copier.readthedocs.io/en/stable/) for project templating.
- [Just](https://github.com/casey/just) for running self-documenting tasks.
- [Mdformat](https://github.com/hukkin/mdformat) for Markdown formatting.
- [Pre-commit](https://pre-commit.com/) for managing pre-commit hooks.
- [ShellCheck](https://github.com/koalaman/shellcheck) for shell script linting.
- [Shfmt](https://github.com/mvdan/sh) for shell script formatting.
- [Uv](https://docs.astral.sh/uv/) for managing Python and friends.

Same goes for the following utilities:

- [Exec-cmds-defer-errors](https://pypi.org/project/exec-cmds-defer-errors/).
- [Filter-pre-commit-hooks](https://pypi.org/project/filter-pre-commit-hooks/).

Common tasks like initialization and runnings tests are covered by and
documented in [`Justfile`](./Justfile). To run a complete suite of tasks, just
invoke `just` without arguments.

This projects supports [Development Containers](https://containers.dev/). Check
out [`.devcontainer/README.md`](./.devcontainer/README.md) for more information.
