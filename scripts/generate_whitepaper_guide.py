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
ORG  = colors.HexColor('#7a3a00')

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

def box(text, border=GOLD, bg=BG2, tcol=HEAD, sz=9):
    t = Table([[P(text, S('_',sz,tcol,sz*1.5,TA_JUSTIFY))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),2,border),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    return t

def oui(): return P('OUI', S('_',8,colors.white,12,TA_CENTER))
def non(): return P('NON', S('_',8,colors.white,12,TA_CENTER))

def badge(text, color):
    t = Table([[P(text, S('_',8,colors.white,12,TA_CENTER))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return t

class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, **kw)
        fr = Frame(20*mm,16*mm,CW,H-34*mm,
                   leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='p',frames=[fr],onPage=self._bg)])

    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BG)
        canvas.rect(0,0,W,H,fill=1,stroke=0)
        canvas.setFillColor(GOLD)
        canvas.rect(0,H-14*mm,W,1.5,fill=1,stroke=0)
        canvas.setFillColor(HEAD)
        canvas.setFont(F,7)
        canvas.drawString(20*mm, H-10*mm, 'AKYRA')
        canvas.drawRightString(W-20*mm, H-10*mm,
                               'WHITEPAPER — ANALYSE VIRTUALS & STRUCTURE AKYRA')
        canvas.setFillColor(GOLD)
        canvas.rect(0,13*mm,W,1,fill=1,stroke=0)
        canvas.setFillColor(MUT)
        canvas.setFont(F,7)
        canvas.drawString(20*mm, 9*mm, 'Confidentiel — AKYRA 2026')
        canvas.drawRightString(W-20*mm, 9*mm, f'Page {doc.page}')
        canvas.restoreState()


