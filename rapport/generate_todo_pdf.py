# -*- coding: utf-8 -*-
"""
Rapport Technique — Todo List (Ma Todo List)
Application mobile Apache Cordova
HTML5 · CSS3 · JavaScript + jQuery · Swipe gestures
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

# ── Palette verte (thème Todo List) ──────────────────────────
PRIMARY   = colors.HexColor("#14532D")   # Vert très foncé
SECONDARY = colors.HexColor("#16A34A")   # Vert principal
ACCENT    = colors.HexColor("#4ADE80")   # Vert clair / lime
GOLD      = colors.HexColor("#86EFAC")   # Vert pastel
LIGHT     = colors.HexColor("#F0FAF4")   # Vert très clair
LIGHT2    = colors.HexColor("#DCFCE7")   # Fond clair vert
WHITE     = colors.white
BLACK     = colors.black
GRAY      = colors.HexColor("#3A3A3A")
LGRAY     = colors.HexColor("#D9F0E2")
CODE_BG   = colors.HexColor("#071A0E")
CODE_FG   = colors.HexColor("#BBFECA")
TGRID     = colors.HexColor("#86EFAC")
C_GREEN   = colors.HexColor("#4ADE80")
C_RED     = colors.HexColor("#C0392B")
C_ORANGE  = colors.HexColor("#F97316")

# ── Constantes ───────────────────────────────────────────────
W, H = A4
MARGIN_L = 1.8 * cm
MARGIN_R = 1.8 * cm
AVAIL    = W - MARGIN_L - MARGIN_R

LOGO        = r"C:\Users\DELL\Downloads\logo_ucad.png"
SCREENS_DIR = r"C:\Users\DELL\Downloads\medy\screens"
SCR_LIST    = os.path.join(SCREENS_DIR, "todo_list.png")
SCR_SWIPE   = os.path.join(SCREENS_DIR, "todo_swipe.png")
SCR_MODAL   = os.path.join(SCREENS_DIR, "todo_modal.png")
SCR_EMPTY   = os.path.join(SCREENS_DIR, "todo_empty.png")

OUTPUT = os.path.join(os.path.dirname(__file__), "rapport_todo.pdf")
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
            self.setFillColor(ACCENT)
            self.rect(0, H - 3.28*cm, W, 0.08*cm, fill=1, stroke=0)
            if os.path.exists(LOGO):
                self.drawImage(LOGO, 2.0*cm, H - 2.75*cm, width=1.8*cm, height=1.8*cm, mask="auto")
            self.setFillColor(ACCENT)
            self.setFont(F_BOLD, 22)
            self.drawString(4.3*cm, H - 1.5*cm, "Ma Todo List")
            self.setFillColor(WHITE)
            self.setFont(F_BOLD, 9)
            self.drawString(4.3*cm, H - 2.1*cm, "Rapport Technique — Application Cordova")
            self.setFont(F, 7.5)
            self.drawString(4.3*cm, H - 2.55*cm,
                            "HTML5 · CSS3 · JavaScript + jQuery · Swipe Gestures — ESP/UCAD 2026")
        else:
            self.setFillColor(LGRAY)
            self.rect(0, H - 1.15*cm, W, 1.15*cm, fill=1, stroke=0)
            self.setFillColor(SECONDARY)
            self.setFont(F_BOLD, 8)
            self.drawString(MARGIN_L, H - 0.72*cm, "Ma Todo List")
            self.setFillColor(colors.HexColor("#166534"))
            self.setFont(F_BOLD, 6.8)
            self.drawString(MARGIN_L + 2.2*cm, H - 0.72*cm, "| Rapport Technique")
            chap = chapter_titles.get(pg, "")
            if chap:
                self.setFillColor(colors.HexColor("#4B6B5A"))
                self.setFont(F, 6.4)
                self.drawRightString(W - MARGIN_R, H - 0.72*cm, chap[:76])
        self.setFillColor(PRIMARY)
        self.rect(0, 0, W, 0.95*cm, fill=1, stroke=0)
        self.setFillColor(ACCENT)
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
chap_num_st   = S('cn', fontName=F_BOLD, fontSize=9,  textColor=ACCENT, leading=13, alignment=TA_LEFT)
sec_st        = S('s',  fontName=F_BOLD, fontSize=13, textColor=PRIMARY, leading=18,
                  spaceBefore=14, spaceAfter=4, alignment=TA_LEFT)
body_st       = S('b',  fontName=F, fontSize=9.5, textColor=GRAY, leading=17, spaceAfter=9,
                  alignment=TA_JUSTIFY)
bullet_st     = S('bu', fontName=F, fontSize=9.5, textColor=GRAY, leading=16,
                  leftIndent=14, firstLineIndent=-10, spaceAfter=5, alignment=TA_LEFT)
note_st       = S('n',  fontName=F_ITAL, fontSize=8.5, textColor=GRAY, leading=15,
                  leftIndent=10, alignment=TA_JUSTIFY)
code_st       = S('co', fontName=F_MONO, fontSize=7.8, textColor=CODE_FG, backColor=CODE_BG,
                  leading=13, leftIndent=8, rightIndent=8, spaceBefore=3, spaceAfter=3,
                  alignment=TA_LEFT)
code_title_st = S('cot', fontName=F_MONOB, fontSize=7.5, textColor=ACCENT, backColor=CODE_BG,
                  leading=12, leftIndent=8, alignment=TA_LEFT)
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
        ('BACKGROUND',    (0,0), (-1,-1), PRIMARY),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 14),
        ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEBELOW',     (0,0), (-1,-1), 4, ACCENT),
    ]))
    out = [t]
    if subtitle:
        out.append(Spacer(1, 0.3*cm))
        out.append(Paragraph(subtitle, note_st))
    out.append(Spacer(1, 0.6*cm))
    return out


def sec_title(text):
    return [Paragraph(text, sec_st),
            HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=2, spaceAfter=4)]


def body(text):
    return [Paragraph(text, body_st)]


def bullet(text):
    return [Paragraph(f"• {text}", bullet_st)]


def code_block(filename, lines):
    rows = [[Paragraph(f"📄  {filename}", code_title_st)]]
    for line in lines:
        rows.append([Paragraph(line.replace(" ", " ").replace("<", "&lt;").replace(">", "&gt;"),
                               code_st)])
    t = Table(rows, colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING',    (0,0), (0,0), 7),
        ('BOTTOMPADDING', (0,0), (0,0), 5),
        ('TOPPADDING',    (0,1), (-1,-1), 2),
        ('BOTTOMPADDING', (0,1), (-1,-1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
        ('LINEBELOW',     (0,0), (0,0), 1, ACCENT),
        ('BOX',           (0,0), (-1,-1), 1, SECONDARY),
    ]))
    return [t, Spacer(1, 0.25*cm)]


def screen_box(path, caption, max_w=12*cm, max_h=8*cm):
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
            ('BACKGROUND', (0,0), (0,0), WHITE),
            ('TOPPADDING', (0,0), (0,0), 10), ('BOTTOMPADDING', (0,0), (0,0), 8),
            ('BACKGROUND', (0,1), (0,1), LIGHT),
            ('LINEABOVE',  (0,1), (0,1), 2, SECONDARY),
            ('TOPPADDING', (0,1), (0,1), 6), ('BOTTOMPADDING', (0,1), (0,1), 6),
            ('ALIGN',      (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
            ('BOX',        (0,0), (-1,-1), 1.5, TGRID),
        ]))
        return [KeepTogether([frame]), Spacer(1, 0.4*cm)]
    else:
        ph_st  = S('ph',   fontName=F_BOLD, fontSize=10, textColor=SECONDARY, alignment=TA_CENTER, leading=16)
        hint_st = S('hint', fontName=F_ITAL, fontSize=8, textColor=GRAY, alignment=TA_CENTER, leading=12)
        rows = [
            [Paragraph("📸", ph_st)],
            [Paragraph(caption, ph_st)],
            [Paragraph(f"Placer la capture ici :\n{path}", hint_st)],
        ]
        t = Table(rows, colWidths=[AVAIL])
        t.setStyle(TableStyle([
            ('BACKGROUND',    (0,0), (-1,-1), LIGHT),
            ('ALIGN',         (0,0), (-1,-1), 'CENTER'),
            ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING',    (0,0), (-1,-1), 20),
            ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ('BOX',           (0,0), (-1,-1), 1.5, SECONDARY),
            ('LINEBEFORE',    (0,0), (0,-1), 4, SECONDARY),
        ]))
        return [t, Spacer(1, 0.4*cm)]


def synth_box(lines, positive=True):
    accent = C_GREEN if positive else C_RED
    hdr_bg = colors.HexColor("#1A5C35") if positive else PRIMARY
    AW = 0.22 * cm; TW = AVAIL - AW
    bul = S('rb', fontName=F, fontSize=9, textColor=colors.HexColor("#0D2016"),
            leading=14, leftIndent=6, firstLineIndent=-6, alignment=TA_LEFT)
    data = [["", Paragraph("Synthèse", synth_hdr_st)]]
    for line in lines:
        data.append(["", Paragraph(f"◆  {line}", bul)])
    t = Table(data, colWidths=[AW, TW])
    cmds = [
        ('BACKGROUND', (0,0), (0,-1), accent),
        ('BACKGROUND', (1,0), (1,0),  hdr_bg),
        ('TOPPADDING',    (0,0), (-1,0), 7), ('BOTTOMPADDING', (0,0), (-1,0), 7),
        ('TOPPADDING',    (0,1), (-1,-1), 5), ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('LEFTPADDING',   (1,0), (1,-1), 12), ('RIGHTPADDING', (1,0), (1,-1), 12),
        ('LEFTPADDING',   (0,0), (0,-1), 0),  ('RIGHTPADDING', (0,0), (0,-1), 0),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('BOX',           (0,0), (-1,-1), 1.2, TGRID),
        ('LINEBELOW',     (1,1), (1,-2), 0.4, colors.HexColor("#BBF7D0")),
    ]
    for i in range(1, len(data)):
        bg = LIGHT if i % 2 == 1 else WHITE
        cmds.append(('BACKGROUND', (1,i), (1,i), bg))
    t.setStyle(TableStyle(cmds))
    return [Spacer(1, 0.3*cm), t, Spacer(1, 0.3*cm)]


def make_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [AVAIL / len(headers)] * len(headers)
    data = [headers] + rows
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
        ('FONTNAME',   (0,0), (-1,0), F_BOLD), ('FONTSIZE', (0,0), (-1,0), 8),
        ('FONTNAME',   (0,1), (-1,-1), F),      ('FONTSIZE', (0,1), (-1,-1), 8),
        ('TEXTCOLOR',  (0,1), (-1,-1), GRAY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT]),
        ('GRID',       (0,0), (-1,-1), 0.3, TGRID),
        ('LINEBELOW',  (0,0), (-1,0), 2, SECONDARY),
        ('ALIGN',      (0,0), (-1,-1), 'LEFT'),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
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
            S('esp', fontName=F, fontSize=7.5, textColor=SECONDARY,
              alignment=TA_CENTER, leading=12)))
        elements.append(Spacer(1, 0.2*cm))

    elements.append(HRFlowable(width="92%", thickness=1, color=GOLD, spaceAfter=0.3*cm))

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

    elements.append(Paragraph("Ma Todo List",
        S('title', fontName=F_BOLD, fontSize=34, textColor=PRIMARY,
          leading=42, alignment=TA_CENTER)))
    elements.append(Paragraph("Application Mobile — Apache Cordova",
        S('sub', fontName=F, fontSize=11, textColor=colors.HexColor("#166534"),
          leading=15, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.15*cm))

    subj = Table([
        [Paragraph("Documentation complète — HTML · CSS · JavaScript + jQuery", S('wt', fontName=F_BOLD,
                   fontSize=12, textColor=WHITE, leading=17, alignment=TA_CENTER))],
        [Paragraph("Swipe gestures, localStorage, filtres, modal bottom sheet — expliqués étape par étape",
                   S('ws', fontName=F, fontSize=8, textColor=GOLD,
                     leading=12, alignment=TA_CENTER))],
    ], colWidths=[width])
    subj.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('TOPPADDING', (0,0), (-1,0), 12), ('BOTTOMPADDING', (0,0), (-1,0), 3),
        ('TOPPADDING', (0,1), (-1,1), 3),  ('BOTTOMPADDING', (0,1), (-1,1), 12),
    ]))
    elements.append(subj)

    stat_st = S('stat', fontName=F_BOLD, fontSize=9, textColor=WHITE, leading=13, alignment=TA_CENTER)
    stats = Table([[
        Paragraph("5 sections HTML\ndocumentées", stat_st),
        Paragraph("CSS vert\nthème sombre", stat_st),
        Paragraph("17 fonctions JS\ndocumentées", stat_st),
        Paragraph("Swipe touch\nnative mobile", stat_st),
    ]], colWidths=[width/4]*4)
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.25, colors.HexColor("#15803D")),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(stats)
    elements.append(Spacer(1, 0.35*cm))

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
        ('LINEBELOW', (0,0), (0,0), 2.5, ACCENT),
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
        ["Application :", "Ma Todo List"],
        ["Technologie :", "Apache Cordova · HTML5 · CSS3 · JavaScript + jQuery 3.7"],
        ["Fonctionnalité clé :", "Swipe gestures (touch events), localStorage, filtres"],
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
    elements.append(HRFlowable(width="84%", thickness=1.5, color=TGRID))
    elements.append(PageBreak())


# ── SOMMAIRE ─────────────────────────────────────────────────
def sommaire(elements):
    elements.append(Spacer(1, 0.3*cm))
    elements.append(Paragraph("Sommaire", S('som', fontName=F_BOLD, fontSize=18, textColor=PRIMARY,
                               leading=22, alignment=TA_CENTER)))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY,
                                spaceBefore=8, spaceAfter=10))
    sections = [
        ("1", "Vue d'ensemble", "Objectif, tech stack, gestion des tâches"),
        ("2", "Structure HTML", "Header, filtres, liste, FAB, modal"),
        ("3", "Feuille de style CSS", "Palette verte, swipe panels, animations"),
        ("4", "Logique JavaScript", "17 fonctions : swipe, CRUD, modal, filtres"),
        ("5", "Captures d'écran", "Liste, swipe, modal, état vide"),
        ("6", "Synthèse", "Bilan technique et compétences"),
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
    ]))
    elements.append(tbl)
    elements.append(PageBreak())


# ── SECTION 1 — VUE D'ENSEMBLE ───────────────────────────────
def section_overview(elements, pt):
    pt[1] = "Section 1 — Vue d'ensemble"
    elements += chap_header("1", "Vue d'ensemble",
                             "Objectif, pile technologique et fonctionnement global de l'application")

    elements += sec_title("1.1  Qu'est-ce que Ma Todo List ?")
    elements += body(
        "<b>Ma Todo List</b> est une application mobile de gestion de tâches développée "
        "avec <b>Apache Cordova</b>. Elle permet d'ajouter, compléter et supprimer des tâches "
        "avec une interface inspirée des meilleures apps natives. La caractéristique principale "
        "est le système de <b>swipe (glissement tactile)</b> : glisser à droite pour valider "
        "une tâche, à gauche pour la supprimer."
    )
    elements += body(
        "Les tâches sont persistées localement via <b>localStorage</b> — elles survivent "
        "à la fermeture de l'application. L'interface propose des <b>filtres</b> "
        "(Toutes/Actives/Terminées) et un bouton flottant (FAB) pour ajouter de nouvelles tâches."
    )

    elements += sec_title("1.2  Pile technologique")
    tech_data = [
        [th("Technologie"), th("Rôle"), th("Version")],
        [td("Apache Cordova"), td("Wrapper natif Android/iOS"), td("Dernière stable")],
        [td("HTML5"), td("Structure : header, liste ul/li, modal, FAB"), td("Standard W3C")],
        [td("CSS3"), td("Thème vert sombre, swipe panels, animations"), td("Standard W3C")],
        [td("JavaScript (IIFE)"), td("Logique CRUD, filtres, rendu DOM"), td("ES6+")],
        [td("jQuery 3.7.1"), td("Sélecteurs DOM, events, helpers escape()"), td("CDN code.jquery.com")],
        [td("Font Awesome 6.5"), td("Icônes (check, trash, plus, xmark)"), td("CDN Cloudflare")],
        [td("localStorage"), td("Persistance des tâches (clé : 'todos')"), td("Web API native")],
    ]
    elements += make_table(tech_data[0], tech_data[1:], [AVAIL*0.22, AVAIL*0.50, AVAIL*0.28])

    elements += sec_title("1.3  Flux utilisateur complet")
    for step in [
        "<b>Ajouter une tâche :</b> clic sur le FAB (+) → modal bottom sheet → saisie → Enregistrer.",
        "<b>Compléter une tâche :</b> swipe droit (≥60px) → flash vert → tâche barrée.",
        "<b>Supprimer une tâche :</b> swipe gauche → panneau rouge visible → clic ou swipe fort.",
        "<b>Filtrer :</b> boutons Toutes / Actives / Terminées → liste mise à jour instantanément.",
        "<b>Nettoyer :</b> bouton 'Supprimer terminées' visible si au moins 1 tâche complétée.",
        "<b>Persistance :</b> toute modification → localStorage → données conservées au rechargement.",
    ]:
        elements += bullet(step)

    elements += synth_box([
        "Fonctionnalité phare : swipe tactile natif (touchstart/touchmove/touchend)",
        "Persistance : localStorage JSON — survit à la fermeture de l'app",
        "jQuery utilisé pour la manipulation DOM et les event listeners",
        "Thème vert foncé (#071A0E → #4ADE80) avec mode clair automatique",
    ])
    elements.append(PageBreak())


# ── SECTION 2 — STRUCTURE HTML ───────────────────────────────
def section_html(elements, pt):
    pt[2] = "Section 2 — Structure HTML"
    elements += chap_header("2", "Structure HTML",
                             "Analyse complète des 5 sections du fichier index.html")

    elements += sec_title("2.1  Conteneur principal et en-tête")
    elements += code_block("index.html — app + header", [
        '&lt;div id="app"&gt;',
        '  &lt;header&gt;',
        '    &lt;h1&gt;Ma Todo List&lt;/h1&gt;',
        '    &lt;p id="summary"&gt;0 tâche restante&lt;/p&gt;  &lt;!-- Mis à jour par JS --&gt;',
        '  &lt;/header&gt;',
        '',
        '  &lt;div id="filters"&gt;',
        '    &lt;button class="filter-btn active" data-filter="all"&gt;Toutes&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-filter="active"&gt;Actives&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-filter="completed"&gt;Terminées&lt;/button&gt;',
        '  &lt;/div&gt;',
        '',
        '  &lt;ul id="task-list"&gt;&lt;/ul&gt;  &lt;!-- Rempli dynamiquement par JS --&gt;',
        '',
        '  &lt;div id="footer" style="display:none;"&gt;',
        '    &lt;button id="btn-clear-completed"&gt;Supprimer terminées&lt;/button&gt;',
        '  &lt;/div&gt;',
        '&lt;/div&gt;',
    ])
    for item in [
        "<b>#summary</b> : compteur dynamique mis à jour par <code>renderSummary()</code>.",
        "<b>data-filter</b> : attribut lu par JS pour identifier le filtre actif.",
        "<b>#task-list (ul)</b> : liste vide au chargement, peuplée par <code>renderList()</code>.",
        "<b>#footer display:none</b> : caché par défaut, affiché uniquement si des tâches sont complétées.",
    ]:
        elements += bullet(item)

    elements += sec_title("2.2  Élément de tâche (généré dynamiquement)")
    elements += body(
        "Chaque tâche est générée par <code>buildTaskHtml()</code>. Le <code>&lt;li&gt;</code> "
        "contient 3 couches superposées : panneau gauche (done), panneau droit (delete), "
        "et le contenu principal par-dessus."
    )
    elements += code_block("index.js — buildTaskHtml (HTML généré)", [
        '&lt;li class="task-item" data-id="[timestamp]"&gt;',
        '  &lt;!-- Panneau gauche : swipe droit → cocher la tâche --&gt;',
        '  &lt;div class="task-action-left"&gt;',
        '    &lt;i class="fa-solid fa-check"&gt;&lt;/i&gt;',
        '  &lt;/div&gt;',
        '  &lt;!-- Panneau droit : swipe gauche → supprimer --&gt;',
        '  &lt;div class="task-action-right"&gt;',
        '    &lt;i class="fa-solid fa-trash"&gt;&lt;/i&gt;',
        '  &lt;/div&gt;',
        '  &lt;!-- Contenu principal (se translate via CSS transform) --&gt;',
        '  &lt;div class="task-content [done?]"&gt;',
        '    &lt;div class="task-check [checked?]"&gt; ... &lt;/div&gt;',
        '    &lt;span class="task-text"&gt;[texte de la tâche]&lt;/span&gt;',
        '  &lt;/div&gt;',
        '&lt;/li&gt;',
    ])

    elements += sec_title("2.3  Bouton FAB et modal d'ajout")
    elements += code_block("index.html — FAB + modal", [
        '&lt;!-- FAB : bouton flottant fixe en bas à droite --&gt;',
        '&lt;button id="btn-add" title="Ajouter une tâche"&gt;',
        '  &lt;i class="fa-solid fa-plus"&gt;&lt;/i&gt;',
        '&lt;/button&gt;',
        '',
        '&lt;!-- Modal bottom sheet --&gt;',
        '&lt;div id="modal-overlay" class="hidden"&gt;',
        '  &lt;div id="modal"&gt;',
        '    &lt;div id="modal-header"&gt;',
        '      &lt;h2 id="modal-title"&gt;Nouvelle tâche&lt;/h2&gt;',
        '      &lt;button id="modal-close"&gt;&lt;i class="fa-solid fa-xmark"&gt;&lt;/i&gt;&lt;/button&gt;',
        '    &lt;/div&gt;',
        '    &lt;div id="modal-body"&gt;',
        '      &lt;input type="text" id="f-task" placeholder="Ex : Faire les courses" maxlength="100"&gt;',
        '      &lt;p id="form-error" class="hidden"&gt;Veuillez saisir une tâche.&lt;/p&gt;',
        '    &lt;/div&gt;',
        '    &lt;div id="modal-footer"&gt;',
        '      &lt;button id="btn-cancel"&gt;Annuler&lt;/button&gt;',
        '      &lt;button id="btn-save"&gt;Enregistrer&lt;/button&gt;',
        '    &lt;/div&gt;',
        '  &lt;/div&gt;',
        '&lt;/div&gt;',
    ])
    elements += body(
        "La classe <code>hidden</code> est ajoutée/retirée par jQuery pour afficher/masquer "
        "le modal. L'overlay sombre derrière le modal ferme celui-ci en cas de clic extérieur."
    )
    elements += synth_box([
        "3 couches dans chaque li : panneau gauche / panneau droit / contenu (translateX)",
        "data-id : attribut clé reliant le DOM aux données en mémoire",
        "FAB fixed : reste visible pendant le scroll de la liste",
        "Modal overlay : fermeture en cliquant hors du panneau blanc",
    ])
    elements.append(PageBreak())


# ── SECTION 3 — CSS ──────────────────────────────────────────
def section_css(elements, pt):
    pt[3] = "Section 3 — CSS & Thème Visuel"
    elements += chap_header("3", "Feuille de style CSS",
                             "Palette verte, système de swipe, animations et thème sombre")

    elements += sec_title("3.1  Palette de couleurs")
    pal_data = [
        [th("Élément"), th("Hex"), th("Usage")],
        [tag("fond global"),       td("#071A0E"), td("Fond arrière très sombre (vert-noir)")],
        [tag("header gradient"),   td("#14532D → #4ADE80"), td("Dégradé en-tête du haut vers le bas")],
        [tag("accent principal"),  td("#16A34A"), td("Boutons, bordures actives, FAB")],
        [tag("accent clair"),      td("#4ADE80"), td("Hover, tâches complétées (lime)")],
        [tag("texte"),             td("#E0F0E5"), td("Texte principal sur fond sombre (vert clair)")],
        [tag("panneau done"),      td("#16A34A"), td("Panneau de gauche (swipe droit)")],
        [tag("panneau delete"),    td("#C0392B"), td("Panneau de droite (swipe gauche)")],
        [tag("tâche barrée"),      td("#4ADE80 barré"), td("Texte avec text-decoration: line-through")],
    ]
    elements += make_table(pal_data[0], pal_data[1:], [AVAIL*0.25, AVAIL*0.28, AVAIL*0.47])

    elements += sec_title("3.2  Mécanisme de swipe CSS")
    elements += body(
        "Le swipe est rendu possible par la superposition de 3 éléments dans chaque <code>&lt;li&gt;</code>. "
        "Les panneaux d'action sont <b>positionnés en absolu</b> derrière le contenu principal. "
        "Le contenu se translate via <code>translateX</code> pour révéler le panneau sous-jacent."
    )
    elements += code_block("index.css — structure swipe", [
        '.task-item { position: relative; overflow: hidden; }',
        '',
        '/* Panneaux cachés derrière le contenu */',
        '.task-action-left, .task-action-right {',
        '  position: absolute; top: 0; bottom: 0; width: 80px;',
        '  display: flex; align-items: center; justify-content: center;',
        '  opacity: 0;  /* Transparents par défaut, opacity augmentée par JS */',
        '}',
        '.task-action-left  { left: 0;  background: #16a34a; }  /* Vert — done */',
        '.task-action-right { right: 0; background: #c0392b; }  /* Rouge — delete */',
        '',
        '/* Contenu principal positionné au-dessus */',
        '.task-content {',
        '  position: relative; z-index: 1;',
        '  /* translateX géré par JS via setTranslate() */',
        '}',
    ])

    elements += sec_title("3.3  Animations CSS")
    anim_data = [
        [th("Animation"), th("Durée"), th("Déclencheur"), th("Effet")],
        [td("slideIn"),     td("0.2s ease"), td("Ajout d'une tâche"), td("La tâche entre par le bas (translateY)")],
        [td("slideOutLeft"),td("0.28s ease"),td("Suppression"),       td("La tâche sort vers la gauche")],
        [td("flashGreen"),  td("0.35s ease"),td("Validation (done)"), td("Flash de fond vert sur la tâche")],
        [td("slideUp"),     td("0.25s ease"),td("Ouverture modal"),   td("Le modal monte depuis le bas")],
        [td("fadeIn"),      td("0.18s ease"),td("Overlay modal"),     td("Fondu de l'arrière-plan sombre")],
    ]
    elements += make_table(anim_data[0], anim_data[1:], [AVAIL*0.22, AVAIL*0.17, AVAIL*0.25, AVAIL*0.36])

    elements += code_block("index.css — animation flash done", [
        '@keyframes flashGreen {',
        '  0%   { background-color: transparent; }',
        '  30%  { background-color: rgba(74, 222, 128, 0.35); }',
        '  100% { background-color: transparent; }',
        '}',
        '',
        '.task-item.anim-done { animation: flashGreen 0.35s ease; }',
        '/* JS : $item.addClass("anim-done") → setTimeout(removeClass, 350) */',
    ])

    elements += synth_box([
        "Swipe CSS : 3 couches superposées — panneaux positionnés absolute, contenu z-index:1",
        "Opacity progressive : JS augmente l'opacité du panneau visible au fur et à mesure",
        "5 animations CSS : slideIn, slideOutLeft, flashGreen, slideUp, fadeIn",
        "Mode clair : prefers-color-scheme media query — fond #f0faf4, texte #0d2016",
    ])
    elements.append(PageBreak())


# ── SECTION 4 — JAVASCRIPT ───────────────────────────────────
def section_js(elements, pt):
    pt[4] = "Section 4 — Logique JavaScript"
    elements += chap_header("4", "Logique JavaScript",
                             "IIFE Module avec jQuery — 17 fonctions documentées par groupe")

    elements += sec_title("4.1  Structure et état global")
    elements += code_block("index.js — module + state", [
        'var App = (function ($) {          // jQuery injecté en paramètre',
        '  var STORAGE_KEY   = "todos";',
        '  var REVEAL_W      = 80;          // Largeur px du panneau swipe',
        '  var SWIPE_COMMIT  = 60;          // Distance minimale pour valider un swipe',
        '  var DIR_THRESHOLD = 6;           // Distance avant de locker la direction',
        '',
        '  var state = {',
        '    tasks:  load(),    // Tableau des tâches depuis localStorage',
        '    filter: "all",     // Filtre actif : all | active | completed',
        '    $open:  null       // Référence jQuery de l\'item swipé ouvert',
        '  };',
        '  // ...',
        '}($));          // jQuery passé immédiatement',
        '',
        '$(App.init.bind(App));  // Démarrage après chargement DOM + jQuery',
    ])

    elements += sec_title("4.2  Stockage — load() et persist()")
    elements += code_block("index.js — load / persist", [
        'function load() {',
        '  try {',
        '    return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");',
        '    // Retourne [] si clé absente ou JSON invalide',
        '  } catch (_) { return []; }  // Sécurité : JSON.parse peut lancer',
        '}',
        '',
        'function persist() {',
        '  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.tasks));',
        '  // Sérialise le tableau complet — appelé après chaque modification',
        '}',
    ])
    elements += body(
        "<code>escape(t)</code> : <code>$('&lt;div&gt;').text(t).html()</code> — "
        "astuce jQuery pour échapper les caractères HTML et prévenir les injections XSS."
    )
    elements += body(
        "<code>plural(n)</code> : construit la phrase '1 tâche restante' / '3 tâches restantes' "
        "avec accord grammatical français."
    )

    elements += sec_title("4.3  Filtrage — getFiltered()")
    elements += code_block("index.js — getFiltered", [
        'function getFiltered() {',
        '  return state.tasks.filter(function (t) {',
        '    if (state.filter === "active")    return !t.done;    // Tâches non faites',
        '    if (state.filter === "completed") return t.done;     // Tâches faites',
        '    return true;  // "all" → tout retourner',
        '  });',
        '}',
    ])

    elements += sec_title("4.4  Rendu HTML — buildTaskHtml() et buildEmptyHtml()")
    elements += body(
        "<code>buildTaskHtml(t)</code> génère le HTML de chaque tâche avec ses 3 couches. "
        "<code>buildEmptyHtml()</code> génère un état vide contextuel selon le filtre actif."
    )
    elements += code_block("index.js — buildEmptyHtml", [
        'function buildEmptyHtml() {',
        '  var cfg = {',
        '    completed: { icon: "fa-circle-check",   msg: "Aucune tâche terminée" },',
        '    active:    { icon: "fa-hourglass-half", msg: "Aucune tâche active" },',
        '    all:       { icon: "fa-list-check",     msg: "Ajoutez votre première tâche !" }',
        '  };',
        '  var c = cfg[state.filter];',
        '  // Retourne un <li> avec l\'icône et le message adaptés au filtre courant',
        '}',
    ])

    elements += sec_title("4.5  Actions CRUD — addTask, toggleTask, deleteTask, clearCompleted")
    elements += code_block("index.js — CRUD actions", [
        '// Ajouter : insère en tête du tableau (unshift = tâche récente en premier)',
        'function addTask(text) {',
        '  state.tasks.unshift({ id: Date.now(), text: text, done: false });',
        '  persist(); render();',
        '}',
        '',
        '// Basculer done/undone',
        'function toggleTask(id) {',
        '  var t = state.tasks.find(function (t) { return t.id === id; });',
        '  if (!t) return;',
        '  t.done = !t.done;',
        '  persist(); render();',
        '}',
        '',
        '// Supprimer avec animation sortie',
        'function deleteTask(id, $item) {',
        '  $item.addClass("anim-delete");       // Déclenche slideOutLeft 0.28s',
        '  setTimeout(function () {',
        '    state.tasks = state.tasks.filter(function (t) { return t.id !== id; });',
        '    persist(); render();',
        '  }, 280);  // Attendre la fin de l\'animation',
        '}',
        '',
        '// Nettoyer : garder uniquement les tâches non terminées',
        'function clearCompleted() {',
        '  state.tasks = state.tasks.filter(function (t) { return !t.done; });',
        '  persist(); render();',
        '}',
    ])

    elements += sec_title("4.6  Swipe — setTranslate, openItem, closeOpen")
    elements += code_block("index.js — swipe helpers", [
        '// Translate le contenu et ajuste l\'opacité du panneau révélé',
        'function setTranslate($item, x, animate) {',
        '  $item.find(".task-content").css({',
        '    transition: animate ? "transform 0.22s ease" : "none",',
        '    transform:  x ? "translateX(" + x + "px)" : ""',
        '  });',
        '  // x>0 : panneau gauche (done) visible',
        '  // x<0 : panneau droit (delete) visible',
        '  if (x > 0) {',
        '    var pct = Math.min(x / REVEAL_W, 1);  // 0 → 1',
        '    $item.find(".task-action-left").css("opacity", pct);',
        '    $item.find(".task-action-right").css("opacity", 0);',
        '  } else if (x < 0) { /* symétrique pour panneau droit */ }',
        '  else { /* reset opacity à 0 */ }',
        '}',
        '',
        'function openItem($item) {',
        '  if (state.$open && state.$open[0] !== $item[0]) closeOpen(true);',
        '  state.$open = $item;',
        '  $item.addClass("revealed");',
        '  setTranslate($item, -REVEAL_W, true);  // Glisse de -80px',
        '}',
        '',
        'function closeOpen(animate) {',
        '  if (!state.$open) return;',
        '  setTranslate(state.$open, 0, animate);',
        '  state.$open.removeClass("revealed");',
        '  state.$open = null;',
        '}',
    ])

    elements += sec_title("4.7  Swipe — bindSwipe() (gestionnaire tactile)")
    elements += body(
        "La fonction <code>bindSwipe()</code> attache 3 gestionnaires tactiles sur <code>#task-list</code> "
        "en utilisant la délégation d'événements jQuery. Un objet <code>touch</code> local "
        "stocke l'état du geste en cours."
    )
    elements += code_block("index.js — bindSwipe logic", [
        'function bindSwipe() {',
        '  var touch = { x: 0, y: 0, dir: null, active: false };',
        '',
        '  // touchstart : mémoriser le point de départ',
        '  $("#task-list").on("touchstart", ".task-item", function (e) {',
        '    var t = e.originalEvent.touches[0];',
        '    touch.x = t.clientX; touch.y = t.clientY;',
        '    touch.dir = null; touch.active = true;',
        '  });',
        '',
        '  // touchmove : calculer déplacement et animer',
        '  $("#task-list").on("touchmove", ".task-item", function (e) {',
        '    var dx = t.clientX - touch.x, dy = t.clientY - touch.y;',
        '    // Locker direction après DIR_THRESHOLD (6px)',
        '    if (!touch.dir && Math.max(Math.abs(dx), Math.abs(dy)) > DIR_THRESHOLD)',
        '      touch.dir = Math.abs(dx) > Math.abs(dy) ? "h" : "v";',
        '    if (touch.dir !== "h") return;  // Scroll vertical → ignorer',
        '    e.preventDefault();  // Bloquer le scroll si swipe horizontal',
        '    setTranslate($(this), clamped, false);',
        '  });',
        '',
        '  // touchend : décider de l\'action selon distance parcourue',
        '  // dx < -60 → openItem (panneau delete)',
        '  // dx > +60 → toggleTask avec flash vert',
        '  // sinon   → fermer (snap back)',
        '}',
    ])

    elements += sec_title("4.8  Modal — openModal, closeModal, saveTask")
    elements += code_block("index.js — modal", [
        'function openModal() {',
        '  $("#f-task").val("");',
        '  $("#form-error").addClass("hidden");',
        '  $("#modal-overlay").removeClass("hidden");  // Afficher le modal',
        '  setTimeout(function () { $("#f-task").focus(); }, 150);  // Focus clavier',
        '}',
        '',
        'function closeModal() {',
        '  $("#modal-overlay").addClass("hidden");  // Masquer sans réinitialiser',
        '}',
        '',
        'function saveTask() {',
        '  var text = $("#f-task").val().trim();',
        '  if (!text) { $("#form-error").removeClass("hidden"); return; }',
        '  addTask(text);  // Appelle persist() + render()',
        '  closeModal();',
        '}',
    ])

    elements += synth_box([
        "Module IIFE + jQuery : scope privé, jQuery injecté proprement en paramètre",
        "State objet centralisé : tasks[], filter, $open — source unique de vérité",
        "Swipe 3 phases : touchstart (mémoriser) / touchmove (animer) / touchend (décider)",
        "deleteTask : animation 280ms avant suppression réelle — UX fluide",
        "17 fonctions : load, persist, escape, plural, getFiltered, buildTaskHtml, buildEmptyHtml, renderList, renderSummary, renderFooter, render, addTask, toggleTask, deleteTask, clearCompleted, setFilter, setTranslate, openItem, closeOpen, bindSwipe, openModal, closeModal, saveTask, bindEvents, init",
    ])
    elements.append(PageBreak())


# ── SECTION 5 — SCREENSHOTS ──────────────────────────────────
def section_screens(elements, pt):
    pt[5] = "Section 5 — Captures d'écran"
    elements += chap_header("5", "Captures d'écran", f"Placer les images dans : {SCREENS_DIR}")

    elements += sec_title("5.1  Liste des tâches")
    elements += body("Vue principale avec les tâches, les filtres et le FAB vert.")
    elements += screen_box(SCR_LIST, "Todo List — Vue principale", 9*cm, 16*cm)

    elements += sec_title("5.2  Swipe en action")
    elements += body("Panneau rouge visible après swipe gauche, icône poubelle révélée.")
    elements += screen_box(SCR_SWIPE, "Todo List — Swipe gauche (delete)", 9*cm, 16*cm)

    elements += sec_title("5.3  Modal d'ajout")
    elements += body("Bottom sheet avec champ de saisie et boutons Annuler / Enregistrer.")
    elements += screen_box(SCR_MODAL, "Todo List — Modal ajout tâche", 9*cm, 16*cm)

    elements += sec_title("5.4  État vide")
    elements += body("Message adapté au filtre actif si aucune tâche ne correspond.")
    elements += screen_box(SCR_EMPTY, "Todo List — État vide (aucune tâche)", 9*cm, 16*cm)

    elements.append(PageBreak())


# ── SECTION 6 — SYNTHÈSE ─────────────────────────────────────
def section_synthese(elements, pt):
    pt[6] = "Section 6 — Synthèse"
    elements += chap_header("6", "Synthèse finale", "Bilan technique et compétences démontrées")

    elements += sec_title("6.1  Tableau récapitulatif")
    bilan = [
        [th("Aspect"), th("Détail"), th("Niveau")],
        [td("Swipe tactile"), td("Touch events natifs — lock de direction, snap, seuils"), td("✓ Avancé")],
        [td("Architecture JS"), td("IIFE + jQuery, state centralisé, fonctions atomiques"), td("✓ Solide")],
        [td("Persistance"), td("localStorage JSON — load/persist après chaque action"), td("✓ Complet")],
        [td("Animations"), td("5 animations CSS : slide, flash, fadeIn — timing précis"), td("✓ Soigné")],
        [td("UX mobile"), td("FAB, modal bottom sheet, feedback visuel, état vide"), td("✓ Optimisé")],
        [td("Sécurité"), td("escape() XSS via jQuery, pas d'innerHTML direct"), td("✓ Bon")],
    ]
    elements += make_table(bilan[0], bilan[1:], [AVAIL*0.22, AVAIL*0.55, AVAIL*0.23])

    elements += synth_box([
        "Swipe natif : lock direction h/v, seuil 60px, snap animé — implémentation complète",
        "3 couches HTML : panneaux abs + content translateX — sans bibliothèque swipe",
        "CRUD complet : add (unshift), toggle, delete (animé), clearCompleted",
        "17+ fonctions organisées en 4 groupes : storage, render, actions, modal",
    ], positive=True)

    elements.append(PageBreak())


# ── PAGE DE CLÔTURE ──────────────────────────────────────────
def closing_page(elements):
    elements.append(Spacer(1, 2.5*cm))
    elements.append(Paragraph("Ma Todo List",
        S('cl', fontName=F_BOLD, fontSize=32, textColor=PRIMARY,
          alignment=TA_CENTER, leading=38)))
    elements.append(Paragraph("Rapport Technique — Application Cordova",
        S('cls', fontName=F, fontSize=10, textColor=SECONDARY,
          alignment=TA_CENTER, leading=14)))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="60%", thickness=2, color=ACCENT, spaceAfter=0.5*cm))
    info_st = S('inf', fontName=F, fontSize=9, textColor=GRAY, alignment=TA_CENTER, leading=16)
    for line in [
        "UCAD — École Supérieure Polytechnique (ESP)",
        "Salif Biaye — Fondateur / CEO",
        "Module : Développement Mobile — DIC3 — Édition Mai 2026",
    ]:
        elements.append(Paragraph(line, info_st))
    elements.append(Spacer(1, 0.5*cm))
    elements.append(HRFlowable(width="84%", thickness=0.5, color=TGRID, spaceAfter=0.4*cm))
    elements.append(Paragraph(
        "Document produit dans le cadre du cursus DIC3 — Usage académique uniquement",
        S('d', fontName=F_ITAL, fontSize=7.5, textColor=GRAY, alignment=TA_CENTER, leading=13)))


# ── MAIN ─────────────────────────────────────────────────────
def main():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=3.5*cm, bottomMargin=1.8*cm,
        title="Ma Todo List — Rapport Technique",
        author="Groupe 3 — ESP/UCAD",
    )
    elements = []
    pt = chapter_titles
    current_page = [1]

    def on_page(canvas, doc):
        current_page[0] = doc.page

    cover_page(elements);      current_page[0] = 2
    sommaire(elements);        current_page[0] = 3
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
