"""One place that decides where reports are read from and written to.

By default everything goes in ./outputs. The Orchestrator's --client option points this at
runs/<client>/<timestamp>/ so each client's work stays separate. Override with PM_OUTPUT_DIR.
"""
import os
from pathlib import Path


def out_dir() -> Path:
    return Path(os.environ.get("PM_OUTPUT_DIR", "outputs"))


def out_file(name: str) -> Path:
    """Path of a report in the current output folder (does not create anything)."""
    return out_dir() / name


def out_path(name: str) -> Path:
    """Like out_file, but makes sure the folder exists (use when writing)."""
    d = out_dir()
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def set_out_dir(path) -> None:
    os.environ["PM_OUTPUT_DIR"] = str(path)
