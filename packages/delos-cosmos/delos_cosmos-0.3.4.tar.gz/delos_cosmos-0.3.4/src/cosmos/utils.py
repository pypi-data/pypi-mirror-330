"""Utility functions for the Cosmos API client."""

import json
from collections.abc import Generator
from contextlib import suppress
from pathlib import Path
from typing import IO, Any

import requests

from .exceptions import InvalidInputError


def read_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]:
    """Process the streaming response and yield parsed data."""
    for line in response.iter_lines():
        if not line:
            continue

        line_read = line.decode("utf-8")
        if line_read == "data: [DONE]":
            break

        if line_read.startswith("data: "):
            data = line_read[6:]
            with suppress(json.JSONDecodeError):
                yield json.loads(data)

        elif line_read.startswith("0:"):
            yield line_read[2:].strip('"')


def process_streaming_response(response: requests.Response) -> Generator[str, None, None]:
    """Process the streaming response and yield raw data lines."""
    for line in response.iter_lines():
        if line:
            yield line.decode("utf-8")


def _check_file(filepath: Path | str | None, fileobject: tuple[str, IO[bytes]] | None) -> None:
    """Check if filepath and / or fileobject are provided."""
    if not filepath and not fileobject:
        error_message = "Either filepath or fileobject must be provided."
        raise InvalidInputError(error_message)

    if filepath and fileobject:
        error_message = "Provide either filepath or fileobject, not both."
        raise InvalidInputError(error_message)


def _check_files(
    filepaths: list[Path] | list[str] | None,
    filesobjects: list[tuple[str, IO[bytes]]] | None = None,
) -> None:
    """Check if filepath and / or fileobject are provided."""
    if not filepaths and not filesobjects:
        error_message = "Either filepaths or filesobjects must be provided."
        raise InvalidInputError(error_message)

    if filepaths and filesobjects:
        error_message = "Provide either filepaths or filesobjects, not both."
        raise InvalidInputError(error_message)


def load_file(
    filepath: Path | str | None = None,
    fileobject: tuple[str, IO[bytes]] | None = None,
) -> list[tuple[str, Any]]:
    """Load a file content."""
    _check_file(filepath, fileobject)
    if filepath:
        path = Path(filepath) if isinstance(filepath, str) else filepath
        with path.open("rb") as file:
            return [("file", (path.name, file.read()))]

    elif fileobject:
        filename, file_object = fileobject
        return [("file", (filename, file_object.read()))]
    return []


def load_files(
    filepaths: list[Path] | list[str] | None = None,
    fileobjects: list[tuple[str, IO[bytes]]] | None = None,
) -> list[tuple[str, Any]]:
    """Load files contents."""
    _check_files(filepaths, fileobjects)

    files = []
    if filepaths:
        for fp in filepaths:
            path = Path(fp) if isinstance(fp, str) else fp
            with path.open("rb") as file:
                files.append(("files", (path.name, file.read())))

    elif fileobjects:
        for filename, file_object in fileobjects:
            files.append(("files", (filename, file_object.read())))
    return files
