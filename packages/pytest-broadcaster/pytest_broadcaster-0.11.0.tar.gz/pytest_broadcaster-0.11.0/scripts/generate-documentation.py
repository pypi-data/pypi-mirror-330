"""Generate the code reference pages."""

from __future__ import annotations

import json
import os
import shutil
from os import environ
from pathlib import Path
from typing import Any
from urllib.parse import urljoin

import mkdocs_gen_files.nav

REPOSITORY = "https://charbonnierg.github.io/pytest-broadcaster"

SOURCES = Path(__file__).parent.parent.joinpath("src/schemas")


def replace_refs_and_ids(schema: dict[str, Any], ref_prefix: str) -> None:
    """Replace host in $ref and $id fields in given JSON schema definition."""
    if "$ref" in schema:
        ref_template: str = schema["$ref"]
        ref_value = ref_template.split("/")[0]
        schema["$ref"] = f"{ref_prefix}/{ref_value}"
    if "$id" in schema:
        id_value = schema["$id"]
        schema["$id"] = f"{ref_prefix}/{id_value}"
    for value in schema.values():
        if isinstance(value, dict):
            replace_refs_and_ids(value, ref_prefix)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    replace_refs_and_ids(item, ref_prefix)


def create_schema(source: Path, output_directory: Path, ref_prefix: str) -> None:
    """Create JSON schema in output directory given some source file and prefix."""
    destination = output_directory.joinpath(source.name)
    content = json.loads(source.read_text())
    replace_refs_and_ids(content, ref_prefix)
    destination.write_text(json.dumps(content, indent=2))


def generate_schemas(version: str, repository: str, output_directory: str) -> None:
    """Generate JSON schemas for a given version and git repository."""
    # Validate reference and output
    if not (version and repository and output_directory):
        error = "version, repository and output_directory must not be empty"
        raise ValueError(error)
    if output_directory.startswith("/"):
        error = "output must be a relative relative path"
        raise ValueError(error)
    ref_prefix = repository
    if not ref_prefix.endswith("/"):
        ref_prefix += "/"
    # Join with version
    ref_prefix = urljoin(ref_prefix, version)
    # Clean output directory
    destination = Path(output_directory)
    shutil.rmtree(destination, ignore_errors=True)
    destination.mkdir(parents=False, exist_ok=True)
    # Normalize repository and output
    if not ref_prefix.endswith("/"):
        ref_prefix += "/"
    if output_directory.endswith("/"):  # noqa: FURB188
        output_directory = output_directory[:-1]
    # Build full repository URL
    target = output_directory
    if target.startswith("docs"):
        target = target[5:]
    ref_prefix = urljoin(ref_prefix, target)
    # Generate all schemas
    schemas: dict[str, dict[str, Any]] = {}
    for source in SOURCES.glob("*.json"):
        module = source.name.replace(".json", "")
        schema_content = json.loads(source.read_text())
        title = "".join(
            [
                part.capitalize()
                for part in schema_content.get("title", module).split(" ")
            ]
        )
        schema_import = f"pytest_broadcaster.models.{module}.{title}"
        schema_url = f"{ref_prefix}/{source.name}"
        schema_description = schema_content.get("description", "")
        name = f"[{title}][{schema_import}]"
        schemas[name] = {
            "description": schema_description,
            "url": schema_url,
        }
        create_schema(
            source=source, output_directory=destination, ref_prefix=ref_prefix
        )
    generate_schemas_index(schemas)


def generate_schemas_index(schemas: dict[str, dict[str, Any]]) -> None:
    """Generate the schemas index page."""
    with mkdocs_gen_files.open("schemas/index.md", "w") as index:
        content = ""
        content += "# JSON Schemas"
        content += "\n\n"
        content += "The table below contains the JSON schemas used in the project:"
        content += "\n\n"
        content += "| Schema | Description | URL |"
        content += "\n"
        content += "| ------ | ----------- | --- |"
        content += "\n"
        for schema_name, schema in schemas.items():
            schema_desc = schema["description"]
            schema_url = schema["url"]
            row = f"| {schema_name} | {schema_desc} | [{schema_url}]({schema_url}) |"
            content += row
            content += "\n"
        index.write(content)


def generate_license_file() -> None:
    """Generate the LICENSE.md file."""
    with mkdocs_gen_files.open("LICENSE.md", "w") as docs_license_file:
        repo_license_file = Path("LICENSE")
        if repo_license_file.is_file():
            content = repo_license_file.read_text()
            content += "\n\n"
            content += """
<style>
  .md-content__button {
    display: none;
  }
</style>
"""
            docs_license_file.write(content)
        else:
            docs_license_file.write("No license file found")


generate_license_file()
generate_schemas(
    version=os.environ.get("VERSION", "latest"),
    repository=environ.get("REPOSITORY", REPOSITORY),
    output_directory="docs/schemas",
)
