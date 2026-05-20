# -*- coding: utf-8 -*-
"""
Rapport Technique — Calculateur IMC
Application mobile Apache Cordova
HTML5 · CSS3 · JavaScript Vanilla
Auteur : Salif Biaye — Groupe 3 — ESP/UCAD 2026
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, Image as RLImage, KeepTogether
)
from reportlab.pdfgen import canvas as pdfcanvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# ── Polices ──────────────────────────────────────────────────
FONTS_DIR = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial",            os.path.join(FONTS_DIR, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold",       os.path.join(FONTS_DIR, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic",     os.path.join(FONTS_DIR, "ariali.ttf")))
pdfmetrics.registerFont(TTFont("Arial-BoldItalic", os.path.join(FONTS_DIR, "arialbi.ttf")))
pdfmetrics.registerFont(TTFont("CourierNew",       os.path.join(FONTS_DIR, "cour.ttf")))
pdfmetrics.registerFont(TTFont("CourierNew-Bold",  os.path.join(FONTS_DIR, "courbd.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-Bold",
                               italic="Arial-Italic", boldItalic="Arial-BoldItalic")
F = "Arial"; F_BOLD = "Arial-Bold"; F_ITAL = "Arial-Italic"
F_MONO = "CourierNew"; F_MONOB = "CourierNew-Bold"

# ── Palette violette (thème IMC Calculator) ──────────────────
PRIMARY   = colors.HexColor("#2E1065")
SECONDARY = colors.HexColor("#6D28D9")
ACCENT    = colors.HexColor("#7C3AED")
GOLD      = colors.HexColor("#A78BFA")
LIGHT     = colors.HexColor("#EDE9FE")
LIGHT2    = colors.HexColor("#F5F3FF")
WHITE     = colors.white
BLACK     = colors.black
GRAY      = colors.HexColor("#3A3A3A")
LGRAY     = colors.HexColor("#E5E0F5")
CODE_BG   = colors.HexColor("#1E1035")
CODE_FG   = colors.HexColor("#DDD6FE")
TGRID     = colors.HexColor("#C4B5FD")
C_GREEN   = colors.HexColor("#00E87A")
C_ORANGE  = colors.HexColor("#FFB443")
C_RED     = colors.HexColor("#FF4D6A")

# ── Constantes ───────────────────────────────────────────────
W, H = A4
MARGIN_L = 1.8 * cm
MARGIN_R = 1.8 * cm
AVAIL    = W - MARGIN_L - MARGIN_R

LOGO         = r"C:\Users\DELL\Downloads\logo_ucad.png"
SCREENS_DIR  = r"C:\Users\DELL\Downloads\medy\screens"
SCR_FORM     = os.path.join(SCREENS_DIR, "imc_form.png")
SCR_RESULT   = os.path.join(SCREENS_DIR, "imc_result.png")
SCR_ERROR    = os.path.join(SCREENS_DIR, "imc_error.png")

OUTPUT = os.path.join(os.path.dirname(__file__), "rapport_imc.pdf")
chapter_titles = {}


# ── Header / Footer Canvas ───────────────────────────────────
class HFCanvas(pdfcanvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_hf(total)
            pdfcanvas.Canvas.showPage(self)
        pdfcanvas.Canvas.save(self)

    def _draw_hf(self, total):
        pg = self._pageNumber
        self.saveState()
        if pg == 1:
            self.setFillColor(PRIMARY)
            self.rect(0, H - 3.2*cm, W, 3.2*cm, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, H - 3.28*cm, W, 0.08*cm, fill=1, stroke=0)
            if os.path.exists(LOGO):
                self.drawImage(LOGO, 2.0*cm, H - 2.75*cm, width=1.8*cm, height=1.8*cm, mask="auto")
            self.setFillColor(GOLD)
            self.setFont(F_BOLD, 22)
            self.drawString(4.3*cm, H - 1.5*cm, "Calculateur IMC")
            self.setFillColor(WHITE)
            self.setFont(F_BOLD, 9)
            self.drawString(4.3*cm, H - 2.1*cm, "Rapport Technique — Application Cordova")
            self.setFont(F, 7.5)
            self.drawString(4.3*cm, H - 2.55*cm,
                            "HTML5 · CSS3 · JavaScript Vanilla — Groupe 3 — ESP/UCAD 2026")
        else:
            self.setFillColor(LGRAY)
            self.rect(0, H - 1.15*cm, W, 1.15*cm, fill=1, stroke=0)
            self.setFillColor(SECONDARY)
            self.setFont(F_BOLD, 8)
            self.drawString(MARGIN_L, H - 0.72*cm, "Calculateur IMC")
            self.setFillColor(ACCENT)
            self.setFont(F_BOLD, 6.8)
            self.drawString(MARGIN_L + 2.2*cm, H - 0.72*cm, "| Rapport Technique")
            chap = chapter_titles.get(pg, "")
            if chap:
                self.setFillColor(colors.HexColor("#6B6B8A"))
                self.setFont(F, 6.4)
                self.drawRightString(W - MARGIN_R, H - 0.72*cm, chap[:76])
        self.setFillColor(PRIMARY)
        self.rect(0, 0, W, 0.95*cm, fill=1, stroke=0)
        self.setFillColor(GOLD)
        self.rect(0, 0.95*cm, W, 0.06*cm, fill=1, stroke=0)
        self.setFillColor(WHITE)
        self.setFont(F_BOLD, 6.2)
        self.drawString(MARGIN_L, 0.36*cm, "Salif Biaye — ESP/UCAD 2026")
        if pg > 1:
            self.drawRightString(W - MARGIN_R, 0.36*cm, f"Page {pg}")
        self.restoreState()


# ── Styles ───────────────────────────────────────────────────
def S(name, **kw):
    return ParagraphStyle(name, **kw)

chap_title_st = S('ct', fontName=F_BOLD, fontSize=18, textColor=WHITE, leading=24, alignment=TA_LEFT)
chap_num_st   = S('cn', fontName=F_BOLD, fontSize=9,  textColor=GOLD,  leading=13, alignment=TA_LEFT)
sec_st        = S('s',  fontName=F_BOLD, fontSize=13, textColor=PRIMARY, leading=18,
                  spaceBefore=14, spaceAfter=4, alignment=TA_LEFT)
body_st       = S('b',  fontName=F, fontSize=9.5, textColor=GRAY, leading=17, spaceAfter=9,
                  alignment=TA_JUSTIFY)
bullet_st     = S('bu', fontName=F, fontSize=9.5, textColor=GRAY, leading=16,
                  leftIndent=14, firstLineIndent=-10, spaceAfter=5, alignment=TA_LEFT)
note_st       = S('n',  fontName=F_ITAL, fontSize=8.5, textColor=GRAY, leading=15,
                  leftIndent=10, alignment=TA_JUSTIFY)
code_st       = S('co', fontName=F_MONO, fontSize=8, textColor=CODE_FG, backColor=CODE_BG,
                  leading=13, leftIndent=8, rightIndent=8, spaceBefore=4, spaceAfter=4,
                  alignment=TA_LEFT)
code_title_st = S('cot', fontName=F_MONOB, fontSize=7.5, textColor=GOLD, backColor=CODE_BG,
                  leading=12, leftIndent=8, alignment=TA_LEFT)
synth_body_st = S('sb', fontName=F, fontSize=9, textColor=colors.HexColor("#1C2E3D"),
                  leading=14, leftIndent=6, firstLineIndent=-6)
synth_hdr_st  = S('sh', fontName=F_BOLD, fontSize=9.5, textColor=WHITE, leading=13, alignment=TA_LEFT)
label_st      = S('la', fontName=F_BOLD, fontSize=8, textColor=PRIMARY, leading=12, alignment=TA_LEFT)
value_st      = S('va', fontName=F, fontSize=8, textColor=GRAY, leading=12, alignment=TA_LEFT)
th_st         = S('th', fontName=F_BOLD, fontSize=8, textColor=WHITE, alignment=TA_CENTER)
td_st         = S('td', fontName=F, fontSize=8, textColor=GRAY, alignment=TA_LEFT)
tag_st        = S('tag', fontName=F_MONOB, fontSize=8, textColor=SECONDARY, alignment=TA_LEFT)


# ── Composants ───────────────────────────────────────────────
def chap_header(num, title, subtitle=""):
    nc = 4.2 * cm
    row = [[Paragraph(f"SECTION {num}", chap_num_st), Paragraph(title, chap_title_st)]]
    t = Table(row, colWidths=[nc, AVAIL - nc])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), PRIMARY),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING',   (0, 0), (-1, -1), 10),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 10),
        ('TOPPADDING',    (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LINEBELOW',     (0, 0), (-1, -1), 4, GOLD),
    ]))
    out = [t]
    if subtitle:
        out.append(Spacer(1, 0.3*cm))
        out.append(Paragraph(subtitle, note_st))
    out.append(Spacer(1, 0.6*cm))
    return out


def sec_title(text):
    return [Paragraph(text, sec_st),
            HRFlowable(width="100%", thickness=1, color=GOLD, spaceBefore=2, spaceAfter=4)]


def body(text):
    return [Paragraph(text, body_st)]


def bullet(text):
    return [Paragraph(f"• {text}", bullet_st)]


def code_block(filename, lines):
    """Code snippet avec en-tête fichier et fond sombre."""
    rows = [[Paragraph(f"📄  {filename}", code_title_st)]]
    for line in lines:
        rows.append([Paragraph(line.replace(" ", " ").replace("<", "&lt;").replace(">", "&gt;"),
                               code_st)])
    t = Table(rows, colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0, 0), (-1, -1), CODE_BG),
        ('TOPPADDING',    (0, 0), (0, 0), 7),
        ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ('TOPPADDING',    (0, 1), (-1, -1), 2),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 2),
        ('LEFTPADDING',   (0, 0), (-1, -1), 8),
        ('RIGHTPADDING',  (0, 0), (-1, -1), 8),
        ('LINEBELOW',     (0, 0), (0, 0), 1, GOLD),
        ('BOX',           (0, 0), (-1, -1), 1, SECONDARY),
    ]))
    return [t, Spacer(1, 0.25*cm)]


def screen_box(path, caption, max_w=12*cm, max_h=8*cm):
    """Affiche l'image si elle existe, sinon un cadre placeholder."""
    cap_st = S('sc', fontName=F_ITAL, fontSize=8.5, textColor=PRIMARY,
               alignment=TA_CENTER, leading=12)
    if os.path.exists(path):
        img = RLImage(path)
        ratio = img.imageWidth / img.imageHeight
        w = min(max_w, AVAIL - 1*cm)
        h = w / ratio
        if h > max_h:
            h = max_h; w = h * ratio
        img.drawWidth = w; img.drawHeight = h
        inner = AVAIL - 1*cm
        frame = Table([[img], [Paragraph(f"Capture — {caption}", cap_st)]],
                      colWidths=[inner])
        frame.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, 0), WHITE),
            ('TOPPADDING', (0, 0), (0, 0), 10), ('BOTTOMPADDING', (0, 0), (0, 0), 8),
            ('BACKGROUND', (0, 1), (0, 1), colors.HexColor("#F0EBFF")),
            ('LINEABOVE',  (0, 1), (0, 1), 2, GOLD),
            ('TOPPADDING', (0, 1), (0, 1), 6), ('BOTTOMPADDING', (0, 1), (0, 1), 6),
            ('ALIGN',      (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
            ('BOX',        (0, 0), (-1, -1), 1.5, TGRID),
        ]))
        return [KeepTogether([frame]), Spacer(1, 0.4*cm)]
    else:
        ph_st = S('ph', fontName=F_BOLD, fontSize=10, textColor=SECONDARY,
                  alignment=TA_CENTER, leading=16)
        hint_st = S('hint', fontName=F_ITAL, fontSize=8, textColor=GRAY,
                    alignment=TA_CENTER, leading=12)
        rows = [
            [Paragraph("📸", ph_st)],
            [Paragraph(caption, ph_st)],
            [Paragraph(f"Placer la capture ici :\n{path}", hint_st)],
        ]
        t = Table(rows, colWidths=[AVAIL])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0, 0), (-1, -1), LIGHT2),
            ('ALIGN',         (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING',    (0, 0), (-1, -1), 22),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 22),
            ('BOX',           (0, 0), (-1, -1), 1.5, SECONDARY),
            ('LINEBEFORE',    (0, 0), (0, -1), 4, SECONDARY),
        ]))
        return [t, Spacer(1, 0.4*cm)]


