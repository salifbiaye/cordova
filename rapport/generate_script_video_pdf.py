# -*- coding: utf-8 -*-
"""
Generate a clean PDF from the YouTube presentation script.
"""

from html import escape as html_escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "script_video_youtube.md"
OUTPUT = ROOT / "rapport" / "script_video_youtube.pdf"
FONTS_DIR = Path(r"C:\Windows\Fonts")


def register_fonts():
    pdfmetrics.registerFont(TTFont("Arial", str(FONTS_DIR / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(FONTS_DIR / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(FONTS_DIR / "ariali.ttf")))


register_fonts()

PRIMARY = colors.HexColor("#14532D")
SECONDARY = colors.HexColor("#16A34A")
ACCENT = colors.HexColor("#4ADE80")
LIGHT = colors.HexColor("#F0FAF4")
TEXT = colors.HexColor("#26332B")
MUTED = colors.HexColor("#5D6B63")
LINE = colors.HexColor("#CFE8D8")


STYLES = {
    "title": ParagraphStyle(
        "title",
        fontName="Arial-Bold",
        fontSize=22,
        leading=28,
        textColor=PRIMARY,
        alignment=TA_CENTER,
        spaceAfter=14,
    ),
    "h1": ParagraphStyle(
        "h1",
        fontName="Arial-Bold",
        fontSize=17,
        leading=22,
        textColor=PRIMARY,
        spaceBefore=16,
        spaceAfter=8,
    ),
    "h2": ParagraphStyle(
        "h2",
        fontName="Arial-Bold",
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=5,
    ),
    "h3": ParagraphStyle(
        "h3",
        fontName="Arial-Bold",
        fontSize=10.5,
        leading=14,
        textColor=PRIMARY,
        spaceBefore=7,
        spaceAfter=3,
    ),
    "body": ParagraphStyle(
        "body",
        fontName="Arial",
        fontSize=9.5,
        leading=14,
        textColor=TEXT,
        spaceAfter=6,
    ),
    "speech": ParagraphStyle(
        "speech",
        fontName="Arial-Italic",
        fontSize=9.5,
        leading=14,
        textColor=TEXT,
        leftIndent=10,
        rightIndent=6,
        borderColor=LINE,
        borderWidth=0.6,
        borderPadding=6,
        backColor=LIGHT,
        spaceBefore=3,
        spaceAfter=8,
    ),
    "bullet": ParagraphStyle(
        "bullet",
        fontName="Arial",
        fontSize=9.2,
        leading=13,
        textColor=TEXT,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3,
    ),
    "small": ParagraphStyle(
        "small",
        fontName="Arial",
        fontSize=8,
        leading=11,
        textColor=MUTED,
    ),
    "table_head": ParagraphStyle(
        "table_head",
        fontName="Arial-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=TA_LEFT,
    ),
    "table_cell": ParagraphStyle(
        "table_cell",
        fontName="Arial",
        fontSize=7.5,
        leading=10,
        textColor=TEXT,
    ),
}


def fmt(text):
    text = html_escape(text.strip())
    parts = text.split("`")
    if len(parts) > 1:
        rebuilt = []
        for i, part in enumerate(parts):
            if i % 2:
                rebuilt.append(f'<font name="Arial-Bold" color="#14532D">{part}</font>')
            else:
                rebuilt.append(part)
        text = "".join(rebuilt)
    return text


def parse_table(lines, index):
    rows = []
    while index < len(lines) and lines[index].strip().startswith("|"):
        raw = lines[index].strip()
        cells = [cell.strip() for cell in raw.strip("|").split("|")]
        if not all(set(cell) <= {"-", " "} for cell in cells):
            rows.append(cells)
        index += 1
    return rows, index


def table_flowables(rows):
    if not rows:
        return []

    flow = []
    header = rows[0]
    body = rows[1:]

    if len(header) == 3 and header[0].lower().startswith("temps"):
        data = [[
            Paragraph(fmt(header[0]), STYLES["table_head"]),
            Paragraph(fmt(header[1]), STYLES["table_head"]),
            Paragraph(fmt(header[2]), STYLES["table_head"]),
        ]]
        for row in body:
            padded = row + [""] * (3 - len(row))
            data.append([
                Paragraph(fmt(padded[0]), STYLES["table_cell"]),
                Paragraph(fmt(padded[1]), STYLES["table_cell"]),
                Paragraph(fmt(padded[2]), STYLES["table_cell"]),
            ])
        table = Table(data, colWidths=[2.3 * cm, 3.2 * cm, 10.3 * cm], repeatRows=1)
    else:
        col_count = max(len(row) for row in rows)
        width = 15.8 * cm / col_count
        data = []
        for r, row in enumerate(rows):
            style = STYLES["table_head"] if r == 0 else STYLES["table_cell"]
            padded = row + [""] * (col_count - len(row))
            data.append([Paragraph(fmt(cell), style) for cell in padded])
        table = Table(data, colWidths=[width] * col_count, repeatRows=1)

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
        ("BACKGROUND", (0, 1), (-1, -1), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    flow.extend([table, Spacer(1, 0.25 * cm)])
    return flow


def build_story():
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0

    story.append(Spacer(1, 0.4 * cm))
    story.append(Paragraph("Script video YouTube", STYLES["title"]))
    story.append(Paragraph("Presentation de l'application Todo List Cordova", STYLES["title"]))
    story.append(Spacer(1, 0.2 * cm))
    story.append(HRFlowable(width="100%", thickness=2, color=ACCENT, spaceAfter=0.5 * cm))

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if not stripped:
            story.append(Spacer(1, 0.08 * cm))
            i += 1
            continue

        if stripped.startswith("|"):
            rows, i = parse_table(lines, i)
            story.extend(table_flowables(rows))
            continue

        if stripped.startswith("# "):
            i += 1
            continue
        if stripped.startswith("## "):
            text = stripped[3:]
            story.append(Paragraph(fmt(text), STYLES["h1"]))
            story.append(HRFlowable(width="100%", thickness=0.7, color=LINE, spaceAfter=0.15 * cm))
        elif stripped.startswith("### "):
            story.append(Paragraph(fmt(stripped[4:]), STYLES["h2"]))
        elif stripped.startswith("#### "):
            story.append(Paragraph(fmt(stripped[5:]), STYLES["h3"]))
        elif stripped.startswith("- "):
            story.append(Paragraph("- " + fmt(stripped[2:]), STYLES["bullet"]))
        elif stripped.startswith('"') and stripped.endswith('"'):
            story.append(Paragraph(fmt(stripped), STYLES["speech"]))
        else:
            story.append(Paragraph(fmt(stripped), STYLES["body"]))
        i += 1

    story.append(PageBreak())
    story.append(Paragraph("Check-list avant enregistrement", STYLES["h1"]))
    for item in [
        "Ouvrir le repo avant de lancer l'enregistrement.",
        "Garder la partie code sous les 2 minutes.",
        "Montrer l'ajout, le filtrage, la suppression et la persistance.",
        "Montrer rapidement Contactel et le Calculateur IMC en bonus.",
        "Finir par le dossier du projet et les rapports.",
    ]:
        story.append(Paragraph("- " + fmt(item), STYLES["bullet"]))

    return story


class FooterCanvas(canvas.Canvas):
    def save(self):
        total = self._pageNumber
        for page_num in range(1, total + 1):
            pass
        super().save()

    def showPage(self):
        self.draw_footer()
        super().showPage()

    def draw_footer(self):
        self.saveState()
        self.setFillColor(PRIMARY)
        self.rect(0, 0, A4[0], 0.7 * cm, stroke=0, fill=1)
        self.setFillColor(colors.white)
        self.setFont("Arial-Bold", 7)
        self.drawString(1.6 * cm, 0.27 * cm, "Script video YouTube - Todo List Cordova")
        self.drawRightString(A4[0] - 1.6 * cm, 0.27 * cm, f"Page {self._pageNumber}")
        self.restoreState()


def main():
    doc = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=1.6 * cm,
        leftMargin=1.6 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.2 * cm,
        title="Script video YouTube - Todo List Cordova",
        author="Codex",
    )
    doc.build(build_story(), canvasmaker=FooterCanvas)
    print(str(OUTPUT))


if __name__ == "__main__":
    main()