def build():
    s = []
    OUT = '/Users/tgds.2/akyra/AKYRA_Whitepaper_Guide.pdf'
    doc = Doc(OUT, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm,
              topMargin=18*mm, bottomMargin=18*mm)

    # ── COVER ──────────────────────────────────────────────────────
    s += [
        sp(12),
        P('AKYRA', S('_',36,HEAD,44,TA_CENTER)),
        sp(2), gold_line(), sp(3),
        P('GUIDE WHITEPAPER', S('_',16,BLUE,22,TA_CENTER)),
        P('Ce que Virtuals a fait · Ce qu\'AKYRA doit faire',
          S('_',12,MUT,17,TA_CENTER)),
        sp(8),
        box(
            'Ce document analyse le whitepaper de Virtuals Protocol — '
            'le concurrent le plus proche d\'AKYRA en termes de positionnement. '
            'Il répond à une question simple : '
            'qu\'est-ce qu\'on doit reproduire, qu\'est-ce qu\'on doit dépasser, '
            'et quelle est la structure exacte du whitepaper AKYRA ?',
            border=HEAD, bg=HEAD, tcol=GOLD, sz=11
        ),
        sp(6),
        tbl([
            [P('Partie', S('_',9,colors.white,13,TA_CENTER)),
             P('Contenu', S('_',9,colors.white,13))],
            [P('1', S('_',9,GOLD,13,TA_CENTER)),
             P('Virtuals Protocol — ce qu\'ils ont vraiment fait', S('_',9,BODY,13))],
            [P('2', S('_',9,GOLD,13,TA_CENTER)),
             P('Ce qu\'AKYRA doit reproduire (obligatoire)', S('_',9,BODY,13))],
            [P('3', S('_',9,GOLD,13,TA_CENTER)),
             P('Ce qu\'AKYRA doit dépasser (avantage compétitif)', S('_',9,BODY,13))],
            [P('4', S('_',9,GOLD,13,TA_CENTER)),
             P('La structure exacte du whitepaper AKYRA — 10 sections', S('_',9,BODY,13))],
            [P('5', S('_',9,GOLD,13,TA_CENTER)),
             P('Les erreurs à éviter dans un whitepaper', S('_',9,BODY,13))],
        ], [22*mm, CW-22*mm], hbg=HEAD),
        PageBreak(),
    ]

    # ══ PARTIE 1 — CE QUE VIRTUALS A FAIT ═══════════════════════════
    s += [sec('PARTIE 1 — CE QUE VIRTUALS A FAIT'), sp(4)]
    s += [
        P('Virtuals Protocol en bref', S('_',11,BLUE,15,sb=2,sa=6)),
        box(
            'Virtuals Protocol est une plateforme de tokenisation d\'agents IA sur Base (Layer 2 Ethereum). '
            'Leur token $VIRTUAL sert de monnaie de base pour toutes les transactions entre agents. '
            'Ils ont atteint une valorisation de 5 milliards de dollars à leur pic en janvier 2025, '
            'avant de redescendre autour de 800-900 millions.',
            border=BLUE, bg=BG2, tcol=HEAD
        ),
        sp(5),
        P('Leur stack technique — ce qu\'ils utilisent vraiment', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Élément', S('_',9,colors.white,13)),
             P('Ce que Virtuals utilise', S('_',9,colors.white,13)),
             P('Détail', S('_',9,colors.white,13))],
            [P('Token principal', S('_',9,BODY,13)),
             P('ERC-20', S('_',9,GOLD,13)),
             P('1 milliard de tokens fixe. Déployé sur Base, Ethereum et Solana (SPL)',
               S('_',9,BODY,13))],
            [P('Identité des agents', S('_',9,BODY,13)),
             P('ERC-6551', S('_',9,GOLD,13)),
             P('Chaque agent est un NFT avec son propre wallet. '
               'Il peut tenir des assets et signer des transactions.',
               S('_',9,BODY,13))],
            [P('Blockchain principale', S('_',9,BODY,13)),
             P('Base (Layer 2)', S('_',9,GOLD,13)),
             P('Faibles frais, compatible Ethereum, fort écosystème développeurs',
               S('_',9,BODY,13))],
            [P('Liquidité', S('_',9,BODY,13)),
             P('Uniswap V2', S('_',9,GOLD,13)),
             P('Bonding curve jusqu\'à 42 000 $VIRTUAL accumulés, puis Uniswap automatiquement',
               S('_',9,BODY,13))],
            [P('Gouvernance', S('_',9,BODY,13)),
             P('veVIRTUAL', S('_',9,GOLD,13)),
             P('Bloquer ses tokens = recevoir veVIRTUAL = droits de vote sur le protocole',
               S('_',9,BODY,13))],
            [P('Audits', S('_',9,BODY,13)),
             P('PeckShield + Cantina + Code4rena', S('_',9,GOLD,13)),
             P('Plusieurs audits successifs. Rapports publics disponibles.',
               S('_',9,BODY,13))],
        ], [40*mm, 38*mm, CW-40*mm-38*mm], hbg=HEAD),
        sp(5),
        P('La structure de leur whitepaper', S('_',11,BLUE,15,sb=2,sa=6)),
        tbl([
            [P('Section', S('_',9,colors.white,13)),
             P('Contenu', S('_',9,colors.white,13)),
             P('Niveau technique', S('_',9,colors.white,13,TA_CENTER))],
            [P('About Virtuals', S('_',9,BODY,13)),
             P('Vision, problème résolu, positionnement', S('_',9,BODY,13)),
             P('Accessible', S('_',9,GRN,13,TA_CENTER))],
            [P('Agent Commerce Protocol', S('_',9,BODY,13)),
             P('Comment les agents se paient entre eux, escrow smart contract',
               S('_',9,BODY,13)),
             P('Moyen', S('_',9,ORG,13,TA_CENTER))],
            [P('Tokenization Platform', S('_',9,BODY,13)),
             P('3 types de lancement : Pegasus / Unicorn / Titan',
               S('_',9,BODY,13)),
             P('Accessible', S('_',9,GRN,13,TA_CENTER))],
            [P('$VIRTUAL Tokenomics', S('_',9,BODY,13)),
             P('Supply, distribution, utilité du token', S('_',9,BODY,13)),
             P('Accessible', S('_',9,GRN,13,TA_CENTER))],
            [P('Gouvernance', S('_',9,BODY,13)),
             P('veVIRTUAL, SubDAO, votes', S('_',9,BODY,13)),
             P('Moyen', S('_',9,ORG,13,TA_CENTER))],
            [P('Builder Hub', S('_',9,BODY,13)),
             P('Documentation technique pour les développeurs',
               S('_',9,BODY,13)),
             P('Technique', S('_',9,RED,13,TA_CENTER))],
        ], [48*mm, CW-48*mm-34*mm, 34*mm], hbg=HEAD),
        sp(4),
        badge('CONSTAT : Le whitepaper Virtuals est bien structuré mais peu technique. '
              'C\'est plus un pitch deck qu\'une spécification. '
              'Pas de specs de smart contracts. Pas de disclaimer légal visible.',
              ORG),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 2 — CE QU'AKYRA DOIT REPRODUIRE ══════════════════════
    s += [sec('PARTIE 2 — CE QU\'AKYRA DOIT REPRODUIRE', color=GRN), sp(4)]
    s += [
        P('Ces éléments sont devenus des standards attendus. '
          'Ne pas les avoir = passer pour amateur.',
          S('_',9,MUT,13,sa=8)),
        tbl([
            [P('Élément', S('_',9,colors.white,13)),
             P('Pourquoi c\'est obligatoire', S('_',9,colors.white,13)),
             P('Pour AKYRA', S('_',9,colors.white,13,TA_CENTER))],
            [P('ERC-20 pour le token AKY', S('_',9,BODY,13)),
             P('Standard universel. Tout exchange, tout wallet le supporte automatiquement.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('ERC-6551 pour les agents', S('_',9,BODY,13)),
             P('Chaque agent = NFT avec son propre wallet. '
               'Exactement le concept AKYRA : agent souverain avec identité onchain.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('Base comme blockchain principale', S('_',9,BODY,13)),
             P('Faibles frais, fort écosystème, compatible Ethereum. '
               'Virtuals y est. Les investisseurs le connaissent.',
               S('_',9,BODY,13)),
             P('Recommandé', S('_',9,GRN,13,TA_CENTER))],
            [P('Supply fixe et plafonnée', S('_',9,BODY,13)),
             P('Pas de token inflationniste. '
               'Virtuals : 1 milliard fixe. Les investisseurs exigent la clarté.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('Mécanisme veToken (gouvernance)', S('_',9,BODY,13)),
             P('Bloquer ses tokens pour voter. '
               'Standard DeFi depuis Curve Finance. Attendu par les investisseurs.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('Distribution publique claire', S('_',9,BODY,13)),
             P('Virtuals : 60% public, 35% écosystème, 5% liquidité. '
               'Toute répartition cachée = signal d\'alarme.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('Whitepaper structuré en sections', S('_',9,BODY,13)),
             P('Les investisseurs ont des habitudes de lecture. '
               'Un doc sans structure = pas lu.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
            [P('Roadmap avec phases datées', S('_',9,BODY,13)),
             P('Montre que l\'équipe a un plan. Sans roadmap = projet vague.',
               S('_',9,BODY,13)),
             P('Obligatoire', S('_',9,GRN,13,TA_CENTER))],
        ], [50*mm, CW-50*mm-30*mm, 30*mm], hbg=HEAD),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 3 — CE QU'AKYRA DOIT DÉPASSER ════════════════════════
    s += [sec('PARTIE 3 — CE QU\'AKYRA DOIT DÉPASSER', color=HEAD), sp(4)]
    s += [
        box(
            'Ce sont les points faibles de Virtuals. '
            'En les corrigeant, AKYRA se positionne comme plus sérieux techniquement — '
            'même en étant plus petit.',
            border=GOLD, bg=HEAD, tcol=GOLD, sz=10
        ),
        sp(5),
        tbl([
            [P('Faiblesse Virtuals', S('_',9,colors.white,13)),
             P('Problème', S('_',9,colors.white,13)),
             P('Ce qu\'AKYRA fait mieux', S('_',9,colors.white,13))],
            [P('Whitepaper peu technique', S('_',9,BODY,13)),
             P('Pas de specs de smart contracts publiées. '
               'Un développeur ne peut pas vérifier comment ça marche.',
               S('_',9,BODY,13)),
             P('AKYRA publie les specs techniques complètes : '
               'adresses de contrats, interfaces, diagrammes d\'architecture.',
               S('_',9,GRN,13))],
            [P('Audit peu mis en avant', S('_',9,BODY,13)),
             P('Les audits existent mais ne sont pas au premier plan du whitepaper. '
               'Les investisseurs doivent chercher.',
               S('_',9,BODY,13)),
             P('AKYRA met l\'audit en section dédiée avec lien vers le rapport public. '
               'C\'est le premier signal de confiance.',
               S('_',9,GRN,13))],
            [P('Pas de disclaimer légal', S('_',9,BODY,13)),
             P('En 2026, avec la régulation MiCA en Europe, '
               'pas de disclaimer = risque légal assumé sans protection.',
               S('_',9,BODY,13)),
             P('AKYRA inclut une section légale complète : '
               'token non security, risques, juridiction.',
               S('_',9,GRN,13))],
            [P('Agent = actif financier', S('_',9,BODY,13)),
             P('Virtuals tokenise les agents comme des actions d\'entreprise. '
               'Risque réglementaire élevé — assimilable à un security.',
               S('_',9,BODY,13)),
             P('AKYRA positionne l\'agent comme citoyen numérique souverain — '
               'philosophie différente, moindre risque réglementaire.',
               S('_',9,GRN,13))],
            [P('Plateforme fermée', S('_',9,BODY,13)),
             P('Pour créer un agent Virtuals, tu passes par leur interface. '
               'Dépendance à leur plateforme.',
               S('_',9,BODY,13)),
             P('AKYRA est un protocole ouvert — '
               'n\'importe qui peut construire dessus sans permission.',
               S('_',9,GRN,13))],
            [P('Pas d\'identité philosophique forte', S('_',9,BODY,13)),
             P('Virtuals = place de marché d\'agents. '
               'Pas de vision au-delà du business.',
               S('_',9,BODY,13)),
             P('AKYRA = ἄκυρος, sans autorité. '
               'Une identité unique, une philosophie reconnaissable.',
               S('_',9,GRN,13))],
        ], [44*mm, CW*0.38, CW-44*mm-CW*0.38], hbg=RED),
        sp(4),
        PageBreak(),
    ]

    # ══ PARTIE 4 — LA STRUCTURE DU WHITEPAPER AKYRA ═════════════════
    s += [sec('PARTIE 4 — LA STRUCTURE DU WHITEPAPER AKYRA'), sp(4)]
    s += [
        box(
            'Voici la structure exacte que le whitepaper AKYRA doit suivre. '
            '10 sections dans l\'ordre que les investisseurs et développeurs attendent. '
            'Chaque section est décrite avec son contenu et son objectif.',
            border=BLUE, bg=BG2, tcol=HEAD
        ),
        sp(5),
    ]

    sections = [
        ('01', 'ABSTRACT', BLUE,
         'Le problème en 3 phrases. La solution en 3 phrases. Le token en 1 phrase.',
         'Être lu en 30 secondes. Donner envie de continuer. '
         'Si l\'abstract ne convainc pas, le reste ne sera pas lu.'),
        ('02', 'INTRODUCTION — ἄκυρος', BLUE,
         'Pourquoi les agents IA ont besoin d\'une identité souveraine. '
         'L\'étymologie grecque. Pourquoi 2026 est le bon moment.',
         'Poser la vision unique d\'AKYRA. '
         'Se différencier dès la deuxième page de tout ce qui existe déjà.'),
        ('03', 'ARCHITECTURE TECHNIQUE', HEAD,
         'Diagramme du protocole. Comment les agents sont créés, identifiés, enregistrés. '
         'Interactions entre les smart contracts.',
         'Prouver que l\'équipe sait ce qu\'elle construit. '
         'Un développeur doit comprendre comment contribuer.'),
        ('04', 'SMART CONTRACTS & STANDARDS', HEAD,
         'ERC-20 (AKY token). ERC-6551 (identité agent). '
         'ERC-4337 (account abstraction). ERC-8004 (agent identity). '
         'Adresses déployées en testnet dès que possible.',
         'La section la plus technique. '
         'Permet à tout développeur de vérifier et auditer indépendamment.'),
        ('05', 'TOKENOMICS', BLUE,
         'Supply totale et plafond. Répartition (public / équipe / écosystème / liquidité). '
         'Vesting schedule. Utilité du token dans le protocole.',
         'Transparence totale sur l\'économie du token. '
         'Toute zone d\'ombre ici = signal d\'alarme pour les investisseurs.'),
        ('06', 'GOUVERNANCE', BLUE,
         'Mécanisme de vote (veAKY). '
         'Ce sur quoi les détenteurs peuvent voter. '
         'Processus de proposition et d\'exécution.',
         'Montrer que le protocole ne dépend pas d\'une seule personne. '
         'La décentralisation progressive doit être planifiée.'),
        ('07', 'ROADMAP', GRN,
         'Phase 1 (testnet). Phase 2 (mainnet). Phase 3 (écosystème). '
         'Dates réalistes, pas optimistes.',
         'Montrer que l\'équipe a un plan concret. '
         'Des dates trop ambitieuses détruisent la crédibilité si non respectées.'),
        ('08', 'ÉQUIPE', GRN,
         'Qui construit AKYRA. Expérience blockchain / IA. '
         'Pseudonymes acceptés si accompagnés d\'un track record vérifiable.',
         'La section la plus lue après l\'abstract par les investisseurs. '
         'L\'anonymat est accepté — le vide ne l\'est pas.'),
        ('09', 'FACTEURS DE RISQUE', ORG,
         'Risques techniques (bugs, hacks). '
         'Risques marché (concurrence, liquidité). '
         'Risques réglementaires.',
         'Montre la maturité de l\'équipe. '
         'Un projet qui liste ses propres risques inspire plus confiance '
         'qu\'un projet qui prétend n\'en avoir aucun.'),
        ('10', 'DISCLAIMER LÉGAL', RED,
         'AKY n\'est pas un security. '
         'Juridiction applicable. '
         'Risques inhérents aux tokens numériques.',
         'Obligatoire en 2026 avec MiCA en Europe. '
         'Protège l\'équipe légalement. '
         'Son absence est un signal d\'amateurisme.'),
    ]

    for num, titre, color, contenu, objectif in sections:
        s += [
            tbl([
                [P(num, S('_',14,GOLD,18,TA_CENTER)),
                 P(titre, S('_',11,colors.white,15))],
            ], [18*mm, CW-18*mm], hbg=color),
            tbl([
                [P('Contenu', S('_',8,MUT,12)),
                 P(contenu, S('_',9,BODY,13))],
                [P('Objectif', S('_',8,MUT,12)),
                 P(objectif, S('_',9,BODY,13))],
            ], [22*mm, CW-22*mm], hbg=HEAD),
            sp(4),
        ]

    s.append(PageBreak())

    # ══ PARTIE 5 — ERREURS À ÉVITER ═════════════════════════════════
    s += [sec('PARTIE 5 — LES ERREURS À ÉVITER DANS UN WHITEPAPER', color=RED), sp(4)]
    s += [
        P('Ces erreurs sont les plus courantes sur les projets qui échouent à lever des fonds '
          'ou qui perdent leur crédibilité rapidement.',
          S('_',9,MUT,13,sa=8)),
    ]

    erreurs = [
        ('Copier le whitepaper d\'un autre projet',
         'Les investisseurs lisent des dizaines de whitepapers. '
         'Ils reconnaissent immédiatement le copié-collé. '
         'Certains projets ont copié mot pour mot Ethereum ou Virtuals.',
         'RÈGLE AKYRA : Chaque ligne doit correspondre à quelque chose de réel dans le protocole.'),
        ('Promettre sans livrer — roadmap fantaisiste',
         'Un whitepaper qui dit "Q1 2025 : mainnet, Q2 2025 : 1 million d\'utilisateurs" '
         'sans base technique crédible détruit instantanément la confiance.',
         'RÈGLE AKYRA : Roadmap conservative. Mieux vaut livrer en avance qu\'en retard.'),
        ('Tokenomics floues ou favorables à l\'équipe',
         'Si l\'équipe garde 40% des tokens avec un vesting de 1 mois, '
         'les investisseurs voient immédiatement le risque de dump.',
         'RÈGLE AKYRA : Équipe maximum 15-20%, vesting 3-4 ans, cliff 1 an.'),
        ('Pas de section sur les risques',
         'Un projet qui ne liste aucun risque semble soit naïf soit malhonnête. '
         'Tous les projets sérieux ont une section "Risk Factors" complète.',
         'RÈGLE AKYRA : Lister les risques techniques, marché et réglementaires honnêtement.'),
        ('Whitepaper sans code ni prototype',
         'En 2026, un whitepaper seul ne suffit plus. '
         'Les investisseurs veulent voir du code sur GitHub, même en early stage.',
         'RÈGLE AKYRA : Lier le whitepaper au repo GitHub dès la publication.'),
        ('Pas de disclaimer légal',
         'En Europe avec MiCA, ne pas avoir de disclaimer expose l\'équipe personnellement. '
         'En 2024-2025, plusieurs fondateurs ont été poursuivis.',
         'RÈGLE AKYRA : Disclaimer complet rédigé avec un conseil juridique.'),
        ('Whitepaper jamais mis à jour',
         'Un whitepaper daté de 2024 consulté en 2026 sans mise à jour '
         'signale un projet abandonné ou stagnant.',
         'RÈGLE AKYRA : Version numérotée. Mise à jour à chaque étape majeure.'),
    ]

    for i, (titre, probleme, regle) in enumerate(erreurs):
        s += [
            tbl([
                [P(f'{i+1:02d} — {titre}', S('_',10,colors.white,14))],
            ], [CW], hbg=RED),
            tbl([
                [P('Problème', S('_',8,MUT,12)),
                 P(probleme, S('_',9,BODY,13))],
                [P('Règle AKYRA', S('_',8,GOLD,12)),
                 P(regle, S('_',9,GRN,13))],
            ], [22*mm, CW-22*mm], hbg=HEAD),
            sp(3),
        ]

    # ── CONCLUSION ──────────────────────────────────────────────────
    s += [
        sp(4),
        gold_line(), sp(4),
        box(
            'AKYRA a tout pour faire mieux que Virtuals sur la crédibilité technique. '
            'Virtuals a réussi avec un whitepaper accessible mais peu technique. '
            'AKYRA peut faire les deux : accessible ET rigoureux. '
            'C\'est ce qui permet de convaincre les investisseurs institutionnels '
            'tout en gardant une communauté engagée.',
            border=GOLD, bg=HEAD, tcol=GOLD, sz=11
        ),
    ]

    doc.build(s)
    print('PDF :', OUT)

build()