def synth_box(lines, positive=True):
    accent = C_GREEN if positive else SECONDARY
    hdr_bg = colors.HexColor("#1A5C35") if positive else PRIMARY
    AW = 0.22 * cm
    TW = AVAIL - AW
    bul = S('rb', fontName=F, fontSize=9, textColor=colors.HexColor("#1C2E3D"),
            leading=14, leftIndent=6, firstLineIndent=-6, alignment=TA_LEFT)
    data = [["", Paragraph("Synthèse", synth_hdr_st)]]
    for line in lines:
        data.append(["", Paragraph(f"◆  {line}", bul)])
    t = Table(data, colWidths=[AW, TW])
    cmds = [
        ('BACKGROUND', (0, 0), (0, -1), accent),
        ('BACKGROUND', (1, 0), (1, 0),  hdr_bg),
        ('TOPPADDING',    (0, 0), (-1, 0), 7), ('BOTTOMPADDING', (0, 0), (-1, 0), 7),
        ('TOPPADDING',    (0, 1), (-1, -1), 5), ('BOTTOMPADDING', (0, 1), (-1, -1), 5),
        ('LEFTPADDING',   (1, 0), (1, -1), 12), ('RIGHTPADDING', (1, 0), (1, -1), 12),
        ('LEFTPADDING',   (0, 0), (0, -1), 0),  ('RIGHTPADDING', (0, 0), (0, -1), 0),
        ('VALIGN',        (0, 0), (-1, -1), 'MIDDLE'),
        ('BOX',           (0, 0), (-1, -1), 1.2, colors.HexColor("#9AB0C4")),
        ('LINEBELOW',     (1, 1), (1, -2), 0.4, colors.HexColor("#D4DFE8")),
    ]
    for i in range(1, len(data)):
        bg = LIGHT if i % 2 == 1 else WHITE
        cmds.append(('BACKGROUND', (1, i), (1, i), bg))
    t.setStyle(TableStyle(cmds))
    return [Spacer(1, 0.3*cm), t, Spacer(1, 0.3*cm)]


