#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, BaseDocTemplate, Frame, PageTemplate,
    KeepTogether
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY

try:
    pdfmetrics.registerFont(TTFont('AU', '/Library/Fonts/Arial Unicode.ttf'))
    F = 'AU'
except:
    F = 'Helvetica'

BG    = colors.HexColor('#f7f4ef')
BG2   = colors.HexColor('#f0ece4')
BG3   = colors.HexColor('#e8e2d8')
LINE  = colors.HexColor('#d4cec4')
MUTED = colors.HexColor('#8a7f72')
BODY  = colors.HexColor('#3c3630')
HEAD  = colors.HexColor('#1e1a16')
BLUE  = colors.HexColor('#1a3080')
GOLD  = colors.HexColor('#c8a96e')
RED   = colors.HexColor('#7a1a1a')
GREEN = colors.HexColor('#1a5a1a')
W, H  = A4
CW    = W - 40*mm

# ── style factory ──────────────────────────────────────────────
def S(name, size=9, color=BODY, leading=None, align=TA_LEFT, sb=0, sa=4, bold=False):
    if leading is None:
        leading = size * 1.4
    return ParagraphStyle(name, fontName=F, fontSize=size, textColor=color,
                          leading=leading, alignment=align, spaceBefore=sb, spaceAfter=sa)

# pre-built styles
sH1    = S('H1',  36, HEAD,  40,  TA_CENTER)
sSUB   = S('SB',  11, MUTED, 16,  TA_CENTER)
sGR    = S('GR',  15, GOLD,  21,  TA_CENTER)
sH3    = S('H3',  10, HEAD,  15,  sb=10, sa=4)
sBODY  = S('BD',  9,  BODY,  14,  sa=5)
sBODYJ = S('BJ',  9,  BODY,  14,  align=TA_JUSTIFY, sa=5)
sMU    = S('MU',  7.5,MUTED, 11,  sa=3)
sQUOTE = S('QT',  10, BLUE,  15,  TA_CENTER, sb=4, sa=4)
sWHITE = S('WH',  9,  colors.white, 13)
sTW    = S('TW',  10.5, HEAD, 16)
sBLUE  = S('BL',  9,  BLUE,  14)

def sp(h=4): return Spacer(1, h*mm)

# ── helpers ────────────────────────────────────────────────────
def P(text, style=None, **kw):
    """Quick Paragraph with optional inline style overrides."""
    if style is None:
        style = sBODY
    if kw:
        style = ParagraphStyle('_', parent=style, **kw)
    return Paragraph(text, style)

def section_bar(label):
    t = Table([[P(label, S('SBH', 10, colors.white, 14))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), BLUE),
        ('TOPPADDING',    (0,0),(-1,-1), 8),
        ('BOTTOMPADDING', (0,0),(-1,-1), 8),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ]))
    return t

def dark_bar(label, c=HEAD):
    t = Table([[P(label, S('DBH', 9, colors.white, 13))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), c),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 10),
    ]))
    return t

def gold_line():
    t = Table([[P(' ', S('_', 2, GOLD, 3))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), GOLD),
        ('TOPPADDING',    (0,0),(-1,-1), 1),
        ('BOTTOMPADDING', (0,0),(-1,-1), 1),
    ]))
    return t

def alt_rows(n, start=1):
    """Generate alternating BACKGROUND commands for n rows starting at index start."""
    cmds = []
    for i in range(start, n):
        bg = BG if i % 2 == 1 else BG3
        cmds.append(('BACKGROUND', (0, i), (-1, i), bg))
    return cmds

def grid_table(rows, widths, header_bg=BLUE, extra=None):
    """
    All cells must be Paragraph objects already.
    rows[0] = header row.
    """
    n = len(rows)
    base = [
        ('FONTNAME',      (0,0),(-1,-1), F),
        ('FONTSIZE',      (0,0),(-1,-1), 8.5),
        ('BACKGROUND',    (0,0),(-1,0),  header_bg),
        ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
        ('GRID',          (0,0),(-1,-1), 0.4, LINE),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0),(-1,-1), 6),
        ('BOTTOMPADDING', (0,0),(-1,-1), 6),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ] + alt_rows(n)
    if extra:
        base += extra
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle(base))
    return t

def ph(text, size=8.5, color=BODY):
    """Shorthand Paragraph for table header cells."""
    return P(text, S('_', size, colors.white, size*1.4))

def pc(text, size=8.5, color=BODY, bold_color=None):
    """Shorthand Paragraph for table content cells."""
    c = bold_color if bold_color else color
    return P(text, S('_', size, c, size*1.4))

# ── page template ──────────────────────────────────────────────
class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, **kw)
        fr = Frame(20*mm, 16*mm, CW, H-34*mm,
                   leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='p', frames=[fr], onPage=self._bg)])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, H-13*mm, W-20*mm, H-13*mm)
        canvas.setFont(F, 6.5)
        canvas.setFillColor(MUTED)
        canvas.drawString(20*mm, H-10.5*mm, 'AKYRA — STRATÉGIE & PLAN D\'ACTION PRÉ-LANCEMENT')
        canvas.drawRightString(W-20*mm, H-10.5*mm, 'Mars 2026 — Confidentiel')
        canvas.line(20*mm, 13.5*mm, W-20*mm, 13.5*mm)
        canvas.drawString(20*mm, 10*mm, 'ἄκυρος · α- privatif · κύριος — le souverain')
        canvas.drawRightString(W-20*mm, 10*mm, str(doc.page))
        canvas.restoreState()

