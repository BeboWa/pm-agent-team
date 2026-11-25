import json
import sys

import pytest

from agents.orchestrator.run import main
from tests.fakes import FakeClient

SAMPLE = "examples/company_dossier_sample.json"
FEEDBACK = "examples/feedback_sample.json"


def run_cli(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["orchestrator", *args])
    main()


def test_full_pipeline_runs_in_a_separate_client_folder(fake_api, monkeypatch, tmp_path):
    run_cli(monkeypatch, SAMPLE, "--feedback", FEEDBACK, "--full", "--client", "Acme Inc",
            "--runs-dir", str(tmp_path / "runs"), "--no-log")
    run_dir = next((tmp_path / "runs" / "acme-inc").iterdir())
    for f in ["diagnostic_report.md", "pricing_billing_report.md", "prd_item_1.md", "review_report.md",
              "executive_brief.md", "pipeline_summary.md", "manifest.json",
              "deliverables/deck.pptx", "deliverables/report.docx", "deliverables/readout_prep.md",
              "inputs/company_dossier_sample.json"]:
        assert (run_dir / f).exists(), f
    manifest = json.loads((run_dir / "manifest.json").read_text())
    assert manifest["status"] == "completed" and manifest["client"] == "Acme Inc"
    assert len(manifest["stages"]) == 11
    assert all(not s["missing"] and not s["truncated"] for s in manifest["stages"])
    assert manifest["totals"]["cost_usd"] > 0 and manifest["inputs"]["dossier"]["sha256_prefix"]


def test_two_clients_never_share_a_folder(fake_api, monkeypatch, tmp_path):
    for name in ("Client A", "Client B"):
        run_cli(monkeypatch, SAMPLE, "--client", name, "--runs-dir", str(tmp_path / "runs"), "--no-log")
    assert sorted(p.name for p in (tmp_path / "runs").iterdir()) == ["client-a", "client-b"]


def test_invalid_dossier_stops_before_any_model_call(fake_api, monkeypatch, tmp_path):
    bad = json.loads(open(SAMPLE).read()); bad["mrr_end"] = 999_999
    p = tmp_path / "bad.json"; p.write_text(json.dumps(bad))
    with pytest.raises(SystemExit):
        run_cli(monkeypatch, str(p), "--no-log")
    assert FakeClient.calls == []


def test_missing_api_key_gives_a_clear_message(fake_api, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY")
    with pytest.raises(SystemExit, match="ANTHROPIC_API_KEY"):
        run_cli(monkeypatch, SAMPLE, "--no-log")


def test_basic_run_without_client_writes_to_the_default_output_folder(fake_api, monkeypatch, tmp_path):
    run_cli(monkeypatch, SAMPLE, "--no-log")
    out = tmp_path / "out"
    assert (out / "diagnostic_report.md").exists() and (out / "prd_item_1.md").exists()
    assert not (out / "deliverables").exists()  # only built with --full