def make_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [AVAIL / len(headers)] * len(headers)
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), PRIMARY),
        ('TEXTCOLOR',  (0, 0), (-1, 0), WHITE),
        ('FONTNAME',   (0, 0), (-1, 0), F_BOLD), ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME',   (0, 1), (-1, -1), F),      ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TEXTCOLOR',  (0, 1), (-1, -1), GRAY),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT]),
        ('GRID',       (0, 0), (-1, -1), 0.3, TGRID),
        ('LINEBELOW',  (0, 0), (-1, 0), 2, GOLD),
        ('ALIGN',      (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN',     (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
    ]))
    return [t, Spacer(1, 0.3*cm)]


def th(t): return Paragraph(t, th_st)
def td(t, bold=False):
    st = S('tdc', fontName=F_BOLD if bold else F, fontSize=8, textColor=GRAY, alignment=TA_LEFT)
    return Paragraph(t, st)
def tag(t): return Paragraph(t, tag_st)


# ── PAGE DE GARDE ────────────────────────────────────────────
def cover_page(elements):
    elements.append(Spacer(1, 0.8*cm))
    width = AVAIL
    if os.path.exists(LOGO):
        logo = RLImage(LOGO, width=2.0*cm, height=2.0*cm)
        lt = Table([[logo]], colWidths=[width])
        lt.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER'),
                                 ('BOTTOMPADDING', (0,0), (-1,-1), 4)]))
        elements.append(lt)
        elements.append(Paragraph("UNIVERSITÉ CHEIKH ANTA DIOP DE DAKAR",
            S('ucad', fontName=F_BOLD, fontSize=9, textColor=PRIMARY,
              alignment=TA_CENTER, leading=13)))
        elements.append(Paragraph("École Supérieure Polytechnique — ESP",
            S('esp', fontName=F, fontSize=7.5, textColor=ACCENT,
              alignment=TA_CENTER, leading=12)))
        elements.append(Spacer(1, 0.2*cm))

    elements.append(HRFlowable(width="92%", thickness=1,
                                color=colors.HexColor("#C4B5FD"), spaceAfter=0.3*cm))

    # Badge type de document
    badge = Table([[Paragraph("RAPPORT TECHNIQUE", S('badge', fontName=F_BOLD, fontSize=8,
                   textColor=WHITE, alignment=TA_CENTER))]],
                  colWidths=[5*cm])
    badge.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    bt = Table([[badge]], colWidths=[width])
    bt.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    elements.append(bt)
    elements.append(Spacer(1, 0.2*cm))

    elements.append(Paragraph("Calculateur IMC",
        S('title', fontName=F_BOLD, fontSize=34, textColor=PRIMARY,
          leading=42, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.05*cm))
    elements.append(Paragraph("Application Mobile — Apache Cordova",
        S('sub', fontName=F, fontSize=11, textColor=colors.HexColor("#4C1D95"),
          leading=15, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.15*cm))

    # Sous-titre violet
    subj = Table([
        [Paragraph("Documentation complète — HTML · CSS · JavaScript", S('wt', fontName=F_BOLD,
                   fontSize=12, textColor=WHITE, leading=17, alignment=TA_CENTER))],
        [Paragraph("Explication étape par étape de chaque section, fonction et composant visuel",
                   S('ws', fontName=F, fontSize=8, textColor=colors.HexColor("#C4B5FD"),
                     leading=12, alignment=TA_CENTER))],
    ], colWidths=[width])
    subj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('TOPPADDING', (0,0), (-1,0), 12), ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('TOPPADDING', (0,1), (-1,1), 3),  ('BOTTOMPADDING', (0,1), (-1,1), 12),
    ]))
    elements.append(subj)

    # Stats
    stat_st = S('stat', fontName=F_BOLD, fontSize=9, textColor=WHITE,
                leading=13, alignment=TA_CENTER)
    stats = Table([[
        Paragraph("3 sections HTML\nstructurées", stat_st),
        Paragraph("CSS violet\nthème sombre", stat_st),
        Paragraph("8 fonctions JS\ndocumentées", stat_st),
        Paragraph("Cordova\nmobile-first", stat_st),
    ]], colWidths=[width/4]*4)
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), ACCENT),
        ('GRID', (0,0), (-1,-1), 0.25, colors.HexColor("#6D28D9")),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(stats)
    elements.append(Spacer(1, 0.35*cm))

    # Bloc équipe
    author_name_st = S('an', fontName=F_BOLD, fontSize=14, textColor=PRIMARY,
                        leading=18, alignment=TA_CENTER)
    author_role_st = S('ar', fontName=F, fontSize=9, textColor=GRAY,
                        leading=13, alignment=TA_CENTER)
    author_box = Table([
        [Paragraph("Auteur", S('gh', fontName=F_BOLD, fontSize=8, textColor=WHITE,
                               leading=11, alignment=TA_CENTER))],
        [Paragraph("Salif Biaye", author_name_st)],
        [Paragraph("Fondateur / CEO — DIC3 Informatique & Télécommunications", author_role_st)],
    ], colWidths=[width])
    author_box.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), PRIMARY),
        ('LINEBELOW', (0,0), (0,0), 2.5, GOLD),
        ('BACKGROUND', (0,1), (0,1), LIGHT),
        ('BACKGROUND', (0,2), (0,2), WHITE),
        ('BOX', (0,0), (-1,-1), 1, TGRID),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(author_box)
    elements.append(Spacer(1, 0.3*cm))

    meta = [
        ["Application :", "Calculateur IMC"],
        ["Technologie :", "Apache Cordova · HTML5 · CSS3 · JavaScript Vanilla"],
        ["Module :", "Développement Mobile — DIC3 Informatique & Télécommunications"],
        ["Université :", "UCAD — École Supérieure Polytechnique (ESP)"],
        ["Auteur :", "Salif Biaye — Édition Mai 2026"],
    ]
    mt2 = Table([[Paragraph(a, label_st), Paragraph(b, value_st)] for a, b in meta],
                colWidths=[4.0*cm, width - 4.0*cm])
    mt2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT),
        ('GRID', (0,0), (-1,-1), 0.35, TGRID),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 9), ('RIGHTPADDING', (0,0), (-1,-1), 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    elements.append(mt2)
    elements.append(Spacer(1, 0.2*cm))
    elements.append(HRFlowable(width="84%", thickness=1.5, color=TGRID))
    elements.append(PageBreak())


# ── SOMMAIRE ─────────────────────────────────────────────────
def sommaire(elements):
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("Sommaire", S('som', fontName=F_BOLD, fontSize=18, textColor=PRIMARY,
                               leading=22, alignment=TA_CENTER)))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=GOLD,
                                spaceBefore=8, spaceAfter=10))
    sections = [
        ("1", "Vue d'ensemble", "Objectif, tech stack, fonctionnement global"),
        ("2", "Structure HTML", "Sections <header>, <form>, <div#result>"),
        ("3", "Feuille de style CSS", "Palette violette, thème sombre, SVG ring"),
        ("4", "Logique JavaScript", "Module pattern, 8 fonctions documentées"),
        ("5", "Captures d'écran", "Formulaire, résultat IMC, états d'erreur"),
        ("6", "Synthèse", "Points clés, bilan technique"),
    ]
    h_n = S('hn', fontName=F_BOLD, fontSize=8, textColor=WHITE, alignment=TA_CENTER)
    h_t = S('ht', fontName=F_BOLD, fontSize=8, textColor=WHITE, alignment=TA_LEFT)
    n_s = S('ns', fontName=F_BOLD, fontSize=9, textColor=PRIMARY, alignment=TA_CENTER)
    t_s = S('ts', fontName=F_BOLD, fontSize=9, textColor=BLACK, alignment=TA_LEFT)
    p_s = S('ps', fontName=F_ITAL, fontSize=7.5, textColor=GRAY, alignment=TA_LEFT)
    nw = 1.1*cm; tw = 5.8*cm; pw = AVAIL - nw - tw
    rows = [[Paragraph("N°", h_n), Paragraph("Section", h_t), Paragraph("Contenu", h_t)]]
    for n, t, p in sections:
        rows.append([Paragraph(n, n_s), Paragraph(t, t_s), Paragraph(p, p_s)])
    tbl = Table(rows, colWidths=[nw, tw, pw])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.3, TGRID),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 6), ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ('LINEABOVE', (0,1), (-1,-1), 0.5, TGRID),
    ]))
    elements.append(tbl)
    elements.append(PageBreak())


