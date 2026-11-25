import json

import pytest
from docx import Document
from pptx import Presentation

from agents.deliverables.deck import build_deck, money, scorecard_rows
from agents.deliverables.docx_builder import add_markdown, strip_internal
from agents.deliverables.schema import SLOTS, parse_json, validate
from tests.fakes import presenter_json


def test_parse_json_handles_code_fences():
    assert parse_json("```json\n{\"a\": 1}\n```") == {"a": 1}
    with pytest.raises(ValueError):
        parse_json("no json here")


def test_validate_reorders_and_requires_every_slot():
    deck = json.loads(presenter_json())
    deck["slides"].reverse()
    out, warnings = validate(deck)
    assert [s["slot"] for s in out["slides"]] == SLOTS and warnings == []
    deck["slides"] = deck["slides"][:-1]
    with pytest.raises(ValueError, match="missing slides"):
        validate(deck)


def test_validate_warns_on_long_bullets():
    deck = json.loads(presenter_json())
    deck["slides"][0]["bullets"] = [" ".join(["word"] * 40)]
    _, warnings = validate(deck)
    assert any("long bullet" in w for w in warnings)


def test_money_formatting():
    assert (money(6_000_000), money(456_000), money(950)) == ("$6.0M", "$456K", "$950")


def test_deck_builds_with_notes_and_code_computed_scorecard(tmp_path, sample):
    from agents.diagnostic.metrics import compute_metrics
    metrics = compute_metrics(sample)
    deck, _ = validate(json.loads(presenter_json()))
    path = tmp_path / "deck.pptx"
    build_deck(deck, metrics, "Test Co", str(path))
    prs = Presentation(str(path))
    assert len(prs.slides) == 10
    assert list(prs.slides)[1].notes_slide.notes_text_frame.text == "Notes for diagnosis"
    table = next(sh for sl in prs.slides for sh in sl.shapes if sh.has_table).table
    cells = {table.cell(r, 0).text: table.cell(r, 1).text for r in range(1, len(table.rows))}
    assert cells["Net revenue retention"] == "80.0%"
    assert cells["ARR lost to failed payments (annualized)"] == "$456K"
    assert len(scorecard_rows(metrics)) == len(table.rows) - 1


def test_markdown_converter(tmp_path):
    md = "# Title\n\n## Section\nText with **bold**.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n\n- item\n  - nested\n\n1. first\n\n---\n_Run metrics: 1.0s, 1 in / 1 out tokens, ~$0.0_"
    cleaned = strip_internal(md)
    assert "Run metrics" not in cleaned and not cleaned.startswith("# ")
    doc = Document()
    add_markdown(doc, cleaned)
    path = tmp_path / "x.docx"; doc.save(path)
    d = Document(path)
    assert any(p.style.name.startswith("Heading") and p.text == "Section" for p in d.paragraphs)
    assert len(d.tables) == 1 and d.tables[0].cell(1, 1).text == "2"
    assert any(p.style.name == "List Bullet 2" for p in d.paragraphs)
