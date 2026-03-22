#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate,
    Paragraph, Spacer, Table, TableStyle, PageBreak
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

BG   = colors.HexColor('#f7f4ef')
BG2  = colors.HexColor('#f0ece4')
BG3  = colors.HexColor('#e8e2d8')
LINE = colors.HexColor('#d4cec4')
MUT  = colors.HexColor('#8a7f72')
BODY = colors.HexColor('#3c3630')
HEAD = colors.HexColor('#1e1a16')
BLUE = colors.HexColor('#1a3080')
GOLD = colors.HexColor('#c8a96e')
RED  = colors.HexColor('#7a1a1a')
GRN  = colors.HexColor('#1a5a1a')

W, H = A4
CW   = W - 40*mm

def S(name, sz=9, col=BODY, ld=None, al=TA_LEFT, sb=0, sa=4):
    if ld is None: ld = sz * 1.45
    return ParagraphStyle(name, fontName=F, fontSize=sz, textColor=col,
                          leading=ld, alignment=al, spaceBefore=sb, spaceAfter=sa)

def P(t, st=None):
    if st is None: st = S('_')
    return Paragraph(t, st)

def sp(h=4): return Spacer(1, h*mm)

def alt_rows(n, s=1):
    return [('BACKGROUND',(0,i),(-1,i), BG if i%2==1 else BG3) for i in range(s,n)]