# ── SECTION 1 — VUE D'ENSEMBLE ───────────────────────────────
def section_overview(elements, pt):
    pt[1] = "Section 1 — Vue d'ensemble"
    elements += chap_header("1", "Vue d'ensemble",
                             "Objectif de l'application, pile technologique et fonctionnement global")

    elements += sec_title("1.1  Qu'est-ce que le Calculateur IMC ?")
    elements += body(
        "Le <b>Calculateur IMC</b> (Indice de Masse Corporelle) est une application mobile "
        "développée avec <b>Apache Cordova</b> permettant à un utilisateur d'évaluer sa "
        "composition corporelle en saisissant son poids (masse en kg) et sa taille (en mètres). "
        "L'IMC est calculé selon la formule : <b>IMC = masse ÷ taille²</b>."
    )
    elements += body(
        "Le résultat est affiché accompagné d'une <b>catégorie de santé</b> (insuffisance "
        "pondérale, poids normal, surpoids, obésité) et d'un <b>conseil personnalisé</b>. "
        "Un anneau SVG animé visualise graphiquement la valeur obtenue."
    )

    elements += sec_title("1.2  Pile technologique")
    tech_data = [
        [th("Technologie"), th("Rôle"), th("Version / Source")],
        [td("Apache Cordova"), td("Framework mobile hybride — wrapper natif Android/iOS"), td("Dernière stable")],
        [td("HTML5"), td("Structure de l'interface (sémantique, formulaire, SVG)"), td("Standard W3C")],
        [td("CSS3"), td("Mise en page, thème violet sombre, animations, mode clair"), td("Standard W3C")],
        [td("JavaScript Vanilla"), td("Logique métier, calcul IMC, rendu dynamique"), td("ES6+")],
        [td("Font Awesome 6.5"), td("Icônes vectorielles (balance, règle, flèche)"), td("CDN Cloudflare")],
    ]
    elements += make_table(tech_data[0], tech_data[1:], [AVAIL*0.20, AVAIL*0.52, AVAIL*0.28])

    elements += sec_title("1.3  Flux utilisateur")
    for step in [
        "<b>Étape 1 — Saisie :</b> l'utilisateur entre sa masse (kg) et sa taille (m) dans le formulaire.",
        "<b>Étape 2 — Validation :</b> JavaScript vérifie les bornes (1–500 kg, 0.5–3 m).",
        "<b>Étape 3 — Calcul :</b> IMC = masse / (taille × taille), arrondi à 1 décimale.",
        "<b>Étape 4 — Affichage :</b> la carte résultat apparaît avec la valeur, la catégorie colorée et le conseil.",
        "<b>Étape 5 — Animation :</b> l'anneau SVG se remplit proportionnellement à l'IMC (max 40).",
    ]:
        elements += bullet(step)

    elements += synth_box([
        "Framework : Apache Cordova — code web converti en application Android/iOS",
        "Calcul : IMC = masse / taille² — formule OMS standard",
        "Retour visuel : anneau SVG animé + catégorie colorée + conseil textuel",
        "Thème : violet foncé (#2E1065 → #8B5CF6) avec support mode clair",
    ])
    elements.append(PageBreak())


