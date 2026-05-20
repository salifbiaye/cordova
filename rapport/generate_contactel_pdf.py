# -*- coding: utf-8 -*-
"""
Rapport Technique — Contactel
Application mobile Apache Cordova
HTML5 · CSS3 · JavaScript + jQuery · Gestion de contacts
Auteur : Salif Biaye — ESP/UCAD 2026
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

# ── Palette bleue (thème Contactel) ──────────────────────────
PRIMARY   = colors.HexColor("#1E3A8A")   # Bleu très foncé
SECONDARY = colors.HexColor("#1D4ED8")   # Bleu principal
ACCENT    = colors.HexColor("#60A5FA")   # Bleu clair
GOLD      = colors.HexColor("#93C5FD")   # Bleu pastel
LIGHT     = colors.HexColor("#EFF6FF")   # Bleu très clair
LIGHT2    = colors.HexColor("#DBEAFE")   # Fond clair bleu
WHITE     = colors.white
BLACK     = colors.black
GRAY      = colors.HexColor("#3A3A3A")
LGRAY     = colors.HexColor("#DBEAFE")
CODE_BG   = colors.HexColor("#07101A")
CODE_FG   = colors.HexColor("#BAE6FD")
TGRID     = colors.HexColor("#93C5FD")
C_GREEN   = colors.HexColor("#27AE60")
C_RED     = colors.HexColor("#F87171")
C_EDIT    = colors.HexColor("#60A5FA")

# ── Constantes ───────────────────────────────────────────────
W, H = A4
MARGIN_L = 1.8 * cm
MARGIN_R = 1.8 * cm
AVAIL    = W - MARGIN_L - MARGIN_R

LOGO        = r"C:\Users\DELL\Downloads\logo_ucad.png"
SCREENS_DIR = r"C:\Users\DELL\Downloads\medy\screens"
SCR_LIST    = os.path.join(SCREENS_DIR, "contactel_list.png")
SCR_MODAL   = os.path.join(SCREENS_DIR, "contactel_modal.png")
SCR_CONFIRM = os.path.join(SCREENS_DIR, "contactel_confirm.png")
SCR_SEARCH  = os.path.join(SCREENS_DIR, "contactel_search.png")

OUTPUT = os.path.join(os.path.dirname(__file__), "rapport_contactel.pdf")
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
            self.drawString(4.3*cm, H - 1.5*cm, "Contactel")
            self.setFillColor(WHITE)
            self.setFont(F_BOLD, 9)
            self.drawString(4.3*cm, H - 2.1*cm, "Rapport Technique — Application Cordova")
            self.setFont(F, 7.5)
            self.drawString(4.3*cm, H - 2.55*cm,
                            "HTML5 · CSS3 · JavaScript + jQuery · Gestion de contacts — ESP/UCAD 2026")
        else:
            self.setFillColor(LGRAY)
            self.rect(0, H - 1.15*cm, W, 1.15*cm, fill=1, stroke=0)
            self.setFillColor(SECONDARY)
            self.setFont(F_BOLD, 8)
            self.drawString(MARGIN_L, H - 0.72*cm, "Contactel")
            self.setFillColor(colors.HexColor("#1E40AF"))
            self.setFont(F_BOLD, 6.8)
            self.drawString(MARGIN_L + 1.5*cm, H - 0.72*cm, "| Rapport Technique")
            chap = chapter_titles.get(pg, "")
            if chap:
                self.setFillColor(colors.HexColor("#4B6280"))
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
tag_st        = S('tag', fontName=F_MONOB, fontSize=8, textColor=SECONDARY, alignment=TA_LEFT)


# ── Composants réutilisables ─────────────────────────────────
def chap_header(num, title, subtitle=""):
    nc = 4.2 * cm
    row = [[Paragraph(f"SECTION {num}", chap_num_st), Paragraph(title, chap_title_st)]]
    t = Table(row, colWidths=[nc, AVAIL - nc])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 10), ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ('TOPPADDING', (0,0), (-1,-1), 14),  ('BOTTOMPADDING', (0,0), (-1,-1), 14),
        ('LINEBELOW', (0,0), (-1,-1), 4, ACCENT),
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

def body(text): return [Paragraph(text, body_st)]
def bullet(text): return [Paragraph(f"• {text}", bullet_st)]


def code_block(filename, lines):
    rows = [[Paragraph(f"📄  {filename}", code_title_st)]]
    for line in lines:
        rows.append([Paragraph(line.replace(" ", " ").replace("<", "&lt;").replace(">", "&gt;"),
                               code_st)])
    t = Table(rows, colWidths=[AVAIL])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), CODE_BG),
        ('TOPPADDING', (0,0), (0,0), 7),   ('BOTTOMPADDING', (0,0), (0,0), 5),
        ('TOPPADDING', (0,1), (-1,-1), 2), ('BOTTOMPADDING', (0,1), (-1,-1), 2),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (0,0), 1, ACCENT),
        ('BOX', (0,0), (-1,-1), 1, SECONDARY),
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
        if h > max_h: h = max_h; w = h * ratio
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
            ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('BOX', (0,0), (-1,-1), 1.5, TGRID),
        ]))
        return [KeepTogether([frame]), Spacer(1, 0.4*cm)]
    else:
        ph_st   = S('ph',   fontName=F_BOLD, fontSize=10, textColor=SECONDARY, alignment=TA_CENTER, leading=16)
        hint_st = S('hint', fontName=F_ITAL, fontSize=8,  textColor=GRAY, alignment=TA_CENTER, leading=12)
        rows = [
            [Paragraph("📸", ph_st)],
            [Paragraph(caption, ph_st)],
            [Paragraph(f"Placer la capture ici :\n{path}", hint_st)],
        ]
        t = Table(rows, colWidths=[AVAIL])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), LIGHT),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 20),  ('BOTTOMPADDING', (0,0), (-1,-1), 20),
            ('BOX', (0,0), (-1,-1), 1.5, SECONDARY),
            ('LINEBEFORE', (0,0), (0,-1), 4, SECONDARY),
        ]))
        return [t, Spacer(1, 0.4*cm)]


def synth_box(lines, positive=True):
    accent = C_GREEN if positive else SECONDARY
    hdr_bg = colors.HexColor("#1A4C8A") if positive else PRIMARY
    AW = 0.22 * cm; TW = AVAIL - AW
    bul = S('rb', fontName=F, fontSize=9, textColor=colors.HexColor("#0D1628"),
            leading=14, leftIndent=6, firstLineIndent=-6, alignment=TA_LEFT)
    data = [["", Paragraph("Synthèse", synth_hdr_st)]]
    for line in lines:
        data.append(["", Paragraph(f"◆  {line}", bul)])
    t = Table(data, colWidths=[AW, TW])
    cmds = [
        ('BACKGROUND', (0,0), (0,-1), accent),
        ('BACKGROUND', (1,0), (1,0),  hdr_bg),
        ('TOPPADDING', (0,0), (-1,0), 7),     ('BOTTOMPADDING', (0,0), (-1,0), 7),
        ('TOPPADDING', (0,1), (-1,-1), 5),    ('BOTTOMPADDING', (0,1), (-1,-1), 5),
        ('LEFTPADDING', (1,0), (1,-1), 12),   ('RIGHTPADDING', (1,0), (1,-1), 12),
        ('LEFTPADDING', (0,0), (0,-1), 0),    ('RIGHTPADDING', (0,0), (0,-1), 0),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOX', (0,0), (-1,-1), 1.2, TGRID),
        ('LINEBELOW', (1,1), (1,-2), 0.4, colors.HexColor("#BFDBFE")),
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
        ('GRID', (0,0), (-1,-1), 0.3, TGRID),
        ('LINEBELOW', (0,0), (-1,0), 2, SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'), ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
    ]))
    return [t, Spacer(1, 0.3*cm)]


def th(t): return Paragraph(t, th_st)
def td(t, bold=False):
    return Paragraph(t, S('tdc', fontName=F_BOLD if bold else F, fontSize=8,
                           textColor=GRAY, alignment=TA_LEFT))
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

    elements.append(Paragraph("Contactel",
        S('title', fontName=F_BOLD, fontSize=38, textColor=PRIMARY,
          leading=46, alignment=TA_CENTER)))
    elements.append(Paragraph("Application Mobile de Gestion de Contacts — Apache Cordova",
        S('sub', fontName=F, fontSize=10, textColor=colors.HexColor("#1E40AF"),
          leading=15, alignment=TA_CENTER)))
    elements.append(Spacer(1, 0.15*cm))

    subj = Table([
        [Paragraph("Documentation complète — HTML · CSS · JavaScript + jQuery", S('wt', fontName=F_BOLD,
                   fontSize=12, textColor=WHITE, leading=17, alignment=TA_CENTER))],
        [Paragraph("CRUD complet, recherche, filtres par groupe, modal d'édition — expliqués étape par étape",
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
        Paragraph("CSS bleu\nthème sombre", stat_st),
        Paragraph("15 fonctions JS\ndocumentées", stat_st),
        Paragraph("CRUD complet\n+ recherche", stat_st),
    ]], colWidths=[width/4]*4)
    stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), SECONDARY),
        ('GRID', (0,0), (-1,-1), 0.25, PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ]))
    elements.append(stats)
    elements.append(Spacer(1, 0.4*cm))

    # Bloc auteur — uniquement Salif Biaye
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
        ["Application :", "Contactel"],
        ["Technologie :", "Apache Cordova · HTML5 · CSS3 · JavaScript + jQuery 3.7"],
        ["Fonctionnalités :", "CRUD contacts, recherche, filtres groupe, avatar initiales, modal"],
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
        ("1", "Vue d'ensemble", "Objectif, CRUD, tech stack"),
        ("2", "Structure HTML", "Header, search, filtres, liste, modal, confirm"),
        ("3", "Feuille de style CSS", "Palette bleue, avatars, modal bottom sheet"),
        ("4", "Logique JavaScript", "15 fonctions CRUD, filtres, modal, recherche"),
        ("5", "Captures d'écran", "Liste, modal, recherche, confirmation"),
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
                             "Objectif, CRUD contacts, pile technologique")

    elements += sec_title("1.1  Qu'est-ce que Contactel ?")
    elements += body(
        "<b>Contactel</b> est une application mobile de gestion de contacts développée "
        "avec <b>Apache Cordova</b>. Elle permet d'ajouter, modifier, supprimer et rechercher "
        "des contacts, chacun associé à un nom, numéro de téléphone, email et groupe "
        "(Famille, Amis, Travail, Autre). Un système d'<b>avatars automatiques</b> génère "
        "les initiales du contact lorsqu'aucune photo n'est disponible."
    )
    elements += body(
        "Les contacts sont triés alphabétiquement et persistent via <b>localStorage</b>. "
        "L'interface propose une <b>barre de recherche</b> combinée à des <b>filtres par groupe</b>, "
        "un modal d'ajout/édition en <b>bottom sheet</b>, et une boîte de confirmation "
        "avant toute suppression."
    )

    elements += sec_title("1.2  Pile technologique")
    tech_data = [
        [th("Technologie"), th("Rôle"), th("Version")],
        [td("Apache Cordova"), td("Wrapper natif Android/iOS"), td("Dernière stable")],
        [td("HTML5"), td("Structure : header, search, filtres, liste, modal, confirm"), td("Standard W3C")],
        [td("CSS3"), td("Thème bleu sombre, avatars, bottom sheet, animations"), td("Standard W3C")],
        [td("JavaScript (IIFE)"), td("CRUD contacts, filtres, recherche, rendu DOM"), td("ES6+")],
        [td("jQuery 3.7.1"), td("Sélecteurs, events, escape XSS, délégation"), td("CDN")],
        [td("localStorage"), td("Persistance JSON (clé : 'contacts')"), td("Web API native")],
    ]
    elements += make_table(tech_data[0], tech_data[1:], [AVAIL*0.22, AVAIL*0.50, AVAIL*0.28])

    elements += sec_title("1.3  Fonctionnalités clés")
    for f in [
        "<b>CRUD complet :</b> Create (ajouter), Read (lister), Update (modifier), Delete (supprimer).",
        "<b>Recherche temps réel :</b> filtre simultané nom + téléphone dès la frappe.",
        "<b>Filtres par groupe :</b> Tous / Famille / Amis / Travail / Autre.",
        "<b>Avatar initiales :</b> génération automatique des 2 premières lettres du nom.",
        "<b>Tri alphabétique :</b> contacts toujours triés par nom (localeCompare 'fr').",
        "<b>Confirmation suppression :</b> boîte de dialogue avant toute suppression.",
    ]:
        elements += bullet(f)

    elements += synth_box([
        "CRUD complet + recherche + filtres : application de gestion complète",
        "Avatar initiales : initials() calcule 2 lettres depuis le nom",
        "Tri : localeCompare('fr') pour un tri alphabétique correct en français",
        "Thème bleu foncé (#07101A → #60A5FA) avec mode clair automatique",
    ])
    elements.append(PageBreak())


# ── SECTION 2 — STRUCTURE HTML ───────────────────────────────
def section_html(elements, pt):
    pt[2] = "Section 2 — Structure HTML"
    elements += chap_header("2", "Structure HTML",
                             "Analyse des 5 sections du fichier index.html")

    elements += sec_title("2.1  App, header et barre de recherche")
    elements += code_block("index.html — header + search", [
        '&lt;div id="app"&gt;',
        '  &lt;header&gt;',
        '    &lt;h1&gt;Contactel&lt;/h1&gt;',
        '    &lt;p id="summary"&gt;0 contact(s)&lt;/p&gt;  &lt;!-- Mis à jour par renderSummary() --&gt;',
        '  &lt;/header&gt;',
        '',
        '  &lt;!-- Barre de recherche combinée avec les filtres --&gt;',
        '  &lt;div id="search-bar"&gt;',
        '    &lt;span class="search-icon"&gt;🔍&lt;/span&gt;',
        '    &lt;input type="search" id="search-input" placeholder="Rechercher un contact..."&gt;',
        '  &lt;/div&gt;',
        '',
        '  &lt;div id="filters"&gt;',
        '    &lt;button class="filter-btn active" data-group="all"&gt;Tous&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-group="Famille"&gt;Famille&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-group="Amis"&gt;Amis&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-group="Travail"&gt;Travail&lt;/button&gt;',
        '    &lt;button class="filter-btn" data-group="Autre"&gt;Autre&lt;/button&gt;',
        '  &lt;/div&gt;',
        '',
        '  &lt;ul id="contact-list"&gt;&lt;/ul&gt;  &lt;!-- Rempli dynamiquement --&gt;',
        '  &lt;button id="btn-add"&gt;+&lt;/button&gt;  &lt;!-- FAB fixe --&gt;',
        '&lt;/div&gt;',
    ])

    elements += sec_title("2.2  Modal d'ajout/édition")
    elements += code_block("index.html — modal", [
        '&lt;div id="modal-overlay" class="hidden"&gt;',
        '  &lt;div id="modal"&gt;',
        '    &lt;div id="modal-header"&gt;',
        '      &lt;h2 id="modal-title"&gt;Nouveau contact&lt;/h2&gt;  &lt;!-- Ou "Modifier le contact" --&gt;',
        '      &lt;button id="modal-close"&gt;✕&lt;/button&gt;',
        '    &lt;/div&gt;',
        '    &lt;div id="modal-body"&gt;',
        '      &lt;!-- Prévisualisation de l\'avatar --&gt;',
        '      &lt;div class="avatar-preview" id="avatar-preview"&gt;',
        '        &lt;img src="img/contact.png" id="avatar-preview-img" alt="contact"&gt;',
        '        &lt;span id="avatar-preview-initials"&gt;&lt;/span&gt;  &lt;!-- Initiales JS --&gt;',
        '      &lt;/div&gt;',
        '      &lt;div class="field"&gt; &lt;label for="f-name"&gt;Nom complet *&lt;/label&gt;',
        '        &lt;input type="text" id="f-name" maxlength="60"&gt; &lt;/div&gt;',
        '      &lt;div class="field"&gt; &lt;label for="f-phone"&gt;Téléphone *&lt;/label&gt;',
        '        &lt;input type="tel" id="f-phone" maxlength="20"&gt; &lt;/div&gt;',
        '      &lt;div class="field"&gt; &lt;label for="f-email"&gt;Email&lt;/label&gt;',
        '        &lt;input type="email" id="f-email" maxlength="80"&gt; &lt;/div&gt;',
        '      &lt;div class="field"&gt; &lt;label for="f-group"&gt;Groupe&lt;/label&gt;',
        '        &lt;select id="f-group"&gt; options Autre/Famille/Amis/Travail &lt;/select&gt; &lt;/div&gt;',
        '      &lt;p id="form-error" class="hidden"&gt;Champs obligatoires.&lt;/p&gt;',
        '    &lt;/div&gt;',
        '    &lt;div id="modal-footer"&gt;',
        '      &lt;button id="btn-cancel"&gt;Annuler&lt;/button&gt;',
        '      &lt;button id="btn-save"&gt;Enregistrer&lt;/button&gt;',
        '    &lt;/div&gt;',
        '  &lt;/div&gt;',
        '&lt;/div&gt;',
    ])
    elements += body(
        "Le même modal gère <b>ajout ET modification</b>. La distinction se fait via "
        "<code>state.editingId</code> : <code>null</code> = nouveau, valeur = édition. "
        "Le titre change dynamiquement : 'Nouveau contact' ou 'Modifier le contact'."
    )

    elements += sec_title("2.3  Boîte de confirmation de suppression")
    elements += code_block("index.html — confirm dialog", [
        '&lt;div id="confirm-overlay" class="hidden"&gt;',
        '  &lt;div id="confirm-box"&gt;',
        '    &lt;p id="confirm-msg"&gt;Supprimer ce contact ?&lt;/p&gt;  &lt;!-- Nom inséré par JS --&gt;',
        '    &lt;div id="confirm-actions"&gt;',
        '      &lt;button id="confirm-no"&gt;Non&lt;/button&gt;',
        '      &lt;button id="confirm-yes"&gt;Oui, supprimer&lt;/button&gt;',
        '    &lt;/div&gt;',
        '  &lt;/div&gt;',
        '&lt;/div&gt;',
    ])
    elements += body(
        "Le message de confirmation inclut le nom du contact : "
        "<code>'Supprimer \"Saliou Diallo\" ?'</code>. "
        "Cela améliore l'UX en évitant les suppressions accidentelles."
    )

    elements += synth_box([
        "Modal unique pour ajout ET édition — state.editingId distingue les deux cas",
        "data-group sur les boutons filtres — JS lit cet attribut pour setFilter()",
        "type=search sur l'input : bouton clear (×) natif sur iOS/Android",
        "Boîte de confirmation avec nom du contact — protection contre les fausses suppressions",
    ])
    elements.append(PageBreak())


# ── SECTION 3 — CSS ──────────────────────────────────────────
def section_css(elements, pt):
    pt[3] = "Section 3 — CSS & Thème Visuel"
    elements += chap_header("3", "Feuille de style CSS",
                             "Palette bleue, système d'avatars, bottom sheet et animations")

    elements += sec_title("3.1  Palette de couleurs")
    pal_data = [
        [th("Élément"), th("Hex"), th("Usage")],
        [tag("fond global"),     td("#07101A"), td("Fond arrière très sombre (bleu-noir)")],
        [tag("header gradient"), td("#1E3A8A → #60A5FA"), td("Dégradé en-tête")],
        [tag("accent blue"),     td("#1D4ED8"), td("Boutons, FAB, filtre actif")],
        [tag("accent clair"),    td("#60A5FA"), td("Hover, focus, éléments secondaires")],
        [tag("texte"),           td("#E0EDF8"), td("Texte principal (bleu très clair)")],
        [tag("input border"),    td("#1E3A5A"), td("Bordure des champs de formulaire")],
        [tag("btn-edit"),        td("#60A5FA"), td("Bouton modifier (bleu clair)")],
        [tag("btn-delete"),      td("#F87171"), td("Bouton supprimer (rouge clair)")],
        [tag("badge groupe"),    td("variable"), td("Couleur selon le groupe du contact")],
    ]
    elements += make_table(pal_data[0], pal_data[1:], [AVAIL*0.25, AVAIL*0.28, AVAIL*0.47])

    elements += sec_title("3.2  Système d'avatars")
    elements += body(
        "Chaque contact a un avatar circulaire de 48px. Si une image est disponible "
        "(<code>img/contact.png</code>), elle est affichée. Sinon, le JS génère les "
        "initiales et les affiche sur fond dégradé bleu."
    )
    elements += code_block("index.css — avatar contact", [
        '.contact-avatar {',
        '  width: 48px; height: 48px; border-radius: 50%;',
        '  overflow: hidden; flex-shrink: 0;',
        '  background: linear-gradient(135deg, #1d4ed8, #60a5fa);  /* Fond initiales */',
        '  display: flex; align-items: center; justify-content: center;',
        '  font-weight: 700; color: white; font-size: 16px;',
        '}',
        '',
        '/* Prévisualisation dans le modal (64px) */',
        '.avatar-preview {',
        '  width: 64px; height: 64px; border-radius: 50%;',
        '  background: linear-gradient(135deg, #1e3a8a, #60a5fa);',
        '  /* JS bascule entre img et span#initiales */',
        '}',
    ])

    elements += sec_title("3.3  Animations")
    anim_data = [
        [th("Animation"), th("Durée"), th("Déclencheur"), th("Effet")],
        [td("slideIn"),   td("0.2s ease"), td("Nouveau contact"), td("Contact entre depuis le bas")],
        [td("slideUp"),   td("0.25s ease"), td("Ouverture modal"),  td("Modal monte depuis le bas")],
        [td("fadeIn"),    td("0.18s ease"), td("Overlay modal"),    td("Fondu de l'arrière-plan")],
        [td("zoomIn"),    td("0.2s ease"), td("Boîte de confirm"), td("La boîte grossit depuis 0.8×")],
    ]
    elements += make_table(anim_data[0], anim_data[1:], [AVAIL*0.20, AVAIL*0.17, AVAIL*0.25, AVAIL*0.38])

    elements += synth_box([
        "Avatar : fond dégradé bleu avec initiales JS — dégradé naturel même sans photo",
        "Bottom sheet modal : slideUp 0.25s — imite le comportement natif iOS/Android",
        "zoomIn confirm : 0.8× → 1.0× — feedback visuel fort avant suppression",
        "Mode clair : prefers-color-scheme — fond #eff6ff, texte #0d1628",
    ])
    elements.append(PageBreak())


# ── SECTION 4 — JAVASCRIPT ───────────────────────────────────
def section_js(elements, pt):
    pt[4] = "Section 4 — Logique JavaScript"
    elements += chap_header("4", "Logique JavaScript",
                             "IIFE + jQuery — 15 fonctions CRUD, filtres, recherche, modal documentées")

    elements += sec_title("4.1  Structure, état global et constantes")
    elements += code_block("index.js — module + state + AVATAR_CLASS", [
        'var App = (function ($) {',
        '  var STORAGE_KEY = "contacts";',
        '',
        '  // Mapping groupe → classe CSS pour la couleur du badge',
        '  var AVATAR_CLASS = {',
        '    Famille: "g-Famille",   // CSS : badge vert',
        '    Amis:    "g-Amis",      // CSS : badge bleu clair',
        '    Travail: "g-Travail",   // CSS : badge orange',
        '    Autre:   "g-Autre"      // CSS : badge gris',
        '  };',
        '',
        '  var state = {',
        '    contacts:   load(),   // Tableau de contacts depuis localStorage',
        '    group:      "all",    // Filtre groupe actif',
        '    search:     "",       // Terme de recherche en cours',
        '    editingId:  null,     // ID du contact en cours d\'édition (null=création)',
        '    deletingId: null      // ID du contact en attente de suppression',
        '  };',
        '}($));',
    ])

    elements += sec_title("4.2  Stockage, escape et initiales")
    elements += code_block("index.js — helpers", [
        '// load : JSON.parse depuis localStorage, [] si absent ou corrompu',
        'function load() {',
        '  try { return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]"); }',
        '  catch (_) { return []; }',
        '}',
        '',
        '// persist : sérialise le tableau complet à chaque modification',
        'function persist() {',
        '  localStorage.setItem(STORAGE_KEY, JSON.stringify(state.contacts));',
        '}',
        '',
        '// escape : prévenir les injections XSS via astuce jQuery',
        'function escape(text) { return $("&lt;div&gt;").text(String(text)).html(); }',
        '',
        '// initials : extraire les 2 premières initiales du nom',
        'function initials(name) {',
        '  var parts = name.trim().split(/\\s+/);',
        '  return parts.length >= 2',
        '    ? parts[0][0] + parts[1][0]   // "Salif Biaye" → "SB"',
        '    : parts[0].slice(0, 2);        // "Saliou" → "Sa"',
        '}',
    ])

    elements += sec_title("4.3  Filtrage et tri — getFiltered()")
    elements += code_block("index.js — getFiltered", [
        'function getFiltered() {',
        '  return state.contacts',
        '    .filter(function (c) {',
        '      var matchGroup  = state.group === "all" || c.group === state.group;',
        '      var matchSearch = !state.search ||',
        '        c.name.toLowerCase().includes(state.search) ||',
        '        c.phone.includes(state.search);      // Chercher aussi dans le téléphone',
        '      return matchGroup && matchSearch;       // Les deux conditions réunies',
        '    })',
        '    .sort(function (a, b) {',
        '      return a.name.localeCompare(b.name, "fr");  // Tri alphabétique français',
        '    });',
        '}',
        '',
        '// localeCompare("fr") : gère é, è, ê, ç, à correctement',
    ])

    elements += sec_title("4.4  Rendu HTML — buildContactHtml()")
    elements += code_block("index.js — buildContactHtml", [
        'function buildContactHtml(c) {',
        '  return \'&lt;li class="contact-item" data-id="\' + c.id + \'"&gt;\' +',
        '    \'&lt;div class="contact-avatar"&gt;\' +',
        '      \'&lt;img src="img/contact.png" class="avatar-img" alt="contact"&gt;\' +',
        '    \'&lt;/div&gt;\' +',
        '    \'&lt;div class="contact-info"&gt;\' +',
        '      \'&lt;div class="contact-name"&gt;\'  + escape(c.name)  + \'&lt;/div&gt;\' +',
        '      \'&lt;div class="contact-phone"&gt;\' + escape(c.phone) + \'&lt;/div&gt;\' +',
        '      \'&lt;span class="contact-group-badge"&gt;\' + escape(c.group) + \'&lt;/span&gt;\' +',
        '    \'&lt;/div&gt;\' +',
        '    \'&lt;div class="contact-actions"&gt;\' +',
        '      \'&lt;button class="btn-edit"   data-id="\' + c.id + \'"&gt;...&lt;/button&gt;\' +',
        '      \'&lt;button class="btn-delete" data-id="\' + c.id + \'"&gt;...&lt;/button&gt;\' +',
        '    \'&lt;/div&gt;\' +',
        '  \'&lt;/li&gt;\';',
        '}',
        '',
        '// escape() sur name, phone, group : protection XSS systématique',
    ])

    elements += sec_title("4.5  Modal — openModal, closeModal, updateAvatarPreview, readForm, saveContact")
    elements += code_block("index.js — modal functions", [
        '// openModal(id) : ouvre en mode édition (id≠null) ou création (id=null)',
        'function openModal(id) {',
        '  state.editingId = id;',
        '  var c = id ? state.contacts.find(function (x) { return x.id === id; }) : null;',
        '  $("#modal-title").text(c ? "Modifier le contact" : "Nouveau contact");',
        '  // Pré-remplir le formulaire si édition',
        '  $("#f-name").val(c ? c.name : "");',
        '  $("#f-phone").val(c ? c.phone : "");',
        '  // ...',
        '  updateAvatarPreview(c ? c.name : "");',
        '  $("#modal-overlay").removeClass("hidden");',
        '}',
        '',
        '// updateAvatarPreview : bascule entre image et initiales',
        'function updateAvatarPreview(name) {',
        '  var ini = name && name.trim() ? initials(name) : "";',
        '  if (ini) {',
        '    $("#avatar-preview-img").hide();',
        '    $("#avatar-preview-initials").text(ini).show();',
        '  } else {',
        '    $("#avatar-preview-img").show();',
        '    $("#avatar-preview-initials").hide();',
        '  }',
        '}',
        '',
        '// saveContact : valide, crée ou met à jour, persist + render',
        'function saveContact() {',
        '  var data = readForm();  // { name, phone, email, group }',
        '  if (!data.name || !data.phone) {',
        '    $("#form-error").removeClass("hidden"); return;',
        '  }',
        '  if (state.editingId) {',
        '    // Mise à jour : Object.assign sur le contact existant',
        '    var existing = state.contacts.find(function (c) { return c.id === state.editingId; });',
        '    if (existing) Object.assign(existing, data);',
        '  } else {',
        '    // Création : id = Date.now() (timestamp unique)',
        '    state.contacts.push({ id: Date.now(), ...data });',
        '  }',
        '  persist(); render(); closeModal();',
        '}',
    ])

    elements += sec_title("4.6  Suppression — askDelete, cancelDelete, confirmDelete")
    elements += code_block("index.js — delete flow", [
        '// askDelete : mémorise l\'ID et affiche la confirmation avec le nom',
        'function askDelete(id) {',
        '  state.deletingId = id;',
        '  var c    = state.contacts.find(function (x) { return x.id === id; });',
        '  var name = c ? c.name : "ce contact";',
        '  $("#confirm-msg").text(\'Supprimer "\' + escape(name) + \'" ?\');',
        '  $("#confirm-overlay").removeClass("hidden");',
        '}',
        '',
        '// cancelDelete : annuler — reset deletingId',
        'function cancelDelete() {',
        '  $("#confirm-overlay").addClass("hidden");',
        '  state.deletingId = null;',
        '}',
        '',
        '// confirmDelete : filtrer le contact hors du tableau',
        'function confirmDelete() {',
        '  state.contacts = state.contacts.filter(function (c) {',
        '    return c.id !== state.deletingId;  // Garder tous sauf celui à supprimer',
        '  });',
        '  persist(); render(); cancelDelete();',
        '}',
    ])

    elements += synth_box([
        "openModal(id) : double usage création/édition — state.editingId null ou valeur",
        "updateAvatarPreview : live preview des initiales pendant la saisie du nom",
        "saveContact : Object.assign pour mise à jour in-place sans remplacer l'objet",
        "askDelete → confirmDelete : 3 étapes sécurisées avec nom affiché dans la confirmation",
        "getFiltered : recherche combinée (nom OU téléphone) + filtre groupe + tri localeCompare",
    ])
    elements.append(PageBreak())


# ── SECTION 5 — SCREENSHOTS ──────────────────────────────────
def section_screens(elements, pt):
    pt[5] = "Section 5 — Captures d'écran"
    elements += chap_header("5", "Captures d'écran", f"Placer les images dans : {SCREENS_DIR}")

    elements += sec_title("5.1  Liste des contacts")
    elements += body("Vue principale avec liste triée, avatars, badges groupes, boutons edit/delete.")
    elements += screen_box(SCR_LIST, "Contactel — Liste des contacts", 9*cm, 16*cm)

    elements += sec_title("5.2  Modal d'ajout / modification")
    elements += body("Bottom sheet avec prévisualisation de l'avatar, formulaire, validation.")
    elements += screen_box(SCR_MODAL, "Contactel — Modal ajout contact", 9*cm, 16*cm)

    elements += sec_title("5.3  Barre de recherche active")
    elements += body("Filtrage temps réel par nom ou téléphone.")
    elements += screen_box(SCR_SEARCH, "Contactel — Recherche en cours", 9*cm, 16*cm)

    elements += sec_title("5.4  Boîte de confirmation de suppression")
    elements += body("Dialogue centré avec nom du contact à supprimer.")
    elements += screen_box(SCR_CONFIRM, "Contactel — Confirmation suppression", 9*cm, 16*cm)

    elements.append(PageBreak())


# ── SECTION 6 — SYNTHÈSE ─────────────────────────────────────
def section_synthese(elements, pt):
    pt[6] = "Section 6 — Synthèse"
    elements += chap_header("6", "Synthèse finale", "Bilan technique et compétences démontrées")

    elements += sec_title("6.1  Tableau récapitulatif")
    bilan = [
        [th("Aspect"), th("Détail"), th("Niveau")],
        [td("CRUD complet"), td("Create, Read, Update, Delete — 4 opérations fonctionnelles"), td("✓ Complet")],
        [td("Recherche"), td("Filtre temps réel sur nom ET téléphone, insensible à la casse"), td("✓ Avancé")],
        [td("Avatars"), td("initials() calcule les initiales, preview live pendant la saisie"), td("✓ Soigné")],
        [td("Tri"), td("localeCompare('fr') — alphabétique avec accents corrects"), td("✓ Solide")],
        [td("UX"), td("Bottom sheet, confirmation nominative, FAB, état vide"), td("✓ Optimisé")],
        [td("Sécurité"), td("escape() XSS sur tous les champs affichés"), td("✓ Bon")],
    ]
    elements += make_table(bilan[0], bilan[1:], [AVAIL*0.22, AVAIL*0.55, AVAIL*0.23])

    elements += synth_box([
        "15 fonctions : load, persist, escape, initials, getFiltered, buildContactHtml, renderList, renderSummary, render, setFilter, setSearch, openModal, closeModal, updateAvatarPreview, readForm, saveContact, askDelete, cancelDelete, confirmDelete, bindEvents, init",
        "Recherche combinée : nom.toLowerCase().includes() || phone.includes() — temps réel",
        "Object.assign : mise à jour propre des propriétés sans recréer l'objet",
        "Double modal : un seul panneau pour créer ET modifier — state.editingId discriminant",
    ], positive=True)
    elements.append(PageBreak())


# ── PAGE DE CLÔTURE ──────────────────────────────────────────
def closing_page(elements):
    elements.append(Spacer(1, 2.5*cm))
    elements.append(Paragraph("Contactel",
        S('cl', fontName=F_BOLD, fontSize=36, textColor=PRIMARY,
          alignment=TA_CENTER, leading=42)))
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
        title="Contactel — Rapport Technique",
        author="Salif Biaye — ESP/UCAD",
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