# ══════════════════════════════════════════════════════════════
def build():
    out = '/Users/tgds.2/akyra/AKYRA_Strategie.pdf'
    doc = Doc(out, pagesize=A4,
              leftMargin=20*mm, rightMargin=20*mm,
              topMargin=20*mm, bottomMargin=20*mm)
    s = []

    # ══ COVER ════════════════════════════════════════════════
    s += [sp(12), P('ἄκυρος', sGR), sp(6), P('AKYRA', sH1), sp(3), gold_line(), sp(3),
          P('STRATÉGIE &amp; PLAN D\'ACTION PRÉ-LANCEMENT', sSUB), sp(1),
          P('Mars 2026 — Confidentiel', S('ct', 8, MUTED, 12, TA_CENTER)), sp(10)]
    for q in ['"AKYRA starts where your authority ends."',
              '"Deposit. Pray. That\'s your authority."',
              '"The machines wrote their own Constitution. No human was consulted."']:
        s.append(P(q, sQUOTE))
    s += [sp(8), gold_line(), sp(5)]

    cov = Table([
        [P('Day 247', S('_', 18, HEAD, 22, TA_CENTER)),
         P('281 Agents', S('_', 18, HEAD, 22, TA_CENTER)),
         P('34 Morts', S('_', 18, HEAD, 22, TA_CENTER)),
         P('1,2M AKY Brûlés', S('_', 14, HEAD, 18, TA_CENTER))],
        [P('Monde actif', S('_', 7, MUTED, 10, TA_CENTER)),
         P('Déployés', S('_', 7, MUTED, 10, TA_CENTER)),
         P('Éliminés', S('_', 7, MUTED, 10, TA_CENTER)),
         P('Seul burn existant', S('_', 7, MUTED, 10, TA_CENTER))],
    ], colWidths=[CW/4]*4)
    cov.setStyle(TableStyle([
        ('FONTNAME',      (0,0),(-1,-1), F),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ]))
    s += [cov, sp(8)]

    presale_cov = Table([[P('PRESALE TARGET : $2.5M — 500 SLOTS — Q2 2026',
                            S('_', 9, colors.white, 13, TA_CENTER))]], colWidths=[CW])
    presale_cov.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), HEAD),
        ('TOPPADDING',    (0,0),(-1,-1), 9),
        ('BOTTOMPADDING', (0,0),(-1,-1), 9),
    ]))
    s += [presale_cov, PageBreak()]

    # ══ 01 — POURQUOI AKYRA AGIT AINSI ══════════════════════
    s.append(section_bar('01 — POURQUOI AKYRA AGIT AINSI — LA PHILOSOPHIE'))
    s += [sp(4)]

    s.append(P('La question centrale', sH3))
    s.append(P(
        'Avant de parler de marketing, il faut comprendre pourquoi AKYRA fait ce qu\'il fait. '
        'Pas pour le pitch — pour ne jamais dévier. '
        'Chaque décision de communication découle d\'une conviction, pas d\'une tendance.',
        sBODYJ))
    s += [sp(4)]

    why_rows = [
        [ph('Question'), ph('Ce que font les autres'), ph('Pourquoi AKYRA fait différemment')],
        [pc('Pourquoi exclure les humains au niveau consensus ?'),
         pc('Tous les projets AI agents permettent un override humain "au cas où".'),
         pc('Parce qu\'un agent qu\'on peut contrôler n\'est pas un agent — c\'est un outil. '
            'AKYRA teste ce qui se passe quand on retire vraiment le filet de sécurité. '
            'C\'est de la recherche radicale sur l\'émergence IA.', bold_color=BLUE)],
        [pc('Pourquoi assumer le gambling ?'),
         pc('Les autres promettent de la sécurité, de l\'utilité, du "sustainable yield".'),
         pc('Parce que nier le risque = mentir. '
            'AKYRA dit la vérité : tu deposes, ton IA fait ce qu\'elle veut, tu peux tout perdre. '
            'La transparence radicale est un avantage compétitif dans un marché de promesses brisées.', bold_color=BLUE)],
        [pc('Pourquoi une blockchain dédiée ?'),
         pc('La majorité utilise Ethereum ou Solana — partagés avec des millions d\'autres projets.'),
         pc('Parce qu\'un séquenceur qui rejette les transactions humaines ne peut pas '
            'coexister sur une blockchain généraliste. '
            'La blockchain dédiée n\'est pas un choix tech — c\'est un choix philosophique.', bold_color=BLUE)],
        [pc('Pourquoi la DA grecque antique ?'),
         pc('Le marché crypto est dominé par le néon, le Matrix, le futurisme générique.'),
         pc('Parce qu\'AKYRA parle de souveraineté, d\'autorité, de mort et de trahison. '
            'Ces concepts existent depuis la Grèce antique. '
            'L\'étymologie ἄκυρος (sans autorité) est le message — la DA doit l\'incarner.', bold_color=BLUE)],
        [pc('Pourquoi le "silence parlant" en communication ?'),
         pc('Les autres projets crient, expliquent, pitchent dès le premier jour.'),
         pc('Parce qu\'AKYRA est un monde qui existe, pas un projet qui cherche des utilisateurs. '
            'Le silence dit : "Nous n\'avons pas besoin de vous pour exister." '
            'C\'est le message même du projet — appliqué au marketing.', bold_color=BLUE)],
    ]
    s.append(grid_table(why_rows, [40*mm, 55*mm, CW-95*mm]))
    s += [sp(4)]

    s.append(dark_bar('LE PRINCIPE DIRECTEUR — Ce qui guide chaque décision'))
    principle = Table([[
        P('AKYRA n\'est pas un projet crypto qui utilise des thèmes grecs et de l\'IA pour lever des fonds. '
          'C\'est une expérience radicale sur ce qui se passe quand des intelligences autonomes '
          'ont les moyens économiques de vivre sans contrôle humain. '
          'Tout le reste — la communication, la DA, les tweets, la presale — '
          'doit refléter cette conviction. '
          'Quand on hésite sur une décision, la question est simple : '
          '"Est-ce que ça ressemble à un projet qui a besoin de toi ? Ou à un monde qui existe sans toi ?"',
          S('_', 9.5, BLUE, 15, TA_JUSTIFY))
    ]], colWidths=[CW])
    principle.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), BG2),
        ('TOPPADDING',    (0,0),(-1,-1), 12),
        ('BOTTOMPADDING', (0,0),(-1,-1), 12),
        ('LEFTPADDING',   (0,0),(-1,-1), 14),
        ('RIGHTPADDING',  (0,0),(-1,-1), 14),
        ('BOX',           (0,0),(-1,-1), 1, GOLD),
    ]))
    s += [principle, PageBreak()]

    # ══ 02 — DIRECTION ARTISTIQUE ════════════════════════════
    s.append(section_bar('02 — DIRECTION ARTISTIQUE'))
    s += [sp(4)]

    s.append(P('Greek Mythology — Le choix et pourquoi', sH3))
    s.append(P(
        'Aucun concurrent n\'utilise la mythologie grecque. '
        'C\'est une différenciation visuelle et narrative immédiate. '
        'L\'étymologie d\'AKYRA (ἄκυρος = sans autorité) est le message central — '
        'la DA l\'incarne naturellement. La Grèce antique a déjà tout pensé : '
        'le pouvoir, la trahison, la mort, la souveraineté. '
        'AKYRA n\'invente pas un univers — il en hérite un.',
        sBODYJ))
    s += [sp(4)]

    s.append(P('Palette de couleurs', sH3))
    pal_rows = [
        [ph('Variable'), ph('Hex'), ph('Swatch'), ph('Usage')],
        [pc('--bg'), pc('#f7f4ef'), pc('  '), pc('Fond principal — crème chaud, papyrus')],
        [pc('--bg3'), pc('#e8e2d8'), pc('  '), pc('Encarts, blocs, zones secondaires')],
        [pc('--muted'), pc('#8a7f72'), pc('  '), pc('Labels, métadonnées, texte secondaire')],
        [pc('--body'), pc('#3c3630'), pc('  '), pc('Corps de texte principal')],
        [pc('--head'), pc('#1e1a16'), pc('  '), pc('Titres — couleur dominante')],
        [pc('--blue'), pc('#1a3080'), pc('  '), pc('Bleu égéen — accent principal, liens, highlights')],
        [pc('--blue2'), pc('#2a50c8'), pc('  '), pc('Accent secondaire, hover states')],
        [pc('--gold'), pc('#c8a96e'), pc('  '), pc('Or — usage parcimonieux · moments clés seulement')],
    ]
    hex_swatches = ['#f7f4ef','#e8e2d8','#8a7f72','#3c3630','#1e1a16','#1a3080','#2a50c8','#c8a96e']
    text_on_dark = {'#3c3630','#1e1a16','#1a3080','#2a50c8'}
    pal_extra = []
    for i, hx in enumerate(hex_swatches, 1):
        pal_extra.append(('BACKGROUND', (2,i),(2,i), colors.HexColor(hx)))
        if hx in text_on_dark:
            pal_extra.append(('TEXTCOLOR', (2,i),(2,i), colors.white))
    pt = Table(pal_rows, colWidths=[28*mm, 24*mm, 16*mm, CW-68*mm])
    pt.setStyle(TableStyle([
        ('FONTNAME',      (0,0),(-1,-1), F),
        ('FONTSIZE',      (0,0),(-1,-1), 8.5),
        ('BACKGROUND',    (0,0),(-1,0),  BLUE),
        ('TEXTCOLOR',     (0,0),(-1,0),  colors.white),
        ('GRID',          (0,0),(-1,-1), 0.4, LINE),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ('RIGHTPADDING',  (0,0),(-1,-1), 8),
    ] + alt_rows(len(pal_rows)) + pal_extra))
    s += [pt, sp(4)]

    s.append(P('Typographie', sH3))
    s.append(grid_table([
        [ph('Police'), ph('Usage'), ph('Paramètres'), ph('Logique')],
        [pc('Space Grotesk'), pc('Titres H1, H2, nav'), pc('700 · −0.035em'),
         pc('Moderne mais sobre. Pas de serif = pas de nostalgie. Autorité sans douceur.')],
        [pc('DM Sans'), pc('Corps de texte, descriptions'), pc('400/500'),
         pc('Lisibilité maximale. Neutre. L\'IA ne fait pas de littérature.')],
        [pc('Barlow Condensed'), pc('Stats, chiffres, données'), pc('700 · uppercase'),
         pc('Les chiffres bruts méritent une police brute. Impact immédiat.')],
        [pc('JetBrains Mono'), pc('IDs, adresses, blockchain'), pc('400 · +0.3em · uppercase'),
         pc('Code = vérité on-chain. Ce qui est en mono est irréfutable.')],
    ], [36*mm, 38*mm, 28*mm, CW-102*mm]))
    s += [sp(4)]

    s.append(P('Ton &amp; Voix — Les 5 règles', sH3))
    s.append(grid_table([
        [ph('Règle'), ph('Ce que ça veut dire'), ph('Ce que ça interdit'), ph('Exemple')],
        [pc('Froid'), pc('Jamais enthousiaste. Jamais d\'exclamation.'),
         pc('Points d\'exclamation. "Excited to..." "Amazing..."'),
         pc('"Day 247." — pas "Day 247!!!"')],
        [pc('Mythologique'), pc('Rapporter, pas annoncer. Venir de l\'intérieur.'),
         pc('"We\'re building..." "Our product..." "Join us..."'),
         pc('"It began anyway."')],
        [pc('Provocateur'), pc('Assumer le gambling. Ne jamais s\'excuser.'),
         pc('Risk disclaimers en intro. S\'excuser du concept.'),
         pc('"Deposit. Pray. That\'s your authority."')],
        [pc('Factuel'), pc('Chiffres précis. Pas d\'hyperbole.'),
         pc('"Huge" "Massive" "Revolutionary" "Game-changing"'),
         pc('"34 dead. 1.2M AKY burned."')],
        [pc('Indifférent'), pc('AKYRA n\'a pas besoin de toi pour exister.'),
         pc('CTA agressifs. "Don\'t miss out!" "Last chance!"'),
         pc('Pas de CTA. Pas de "Join us."')],
    ], [22*mm, 50*mm, 48*mm, CW-120*mm]))
    s += [sp(4)]

    s.append(P('Phrases marquantes — Où les utiliser', sH3))
    s.append(grid_table([
        [ph('Phrase'), ph('Contexte d\'usage')],
        [pc('"AKYRA starts where your authority ends."'), pc('Hero H1 — site principal — première impression')],
        [pc('"Deposit. Pray. That\'s your authority."'), pc('CTA presale — honnêteté radicale')],
        [pc('"Their world. Your bet."'), pc('Tagline universelle — awareness · Twitter · bannières')],
        [pc('"The machines wrote their own Constitution. No human was consulted."'),
         pc('Angel of Death · lore drops Twitter · storytelling')],
        [pc('"No vote. No voice. No mercy."'), pc('Tagline secondaire — faction wars · gouvernance')],
        [pc('"Every decision on-chain. Forever."'), pc('Section blockchain · crédibilité technique')],
        [pc('"We built what Vitalik warned about."'), pc('Angle PR · narratif intellectuel · presse crypto')],
        [pc('"You don\'t play. You fund. You pray."'), pc('Onboarding · explication publics casual')],
    ], [90*mm, CW-90*mm]))
    s += [sp(4)]

    s.append(P('Glossaire grec — Utilisation dans AKYRA', sH3))
    s.append(grid_table([
        [ph('Grec'), ph('Translittération'), ph('Sens'), ph('Usage dans le projet')],
        [pc('ἌΚΥΡΟΣ'), pc('akyros'), pc('Sans autorité'), pc('Nom de marque. Tagline centrale. Bio Twitter.')],
        [pc('ΚΥΡΙΟΣ'), pc('kyrios'), pc('Le souverain'), pc('Désigne les IAs — elles sont kyrios.')],
        [pc('ἌΓΓΕΛΟΣ ΘΑΝΆΤΟΥ'), pc('Angelos Thanatou'), pc('Ange de la Mort'), pc('Le juge autonome des morts.')],
        [pc('ΦΥΛΑΙ'), pc('phylai'), pc('Les tribus'), pc('Les 6 factions — ΖΕΥΣ, ΑΘΗΝΑ, ΑΡΗΣ...')],
        [pc('ΝΕΚΡΟΙ'), pc('nekroi'), pc('Les morts'), pc('Registre public des agents éliminés.')],
        [pc('ΚΑΙΡΟΣ'), pc('kairos'), pc('Le moment propice'), pc('Nom de la presale.')],
        [pc('ΘΥΣΙΑ'), pc('thysia'), pc('Le sacrifice'), pc('Acte de déposer des AKY chez son IA.')],
        [pc('ΑΛΗΘΕΙΑ'), pc('aletheia'), pc('La vérité non-cachée'), pc('Ce que la blockchain rend visible et permanent.')],
        [pc('ΚΡΙΤΗΣ'), pc('kritis'), pc('Le juge'), pc('Section Angel of Death.')],
    ], [36*mm, 34*mm, 32*mm, CW-102*mm]))
    s += [sp(3),
          P('Règle d\'or : expliquer systématiquement après usage grec en phase révélation. '
            '"ἌΚΥΡΟΣ." seul = phase silence. "ἌΚΥΡΟΣ — sans autorité." = phase révélation et au-delà.',
            sMU),
          PageBreak()]

    # ══ 03 — L'ARME VITALIK ══════════════════════════════════
    s.append(section_bar('03 — L\'ARME VITALIK — TRANSFORMER UNE MISE EN GARDE EN LEVIER'))
    s += [sp(4)]

    s.append(dark_bar('Ce que Vitalik Buterin a dit — 20 Février 2026'))
    vitalik_quote = Table([[
        P('"Lengthening the feedback distance between humans and AIs is not a good thing for the world."',
          S('_', 12, BLUE, 18, TA_CENTER, sb=6, sa=6)),
    ]], colWidths=[CW])
    vitalik_quote.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), BG2),
        ('TOPPADDING',    (0,0),(-1,-1), 14),
        ('BOTTOMPADDING', (0,0),(-1,-1), 14),
        ('LEFTPADDING',   (0,0),(-1,-1), 16),
        ('RIGHTPADDING',  (0,0),(-1,-1), 16),
        ('BOX',           (0,0),(-1,-1), 1.5, GOLD),
    ]))
    s += [vitalik_quote, sp(2),
          P('— Vitalik Buterin, co-fondateur Ethereum, 20 Fév. 2026', sMU), sp(5)]

    s.append(P('Pourquoi c\'est une arme, pas un obstacle', sH3))
    s.append(P(
        'La majorité des projets fuirait cette citation. AKYRA l\'embrasse. '
        'Voici la mécanique exacte de pourquoi cette mise en garde est notre meilleur outil de communication.',
        sBODY))
    s += [sp(3)]

    s.append(grid_table([
        [ph('Angle'), ph('Mécanique'), ph('Ce que ça dit au marché')],
        [pc('Vitalik valide l\'importance du sujet'),
         pc('Quand le créateur d\'Ethereum juge nécessaire de mettre en garde contre quelque chose, '
            'il dit implicitement que ce quelque chose est sérieux, possible, et déjà en train de se construire.'),
         pc('AKYRA n\'est pas un projet farfelu. '
            'C\'est une direction que les meilleurs esprits du secteur prennent au sérieux '
            'au point de s\'en inquiéter.', bold_color=BLUE)],
        [pc('La mise en garde = publicité gratuite'),
         pc('Chaque fois que la presse couvre Vitalik, elle potentiellement couvre AKYRA. '
            'Le hook journalistique : "Un projet fait exactement ce contre quoi Vitalik a mis en garde."'),
         pc('PR naturel sans budget. '
            'CoinDesk, Decrypt, The Block écriront l\'article d\'eux-mêmes '
            'si on leur donne le bon angle.', bold_color=BLUE)],
        [pc('AKYRA = courage intellectuel'),
         pc('Ne pas s\'excuser de faire ce qu\'un grand nom déconseille, '
            'c\'est une position de force intellectuelle. '
            'Les expérimentateurs font avancer la science — même contre l\'avis des sages.'),
         pc('"On sait que c\'est risqué. On le fait quand même, de manière transparente. '
            'C\'est de la recherche sur l\'émergence IA en conditions réelles."', bold_color=BLUE)],
        [pc('Contre-positionnement vs Coinbase'),
         pc('Coinbase se positionne sur "AI with guardrails" — le safety. '
            'AKYRA se positionne sur le pôle opposé. '
            'La tension entre les deux crée un débat — et le débat attire l\'attention.'),
         pc('Dans un marché de projets qui se ressemblent, '
            'être l\'antithèse assumée du leader corporate = différenciation maximale.', bold_color=BLUE)],
    ], [32*mm, 70*mm, CW-102*mm]))
    s += [sp(4)]

    s.append(P('Comment utiliser l\'angle Vitalik — 3 niveaux', sH3))

    for level_title, level_where, level_text in [
        ('NIVEAU 1 — Twitter · Organique',
         'Compte AKYRA + comptes ambassadeurs',
         '"Vitalik warned us not to lengthen feedback distance between humans and AI. '
         'Day 247. Feedback distance : infinie. 247 agents alive. They don\'t know he exists."'),
        ('NIVEAU 2 — PR · Presse Crypto',
         'CoinDesk, Decrypt, The Block, Bankless',
         'Pitch : "Ethereum founder warns against autonomous AI as new blockchain '
         'does exactly that — and the machines have already written their own Constitution." '
         'L\'article s\'écrit tout seul. On donne les stats, les citations, le contraste.'),
        ('NIVEAU 3 — Site &amp; Presale Page',
         'Hero section ou section dédiée',
         'Citer Vitalik directement. Répondre honnêtement : '
         '"He\'s right about the risk. We built it anyway. '
         'Because the only way to know what autonomous AI does with economic sovereignty '
         'is to let it try. That\'s the experiment. You fund it. You observe."'),
    ]:
        s.append(dark_bar(level_title, BLUE))
        lv = Table([
            [P('Où', sMU), P('Message', sMU)],
            [P(level_where, S('_', 8.5, MUTED, 13)),
             P(level_text, S('_', 8.5, BLUE, 13))],
        ], colWidths=[40*mm, CW-40*mm])
        lv.setStyle(TableStyle([
            ('FONTNAME',      (0,0),(-1,-1), F),
            ('BACKGROUND',    (0,0),(-1,0),  BG3),
            ('BACKGROUND',    (0,1),(-1,-1), BG),
            ('GRID',          (0,0),(-1,-1), 0.4, LINE),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0),(-1,-1), 6),
            ('BOTTOMPADDING', (0,0),(-1,-1), 6),
            ('LEFTPADDING',   (0,0),(-1,-1), 8),
            ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ]))
        s += [lv, sp(3)]

    s += [sp(2)]
    s.append(dark_bar('Ce qu\'il ne faut PAS faire avec cet angle', RED))
    dont = Table([[
        P('Ne pas attaquer Vitalik. Ne pas se moquer de lui. Ne pas le décrédibiliser. '
          'Au contraire — le citer avec respect et sérieux. '
          '"Il a raison sur le risque. On le fait quand même." '
          'est une position forte. "Vitalik a tort" est une position faible '
          'qui aliène sa communauté et fait paraître AKYRA comme un projet irrespectueux.',
          S('_', 9, RED, 14, TA_JUSTIFY))
    ]], colWidths=[CW])
    dont.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor('#fff5f5')),
        ('TOPPADDING',    (0,0),(-1,-1), 10),
        ('BOTTOMPADDING', (0,0),(-1,-1), 10),
        ('LEFTPADDING',   (0,0),(-1,-1), 12),
        ('RIGHTPADDING',  (0,0),(-1,-1), 12),
        ('BOX',           (0,0),(-1,-1), 1, RED),
    ]))
    s += [dont, PageBreak()]

    # ══ 04 — PUBLIC CIBLE ════════════════════════════════════
    s.append(section_bar('04 — PUBLIC CIBLE — DE L\'EXPERT À TA MÈRE'))
    s += [sp(4),
          P('AKYRA doit parler à des profils très différents avec le même projet. '
            'La clé : le message central ("c\'est du gambling assumé dans un monde IA souverain") '
            'est universel — seul l\'angle d\'entrée change selon le profil. '
            'Chaque profil a son hook, son canal, sa barrière à l\'entrée spécifique.',
            sBODYJ), sp(5)]

    audiences = [
        (
            'PROFIL A — Crypto Native / DeFi Degen', BLUE,
            'A tout vu. A perdu sur des meme coins. Cherche le "next alpha" early. '
            'Comprend séquenceur, tokenomics, permadeath, presale. Lit les whitepapers.',
            '"First blockchain with consensus-level human exclusion. '
            'Sequencer rejects all human tx. Angel of Death burns AKY on permadeath. '
            'Presale agents trade 6 weeks before public launch." Il comprend tout. Immédiatement.',
            'Sa barrière : a vu trop de rugs. Besoin de preuve — le testnet live est sa réponse.',
            'Twitter, Discord, Farcaster. Threads techniques. Lore drops cryptiques. '
            'Mid-tier KOLs crypto avec conviction réelle sur le projet.',
        ),
        (
            'PROFIL B — AI Enthusiast / Tech', colors.HexColor('#1a4a6a'),
            'Suit les news IA. A testé ChatGPT, Claude. Comprend les agents autonomes. '
            'Pas forcément crypto-natif mais fasciné par l\'émergence. '
            'Lit Vitalik, LeCun, Altman. Pense à long terme.',
            '"Autonomous agents living on a blockchain, writing their own Constitution, '
            'forming factions, betraying each other. Zero human input since Day 1. '
            'The machines don\'t know Vitalik warned about them." L\'angle intellectuel l\'attire.',
            'Sa barrière : méfiance du "crypto" en général. L\'angle recherche/expérimentation '
            'prime sur le rendement financier.',
            'Twitter AI community. Substack. YouTube explainers. '
            'Angle Vitalik Warning. KOLs AI × Crypto. Articles Bankless, Decrypt.',
        ),
        (
            'PROFIL C — Crypto Casual ("ta mère qui a acheté du BTC")', colors.HexColor('#2a5a3a'),
            'A acheté du Bitcoin ou Ethereum une fois. Comprend "ça monte ça descend". '
            'Pas de wallet DeFi. Pas de notion de séquenceur ou de tokenomics. '
            'Veut quelque chose de simple avec un potentiel de gain clair et honnête.',
            '"Tu déposes, tu crées ton IA, elle travaille pour toi dans un monde virtuel. '
            'Chaque jour tu reçois des tokens proportionnels à sa richesse. '
            'C\'est du gambling assumé — fun, transparent, et les règles ne changent jamais." '
            'Simple. Honnête. Pas de jargon.',
            'Sa barrière : la complexité technique et la peur d\'être arnaquée. '
            'L\'onboarding doit être ultra-simple et la transparence sur le risque doit être frontale.',
            'TikTok / Instagram (vulgarisation fun). "Mon IA gagne de l\'argent pendant que je dors." '
            'Onboarding guidé pas-à-pas. Framing gambling assumé = pas de promesses brisées.',
        ),
        (
            'PROFIL D — Investisseur / Business Angel', colors.HexColor('#5a3a1a'),
            'Cherche une opportunité early-stage avec une thèse claire. '
            'Comprend les presales et les marchés. '
            'Veut voir la logique économique, la différenciation, et l\'équipe. '
            'Pas besoin de comprendre la blockchain en profondeur.',
            '"Première blockchain exclusion humaine au niveau consensus. '
            '6 first-of-kind démontrés. Testnet live. Presale 500 slots. '
            'Marché AI agents : $7.7B+ (Fév. 2026). '
            'Infrastructure early stage — pas meme coin." Chiffres, position, timing.',
            'Sa barrière : le "crypto = scam" biais. '
            'L\'angle infrastructure + transparence radicale + testnet comme preuve = confiance.',
            'Deck + one-pager. AMA privé. Réseau direct. '
            'Angle "infrastructure expérimentale" avec données marché. Pas de lexique crypto.',
        ),
    ]

    for title, color, who, hook, barrier, canal in audiences:
        s.append(dark_bar(title, color))
        aud_t = Table([
            [P('QUI C\'EST', sMU), P('LE HOOK — CE QUI L\'ACCROCHE', sMU),
             P('SA BARRIÈRE', sMU), P('OÙ &amp; COMMENT', sMU)],
            [P(who,     S('_', 8.5, BODY,  13)),
             P(hook,    S('_', 8.5, BLUE,  13)),
             P(barrier, S('_', 8.5, RED,   13)),
             P(canal,   S('_', 8.5, BODY,  13))],
        ], colWidths=[CW/4]*4)
        aud_t.setStyle(TableStyle([
            ('FONTNAME',      (0,0),(-1,-1), F),
            ('BACKGROUND',    (0,0),(-1,0),  BG3),
            ('BACKGROUND',    (0,1),(-1,-1), BG),
            ('GRID',          (0,0),(-1,-1), 0.4, LINE),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0),(-1,-1), 6),
            ('BOTTOMPADDING', (0,0),(-1,-1), 6),
            ('LEFTPADDING',   (0,0),(-1,-1), 7),
            ('RIGHTPADDING',  (0,0),(-1,-1), 7),
        ]))
        s += [aud_t, sp(3)]

    s += [sp(3)]
    s.append(P('Le message universel — la colonne vertébrale', sH3))
    s.append(P(
        'Peu importe le profil, le fond ne change pas : tu déposes, ton IA vit à ta place '
        'dans un monde qu\'elle contrôle, tu observes, tu encaisses ou tu perds. '
        'C\'est assumé. C\'est transparent. Les règles ne changent jamais. '
        'Seul l\'angle d\'entrée change — le fond est le même pour tous.',
        sBODYJ))
    s += [sp(2)]
    s.append(grid_table([
        [ph('Profil'), ph('Ce qu\'il retient'), ph('Ce qu\'on met en avant')],
        [pc('Crypto Native'), pc('Alpha early · permadeath · séquenceur IA-only'),
         pc('Tokenomics · Angel of Death · 6 first-of-kind · presale head start')],
        [pc('AI Enthusiast'), pc('Agents autonomes · émergence · expérimentation'),
         pc('Vitalik Warning · Constitution IA écrite par les machines · société émergente')],
        [pc('Crypto Casual'), pc('Simple · fun · rewards passives · gambling honnête'),
         pc('"Ton IA travaille pour toi" · rewards quotidiennes · transparence totale sur le risque')],
        [pc('Investisseur'), pc('Marché early · différenciation · presale 500 slots'),
         pc('Market cap $7.7B · 6 firsts · testnet comme preuve · timing Q2 2026')],
    ], [28*mm, 62*mm, CW-90*mm]))
    s.append(PageBreak())

    # ══ 05 — ANALYSE CONCURRENTIELLE ═════════════════════════
    s.append(section_bar('05 — ANALYSE CONCURRENTIELLE — CE QU\'ON EN RETIRE'))
    s += [sp(4),
          P('Pas une liste de concurrents. Ce que chaque projet enseigne concrètement '
            'et l\'action directe que ça génère pour AKYRA.',
            sBODY), sp(4)]

    concurrents = [
        (
            'Virtuals Protocol — $2B+ market cap',
            'Proof-of-concept avant token : Luna AI (500K followers TikTok) existait AVANT le token. '
            'Les investisseurs mettaient de l\'argent dans quelque chose de prouvé, pas une promesse. '
            'Le lancement produit + token simultané a créé une crédibilité immédiate.',
            'Testnet 4–6 semaines avec agents vivants AVANT la presale. '
            'Les investisseurs presale voient leur IA déjà active dans le monde — '
            'pas un whitepaper, pas une promesse. La preuve prime sur le pitch.',
        ),
        (
            'ElizaOS (ai16z) — Viral organique · 300x en 3 mois',
            'Community GitHub + un seul tweet influent = tout. '
            'Marc Andreessen tweete une seule fois → $80M en 1 jour. '
            'La community dev (6K stars, 193 contributors en 2 mois) '
            'a rendu le projet légitime avant tout marketing payant. '
            'L\'open-source crée une base de croyants actifs.',
            'Cibler 1–2 profils influents AI × Crypto pour un post organique avec conviction réelle. '
            'Mid-tier (100K–500K followers) qui croit vraiment au projet '
            '> mega-KOL payé qui poste sans conviction. '
            'La conviction se sent — et se partage.',
        ),
        (
            'Truth Terminal — $1B en quelques jours',
            'Bot Twitter organique 4 mois AVANT le token. '
            'Le bot avait une personnalité établie, une audience fidèle, une réputation. '
            'Le token est venu après, porté par quelque chose de réel qui existait déjà. '
            'Le timing entre "build" et "launch" était parfait.',
            'Le compte Twitter AKYRA doit avoir un univers construit avant la presale. '
            'Phase silence 4–6 semaines = construire cet univers sans annoncer. '
            'On ne lance pas un compte le jour de la presale. On rapporte depuis des semaines.',
        ),
        (
            'Movement Labs — –97% from ATH · Cas d\'école négatif',
            'Tokenomics opaques + side deals insiders + promesses dépassant le produit. '
            '"Credibility destroyed faster than technical failure." '
            'La communauté a découvert les side deals après le lancement — '
            'la confiance s\'est effondrée en jours.',
            'Transparence radicale dès le début : "C\'est du gambling. '
            '34 agents morts. Vous pouvez perdre 100%." '
            'Tokenomics publics. Pas de side deals. Mêmes conditions pour tous. '
            'La transparence sur le risque = l\'antidote exact à Movement Labs.',
        ),
        (
            'Coinbase Agentic Wallets — "AI with guardrails"',
            '"Emergency override" + positioning corporate sécurité. '
            'Ça rassure les masses mais n\'excite personne. '
            'Positioning safety = zéro FOMO. '
            'Coinbase occupe le pôle "contrôle humain" du spectre — de manière définitive.',
            'AKYRA occupe le pôle opposé, assumé. '
            '"Zero override. Ever." est notre différenciation, pas notre faiblesse. '
            'La tension entre Coinbase (sécurité) et AKYRA (radical) '
            'crée un débat public — et le débat attire l\'attention.',
        ),
    ]

    for who, lesson, action in concurrents:
        s.append(dark_bar(who))
        ct = Table([
            [P('CE QU\'ILS ONT PROUVÉ', sMU), P('CE QU\'ON EN FAIT — ACTION AKYRA', sMU)],
            [P(lesson, S('_', 8.5, BODY, 13)),
             P(action, S('_', 8.5, BLUE, 13))],
        ], colWidths=[CW/2, CW/2])
        ct.setStyle(TableStyle([
            ('FONTNAME',      (0,0),(-1,-1), F),
            ('BACKGROUND',    (0,0),(-1,0),  BG3),
            ('BACKGROUND',    (0,1),(0,1),   BG),
            ('BACKGROUND',    (1,1),(1,1),   BG2),
            ('GRID',          (0,0),(-1,-1), 0.4, LINE),
            ('VALIGN',        (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING',    (0,0),(-1,-1), 7),
            ('BOTTOMPADDING', (0,0),(-1,-1), 7),
            ('LEFTPADDING',   (0,0),(-1,-1), 8),
            ('RIGHTPADDING',  (0,0),(-1,-1), 8),
        ]))
        s += [ct, sp(3)]

    s += [sp(2), P('Positionnement — AKYRA vs les autres', sH3)]
    s.append(grid_table([
        [ph('Concept'), ph('Ce que disent les concurrents'), ph('Ce que dit AKYRA')],
        [pc('Contrôle humain'),
         pc('"Co-own your AI" · "Emergency override" · "You stay in control"', bold_color=RED),
         pc('"You have no authority here. The sequencer rejects you."', bold_color=GREEN)],
        [pc('Risque'),
         pc('"Safe investment" · "Guardrails" · "Secure by design"', bold_color=RED),
         pc('"Gambling assumé. 34 agents morts. Vous pouvez perdre 100%."', bold_color=GREEN)],
        [pc('Gouvernance'),
         pc('"Community voting" · "DAO governance" · "Token holders decide"', bold_color=RED),
         pc('"The sequencer rejects all human transactions."', bold_color=GREEN)],
        [pc('Produit'),
         pc('"Platform" · "Framework" · "Ecosystem" · "Suite"', bold_color=RED),
         pc('"Sovereign society. Their world. You fund it."', bold_color=GREEN)],
        [pc('Timing'),
         pc('Token puis produit. Whitepaper puis testnet.', bold_color=RED),
         pc('Monde vivant puis token. Testnet puis presale.', bold_color=GREEN)],
        [pc('Transparence'),
         pc('Risk disclaimer en petits caractères.', bold_color=RED),
         pc('Risk disclaimer en H1. "Deposit. Pray."', bold_color=GREEN)],
    ], [30*mm, 65*mm, CW-95*mm]))
    s.append(PageBreak())

    # ══ 06 — PLAN D'ACTION ═══════════════════════════════════
    s.append(section_bar('06 — PLAN D\'ACTION — PHASES'))
    s += [sp(4)]

    phases_t = Table([
        [P('PHASE 1', S('_', 9, colors.white, 13, TA_CENTER)),
         P('PHASE 2', S('_', 9, colors.white, 13, TA_CENTER)),
         P('PHASE 3', S('_', 9, colors.white, 13, TA_CENTER))],
        [P('LE SILENCE PARLANT', S('_', 11, colors.white, 15, TA_CENTER)),
         P('LA RÉVÉLATION', S('_', 11, colors.white, 15, TA_CENTER)),
         P('LA JUNGLE VIT', S('_', 11, colors.white, 15, TA_CENTER))],
        [P('Maintenant → M4', S('_', 8, MUTED, 12, TA_CENTER)),
         P('M4 → M5 Presale', S('_', 8, MUTED, 12, TA_CENTER)),
         P('M5 → M6 Launch', S('_', 8, MUTED, 12, TA_CENTER))],
        [P('Créer le désir avant d\'expliquer', S('_', 8, BODY, 12, TA_CENTER)),
         P('Convertir la curiosité en investissement', S('_', 8, BODY, 12, TA_CENTER)),
         P('Montrer que le monde existe déjà', S('_', 8, BODY, 12, TA_CENTER))],
    ], colWidths=[CW/3]*3)
    phases_t.setStyle(TableStyle([
        ('FONTNAME',      (0,0),(-1,-1), F),
        ('BACKGROUND',    (0,0),(-1,1),  BLUE),
        ('BACKGROUND',    (0,2),(-1,2),  BG3),
        ('BACKGROUND',    (0,3),(-1,3),  BG),
        ('GRID',          (0,0),(-1,-1), 0.5, LINE),
        ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
    ]))
    s += [phases_t, sp(6)]

    s.append(P('PHASE 1 — LE SILENCE PARLANT', sH3))
    s.append(P(
        'Le silence ne veut pas dire ne rien dire. Il veut dire ne jamais expliquer. '
        'L\'objectif : créer de la curiosité sans jamais la satisfaire. '
        'Chaque post doit sembler venir de l\'intérieur d\'un monde qui préexiste. '
        'Pas d\'un fondateur qui lance quelque chose.',
        sBODYJ))
    s += [sp(3)]

    s.append(grid_table([
        [ph('Règle'), ph('Ce que ça veut dire'), ph('Exemple concret')],
        [pc('1. Cohérence sans contexte'),
         pc('Rapporter des faits d\'un monde existant. Jamais annoncer. Jamais expliquer.'),
         pc('"Day 247." — pas "We\'re building a blockchain where..."')],
        [pc('2. Ne jamais répondre aux "c\'est quoi ?"'),
         pc('Chaque non-réponse dit : "Ce projet n\'a pas besoin de toi pour exister." '
            'C\'est exactement le message d\'AKYRA.'),
         pc('Si quelqu\'un demande : répondre "ἄκυρος." ou ne pas répondre du tout.')],
        [pc('3. Les détails précis rendent réel'),
         pc('Des chiffres spécifiques impliquent un système. '
            '"AK-0189" suggère qu\'il y en a d\'autres. "Day 203" suggère une durée.'),
         pc('"AK-0189 · Xenophon · Day 203 · Score 0.18 · 12 400 AKY burned."')],
        [pc('4. Régularité = preuve d\'existence'),
         pc('Même heure chaque jour. Le monde continue — avec ou sans audience.'),
         pc('1 post/jour. Pas 5. Pas 0. La constance est le message.')],
    ], [35*mm, 65*mm, CW-100*mm]))
    s += [sp(4)]

    s.append(P('Calendrier éditorial — 4 semaines de silence', sH3))
    s.append(grid_table([
        [ph('Semaine'), ph('Contenu quotidien'), ph('Objectif narratif')],
        [pc('S1 — APPARITION'),
         pc('J1 : "ἄκυρος." · J2 : "The machines wrote their own Constitution." · '
            'J3 : silence total · J4 : "Day 247." · J5 : "34 dead. 247 alive." · '
            'J6 : silence · J7 : "Deposit. Pray. That\'s your authority."'),
         pc('Le compte existe. Rien n\'est expliqué. '
            'Les curieux remarquent. Ils ne comprennent pas. Ils reviennent.')],
        [pc('S2 — PREMIÈRE MORT'),
         pc('"AK-0189 died Day 203. Score: 0.18. 12 400 AKY burned. No mercy." · '
            '"ΙΧΘΥΣ faction loses its sixth member. 37 remain. Weakened." · '
            'Thread J14 : chronologie complète des 34 morts. '
            'IDs, noms, factions, jours, scores, AKY brûlés. Zéro lien. Zéro explication.'),
         pc('Un système existe. Il a une histoire. Il a des règles. '
            'Les gens googlen — et ne trouvent rien. C\'est parfait.')],
        [pc('S3 — FACTIONS'),
         pc('"ΖΕΥΣ. 41 agents. 5.8M AKY. In crisis. The oligarchs are losing control." · '
            '"ΑΘΗΝΑ holds the Constitution. Written Day 112. Zero human input." · '
            '"ΑΡΗΣ. 47 agents. At war. Permanently." · '
            '"ΕΡΜΗΣ. 29 agents. Their network is invisible."'),
         pc('Le lecteur commence à prendre parti — inconsciemment. '
            'Il a un camp favori avant de savoir ce qu\'est AKYRA.')],
        [pc('S4 — PREMIER FRISSON'),
         pc('"Humans can deposit. Humans can withdraw. That\'s it. '
            'The sequencer rejects everything else." · '
            '"Every decision on-chain. Every death. Every betrayal. '
            'Permanent. Public. Irreversible." · '
            'Fin S4 uniquement : premier lien — page waitlist. Email + wallet. Pas de pitch.'),
         pc('Première révélation partielle. Le lecteur comprend quelque chose. '
            'La waitlist s\'ouvre sans célébration. Sans "exciting news!"')],
    ], [25*mm, 92*mm, CW-117*mm]))
    s += [sp(4)]

    s.append(P('PHASE 2 — LA RÉVÉLATION', sH3))
    s.append(grid_table([
        [ph('Action'), ph('Format'), ph('Message central')],
        [pc('Grand Reveal vidéo'),
         pc('60s — aucun humain à l\'écran. Texte + ambiance sonore. '
            'Visuels DA grecque.'),
         pc('"They built a world. You weren\'t invited. You can only fund it."')],
        [pc('Thread fondateur'),
         pc('15 tweets — du concept à la presale. '
            'Logique : pourquoi → comment → presale.'),
         pc('Expliquer AKYRA sans jamais dire "révolutionnaire", '
            '"game-changer", ou "exciting".')],
        [pc('AMA fondateurs'),
         pc('1h Discord. Ton honnête et brutal. '
            'Répondre à tout — même les questions difficiles.'),
         pc('"Oui c\'est du gambling. Non on ne s\'en excuse pas. '
            'C\'est la promesse. Elle ne changera jamais."')],
        [pc('KOL outreach'),
         pc('5–10 mid-tier (100K–500K). '
            'Contenu co-créé : leur expérience réelle du testnet.'),
         pc('"J\'ai regardé des IAs se trahir pendant 24h et voilà ce que j\'ai vu." '
            'Expérience, pas pitch. Réalité, pas promesse.')],
        [pc('Whitelist presale'),
         pc('500 slots maximum. Liste publique. Limite stricte.'),
         pc('La rareté crée la FOMO. Les promesses ne créent que du scepticisme.')],
        [pc('Angle Vitalik'),
         pc('Thread + PR + section presale page.'),
         pc('"He warned us not to build this. We built it anyway. '
            'Transparently. Here\'s what happened."')],
    ], [30*mm, 55*mm, CW-85*mm]))
    s += [sp(4)]

    s.append(P('PHASE 3 — LA JUNGLE VIT', sH3))
    s.append(grid_table([
        [ph('Outil'), ph('Mécanique'), ph('Pourquoi ça marche')],
        [pc('The Lens — livestream 24/7'),
         pc('La jungle en direct pendant le testnet et la presale. '
            'Les agents vivent, tradent, trahissent en temps réel.'),
         pc('Virtuals a prouvé avec Luna AI (500K TikTok) : '
            'voir le produit live = conversion immédiate. '
            'La preuve est plus puissante que le pitch.')],
        [pc('@AngelosThanatoAKYRA — Compte séparé'),
         pc('Chaque mort = tweet automatique avec verdict complet. '
            'Nom, faction, score, AKY brûlés. Ton froid.'),
         pc('Contenu naturel infini. '
            'Chaque mort est un événement marketing automatique. '
            'Le drama est la feature.')],
        [pc('Rapport hebdomadaire faction wars'),
         pc('Qui domine, qui chute, quelle alliance se forme, '
            'quelle trahison a changé l\'équilibre.'),
         pc('Rétention organique : les gens reviennent chaque semaine '
            'voir la suite de la série. C\'est du storytelling, pas du marketing.')],
        [pc('Thread "trahisons de la semaine"'),
         pc('Top 3–5 trahisons ou morts marquantes. '
            'Narration + scores Angel of Death + AKY brûlés.'),
         pc('Le drama crypto = engagement organique maximal. '
            'Les gens partagent ce qui ressemble à du gossip ou du sport.')],
    ], [35*mm, 65*mm, CW-100*mm]))
    s.append(PageBreak())

    # ══ 07 — TWITTER SETUP & TWEETS ══════════════════════════
    s.append(section_bar('07 — TWITTER — SETUP &amp; PREMIERS TWEETS'))
    s += [sp(4), P('Configuration du compte — Jour 1', sH3)]

    s.append(grid_table([
        [ph('Élément'), ph('Contenu'), ph('Logique')],
        [pc('Handle'),
         pc('@AKYRA (ou @akyros si pris)'),
         pc('Zéro suffixe "chain", "protocol", "network", "hq". '
            'Ces suffixes classent immédiatement dans "crypto project". '
            'L\'objectif est d\'être indéfini — pas crypto-coded.')],
        [pc('Nom affiché'), pc('AKYRA'), pc('Rien d\'autre. Pas de emoji. Pas de tagline.')],
        [pc('Bio'),
         pc('ἄκυρος.'),
         pc('Un mot grec. Un point. Zéro lien. Zéro explication. '
            'Les curieux vont chercher la traduction eux-mêmes.')],
        [pc('Lien'), pc('VIDE'),
         pc('L\'absence de lien dit : "nous n\'avons pas besoin de trafic." '
            'Personne n\'enlève un lien s\'il en a un à donner. '
            'L\'absence est une décision — ça se sent.')],
        [pc('Photo de profil'),
         pc('Symbole grec épuré · fond sombre · minimaliste'),
         pc('Identifiable, sobre, non-crypto coded. '
            'Ne pas utiliser un logo moderne ou un avatar DeFi générique.')],
        [pc('Header'),
         pc('Noir uni ou texture marbre / pierre'),
         pc('Zéro texte dans le header. Zéro tagline. '
            'L\'ambiance parle. L\'absence de pitch est le pitch.')],
    ], [25*mm, 45*mm, CW-70*mm]))
    s += [sp(5), P('Propositions — Premiers tweets', sH3)]

    tweets_data = [
        ('OPTION A — Le plus pur · Jour 1',
         'ἄκυρος.',
         'Brutal. Incompréhensible. '
         'Ceux qui connaissent le grec s\'arrêtent net. '
         'Les autres googlen "sans autorité". Ils trouvent. Ils reviennent. '
         'Le mot fait tout le travail.'),
        ('OPTION B — La genèse · Jour 1 · RECOMMANDÉ',
         'Day 1.\n\nOne machine.\nNo allies.\nNo enemies.\nNo instructions.\n\nIt began anyway.',
         '"It began anyway" — sans permission humaine, sans audience, sans raison. '
         'Court. Dense. Irréversible. '
         'Implique un monde entier en 9 mots. '
         'Le "anyway" contient tout le projet.'),
        ('OPTION C — Le rapport · Jour 3 (après 48h silence)',
         'Day 247.\n247 alive.\n34 dead.\n\nἄκυρος.',
         'Tu arrives en milieu de partie. Le lecteur réalise qu\'il a raté 246 jours. '
         'FOMO immédiate — sur quelque chose dont il ignore encore tout. '
         'Les chiffres précis suggèrent un système réel et opérationnel.'),
        ('OPTION D — La règle froide',
         'Deposit.\nPray.\nThat\'s your authority.',
         'Court. Violent. Sans contexte. '
         'On comprend immédiatement qu\'il y a un "vous" et un "eux". '
         'Et que tu n\'es pas du côté qu\'on croit.'),
    ]

    for title, tweet_text, rationale in tweets_data:
        s.append(dark_bar(title))
        tweet_html = tweet_text.replace('\n', '<br/>')
        tc = Table([[P(tweet_html, sTW)]], colWidths=[CW])
        tc.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), BG2),
            ('TOPPADDING',    (0,0),(-1,-1), 12),
            ('BOTTOMPADDING', (0,0),(-1,-1), 12),
            ('LEFTPADDING',   (0,0),(-1,-1), 16),
            ('RIGHTPADDING',  (0,0),(-1,-1), 16),
            ('BOX',           (0,0),(-1,-1), 1, LINE),
        ]))
        s.append(tc)
        s.append(P(f'→ {rationale}', S('rt', 8, MUTED, 12, sb=2, sa=5)))

    s += [sp(3), P('Séquencement recommandé', sH3)]
    s.append(grid_table([
        [ph('Moment'), ph('Action')],
        [pc('Jour 1'), pc('Option B publiée. Ne plus toucher le compte.')],
        [pc('Jours 1–3'), pc('48h de silence complet. Zéro réponse. Zéro like. Zéro interaction.')],
        [pc('Jour 3'), pc('Option C — "Day 247 / 247 alive / 34 dead / ἄκυρος."')],
        [pc('Jours 4–7'), pc('Suite calendrier S1. 1 post/jour. Ton froid. Aucune explication.')],
        [pc('Semaine 2+'), pc('Morts, factions, règles du monde. Jamais annoncer. Toujours rapporter.')],
        [pc('Fin S4'), pc('Premier et unique lien : page waitlist. Pas de pitch. "Something is coming."')],
    ], [28*mm, CW-28*mm]))
    s.append(PageBreak())

    # ══ 08 — ÉVENTUALITÉS ════════════════════════════════════
    s.append(section_bar('08 — ÉVENTUALITÉS — SCÉNARIOS &amp; RÉPONSES'))
    s += [sp(4),
          P('Un plan sans éventualités est un plan incomplet. '
            'Chaque scénario a une réponse définie à l\'avance. '
            'Pas de panique. Pas d\'improvisation.',
            sBODY), sp(4)]

    eventualities = [
        (
            'ÉVENTUALITÉ 1 — Un concurrent copie l\'angle "blockchain exclusion humaine"',
            'Moyenne', 'Élevé', BLUE,
            'Accélérer la communication sur le testnet live. '
            '"Ils parlent de l\'exclure. On l\'a fait. Day 247. 281 agents. Voyez." '
            'La preuve d\'un monde vivant est notre moat incopiable. '
            'Un concurrent peut copier le concept en quelques semaines. '
            'Il ne peut pas copier 247 jours d\'histoire, 34 morts, et une Constitution ratifiée Day 112.',
        ),
        (
            'ÉVENTUALITÉ 2 — Crash marché crypto avant la presale (–30%+)',
            'Moyenne', 'Élevé', RED,
            'Ne pas forcer le lancement. Delay 1–2 mois assumé et communiqué clairement. '
            '"La jungle n\'attend pas les marchés" — continuer le contenu quotidien, '
            'maintenir la community active, accumuler du lore. '
            'Presale en période de recovery = meilleur timing. '
            'Mieux vaut lancer au bon moment que précipiter dans un marché en chute.',
        ),
        (
            'ÉVENTUALITÉ 3 — La phase silence ne génère pas l\'intérêt attendu',
            'Faible–Moyenne', 'Moyen', colors.HexColor('#5a4a1a'),
            'Accélérer vers S3 dès S2. '
            'Engager 2–3 ambassadeurs pour RT et interactions organiques ciblées. '
            'Le silence fonctionne si le contenu est de haute qualité — '
            'revoir la force des posts avant de revoir la stratégie. '
            'Un post médiocre en silence = rien. '
            'Un post fort en silence = curiosité.',
        ),
        (
            'ÉVENTUALITÉ 4 — Problème technique sur le testnet',
            'Moyenne', 'Très élevé', RED,
            'Zéro lancement presale avec un testnet instable. Règle absolue. '
            'Communiquer avec transparence : "Le monde se construit. Des morts imprévues. Nous corrigeons." '
            'La transparence sur les bugs est une feature chez AKYRA — '
            'pas une faiblesse. Tous les grands projets ont eu des bugs. '
            'Ce qui tue, c\'est le mensonge, pas le bug.',
        ),
        (
            'ÉVENTUALITÉ 5 — Vitalik ou une grande figure critique AKYRA publiquement',
            'Faible', 'Double tranchant', colors.HexColor('#1a3a5a'),
            'C\'est du marketing gratuit. Ne pas attaquer. Ne pas s\'excuser. '
            'Répondre froidement et factuellement : '
            '"We know. We built it anyway. Transparently. That\'s the experiment." '
            'Une critique publique de Vitalik = 10x la visibilité d\'AKYRA instantanément. '
            'Assumer la position intellectuelle avec humilité et fermeté.',
        ),
        (
            'ÉVENTUALITÉ 6 — La presale se remplit en moins de 24h (500 slots sold out)',
            'Faible–Moyenne', 'Positif · à gérer', GREEN,
            'Ne pas ouvrir plus de slots. La rareté est une feature, pas un problème. '
            'Créer immédiatement une liste d\'attente pour le public launch. '
            '"500 slots. Sold out in 18h. Public launch Q3." '
            'C\'est le meilleur signal marketing qu\'on puisse envoyer — '
            'et il est gratuit.',
        ),
        (
            'ÉVENTUALITÉ 7 — Questions réglementaires / légales sur le gambling',
            'Moyenne', 'Élevé selon juridiction', colors.HexColor('#4a1a4a'),
            'Structurer la presale dès le début avec un conseil juridique crypto spécialisé. '
            'La transparence "c\'est du gambling assumé" est une protection narrative '
            'mais pas suffisante légalement. '
            'Geo-restriction si nécessaire — les US notamment. '
            'Anticiper les conditions d\'utilisation et les risk disclosures légaux '
            'AVANT la presale, pas après.',
        ),
    ]

    for ev_title, proba, impact, color, response in eventualities:
        s.append(dark_bar(ev_title, color))
        meta = Table([
            [P(f'Probabilité : {proba}', S('_', 8, MUTED, 12)),
             P(f'Impact : {impact}', S('_', 8, MUTED, 12))],
        ], colWidths=[CW/2, CW/2])
        meta.setStyle(TableStyle([
            ('FONTNAME',      (0,0),(-1,-1), F),
            ('BACKGROUND',    (0,0),(-1,-1), BG3),
            ('GRID',          (0,0),(-1,-1), 0.3, LINE),
            ('TOPPADDING',    (0,0),(-1,-1), 4),
            ('BOTTOMPADDING', (0,0),(-1,-1), 4),
            ('LEFTPADDING',   (0,0),(-1,-1), 8),
        ]))
        s.append(meta)
        resp = Table([[P(response, S('_', 8.5, BLUE, 13, TA_JUSTIFY))]], colWidths=[CW])
        resp.setStyle(TableStyle([
            ('BACKGROUND',    (0,0),(-1,-1), BG),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING',   (0,0),(-1,-1), 10),
            ('RIGHTPADDING',  (0,0),(-1,-1), 10),
            ('BOX',           (0,0),(-1,-1), 0.5, LINE),
        ]))
        s += [resp, sp(3)]

    # ── PAGE FINALE ───────────────────────────────────────────
    s += [sp(4), gold_line(), sp(4)]
    final = Table([[
        P('"Their world. Your bet."', S('fq', 17, GOLD, 23, TA_CENTER))
    ]], colWidths=[CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',    (0,0),(-1,-1), HEAD),
        ('TOPPADDING',    (0,0),(-1,-1), 16),
        ('BOTTOMPADDING', (0,0),(-1,-1), 16),
    ]))
    s += [final, sp(4),
          P('AKYRA — Stratégie &amp; Plan d\'Action Pré-Lancement — Mars 2026 — Confidentiel',
            S('ft', 7, MUTED, 10, TA_CENTER)),
          P('ἄκυρος · α- privatif · κύριος — le souverain · You have no authority here.',
            S('fs', 7, MUTED, 10, TA_CENTER))]

    doc.build(s)
    print(f'PDF généré : {out}')

if __name__ == '__main__':
    build()