# ── SECTION 2 — STRUCTURE HTML ───────────────────────────────
def section_html(elements, pt):
    pt[2] = "Section 2 — Structure HTML"
    elements += chap_header("2", "Structure HTML",
                             "Analyse détaillée de chaque balise et section du fichier index.html")

    elements += sec_title("2.1  En-tête du document (<head>)")
    elements += body(
        "Le <code>&lt;head&gt;</code> configure les métadonnées essentielles pour une application "
        "mobile Cordova :"
    )
    elements += code_block("index.html — head", [
        '&lt;meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no"&gt;',
        '&lt;!-- Désactive le zoom utilisateur pour une UX d\'app native --&gt;',
        '&lt;meta http-equiv="Content-Security-Policy" content="default-src \'self\' ..."&gt;',
        '&lt;!-- Politique de sécurité Cordova : whitelist des ressources autorisées --&gt;',
        '&lt;link rel="stylesheet" href="https://cdnjs.cloudflare.com/...font-awesome...css"&gt;',
        '&lt;link rel="stylesheet" href="css/index.css"&gt;',
    ])
    for item in [
        "<b>viewport user-scalable=no</b> : empêche le zoom, simule le comportement d'une app native.",
        "<b>Content-Security-Policy</b> : directive de sécurité Cordova, liste les sources autorisées.",
        "<b>Font Awesome</b> : chargé depuis CDN pour les icônes (balance, règle, flèche).",
    ]:
        elements += bullet(item)

    elements += sec_title("2.2  Conteneur principal (#app)")
    elements += body(
        "Tout le contenu visible est encapsulé dans <code>&lt;div id=\"app\"&gt;</code>, "
        "racine CSS qui applique le thème global (fond sombre, police, max-width)."
    )
    elements += code_block("index.html — structure générale", [
        '&lt;div id="app"&gt;',
        '  &lt;header&gt; ... &lt;/header&gt;      &lt;!-- Bande titre dégradé violet --&gt;',
        '  &lt;div class="content"&gt;              &lt;!-- Zone scrollable --&gt;',
        '    &lt;form id="imc-form"&gt; ... &lt;/form&gt;  &lt;!-- Formulaire saisie --&gt;',
        '    &lt;div id="result" hidden&gt; ... &lt;/div&gt; &lt;!-- Carte résultat --&gt;',
        '  &lt;/div&gt;',
        '&lt;/div&gt;',
    ])

    elements += sec_title("2.3  En-tête visuelle (<header>)")
    elements += body(
        "L'en-tête contient le titre de l'application et un sous-titre descriptif, "
        "stylisés avec le dégradé violet."
    )
    elements += code_block("index.html — header", [
        '&lt;header&gt;',
        '  &lt;div class="header-inner"&gt;',
        '    &lt;h1&gt;Calculateur IMC&lt;/h1&gt;',
        '    &lt;p class="subtitle"&gt;Évaluez votre composition corporelle en quelques secondes.&lt;/p&gt;',
        '  &lt;/div&gt;',
        '&lt;/header&gt;',
    ])

    elements += sec_title("2.4  Formulaire de saisie (#imc-form)")
    elements += body(
        "Le formulaire est déclaré avec l'attribut <code>novalidate</code> — la validation "
        "est entièrement gérée en JavaScript pour un contrôle total sur les messages d'erreur. "
        "La grille 3 colonnes (masse / séparateur / taille) est structurée par <code>.field-group</code>."
    )
    elements += code_block("index.html — form", [
        '&lt;form id="imc-form" novalidate&gt;',
        '  &lt;div class="field-group"&gt;     &lt;!-- Grille 3 colonnes CSS --&gt;',
        '    &lt;div class="field"&gt;',
        '      &lt;label for="masse"&gt;&lt;i class="fa-solid fa-weight-scale"&gt;&lt;/i&gt; Masse &lt;span class="unit"&gt;kg&lt;/span&gt;&lt;/label&gt;',
        '      &lt;input type="number" id="masse" placeholder="70" min="1" max="500" step="0.1" inputmode="decimal" required&gt;',
        '      &lt;span class="field-hint"&gt;Entre 1 et 500 kg&lt;/span&gt;',
        '    &lt;/div&gt;',
        '    &lt;div class="field-divider"&gt;/&lt;/div&gt;  &lt;!-- Séparateur visuel --&gt;',
        '    &lt;div class="field"&gt; ... taille ... &lt;/div&gt;',
        '  &lt;/div&gt;',
        '  &lt;button type="submit" class="btn-submit"&gt;',
        '    &lt;span&gt;Calculer l\'IMC&lt;/span&gt; &lt;i class="fa-solid fa-arrow-right"&gt;&lt;/i&gt;',
        '  &lt;/button&gt;',
        '&lt;/form&gt;',
    ])
    for item in [
        "<b>type=\"number\"</b> : clavier numérique sur mobile.",
        "<b>inputmode=\"decimal\"</b> : clavier décimal (virgule disponible) sur iOS/Android.",
        "<b>min/max</b> : bornes HTML natives (doublées en JS pour fiabilité).",
        "<b>step=\"0.1\"</b> / <b>step=\"0.01\"</b> : précision adaptée à chaque champ.",
    ]:
        elements += bullet(item)

    elements += sec_title("2.5  Carte résultat (#result)")
    elements += body(
        "La carte est initialement cachée (<code>hidden</code>). Elle est affichée par JS "
        "après calcul. Elle contient un <b>anneau SVG</b>, la valeur numérique de l'IMC, "
        "la catégorie et le conseil."
    )
    elements += code_block("index.html — result card", [
        '&lt;div id="result" class="result" aria-live="polite" hidden&gt;',
        '  &lt;div class="result-ring"&gt;',
        '    &lt;svg class="ring-svg" viewBox="0 0 120 120"&gt;',
        '      &lt;circle class="ring-bg"   cx="60" cy="60" r="50"/&gt; &lt;!-- Fond gris --&gt;',
        '      &lt;circle class="ring-fill" cx="60" cy="60" r="50"/&gt; &lt;!-- Arc animé --&gt;',
        '    &lt;/svg&gt;',
        '    &lt;div class="result-value-wrap"&gt;',
        '      &lt;span id="result-value"&gt;--&lt;/span&gt;     &lt;!-- Valeur IMC --&gt;',
        '      &lt;span class="result-label-imc"&gt;IMC&lt;/span&gt;',
        '    &lt;/div&gt;',
        '  &lt;/div&gt;',
        '  &lt;p id="result-category"&gt;--&lt;/p&gt;  &lt;!-- Catégorie colorée --&gt;',
        '  &lt;p id="result-advice"&gt;&lt;/p&gt;      &lt;!-- Conseil personnalisé --&gt;',
        '&lt;/div&gt;',
    ])
    elements += body(
        "L'attribut <code>aria-live=\"polite\"</code> annonce le résultat aux lecteurs d'écran "
        "dès qu'il apparaît — bonne pratique d'accessibilité."
    )
    elements += body(
        "<b>Technique SVG — anneau animé :</b> les deux cercles ont le même centre (cx=60, cy=60) "
        "et le même rayon (r=50). Le cercle <code>.ring-fill</code> utilise "
        "<code>stroke-dasharray</code> et <code>stroke-dashoffset</code> pour créer l'arc "
        "proportionnel à l'IMC."
    )
    elements += synth_box([
        "novalidate : validation 100% JS pour maîtriser les messages d'erreur",
        "inputmode=decimal : clavier adapté sur iOS/Android",
        "SVG ring : stroke-dashoffset animé par CSS transition 1s ease",
        "aria-live=polite : accessibilité — annonce vocale du résultat",
    ])
    elements.append(PageBreak())


