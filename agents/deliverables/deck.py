"""Render the readout deck with python-pptx. Scorecard numbers come from code, not the model."""
from __future__ import annotations
from datetime import date

from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

NAVY = RGBColor(0x1F, 0x2A, 0x44)
PURPLE = RGBColor(0x53, 0x4A, 0xB7)
GRAY = RGBColor(0x5F, 0x66, 0x75)
LIGHT = RGBColor(0xEE, 0xED, 0xFE)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
FONT = "Calibri"


def money(v: float) -> str:
    v = float(v)
    if abs(v) >= 1e6:
        return f"${v / 1e6:.1f}M"
    if abs(v) >= 1e3:
        return f"${v / 1e3:.0f}K"
    return f"${v:,.0f}"


def scorecard_rows(m: dict) -> list:
    rows = []
    if "arr_end" in m:
        rows.append(("ARR at end of period", money(m["arr_end"]), "n/a"))
    if "arr_growth_pct" in m:
        rows.append(("ARR growth over the period", f"{m['arr_growth_pct']}%", "n/a"))
    if "nrr_pct" in m:
        rows.append(("Net revenue retention", f"{m['nrr_pct']}%", "Above 100%"))
    if "grr_pct" in m:
        rows.append(("Gross revenue retention", f"{m['grr_pct']}%", "Above 85 to 90%"))
    if "logo_churn_pct" in m:
        rows.append(("Customer churn over the period", f"{m['logo_churn_pct']}%", "n/a"))
    if "cac_payback_months" in m:
        rows.append(("CAC payback", f"{m['cac_payback_months']} months", "Under 12 to 18 months"))
    if "ltv_to_cac" in m:
        rows.append(("LTV to CAC", f"{m['ltv_to_cac']}x", "Above 3x"))
    if "involuntary_churn_annualized_arr_at_risk" in m:
        rows.append(("ARR lost to failed payments (annualized)", money(m["involuntary_churn_annualized_arr_at_risk"]), "n/a"))
    return rows


def _tb(slide, x, y, w, h, text, size, bold=False, color=NAVY, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size, r.font.bold, r.font.color.rgb, r.font.name = Pt(size), bold, color, FONT
    return box


def _rect(slide, x, y, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s


def _bullets(slide, bullets, x, y, w):
    n, chars = len(bullets), sum(len(b) for b in bullets)
    size = (26 if (n <= 3 and chars <= 360) else 24 if (chars <= 380 and n <= 4) else 22 if chars <= 520
            else 20 if chars <= 680 else 18 if chars <= 850 else 16)
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(4.9))
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(round(size * 0.7))
        pPr = p._p.get_or_add_pPr()
        pPr.set("marL", str(Inches(0.32)))
        pPr.set("indent", str(-Inches(0.32)))
        etree.SubElement(pPr, qn("a:buChar")).set("char", "\u2022")
        r = p.add_run()
        r.text = b
        r.font.size, r.font.color.rgb, r.font.name = Pt(size), NAVY, FONT


def _chrome(slide, title, footer, number):
    _tb(slide, 0.7, 0.5, 11.9, 0.95, title, 30, bold=True, anchor=MSO_ANCHOR.BOTTOM)
    _rect(slide, 0.7, 1.55, 1.0, 0.06, PURPLE)
    _tb(slide, 0.7, 7.0, 10.5, 0.3, footer, 11, color=GRAY)
    _tb(slide, 11.9, 7.0, 0.75, 0.3, str(number), 11, color=GRAY, align=PP_ALIGN.RIGHT)


def _notes(slide, text):
    if text:
        slide.notes_slide.notes_text_frame.text = text


def build_deck(deck: dict, metrics: dict, company: str, path: str) -> None:
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
    blank = prs.slide_layouts[6]
    footer = f"{company}  |  Monetization diagnostic  |  Draft for discussion, hypotheses to validate"
    n = 0

    s = prs.slides.add_slide(blank)
    n += 1
    _rect(s, 0, 0, 0.35, 7.5, PURPLE)
    _tb(s, 1.0, 2.0, 11.2, 1.9, deck["title"], 40, bold=True, anchor=MSO_ANCHOR.BOTTOM)
    _rect(s, 1.0, 4.1, 1.2, 0.08, PURPLE)
    _tb(s, 1.0, 4.4, 11.2, 0.9, deck["subtitle"], 22, color=GRAY)
    _tb(s, 1.0, 6.5, 11.2, 0.4, f"{company}  |  {date.today():%B %Y}", 14, color=GRAY)

    def content(slide_def):
        nonlocal n
        sl = prs.slides.add_slide(blank)
        n += 1
        _chrome(sl, slide_def["title"], footer, n)
        _bullets(sl, slide_def["bullets"], 0.7, 1.95, 11.9)
        _notes(sl, slide_def.get("notes", ""))

    slides = {x["slot"]: x for x in deck["slides"]}
    content(slides["diagnosis"])

    rows = scorecard_rows(metrics)
    if rows:
        sl = prs.slides.add_slide(blank)
        n += 1
        _chrome(sl, "The numbers behind the diagnosis", footer, n)
        shape = sl.shapes.add_table(len(rows) + 1, 3, Inches(0.7), Inches(1.95), Inches(11.9), Inches(0.46 * (len(rows) + 1)))
        tbl = shape.table
        for i, w in enumerate((5.2, 3.2, 3.5)):
            tbl.columns[i].width = Inches(w)
        for r_i in range(len(rows) + 1):
            tbl.rows[r_i].height = Inches(0.46)
            vals = ("Metric", "Value", "Rule of thumb") if r_i == 0 else rows[r_i - 1]
            for c_i, val in enumerate(vals):
                cell = tbl.cell(r_i, c_i)
                cell.fill.solid()
                cell.fill.fore_color.rgb = PURPLE if r_i == 0 else (LIGHT if r_i % 2 == 0 else WHITE)
                cell.vertical_anchor = MSO_ANCHOR.MIDDLE
                p = cell.text_frame.paragraphs[0]
                run = p.add_run()
                run.text = val
                run.font.size, run.font.name = Pt(16), FONT
                run.font.bold = (r_i == 0) or (c_i == 1)
                run.font.color.rgb = WHITE if r_i == 0 else NAVY
        _tb(sl, 0.7, 1.95 + 0.46 * (len(rows) + 1) + 0.2, 11.9, 0.6,
            "Figures supplied by the company; calculations done in code. Rules of thumb vary by segment and stage.", 12, color=GRAY)
        _notes(sl, "Walk through the three or four numbers that matter most to this company. Be clear these come from the figures they supplied, and that rules of thumb are guides, not targets.")

    for slot in ("leaks", "bets", "pricing", "plan", "decisions", "risks"):
        content(slides[slot])

    sl = prs.slides.add_slide(blank)
    n += 1
    _chrome(sl, "How to read this", footer, n)
    _bullets(sl, [
        "These are hypotheses to validate, not forecasts or guarantees.",
        "Built from aggregate figures you supplied. No customer-level data was used.",
        "The analysis is AI-assisted and was reviewed by a person before delivery.",
        "Scenario figures depend on the stated assumptions. Test before committing.",
    ], 0.7, 1.95, 11.9)
    _notes(sl, "Close by restating that nothing here is a guarantee, and agree the first validation step and owner before the call ends.")

    prs.save(path)
