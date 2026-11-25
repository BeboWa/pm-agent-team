"""Render the full report as a Word document from the Markdown stage reports."""
from __future__ import annotations
import re
from datetime import date

from docx import Document
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt

CLIENT_ORDER = ["Executive Brief", "Company Diagnostic", "Pricing & Billing", "Discovery",
                "Prioritization", "PRD", "Delivery", "Launch / GTM", "Analytics"]

INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|(?<!\*)\*[^*\s][^*]*\*(?!\*)|(?<!\w)_[^_]+_(?!\w))")
TABLE_SEP = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
BULLET = re.compile(r"^(\s*)[-*+]\s+(.*)")
NUMBERED = re.compile(r"^(\s*)(\d+)[.)]\s+(.*)")


def strip_internal(text: str) -> str:
    text = re.sub(r"\n+---\s*\n_Run metrics:[^\n]*_\s*$", "", text.strip())
    lines = text.split("\n")
    if lines and lines[0].startswith("# "):
        lines = lines[1:]
    return "\n".join(lines).strip()


def plain(text: str) -> str:
    return re.sub(r"[*_`]", "", text).strip()


def add_inline(par, text: str, size: float | None = None):
    for part in INLINE.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = par.add_run(part[2:-2]); run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = par.add_run(part[1:-1]); run.font.name = "Consolas"
        elif (part.startswith("*") and part.endswith("*")) or (part.startswith("_") and part.endswith("_")):
            run = par.add_run(part[1:-1]); run.italic = True
        else:
            run = par.add_run(part)
        if size:
            run.font.size = Pt(size)


def _table(doc, lines):
    rows = [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in lines if not TABLE_SEP.match(ln.strip())]
    if not rows:
        return
    cols = max(len(r) for r in rows)
    t = doc.add_table(rows=len(rows), cols=cols)
    t.style = "Light Grid Accent 1"
    for i, row in enumerate(rows):
        for j in range(cols):
            cell = t.cell(i, j)
            cell.text = ""
            par = cell.paragraphs[0]
            add_inline(par, row[j] if j < len(row) else "", size=9)
            if i == 0:
                for run in par.runs:
                    run.bold = True
    doc.add_paragraph()


def add_markdown(doc, md: str):
    lines, i, in_code = md.split("\n"), 0, False
    while i < len(lines):
        ln = lines[i]
        s = ln.strip()
        if s.startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code:
            par = doc.add_paragraph()
            run = par.add_run(ln)
            run.font.name, run.font.size = "Consolas", Pt(9)
        elif not s or re.fullmatch(r"-{3,}", s):
            pass
        elif s.startswith("#"):
            level = len(s) - len(s.lstrip("#"))
            doc.add_heading(plain(s.lstrip("#")), level={1: 2, 2: 2, 3: 3}.get(level, 4))
        elif s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append(lines[i]); i += 1
            _table(doc, block)
            continue
        elif BULLET.match(ln):
            m = BULLET.match(ln)
            par = doc.add_paragraph(style="List Bullet 2" if len(m.group(1)) >= 2 else "List Bullet")
            add_inline(par, m.group(2))
        elif NUMBERED.match(ln):
            m = NUMBERED.match(ln)
            par = doc.add_paragraph()
            par.paragraph_format.left_indent = Inches(0.25 + 0.25 * (len(m.group(1)) // 2))
            par.paragraph_format.first_line_indent = Inches(-0.25)
            add_inline(par, f"{m.group(2)}. {m.group(3)}")
        elif s.startswith(">"):
            par = doc.add_paragraph()
            add_inline(par, "_" + s.lstrip("> ").strip() + "_")
        else:
            par = doc.add_paragraph()
            add_inline(par, s)
        i += 1


def _page_number(par):
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    r = OxmlElement("w:r")
    t = OxmlElement("w:t")
    t.text = "1"
    r.append(t)
    fld.append(r)
    par._p.append(fld)


def build_docx(reports: dict, company: str, path: str) -> None:
    doc = Document()
    doc.styles["Normal"].font.name = "Calibri"
    doc.styles["Normal"].font.size = Pt(11)
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Inches(0.9)
    hp = sec.header.paragraphs[0]
    hp.text = f"{company}  |  Draft for discussion. Hypotheses to validate."
    for r in hp.runs:
        r.font.size = Pt(9)
    fp = sec.footer.paragraphs[0]
    fp.alignment = 2
    _page_number(fp)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_heading("Monetization diagnostic", level=0)
    p = doc.add_paragraph()
    run = p.add_run(company); run.font.size = Pt(18)
    p = doc.add_paragraph()
    run = p.add_run(f"Draft for discussion  |  {date.today():%B %Y}"); run.font.size = Pt(12)
    p = doc.add_paragraph()
    add_inline(p, "_This document presents hypotheses based on aggregate figures supplied by the company. "
                  "The analysis is AI-assisted and was reviewed by a person. It is not a forecast or a guarantee._")
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

    first = True
    for name in CLIENT_ORDER:
        if name not in reports:
            continue
        if not first:
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
        first = False
        doc.add_heading(name, level=1)
        add_markdown(doc, strip_internal(reports[name]))
    doc.save(path)