# ── SECTION 3 — CSS ──────────────────────────────────────────
def section_css(elements, pt):
    pt[3] = "Section 3 — CSS & Thème Visuel"
    elements += chap_header("3", "Feuille de style CSS",
                             "Palette violette, thème sombre, layout et animations SVG")

    elements += sec_title("3.1  Palette de couleurs")
    pal_data = [
        [th("Variable CSS"), th("Hex"), th("Usage")],
        [tag("fond global"),       td("#0d0718"), td("Fond arrière très sombre (presque noir violet)")],
        [tag("header gradient"),   td("#2E1065 → #A78BFA"), td("Dégradé en-tête de haut en bas")],
        [tag("accent principal"),  td("#6D28D9"), td("Bouton, bordures actives, ring stroke")],
        [tag("accent clair"),      td("#8B5CF6"), td("Hover, focus, éléments secondaires")],
        [tag("texte"),             td("#EDE9FE"), td("Texte principal sur fond sombre (lavande))")],
        [tag("champ input"),       td("#130A24"), td("Fond des inputs (plus sombre que le fond global)")],
        [tag("erreur"),            td("#FF4D6A"), td("Bordure rouge-rose si validation échoue")],
        [tag("IMC normal"),        td("#00E87A"), td("Catégorie Poids normal — vert vif")],
        [tag("IMC surpoids"),      td("#FFB443"), td("Catégorie Surpoids — orange")],
        [tag("IMC obésité"),       td("#FF4D6A"), td("Catégorie Obésité — rouge-rose")],
    ]
    elements += make_table(pal_data[0], pal_data[1:], [AVAIL*0.27, AVAIL*0.28, AVAIL*0.45])

    elements += sec_title("3.2  Layout et structure")
    elements += body(
        "L'application utilise un layout <b>Flexbox</b> centré, avec une largeur maximale "
        "de <b>480px</b> pour conserver l'apparence mobile sur grand écran. "
        "La zone de contenu est scrollable, le header reste fixe en haut."
    )
    elements += code_block("index.css — layout principal", [
        '#app {',
        '  display: flex; flex-direction: column;',
        '  min-height: 100vh;',
        '  background: #0d0718; color: #ede9fe;',
        '  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;',
        '}',
        '',
        'header { background: linear-gradient(160deg, #2e1065, #6d28d9, #a78bfa); }',
        '',
        '.field-group {',
        '  display: grid;',
        '  grid-template-columns: 1fr auto 1fr;  /* Masse | / | Taille */',
        '  gap: 12px; align-items: center;',
        '}',
    ])

    elements += sec_title("3.3  Animation de l'anneau SVG")
    elements += body(
        "L'effet d'anneau progressif est obtenu en manipulant les propriétés SVG "
        "<code>stroke-dasharray</code> et <code>stroke-dashoffset</code> via CSS et JavaScript."
    )
    elements += code_block("index.css — ring SVG", [
        '.ring-fill {',
        '  fill: none;',
        '  stroke: #8b5cf6;               /* Couleur par défaut, changée par JS */',
        '  stroke-width: 12;',
        '  stroke-linecap: round;',
        '  stroke-dasharray: 314;         /* 2π × r=50 ≈ 314 — périmètre complet */',
        '  stroke-dashoffset: 314;        /* Anneau invisible au départ */',
        '  transform: rotate(-90deg);     /* Commence à midi (haut) */',
        '  transform-origin: center;',
        '  transition: stroke-dashoffset 1s ease, stroke 0.4s ease;',
        '}',
        '',
        '/* JS : fill.style.strokeDashoffset = 314 * (1 - imc/40) */',
    ])

    elements += sec_title("3.4  Mode clair (media query)")
    elements += body(
        "L'application respecte la préférence système de l'utilisateur via "
        "<code>@media (prefers-color-scheme: light)</code>. Les couleurs s'adaptent "
        "automatiquement sans JavaScript."
    )
    elements += code_block("index.css — light mode", [
        '@media (prefers-color-scheme: light) {',
        '  #app  { background: #f5f3ff; color: #1e0a44; }',
        '  header { background: linear-gradient(160deg, #4c1d95, #7c3aed, #a78bfa); }',
        '  .field input { background: #ffffff; color: #1e0a44; border-color: #c4b5fd; }',
        '  .result { background: #ede9fe; }',
        '}',
    ])

    elements += synth_box([
        "Palette : violet foncé #0d0718 → lavande #a78bfa — 5 tons",
        "Grid 3 colonnes : mise en page originale masse/séparateur/taille",
        "SVG ring : stroke-dashoffset animé (1s ease) via calcul JS",
        "Mode clair automatique via prefers-color-scheme — aucun JS nécessaire",
    ])
    elements.append(PageBreak())


