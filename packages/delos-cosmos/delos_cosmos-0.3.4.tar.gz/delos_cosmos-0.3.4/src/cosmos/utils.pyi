from collections.abc import Generator
from pathlib import Path
from typing import IO, Any

import requests

def read_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]: ...
def process_streaming_response(response: requests.Response) -> Generator[dict[str, Any], None, None]: ...
def load_file(
    filepath: Path | str | None = None,
    fileobject: tuple[str, IO[bytes]] | None = None,
) -> list[tuple[str, Any]]: ...
def load_files(
    filepaths: list[Path] | list[str] | None = None,
    fileobjects: list[tuple[str, IO[bytes]]] | None = None,
) -> list[tuple[str, Any]]: ...
