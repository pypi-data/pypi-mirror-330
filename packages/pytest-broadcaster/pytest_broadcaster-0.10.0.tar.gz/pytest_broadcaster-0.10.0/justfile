_list:
    just --list

[group("dev")]
install:
    uv sync --frozen

[group("dev")]
format:
    uv run ruff format
    uv run ruff check --select I --fix
    just --dump > justfile.fmt
    mv justfile.fmt justfile

[group("dev")]
check-format:
    uv run ruff format --check

[group("dev")]
check-code:
    uv run ruff check

[group("dev")]
check-types:
    uv run mypy src tests

[group("pre-commit")]
check: check-code check-format check-types check-schemas

[group("dev")]
test:
    uv run coverage run --rcfile=pyproject.toml -m pytest
    uv run coverage html
    uv run coverage report -m

[group("coverage")]
cov:
    #!/usr/bin/env python3
    import webbrowser
    import pathlib

    index = pathlib.Path.cwd() / "coverage-report/index.html"
    webbrowser.open(index.as_posix())

[group("package")]
version:
    uv run hatch --quiet build --hooks-only

[group("package")]
lock:
    uv sync --all-groups

[group("docs")]
docs:
    uv run mkdocs serve

[group("docs")]
deploy-docs: check-schemas
    uv run bash ./scripts/deploy-docs.sh

[group("schemas")]
generate-schemas:
    uv run datamodel-codegen --input src/schemas/ --output src/pytest_broadcaster/models --input-file-type jsonschema --disable-timestamp --output-model-type=dataclasses.dataclass --use-field-description --use-schema-description
    uv run ruff check --fix --unsafe-fixes
    uv run ruff format src/pytest_broadcaster/models

[group("schemas")]
check-schemas:
    rm -rf check
    uv run datamodel-codegen --input src/schemas/ --output check --input-file-type jsonschema --disable-timestamp --output-model-type=dataclasses.dataclass --use-field-description --use-schema-description
    uv run ruff check --fix-only --unsafe-fixes ./check
    uv run ruff format ./check
    diff --exclude __pycache__ -r src/pytest_broadcaster/models check