# ── SECTION 4 — JAVASCRIPT ───────────────────────────────────
def section_js(elements, pt):
    pt[4] = "Section 4 — Logique JavaScript"
    elements += chap_header("4", "Logique JavaScript",
                             "Module Pattern IIFE — 8 fonctions documentées étape par étape")

    elements += sec_title("4.1  Module Pattern et constantes")
    elements += body(
        "Le code est encapsulé dans un <b>IIFE (Immediately Invoked Function Expression)</b> "
        "qui retourne uniquement la méthode <code>init</code>. Ce pattern évite de polluer "
        "le scope global et structure proprement le code."
    )
    elements += code_block("index.js — structure globale", [
        'var App = (function () {',
        '  // Constantes privées',
        '  var RING_MAX = 40;   // IMC max pour le remplissage complet de l\'anneau',
        '  var RING_LEN = 314;  // 2 × π × r=50 — périmètre SVG en px',
        '',
        '  // Tableau de catégories IMC',
        '  var CATEGORIES = [ ... ];',
        '',
        '  // Fonctions privées',
        '  function getCategory(imc) { ... }',
        '  function validate(masse, taille) { ... }',
        '  // ...',
        '',
        '  // API publique',
        '  return { init: init };',
        '}());',
        '',
        'App.init();  // Démarrage de l\'application',
    ])

    elements += sec_title("4.2  Tableau CATEGORIES")
    elements += body(
        "Le tableau <code>CATEGORIES</code> contient 5 objets décrivant les plages IMC, "
        "chacun avec un seuil <code>max</code>, un <code>label</code> à afficher, "
        "un <code>advice</code> personnalisé et une <code>color</code> hex."
    )
    cat_data = [
        [th("Catégorie"), th("Seuil max"), th("Couleur"), th("Conseil")],
        [td("Insuffisance pondérale"), td("18.5"), td("#FFB443 (orange)"), td("Consultez un professionnel de santé")],
        [td("Poids normal"),           td("25"),   td("#00E87A (vert)"),   td("Continuez vos bonnes habitudes !")],
        [td("Surpoids"),               td("30"),   td("#FFB443 (orange)"), td("Activité physique recommandée")],
        [td("Obésité modérée"),        td("35"),   td("#FF7043 (rouge-or)"), td("Suivi médical recommandé")],
        [td("Obésité sévère"),         td("∞"),    td("#FF4D6A (rouge-rose)"), td("Consultez rapidement")],
    ]
    elements += make_table(cat_data[0], cat_data[1:], [AVAIL*0.26, AVAIL*0.14, AVAIL*0.20, AVAIL*0.40])

    elements += sec_title("4.3  getCategory(imc)")
    elements += body(
        "Retourne le premier objet CATEGORIES dont le <code>max</code> est supérieur à l'IMC. "
        "Utilise <code>Array.find()</code> — s'arrête au premier match."
    )
    elements += code_block("index.js — getCategory", [
        'function getCategory(imc) {',
        '  return CATEGORIES.find(function (c) {',
        '    return imc < c.max;  // Premier seuil dépassé = bonne catégorie',
        '  });',
        '}',
        '',
        '// Exemple : getCategory(22.5) → { label: "Poids normal", color: "#00e87a", ... }',
    ])

    elements += sec_title("4.4  validate(masse, taille)")
    elements += body(
        "Contrôle les bornes des deux champs. Retourne un tableau des IDs en erreur "
        "(vide si tout est valide). Double validation : HTML <code>min/max</code> + JS."
    )
    elements += code_block("index.js — validate", [
        'function validate(masse, taille) {',
        '  var errors = [];',
        '  if (!masse  || masse  < 1   || masse  > 500) errors.push("masse");',
        '  if (!taille || taille < 0.5 || taille > 3)   errors.push("taille");',
        '  return errors;  // [] = valide, ["masse"] = erreur masse, etc.',
        '}',
    ])

    elements += sec_title("4.5  showErrors(fields)")
    elements += body(
        "Applique la classe <code>.error</code> aux champs invalides (bordure rouge, fond rose). "
        "Réinitialise d'abord toutes les erreurs avant d'appliquer les nouvelles."
    )
    elements += code_block("index.js — showErrors", [
        'function showErrors(fields) {',
        '  // Reset : supprimer toutes les erreurs existantes',
        '  document.getElementById("masse").classList.remove("error");',
        '  document.getElementById("taille").classList.remove("error");',
        '  // Appliquer les nouvelles erreurs',
        '  fields.forEach(function (id) {',
        '    document.getElementById(id).classList.add("error");',
        '  });',
        '}',
    ])

    elements += sec_title("4.6  animateRing(imc, color)")
    elements += body(
        "Anime l'anneau SVG en calculant le <code>stroke-dashoffset</code> proportionnel "
        "à l'IMC. Un délai de 50ms assure que le DOM est prêt avant l'animation."
    )
    elements += code_block("index.js — animateRing", [
        'function animateRing(imc, color) {',
        '  var fill   = document.querySelector(".ring-fill");',
        '  // Calcul : offset = RING_LEN * (1 - proportion)',
        '  // proportion = imc / RING_MAX (plafonné à 1)',
        '  var offset = RING_LEN * (1 - Math.min(imc / RING_MAX, 1));',
        '  fill.style.stroke = color;            // Couleur selon catégorie',
        '  setTimeout(function () {',
        '    fill.style.strokeDashoffset = offset; // Déclenche l\'animation CSS 1s',
        '  }, 50);',
        '}',
        '',
        '// Exemple : IMC=25 → offset=314*(1-25/40)=314*0.375=117.75',
    ])

    elements += sec_title("4.7  showResult(imc, category)")
    elements += body(
        "Met à jour les éléments DOM avec la valeur, la catégorie et le conseil, "
        "affiche la carte résultat, puis la fait défiler en vue."
    )
    elements += code_block("index.js — showResult", [
        'function showResult(imc, category) {',
        '  // Afficher la valeur arrondie à 1 décimale',
        '  document.getElementById("result-value").textContent = Math.round(imc * 10) / 10;',
        '  // Catégorie avec sa couleur',
        '  document.getElementById("result-category").textContent = category.label;',
        '  document.getElementById("result-category").style.color  = category.color;',
        '  // Conseil personnalisé',
        '  document.getElementById("result-advice").textContent = category.advice;',
        '  // Révéler la carte résultat',
        '  var resultDiv = document.getElementById("result");',
        '  resultDiv.removeAttribute("hidden");',
        '  resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });',
        '}',
    ])

    elements += sec_title("4.8  onSubmit(e) — orchestrateur")
    elements += body(
        "Fonction principale déclenchée à la soumission du formulaire. "
        "Elle coordonne validation → calcul → affichage → animation."
    )
    elements += code_block("index.js — onSubmit", [
        'function onSubmit(e) {',
        '  e.preventDefault();  // Empêche le rechargement de la page',
        '',
        '  var masse  = parseFloat(document.getElementById("masse").value);',
        '  var taille = parseFloat(document.getElementById("taille").value);',
        '  var errors = validate(masse, taille);',
        '',
        '  showErrors(errors);',
        '  if (errors.length) return;  // Stop si erreurs',
        '',
        '  var imc      = masse / (taille * taille);  // Formule IMC',
        '  var category = getCategory(imc);',
        '',
        '  showResult(imc, category);   // Afficher la carte',
        '  animateRing(imc, category.color);  // Animer le SVG',
        '}',
    ])

    elements += sec_title("4.9  bindEvents() et init()")
    elements += code_block("index.js — bindEvents / init", [
        'function bindEvents() {',
        '  // Écouter la soumission du formulaire',
        '  document.getElementById("imc-form").addEventListener("submit", onSubmit);',
        '}',
        '',
        'function init() {',
        '  bindEvents();  // Attacher tous les événements',
        '}',
        '',
        'return { init: init };  // Exposer uniquement init',
        '',
        '// Démarrage immédiat',
        'App.init();',
    ])

    elements += synth_box([
        "IIFE Module : scope privé, aucune variable globale exposée",
        "CATEGORIES[] : configuration centralisée des 5 plages IMC",
        "validate() : retourne un tableau d'IDs en erreur pour un reset propre",
        "animateRing() : setTimeout 50ms pour laisser le DOM se mettre à jour",
        "onSubmit() : orchestrateur — 4 étapes séquentielles claires",
    ])
    elements.append(PageBreak())


