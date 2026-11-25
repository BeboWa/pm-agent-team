import json
from pathlib import Path

import pytest

import shared.llm as llm
from tests.fakes import FakeClient

ROOT = Path(__file__).resolve().parent.parent
SAMPLE = ROOT / "examples" / "company_dossier_sample.json"


@pytest.fixture
def sample():
    return json.loads(SAMPLE.read_text())


@pytest.fixture
def fake_api(monkeypatch, tmp_path):
    """Replace the Anthropic client, send all output to a temp folder, and start with a clean call log."""
    FakeClient.calls = []
    monkeypatch.setattr(llm.anthropic, "Anthropic", FakeClient)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    monkeypatch.setenv("PM_OUTPUT_DIR", str(tmp_path / "out"))
    llm.RUN_LOG.clear()
    return FakeClient