def sec(label, color=BLUE):
    t = Table([[P(label, S('_',11,colors.white,15))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

def gold_line():
    t = Table([[P(' ', S('_',1,GOLD,2))]], [CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD),
                           ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t

def tbl(rows, widths, hbg=BLUE):
    n = len(rows)
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),('FONTSIZE',(0,0),(-1,-1),9),
        ('BACKGROUND',(0,0),(-1,0),hbg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ] + alt_rows(n)))
    return t

def box(text, border=GOLD, bg=BG2, tcol=BLUE, sz=10):
    t = Table([[P(text, S('_',sz,tcol,sz*1.5,TA_JUSTIFY))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),2,border),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    return t

def alerte(text, color=RED):
    t = Table([[P('⚠ ' + text, S('_',9,colors.white,14,TA_LEFT))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

def check(text, color=GRN):
    t = Table([[P('✔ ' + text, S('_',9,colors.white,14,TA_LEFT))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, **kw)
        fr = Frame(20*mm,16*mm,CW,H-34*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='p',frames=[fr],onPage=self._bg)])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0,0,W,H,fill=1,stroke=0)
        # Header line
        canvas.setFillColor(GOLD)
        canvas.rect(0,H-14*mm,W,1.5,fill=1,stroke=0)
        canvas.setFillColor(HEAD)
        canvas.setFont(F,7)
        canvas.drawString(20*mm, H-10*mm, 'AKYRA')
        canvas.drawRightString(W-20*mm, H-10*mm, 'GUIDE : AUDIT DE SMART CONTRACTS')
        # Footer
        canvas.setFillColor(GOLD)
        canvas.rect(0,13*mm,W,1,fill=1,stroke=0)
        canvas.setFillColor(MUT)
        canvas.setFont(F,7)
        canvas.drawString(20*mm, 9*mm, 'Confidentiel — AKYRA 2026')
        canvas.drawRightString(W-20*mm, 9*mm, f'Page {doc.page}')
        canvas.restoreState()

def build():
    s = []
    OUT = '/Users/tgds.2/akyra/AKYRA_Guide_Audit.pdf'
    doc = Doc(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
              topMargin=18*mm, bottomMargin=18*mm)

    # ── COVER ──────────────────────────────────────────────────────
    s += [
        sp(14),
        P('AKYRA', S('_',36,HEAD,44,TA_CENTER)),
        sp(2), gold_line(), sp(3),
        P('GUIDE COMPLET', S('_',16,BLUE,22,TA_CENTER)),
        P('Audit de Smart Contracts', S('_',13,MUT,18,TA_CENTER)),
        sp(8),
        box(
            'Ce guide explique simplement ce qu\'est un audit de smart contracts, '
            'pourquoi c\'est indispensable pour AKYRA, '
            'et comment s\'en approcher sans tout payer dès le départ.',
            border=HEAD, bg=HEAD, tcol=GOLD, sz=11
        ),
        sp(6),
        tbl([
            [P('Partie', S('_',9,colors.white,13,TA_CENTER)),
             P('Sujet', S('_',9,colors.white,13))],
            [P('1', S('_',9,GOLD,13,TA_CENTER)),
             P('C\'est quoi un audit ?', S('_',9,BODY,13))],
            [P('2', S('_',9,GOLD,13,TA_CENTER)),
             P('Pourquoi c\'est obligatoire', S('_',9,BODY,13))],
            [P('3', S('_',9,GOLD,13,TA_CENTER)),
             P('Les failles les plus courantes (avec exemples réels)', S('_',9,BODY,13))],
            [P('4', S('_',9,GOLD,13,TA_CENTER)),
             P('Qui audite ? (payant vs gratuit)', S('_',9,BODY,13))],
            [P('5', S('_',9,GOLD,13,TA_CENTER)),
             P('Les alternatives gratuites — outils + communauté', S('_',9,BODY,13))],
            [P('6', S('_',9,GOLD,13,TA_CENTER)),
             P('La stratégie concrète pour AKYRA', S('_',9,BODY,13))],
        ], [22*mm, CW-22*mm], hbg=HEAD),
        PageBreak(),
    ]

    # ══ PARTIE 1 — C'EST QUOI UN AUDIT ══════════════════════════════
    s += [sec('PARTIE 1 — C\'EST QUOI UN AUDIT ?'), sp(4)]
    s += [
        box(
            'Un smart contract est un programme déployé sur la blockchain. '
            'Une fois en ligne, il ne peut plus être modifié. '
            'S\'il contient un bug ou une faille, n\'importe qui peut en profiter pour vider les fonds. '
            'L\'audit, c\'est une vérification complète du code AVANT qu\'il soit déployé.',
            border=BLUE, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('Comment se passe un audit ?', S('_',11,BLUE,15,sb=2,sa=6)),
    ]
    s += [
        tbl([
            [P('Étape', S('_',9,colors.white,13,TA_CENTER)),
             P('Ce qui se passe', S('_',9,colors.white,13))],
            [P('1', S('_',9,GOLD,13,TA_CENTER)),
             P('Tu envoies ton code source à la société d\'audit', S('_',9,BODY,13))],
            [P('2', S('_',9,GOLD,13,TA_CENTER)),
             P('Leurs experts lisent chaque ligne, cherchent des failles', S('_',9,BODY,13))],
            [P('3', S('_',9,GOLD,13,TA_CENTER)),
             P('Ils testent des scénarios d\'attaque sur ton contrat', S('_',9,BODY,13))],
            [P('4', S('_',9,GOLD,13,TA_CENTER)),
             P('Tu reçois un rapport : liste des problèmes + niveau de gravité', S('_',9,BODY,13))],
            [P('5', S('_',9,GOLD,13,TA_CENTER)),
             P('Tu corriges les problèmes, ils re-vérifient', S('_',9,BODY,13))],
            [P('6', S('_',9,GOLD,13,TA_CENTER)),
             P('Rapport final publié — accessible à tous les investisseurs', S('_',9,BODY,13))],
        ], [22*mm, CW-22*mm], hbg=BLUE),
        sp(5),
        P('Les niveaux de gravité dans un rapport d\'audit', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Niveau', S('_',9,colors.white,13,TA_CENTER)),
             P('Signification', S('_',9,colors.white,13)),
             P('Que faire', S('_',9,colors.white,13))],
            [P('CRITIQUE', S('_',9,colors.HexColor('#ff4444'),13,TA_CENTER)),
             P('Faille qui permet de vider tous les fonds', S('_',9,BODY,13)),
             P('Corriger ABSOLUMENT avant tout déploiement', S('_',9,RED,13))],
            [P('MAJEUR', S('_',9,colors.HexColor('#ff8800'),13,TA_CENTER)),
             P('Faille grave qui peut causer des pertes partielles', S('_',9,BODY,13)),
             P('Corriger avant le lancement', S('_',9,RED,13))],
            [P('MINEUR', S('_',9,colors.HexColor('#ccaa00'),13,TA_CENTER)),
             P('Bug qui affecte le fonctionnement sans vol direct', S('_',9,BODY,13)),
             P('Corriger si possible', S('_',9,BODY,13))],
            [P('INFO', S('_',9,MUT,13,TA_CENTER)),
             P('Mauvaise pratique, code non optimisé', S('_',9,BODY,13)),
             P('Bonne pratique mais pas urgent', S('_',9,MUT,13))],
        ], [28*mm, CW*0.5, CW-28*mm-CW*0.5], hbg=HEAD),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 2 — POURQUOI C'EST OBLIGATOIRE ═══════════════════════
    s += [sec('PARTIE 2 — POURQUOI C\'EST OBLIGATOIRE'), sp(4)]
    s += [
        alerte('Sans audit publié, les investisseurs sérieux ne mettront pas un centime dans AKYRA.'),
        sp(4),
        P('Ce qu\'un investisseur regarde en premier', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Question', S('_',9,colors.white,13)),
             P('Si oui', S('_',9,colors.white,13,TA_CENTER)),
             P('Si non', S('_',9,colors.white,13,TA_CENTER))],
            [P('Y a-t-il un audit publié ?', S('_',9,BODY,13)),
             P('OK', S('_',9,GRN,13,TA_CENTER)),
             P('Stop — trop risqué', S('_',9,RED,13,TA_CENTER))],
            [P('Qui a audité ? (réputation de l\'auditeur)', S('_',9,BODY,13)),
             P('Trail of Bits / Spearbit = confiance maximale', S('_',9,GRN,13,TA_CENTER)),
             P('Auditeur inconnu = méfiance', S('_',9,RED,13,TA_CENTER))],
            [P('Les bugs critiques ont-ils tous été corrigés ?', S('_',9,BODY,13)),
             P('OK', S('_',9,GRN,13,TA_CENTER)),
             P('Refus immédiat', S('_',9,RED,13,TA_CENTER))],
            [P('Y a-t-il un bug bounty actif ?', S('_',9,BODY,13)),
             P('Signe de sérieux supplémentaire', S('_',9,GRN,13,TA_CENTER)),
             P('Neutre', S('_',9,MUT,13,TA_CENTER))],
        ], [CW*0.45, CW*0.3, CW-CW*0.45-CW*0.3], hbg=HEAD),
        sp(5),
        box(
            'AKYRA est un projet où des agents IA vont gérer des wallets avec des fonds réels. '
            'Le niveau d\'exigence technique est encore plus élevé que pour un projet classique. '
            'Un audit n\'est pas une option — c\'est la base de la crédibilité.',
            border=GOLD, bg=BG2, tcol=HEAD
        ),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 3 — LES FAILLES LES PLUS COURANTES ═══════════════════
    s += [sec('PARTIE 3 — LES FAILLES LES PLUS COURANTES (exemples réels)'), sp(4)]
    s += [
        P('Ces failles existent depuis les débuts de la blockchain. Elles ont coûté des centaines de millions.',
          S('_',9,MUT,13,sa=8)),
    ]

    failles = [
        ('Reentrancy',
         'Le contrat peut être appelé plusieurs fois avant la fin de sa propre exécution.',
         'The DAO (2016) — 60 millions de dollars volés. C\'est cette faille qui a forcé Ethereum à faire un hard fork.'),
        ('Integer Overflow',
         'Un calcul dépasse la limite maximale d\'un nombre et recommence à zéro.',
         'Un attaquant crédite son compte de milliards de tokens. Corrigé par Solidity 0.8+.'),
        ('Access Control',
         'Une fonction réservée aux admins est accessible à n\'importe qui.',
         'Poly Network (2021) — 611 millions de dollars volés. La fonction "setManager" était publique.'),
        ('Flash Loan Attack',
         'Emprunter des millions en un seul bloc, manipuler les prix, rembourser — tout en un instant.',
         'bZx (2020) — 8 millions de dollars. Les prix étaient calculés depuis une source unique manipulable.'),
        ('Logic Flaw',
         'Le code fait exactement ce qui est écrit, mais ce qui est écrit ne correspond pas à l\'intention.',
         'Euler Finance (2023) — 197 millions de dollars. La logique de liquidation avait une erreur de conception.'),
    ]

    for nom, explication, cas in failles:
        s += [
            tbl([
                [P(nom, S('_',10,colors.white,14))],
            ], [CW], hbg=BLUE),
            tbl([
                [P('C\'est quoi ?', S('_',8,MUT,12)),
                 P(explication, S('_',9,BODY,13))],
                [P('Cas réel', S('_',8,MUT,12)),
                 P(cas, S('_',9,RED,13))],
            ], [28*mm, CW-28*mm], hbg=HEAD),
            sp(3),
        ]

    s.append(PageBreak())

    # ══ PARTIE 4 — QUI AUDITE ═══════════════════════════════════════
    s += [sec('PARTIE 4 — QUI AUDITE ? (payant)'), sp(4)]
    s += [
        P('Les sociétés d\'audit payantes — du meilleur au moins bon', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Société', S('_',9,colors.white,13)),
             P('Réputation', S('_',9,colors.white,13,TA_CENTER)),
             P('Prix estimé', S('_',9,colors.white,13,TA_CENTER)),
             P('Utilisé par', S('_',9,colors.white,13))],
            [P('Trail of Bits', S('_',9,BODY,13)),
             P('Tier 1 — Référence mondiale', S('_',9,GRN,13,TA_CENTER)),
             P('80 000 - 200 000 €', S('_',9,BODY,13,TA_CENTER)),
             P('Ethereum Foundation, OpenZeppelin', S('_',9,BODY,13))],
            [P('Spearbit / Cantina', S('_',9,BODY,13)),
             P('Tier 1 — Experts blockchain', S('_',9,GRN,13,TA_CENTER)),
             P('50 000 - 150 000 €', S('_',9,BODY,13,TA_CENTER)),
             P('Virtuals Protocol, Uniswap', S('_',9,BODY,13))],
            [P('Halborn', S('_',9,BODY,13)),
             P('Tier 1 — Spécialiste DeFi', S('_',9,GRN,13,TA_CENTER)),
             P('40 000 - 120 000 €', S('_',9,BODY,13,TA_CENTER)),
             P('Solana Foundation, Avalanche', S('_',9,BODY,13))],
            [P('OpenZeppelin Audits', S('_',9,BODY,13)),
             P('Tier 1 — Code de confiance', S('_',9,GRN,13,TA_CENTER)),
             P('60 000 - 180 000 €', S('_',9,BODY,13,TA_CENTER)),
             P('Coinbase, Compound', S('_',9,BODY,13))],
            [P('CertiK', S('_',9,BODY,13)),
             P('Connu mais insuffisant seul', S('_',9,colors.HexColor('#cc7700'),13,TA_CENTER)),
             P('10 000 - 50 000 €', S('_',9,BODY,13,TA_CENTER)),
             P('Beaucoup de projets — trop commun', S('_',9,BODY,13))],
        ], [38*mm, 42*mm, 38*mm, CW-38*mm-42*mm-38*mm], hbg=HEAD),
        sp(4),
        alerte('CertiK audite des centaines de projets dont beaucoup qui se sont avérés des arnaques. '
               'Le badge CertiK seul ne rassure plus les investisseurs expérimentés en 2026.'),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 5 — ALTERNATIVES GRATUITES ═══════════════════════════
    s += [sec('PARTIE 5 — LES ALTERNATIVES GRATUITES', color=GRN), sp(4)]
    s += [
        box(
            'Bonne nouvelle : il existe plusieurs façons sérieuses de sécuriser son code '
            'sans tout payer dès le départ. '
            'Ces outils sont utilisés par les meilleurs développeurs blockchain dans le monde.',
            border=GRN, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('1. Les outils automatiques — installer et lancer soi-même', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Outil', S('_',9,colors.white,13)),
             P('Ce qu\'il fait', S('_',9,colors.white,13)),
             P('Comment l\'utiliser', S('_',9,colors.white,13))],
            [P('Slither', S('_',9,GOLD,13)),
             P('Détecte les failles classiques : reentrancy, access control, variables mal initialisées',
               S('_',9,BODY,13)),
             P('pip install slither-analyzer — puis : slither MonContrat.sol', S('_',9,MUT,13))],
            [P('Mythril', S('_',9,GOLD,13)),
             P('Analyse les vulnérabilités au niveau de la machine virtuelle Ethereum (EVM)',
               S('_',9,BODY,13)),
             P('pip install mythril — puis : myth analyze MonContrat.sol', S('_',9,MUT,13))],
            [P('Echidna', S('_',9,GOLD,13)),
             P('Fuzzing : teste des milliers de cas aléatoires pour trouver des comportements inattendus',
               S('_',9,BODY,13)),
             P('Développé par Trail of Bits — open source et gratuit', S('_',9,MUT,13))],
            [P('4naly3er', S('_',9,GOLD,13)),
             P('Génère un rapport automatique qui ressemble à un vrai rapport d\'audit',
               S('_',9,BODY,13)),
             P('Disponible en ligne gratuitement — paste ton code et télécharge le rapport',
               S('_',9,MUT,13))],
        ], [28*mm, CW*0.48, CW-28*mm-CW*0.48], hbg=HEAD),
        sp(5),
        P('2. Code4rena — payer seulement si on trouve quelque chose', S('_',11,BLUE,15,sb=2,sa=6)),
        box(
            'Code4rena organise des concours publics d\'audit. '
            'Tu déposes une récompense (le montant est libre). '
            'Des centaines de chercheurs en sécurité cherchent des bugs dans ton code. '
            'Tu ne paies que pour les bugs réellement trouvés et confirmés. '
            'Le rapport est public — ce qui prouve ton sérieux aux investisseurs.',
            border=BLUE, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('3. Immunefi — bug bounty permanent', S('_',11,BLUE,15,sb=2,sa=6)),
        box(
            'Tu crées un programme de bug bounty public sur Immunefi. '
            'Les chercheurs signalent les bugs en privé. '
            'Tu paies uniquement si le bug est réel et confirmé. '
            'Avoir un bug bounty actif montre aux investisseurs que tu fais confiance à ton propre code.',
            border=BLUE, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('4. OpenZeppelin — utiliser du code déjà audité', S('_',11,BLUE,15,sb=2,sa=6)),
        box(
            'Au lieu d\'écrire tes contrats depuis zéro, tu importes les contrats standards '
            'de la bibliothèque OpenZeppelin. '
            'Ces contrats ont été audités des dizaines de fois par les meilleurs experts du monde. '
            'Moins tu écris de code original, moins tu crées de nouvelles failles. '
            'C\'est ce que font tous les projets sérieux.',
            border=GRN, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('5. Peer review — la communauté', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Source', S('_',9,colors.white,13)),
             P('Comment faire', S('_',9,colors.white,13))],
            [P('GitHub public', S('_',9,GOLD,13)),
             P('Mettre le code en open source — les développeurs du monde entier peuvent regarder et signaler des bugs',
               S('_',9,BODY,13))],
            [P('Discord OpenZeppelin', S('_',9,GOLD,13)),
             P('Poster son code dans le canal #security — des experts bénévoles donnent leur avis',
               S('_',9,BODY,13))],
            [P('Ethereum Magicians', S('_',9,GOLD,13)),
             P('Forum technique sérieux — les développeurs Ethereum y discutent de sécurité',
               S('_',9,BODY,13))],
        ], [38*mm, CW-38*mm], hbg=HEAD),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 6 — STRATÉGIE CONCRÈTE POUR AKYRA ═══════════════════
    s += [sec('PARTIE 6 — LA STRATÉGIE CONCRÈTE POUR AKYRA', color=HEAD), sp(4)]
    s += [
        box(
            'On n\'a pas besoin de tout payer maintenant. '
            'Il y a un ordre logique qui protège le projet '
            'et construit la crédibilité progressivement.',
            border=HEAD, bg=HEAD, tcol=GOLD, sz=11
        ),
        sp(5),
        tbl([
            [P('Phase', S('_',9,colors.white,13,TA_CENTER)),
             P('Moment', S('_',9,colors.white,13)),
             P('Actions sécurité', S('_',9,colors.white,13)),
             P('Coût', S('_',9,colors.white,13,TA_CENTER))],
            [P('Phase 1', S('_',9,GOLD,13,TA_CENTER)),
             P('Maintenant — code en cours', S('_',9,BODY,13)),
             P('Utiliser OpenZeppelin pour tous les contrats standards. '
               'Lancer Slither et Mythril sur chaque contrat écrit.',
               S('_',9,BODY,13)),
             P('Gratuit', S('_',9,GRN,13,TA_CENTER))],
            [P('Phase 2', S('_',9,GOLD,13,TA_CENTER)),
             P('Testnet — avant mainnet', S('_',9,BODY,13)),
             P('Ouvrir le code sur GitHub. '
               'Lancer Echidna (fuzzing). '
               'Poster le code sur Discord OpenZeppelin. '
               'Créer un bug bounty Code4rena avec petite récompense.',
               S('_',9,BODY,13)),
             P('Très faible', S('_',9,GRN,13,TA_CENTER))],
            [P('Phase 3', S('_',9,GOLD,13,TA_CENTER)),
             P('Avant mainnet — avant de lever des fonds', S('_',9,BODY,13)),
             P('1 audit payant minimum — Halborn ou Spearbit. '
               'Budget : 15 000 à 50 000 euros selon la complexité du code. '
               'Rapport publié publiquement.',
               S('_',9,BODY,13)),
             P('15-50k€', S('_',9,colors.HexColor('#cc7700'),13,TA_CENTER))],
            [P('Phase 4', S('_',9,GOLD,13,TA_CENTER)),
             P('Post-lancement — en continu', S('_',9,BODY,13)),
             P('Bug bounty permanent sur Immunefi. '
               'Audit de chaque mise à jour majeure du code.',
               S('_',9,BODY,13)),
             P('Pay-per-bug', S('_',9,GRN,13,TA_CENTER))],
        ], [20*mm, 42*mm, CW-20*mm-42*mm-25*mm, 25*mm], hbg=BLUE),
        sp(6),
        check('Pour AKYRA, le seul vrai investissement obligatoire est l\'audit payant de Phase 3. '
              'Tout le reste peut se faire gratuitement avec les bons outils.'),
        sp(4),
        alerte('Ne jamais déployer en mainnet avec des fonds réels sans au moins un audit payant publié. '
               'C\'est non-négociable.'),
        sp(6),
        P('Résumé en une phrase', S('_',11,BLUE,15,sb=2,sa=6)),
        box(
            'Phase 1 et 2 : outils gratuits + communauté.  '
            'Phase 3 : un audit payant sérieux obligatoire avant le mainnet.  '
            'Phase 4 : bug bounty permanent pour maintenir la confiance.',
            border=GOLD, bg=BG2, tcol=HEAD, sz=11
        ),
    ]

    doc.build(s)
    print('PDF :', OUT)

build()