# ── SECTION 5 — SCREENSHOTS ──────────────────────────────────
def section_screens(elements, pt):
    pt[5] = "Section 5 — Captures d'écran"
    elements += chap_header("5", "Captures d'écran",
                             f"Placer les images dans : {SCREENS_DIR}")

    elements += sec_title("5.1  Formulaire de saisie")
    elements += body("Vue initiale : en-tête violet, deux champs de saisie, bouton de calcul.")
    elements += screen_box(SCR_FORM, "Calculateur IMC — Formulaire de saisie", 9*cm, 16*cm)

    elements += sec_title("5.2  Résultat IMC — Poids normal")
    elements += body("Carte résultat affichée : anneau SVG vert animé, valeur IMC, catégorie colorée, conseil.")
    elements += screen_box(SCR_RESULT, "Calculateur IMC — Résultat (poids normal)", 9*cm, 16*cm)

    elements += sec_title("5.3  État d'erreur")
    elements += body("Validation échouée : bordure rouge sur les champs invalides.")
    elements += screen_box(SCR_ERROR, "Calculateur IMC — Erreur de validation", 9*cm, 16*cm)

    elements.append(PageBreak())


# ── SECTION 6 — SYNTHÈSE ─────────────────────────────────────
def section_synthese(elements, pt):
    pt[6] = "Section 6 — Synthèse"
    elements += chap_header("6", "Synthèse finale",
                             "Bilan technique, points forts et compétences démontrées")

    elements += sec_title("6.1  Bilan technique")
    bilan = [
        [th("Aspect"), th("Détail"), th("Niveau")],
        [td("Architecture JS"), td("IIFE Module Pattern — scope isolé, API minimale"), td("✓ Solide")],
        [td("HTML sémantique"), td("form, label, button, aria-live — accessibilité native"), td("✓ Bon")],
        [td("CSS avancé"), td("Grid 3 col, SVG animation, media query light mode"), td("✓ Avancé")],
        [td("Validation"), td("Double validation HTML + JS avec retour visuel clair"), td("✓ Complet")],
        [td("UX mobile"), td("inputmode, viewport, scroll smooth, animation fluide"), td("✓ Optimisé")],
        [td("Cordova"), td("deviceready stub, CSP configurée, structure www/"), td("✓ Conforme")],
    ]
    elements += make_table(bilan[0], bilan[1:], [AVAIL*0.25, AVAIL*0.52, AVAIL*0.23])

    elements += sec_title("6.2  Compétences démontrées")
    for item in [
        "Maîtrise du <b>JavaScript Vanilla</b> sans dépendances (pas de jQuery, pas de framework).",
        "Utilisation avancée du <b>SVG inline</b> avec animation via stroke-dashoffset.",
        "Connaissance des <b>patterns de conception</b> (Module Pattern / IIFE).",
        "Bonne pratique <b>d'accessibilité</b> (aria-live, labels associés, inputmode).",
        "Respect des <b>contraintes Cordova</b> (CSP, structure www/, deviceready).",
    ]:
        elements += bullet(item)

    elements += synth_box([
        "8 fonctions JS documentées : getCategory, validate, showErrors, animateRing, showResult, onSubmit, bindEvents, init",
        "3 sections HTML : header, form (field-group), result (SVG + texte)",
        "CSS : thème violet, grid layout, SVG ring, mode clair automatique",
        "Zéro dépendance JS : application 100% Vanilla JavaScript",
    ], positive=True)
    elements.append(PageBreak())


# ── PAGE DE CLÔTURE ──────────────────────────────────────────
def closing_page(elements):
    elements.append(Spacer(1, 2.5*cm))
    elements.append(Paragraph("Calculateur IMC",
        S('cl', fontName=F_BOLD, fontSize=32, textColor=PRIMARY,
          alignment=TA_CENTER, leading=38)))
    elements.append(Spacer(1, 0.1*cm))
    elements.append(Paragraph("Rapport Technique — Application Cordova",
        S('cls', fontName=F, fontSize=10, textColor=ACCENT,
          alignment=TA_CENTER, leading=14)))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="60%", thickness=2, color=GOLD, spaceAfter=0.5*cm))
    info_st = S('inf', fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER, leading=16)
    for line in [
        "UCAD — École Supérieure Polytechnique (ESP)",
        "Salif Biaye — Fondateur / CEO",
        "Module : Développement Mobile — DIC3 — Édition Mai 2026",
    ]:
        elements.append(Paragraph(line, info_st))
    elements.append(Spacer(1, 0.8*cm))
    elements.append(HRFlowable(width="84%", thickness=0.5,
                                color=colors.HexColor("#9AB0C4"), spaceAfter=0.5*cm))
    disc_st = S('d', fontName=F_ITAL, fontSize=7.5, textColor=GRAY,
                alignment=TA_CENTER, leading=13)
    elements.append(Paragraph(
        "Document produit dans le cadre du cursus DIC3 — Usage académique uniquement", disc_st))


# ── MAIN ─────────────────────────────────────────────────────
def main():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=3.5*cm, bottomMargin=1.8*cm,
        title="Calculateur IMC — Rapport Technique",
        author="Groupe 3 — ESP/UCAD",
    )
    elements = []
    pt = chapter_titles
    current_page = [1]

    def on_page(canvas, doc):
        current_page[0] = doc.page

    cover_page(elements);    current_page[0] = 2
    sommaire(elements);      current_page[0] = 3
    section_overview(elements, pt)
    section_html(elements, pt)
    section_css(elements, pt)
    section_js(elements, pt)
    section_screens(elements, pt)
    section_synthese(elements, pt)
    closing_page(elements)

    doc.build(elements, canvasmaker=HFCanvas, onLaterPages=on_page)
    print(f"PDF genere : {OUTPUT}")


if __name__ == "__main__":
    main()
