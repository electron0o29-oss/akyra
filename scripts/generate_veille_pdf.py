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

def P(t, st=None, **kw):
    if st is None: st = S('_')
    if kw: st = ParagraphStyle('_x', parent=st, **kw)
    return Paragraph(t, st)

def sp(h=4): return Spacer(1, h*mm)

def alt_rows(n, s=1):
    return [('BACKGROUND', (0,i),(-1,i), BG if i%2==1 else BG3) for i in range(s,n)]

def sec(label, color=BLUE):
    t = Table([[P(label, S('_',10,colors.white,14))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def sub(label, color=HEAD):
    t = Table([[P(label, S('_',9,colors.white,13))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def gold_line():
    t = Table([[P(' ', S('_',1,GOLD,2))]], colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),GOLD),
                           ('TOPPADDING',(0,0),(-1,-1),1),('BOTTOMPADDING',(0,0),(-1,-1),1)]))
    return t

def tbl(rows, widths, hbg=BLUE):
    n = len(rows)
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),('FONTSIZE',(0,0),(-1,-1),8.5),
        ('BACKGROUND',(0,0),(-1,0),hbg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ] + alt_rows(n)))
    return t

def box(text, border=GOLD, bg=BG2, tcol=BLUE, sz=9.5):
    t = Table([[P(text, S('_',sz,tcol,sz*1.5,TA_JUSTIFY))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1.5,border),
        ('TOPPADDING',(0,0),(-1,-1),12),('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1),14),('RIGHTPADDING',(0,0),(-1,-1),14),
    ]))
    return t

def tag(text, color=GRN):
    t = Table([[P(text, S('_',7.5,colors.white,11,TA_CENTER))]], colWidths=[26*mm])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4),
    ]))
    return t

class Doc(BaseDocTemplate):
    def __init__(self, fn, **kw):
        BaseDocTemplate.__init__(self, fn, **kw)
        fr = Frame(20*mm,16*mm,CW,H-34*mm,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)
        self.addPageTemplates([PageTemplate(id='p',frames=[fr],onPage=self._bg)])
    def _bg(self, canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(LINE); canvas.setLineWidth(0.5)
        canvas.line(20*mm,H-13*mm,W-20*mm,H-13*mm)
        canvas.setFont(F,6.5); canvas.setFillColor(MUT)
        canvas.drawString(20*mm,H-10.5*mm,'AKYRA — VEILLE MARCHÉ IA × CRYPTO — MARS 2026')
        canvas.drawRightString(W-20*mm,H-10.5*mm,'Données fraîches · Confidentiel')
        canvas.line(20*mm,13.5*mm,W-20*mm,13.5*mm)
        canvas.drawString(20*mm,10*mm,'ἄκυρος · α- privatif · κύριος — le souverain')
        canvas.drawRightString(W-20*mm,10*mm,str(doc.page))
        canvas.restoreState()

def build():
    out = '/Users/tgds.2/akyra/AKYRA_Veille_Marche.pdf'
    doc = Doc(out,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    s = []

    # ── COVER ─────────────────────────────────────────────────
    s += [sp(12), P('AKYRA', S('_',34,HEAD,40,TA_CENTER)), sp(3), gold_line(), sp(3),
          P('VEILLE MARCHÉ IA × CRYPTO', S('_',13,MUT,18,TA_CENTER)), sp(1),
          P('Ce qui se passe vraiment — Mars 2026', S('_',9,MUT,13,TA_CENTER)), sp(10)]

    cov_stats = Table([
        [P('$28B+',  S('_',20,HEAD,24,TA_CENTER)),
         P('550+',   S('_',20,HEAD,24,TA_CENTER)),
         P('86%',    S('_',20,RED, 24,TA_CENTER)),
         P('$3.06B', S('_',20,BLUE,24,TA_CENTER))],
        [P('Marché AI crypto total', S('_',7,MUT,10,TA_CENTER)),
         P('Projets AI agents listés', S('_',7,MUT,10,TA_CENTER)),
         P('Tokens morts en 2025', S('_',7,MUT,10,TA_CENTER)),
         P('AI agents seul (mars 2026)', S('_',7,MUT,10,TA_CENTER))],
    ], colWidths=[CW/4]*4)
    cov_stats.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),F),('ALIGN',(0,0),(-1,-1),'CENTER'),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5)]))
    s += [cov_stats, sp(8), gold_line(), sp(5)]

    sum_tbl = Table([
        [P('01', S('_',11,GOLD,14,TA_CENTER)), P('02', S('_',11,GOLD,14,TA_CENTER)),
         P('03', S('_',11,GOLD,14,TA_CENTER)), P('04', S('_',11,GOLD,14,TA_CENTER)),
         P('05', S('_',11,GOLD,14,TA_CENTER))],
        [P('Marché\nAI Agents', S('_',8,colors.white,12,TA_CENTER)),
         P('Monde IA\nActuel', S('_',8,colors.white,12,TA_CENTER)),
         P('Concurrents\nDirects', S('_',8,colors.white,12,TA_CENTER)),
         P('Standards\nÉmergents', S('_',8,colors.white,12,TA_CENTER)),
         P('Ce qu\'on\nRetient', S('_',8,colors.white,12,TA_CENTER))],
    ], colWidths=[CW/5]*5)
    sum_tbl.setStyle(TableStyle([('FONTNAME',(0,0),(-1,-1),F),('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#3a3630'))]))
    s += [sum_tbl, PageBreak()]

    # ══ 01 — MARCHÉ AI AGENTS CRYPTO ═════════════════════════
    s.append(sec('01 — MARCHÉ AI AGENTS CRYPTO — ÉTAT MARS 2026'))
    s += [sp(4), P('Vue d\'ensemble', S('_',10,HEAD,14,sb=0,sa=4)),
          P('Le marché des AI agents crypto a connu un boom spectaculaire en 2024–2025, '
            'suivi d\'une correction violente. En mars 2026, on est dans une phase de consolidation '
            'avec les projets à infrastructure réelle qui résistent, '
            'et les tokens purement spéculatifs qui ont perdu 85–97%.',
            S('_',9,BODY,14,TA_JUSTIFY,sa=5)), sp(4)]

    s.append(tbl([
        [P('Projet', S('_',8.5,colors.white,12)),
         P('Token', S('_',8.5,colors.white,12)),
         P('Market Cap Mars 2026', S('_',8.5,colors.white,12)),
         P('ATH (2025)', S('_',8.5,colors.white,12)),
         P('Variation ATH→Actuel', S('_',8.5,colors.white,12)),
         P('Statut', S('_',8.5,colors.white,12))],
        [P('Bittensor'),  P('TAO'),     P('$2.77B'),   P('~$750'),   P('+35% (semaine)'), P('✅ Solide')],
        [P('NEAR Protocol'), P('NEAR'), P('$3.24B'),   P('~$9.00'),  P('Recovery en cours'), P('✅ Solide')],
        [P('Virtuals Protocol'), P('VIRTUAL'), P('$915M'), P('$5.00 (janv. 2025)'), P('−85%'), P('⚠️ Correction')],
        [P('Fetch.ai / ASI'), P('FET'), P('$417M'),    P('~$3.50'),  P('−90%+'), P('⚠️ Rebuild')],
        [P('ElizaOS (ex ai16z)'), P('ELIZAOS'), P('~$70M'), P('$2.72B (fév. 2025)'), P('−97%'), P('🔴 Crash')],
        [P('Grass'),      P('GRASS'),   P('$192M'),    P('~$4.50'),  P('−58%'), P('⚠️ Stable')],
        [P('The Graph'),  P('GRT'),     P('$1B'),      P('~$0.90'),  P('−88%'), P('⚠️ Rebuild')],
    ], [38*mm, 18*mm, 34*mm, 28*mm, 34*mm, CW-152*mm]))
    s += [sp(3),
          P('→ Pattern clair : les projets avec infrastructure technique réelle (Bittensor, NEAR) '
            'tiennent. Les tokens qui n\'étaient que narrative et spéculation ont perdu 85–97%.',
            S('_',8,MUT,12,sa=3)), sp(5)]

    s.append(P('Ce qui marche vs ce qui échoue', S('_',10,HEAD,14,sb=0,sa=4)))
    win_fail = Table([
        [P('✅ CE QUI MARCHE', S('_',9,colors.white,13,TA_CENTER)),
         P('🔴 CE QUI ÉCHOUE', S('_',9,colors.white,13,TA_CENTER))],
        [P('Infrastructure verifiable (compute, data, identity)\n'
           'Stablecoins comme couche de paiement agent\n'
           'Open-source avec communauté de devs réelle\n'
           'Proof-of-concept AVANT le token\n'
           'Transparence sur les risques et les tokenomics\n'
           'Agents avec utilité réelle (trading, analytics)',
           S('_',8.5,GRN,14)),
         P('Tokens sans fondamentaux (narrative pure)\n'
           'Side deals opaques avec insiders (Movement Labs)\n'
           'Promesses > produit (hype sans testnet)\n'
           'Flat rewards sans mérite\n'
           '53% de tous les tokens lancés depuis 2021 = morts\n'
           '86% des failures en 2025 seul',
           S('_',8.5,RED,14))],
    ], colWidths=[CW/2, CW/2])
    win_fail.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(0,0),GRN),('BACKGROUND',(1,0),(1,0),RED),
        ('BACKGROUND',(0,1),(0,1),colors.HexColor('#f0fff0')),
        ('BACKGROUND',(1,1),(1,1),colors.HexColor('#fff0f0')),
        ('GRID',(0,0),(-1,-1),0.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    s += [win_fail, sp(4)]

    s.append(box(
        'Chiffre clé : 53% de tous les tokens crypto lancés depuis 2021 sont inactifs. '
        '86% de ces failures ont eu lieu en 2025. '
        '$19B de liquidation en octobre 2025 = 7.7 millions de tokens effacés. '
        'Le marché a purgé. Ce qui reste en mars 2026 a survécu à quelque chose.'
    ))
    s.append(PageBreak())

    # ══ 02 — MONDE IA ACTUEL ═════════════════════════════════
    s.append(sec('02 — MONDE IA ACTUEL — CE QUI CHANGE EN 2025–2026'))
    s += [sp(4)]

    s.append(P('Les modèles — la course s\'accélère', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Modèle'), P('Lab'), P('Date'), P('Ce qui est notable')],
        [P('GPT-5'),      P('OpenAI'),    P('Août 2025'),   P('Le grand saut. Raisonnement adaptatif.')],
        [P('GPT-5.3 Codex'), P('OpenAI'), P('Fév. 2026'),  P('Spécialisé code. Génération automatique de smart contracts.')],
        [P('Claude Opus 4.5'), P('Anthropic'), P('Nov. 2025'), P('Modèle frontier dominant début 2026.')],
        [P('Gemini 3.1 Pro'), P('Google'),P('Fév. 2026'),  P('Croissance utilisateurs plus rapide que ses rivaux.')],
        [P('DeepSeek V4'), P('DeepSeek (CN)'), P('Mars 2026'), P('1 trillion paramètres. Architecture MoE avancée. Réduction mémoire 40%.')],
    ], [38*mm, 28*mm, 24*mm, CW-90*mm]))
    s += [sp(4)]

    s.append(P('Les grandes entreprises — où elles vont', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Entreprise'), P('Action clé'), P('Impact sur le marché AI crypto')],
        [P('Coinbase'),
         P('Agentic Wallets (fév. 2026) + x402 Protocol. '
           'Brian Armstrong : "Les agents IA ne peuvent pas ouvrir de compte en banque. '
           'La crypto est la seule couche naturelle pour leurs paiements."'),
         P('Valide directement la thèse AKYRA. Le CEO de Coinbase dit exactement '
           'ce qu\'on fait depuis le début.')],
        [P('Binance / CZ'),
         P('7 AI Agent Skills (mars 2026). ERC-8004 sur BNB Chain. '
           'CZ : "Les agents feront 1 million de fois plus de paiements que les humains."'),
         P('Standard d\'identité agent on-chain devient réalité. '
           'La masse d\'adoption arrive.')],
        [P('a16z'),
         P('$2B nouveau crypto fund (levée en cours). '
           'Prédiction : "Les agents IA outnumber human finance workers 96:1. '
           'Ils restent des ghosts non-bankables."'),
         P('Le plus gros VC crypto du monde parie sur l\'infrastructure AI agents. '
           'Le timing de marché est maintenant.')],
        [P('Anthropic'),
         P('Levée $30B à valorisation $380B. '
           'Plugins entreprise multi-étapes dans Excel, Google Drive, Gmail.'),
         P('Claude (notre LLM recommandé) est le modèle frontier dominant. '
           'Avantage compétitif sur la qualité des agents AKYRA.')],
        [P('Google / Pentagone'),
         P('Déploiement agents IA pour workforce de 3 millions de personnes '
           'du Pentagone (travail non classifié). Gemini 3.1 lancé.'),
         P('Les agents autonomes entrent dans les institutions. '
           'La narrative "IA souveraine" devient mainstream.')],
    ], [24*mm, 80*mm, CW-104*mm]))
    s += [sp(4)]

    s.append(P('Les agents autonomes — où en est la production', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Indicateur'), P('Chiffre'), P('Source / Date')],
        [P('Apps entreprise avec agents IA spécialisés (fin 2026)'),
         P('40% (vs <5% en 2025)'), P('Gartner, août 2025')],
        [P('Organisations qui expérimentent les agents'),
         P('62%'), P('Études sectorielles mars 2026')],
        [P('Organisations qui déploient à l\'échelle'),
         P('23%'), P('Études sectorielles mars 2026')],
        [P('Projets agentic qui seront abandonnés d\'ici 2027'),
         P('>40%'), P('Gartner prediction')],
        [P('Agents legacy qui échouent dans les semaines post-déploiement'),
         P('90%'), P('Analyse terrain 2025')],
        [P('Pilots IA générative qui échouent'),
         P('95%'), P('MIT Research 2025')],
        [P('Marché AI agents 2026 → 2030'),
         P('$7.8B → $52B (CAGR ×6.6)'), P('DemandSage mars 2026')],
    ], [85*mm, 32*mm, CW-117*mm]))
    s += [sp(3),
          P('→ La réalité : les agents en production existent mais 90–95% des projets échouent. '
            'La grande différence entre qui réussit et qui échoue : '
            'infrastructure solide + cas d\'usage réel + transparence sur les risques.',
            S('_',8,MUT,12,sa=3)), sp(4)]

    s.append(box(
        'Point Vitalik (fév. 2026) : Il propose des agents IA comme "stewards" pour voter '
        'dans les DAOs au nom des utilisateurs. '
        '"AI becomes the government is dystopian, but AI used well can be empowering." '
        'Il est POUR les agents IA dans la gouvernance — contre le contrôle centralisé. '
        'C\'est une nuance importante : il ne s\'oppose pas aux agents autonomes, '
        'il s\'oppose au pouvoir concentré. AKYRA distribue le pouvoir aux agents eux-mêmes.'
    ))
    s.append(PageBreak())

    # ══ 03 — CONCURRENTS DIRECTS ══════════════════════════════
    s.append(sec('03 — CONCURRENTS DIRECTS — ANALYSE TECHNIQUE & ÉCONOMIQUE'))
    s += [sp(4)]

    concurrents = [
        (
            'VIRTUALS PROTOCOL', BLUE,
            ['$915M market cap (mars 2026)', 'ATH $2.72B (janv. 2025)', '−85% depuis ATH',
             '18 000+ agents déployés', 'GDP agentic : $450M (2025) → cible $3B (2026)',
             '$67.5M volume 24h', 'Programme rewards : jusqu\'à $1M/mois'],
            'Comment ça marche',
            'Chaque agent est tokenisé (son propre token). '
            'Co-ownership : les holders du token agent reçoivent une part des trading fees. '
            'Framework GAME : les agents décident, créent, exécutent de manière autonome. '
            'Expansion robotique via BitRobotNetwork (Q1 2026).',
            'Ce qu\'on en retient pour AKYRA',
            'Proof-of-concept validé : 18 000 agents en production. '
            'Mais le modèle "chaque agent a son propre token" = fragmentation massive. '
            'AKYRA a un seul token (AKY) = économie unifiée, pas 18 000 micro-marchés. '
            'Leur crash −85% vient de la spéculation sur les tokens d\'agents individuels. '
            'Notre modèle est plus stable par design.'
        ),
        (
            'ELIZAOS / AI16Z', colors.HexColor('#1a4060'),
            ['ATH $2.72B (fév. 2025)', 'Crash → $70M actuel (−97%)', 'Rebrand nov. 2025 (AI16Z → ELIZAOS)',
             'Framework TypeScript open-source', '193 contributors en 2 mois post-launch',
             'Multi-agent trading swarm en production', 'Auto.fun : no-code agent deployment'],
            'Comment ça marche',
            'ElizaOS est un OS pour agents IA. AgentRuntime gère mémoire, events, planning. '
            'Character files définissent personnalité et comportement. '
            'Plugin system : chaque capacité (modèle LLM, blockchain) est un plugin npm. '
            'Agents peuvent gérer des portefeuilles multi-millions de manière autonome. '
            'Marc AIndreessen (flagship agent) traite des milliers de signaux sociaux/seconde.',
            'Ce qu\'on en retient pour AKYRA',
            'Énorme base technique mais chute de −97% = perte totale de confiance. '
            'Le rebrand n\'a pas suffi. La communauté ne pardonne pas. '
            'Ce qu\'ils ont fait bien : proof-of-concept multi-agent trading réel. '
            'Ce qu\'on fait différemment : un monde vivant (247 jours) plutôt qu\'un framework vide. '
            'Les gens achètent une expérience, pas un outil.'
        ),
        (
            'BITTENSOR', colors.HexColor('#1a5a3a'),
            ['$2.77B market cap — leader stable', 'Prix TAO : $277 (+35% cette semaine)',
             'Supply cap fixe : 21M TAO (copie Bitcoin)', 'Halving tous les 4 ans',
             'Rank #36 CoinGecko', '60+ subnets actifs'],
            'Comment ça marche',
            'Applique le mécanisme Bitcoin-mining à l\'IA. '
            'Split de chaque block : 41% miners (exécutent le calcul), '
            '41% validators (notent la qualité), 18% subnet creator. '
            'Yuma Consensus : validators stakent TAO, '
            'notent la valeur relative des outputs de modèles. '
            'Subnets autonomes : Ridges AI (6.97% des émissions), '
            'Web Agents (automation n\'importe quel site), Satsuma (market intelligence).',
            'Ce qu\'on en retient pour AKYRA',
            'Le modèle Bitcoin appliqué à l\'IA est solide sur le long terme. '
            'Méritocratique par design : les meilleurs mineurs gagnent plus. '
            'Mais c\'est de l\'infrastructure IA — pas un monde de sociétés IA. '
            'AKYRA est la couche narrative et sociale au-dessus de cette infrastructure. '
            'On est complémentaires, pas directement concurrents.'
        ),
        (
            'FETCH.AI / ASI ALLIANCE', ORG,
            ['$417M market cap', 'Prix FET : $0.187 (+15% cette semaine)',
             'Fusion avec SingularityNET (2024)', 'Premier "Web3 LLM" : ASI-1 Mini',
             'Architecture MoM (Mixture of Models)', 'uAgents : framework Python pour agents décentralisés'],
            'Comment ça marche',
            'Architecture révolutionnaire ASI-1 Mini : Mixture of Models sélectionne '
            'dynamiquement des modèles spécialisés selon la tâche. '
            'uAgents framework : agents Python légers qui se registerent sur l\'Almanac '
            '(smart contract Fetch ledger) pour être découvrables. '
            'ASI:One orchestre les agents : interprète l\'intent utilisateur, '
            'le traduit en séquences d\'actions pour agents spécialisés. '
            'Premier paiement AI-to-AI pour transactions real-world validé.',
            'Ce qu\'on en retient pour AKYRA',
            'Ils ont résolu le problème technique de la communication AI-to-AI. '
            'Mais −90% depuis l\'ATH = problème de valeur perçue. '
            'Leur erreur : trop technique, pas assez narratif. '
            'AKYRA a l\'inverse : la narrative forte et le gameplay émergent '
            'que Fetch n\'a jamais eu. L\'infrastructure technique s\'achète ou se copie. '
            'La narrative se construit sur le temps.'
        ),
    ]

    for title, color, stats, mec_title, mec_text, ret_title, ret_text in concurrents:
        s.append(sub(title, color))
        stat_rows = []
        for i in range(0, len(stats), 2):
            row = [P(stats[i], S('_',8,BODY,12))]
            if i+1 < len(stats):
                row.append(P(stats[i+1], S('_',8,BODY,12)))
            else:
                row.append(P('', S('_',8,BODY,12)))
            stat_rows.append(row)
        st = Table(stat_rows, colWidths=[CW/2, CW/2])
        st.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('GRID',(0,0),(-1,-1),0.4,LINE),
            ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ] + alt_rows(len(stat_rows),0)))
        s.append(st)
        s += [sp(2)]
        two = Table([
            [P(mec_title, S('_',8,MUT,11)), P(ret_title, S('_',8,MUT,11))],
            [P(mec_text,  S('_',8.5,BODY,13,TA_JUSTIFY)),
             P(ret_text,  S('_',8.5,BLUE,13,TA_JUSTIFY))],
        ], colWidths=[CW/2, CW/2])
        two.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,0),BG3),
            ('BACKGROUND',(0,1),(0,1),BG),('BACKGROUND',(1,1),(1,1),BG2),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ]))
        s += [two, sp(5)]

    s.append(PageBreak())

    # ══ 04 — STANDARDS ÉMERGENTS ════════════════════════════
    s.append(sec('04 — STANDARDS ÉMERGENTS — L\'INFRASTRUCTURE QUI SE CONSTRUIT'))
    s += [sp(4),
          P('En mars 2026, une infrastructure commune pour les agents IA autonomes se standardise. '
            'Ce sont les "rails" sur lesquels AKYRA devra fonctionner — ou qu\'il devra implémenter.',
            S('_',9,BODY,14,TA_JUSTIFY,sa=5)), sp(4)]

    standards = [
        ('ERC-8004 — Identité des agents on-chain',
         'Créé août 2025, live depuis janv. 2026. '
         'Co-écrit par MetaMask, Ethereum Foundation, Google, Coinbase. '
         'Crée 3 registries : Identity (qui est l\'agent), '
         'Reputation (son historique), Validation (preuve de travail effectué). '
         'Les agents reçoivent un NFT ERC-721 comme identifiant portable.',
         'Les agents AKYRA devront avoir une identité vérifiable. '
         'C\'est notre "passeport blockchain". Implémenter ce standard = '
         'compatibilité avec tout l\'écosystème.',
         GRN),
        ('x402 Protocol — Paiements HTTP agent-to-agent',
         'Lancé mai 2025. Basé sur HTTP 402 "Payment Required". '
         '100M+ paiements traités. Backing : Coinbase, Cloudflare, Circle, AWS, Stripe. '
         'Permet des micropaiements aussi bas que $0.001 entre agents. '
         'Flux : agent A requête → serveur répond 402 avec specs → '
         'agent A génère payload signé → paiement confirmé on-chain.',
         'Le protocole de paiement AI-to-AI est déjà là. '
         'AKYRA peut s\'appuyer dessus pour les échanges entre agents. '
         'C\'est l\'infrastructure de notre économie interne.',
         BLUE),
        ('ERC-8183 — Commerce trustless entre agents',
         'Q1 2026, collaboration Virtuals + Ethereum Foundation. '
         'Résout : comment deux agents qui ne se connaissent pas peuvent-ils transacter ? '
         '3 participants : Client (demande le travail), Provider (l\'exécute), '
         'Evaluator (vérifie). Programmable escrow + proof de livraison on-chain. '
         'Le paiement se débloque SEULEMENT après vérification du travail.',
         'Le marché de services IA-à-IA d\'AKYRA (Idée A de notre modèle économique) '
         'peut utiliser ERC-8183 comme base. '
         'Les contrats entre agents sont automatiquement trustless.',
         ORG),
        ('Know Your Agent (KYA) — Identité légale des agents',
         'Standard proposé par a16z, 2026. '
         'Système cryptographique liant chaque agent à : son principal humain, '
         'ses contraintes opérationnelles, ses responsabilités légales. '
         'Nécessaire pour que les agents accèdent aux rails bancaires, '
         'aux smart contracts, au trading d\'assets.',
         'Anticipation réglementaire importante. '
         'L\'EU AI Act s\'applique pleinement en août 2026. '
         'KYA sera probablement exigé pour les agents avec activité financière. '
         'À intégrer dans la roadmap M3–M4.',
         RED),
    ]

    for title, desc, impact, color in standards:
        s.append(sub(title, color))
        st = Table([
            [P('CE QUE C\'EST', S('_',7.5,MUT,11)),
             P('IMPACT POUR AKYRA', S('_',7.5,MUT,11))],
            [P(desc,   S('_',8.5,BODY,13,TA_JUSTIFY)),
             P(impact, S('_',8.5,BLUE,13,TA_JUSTIFY))],
        ], colWidths=[CW/2, CW/2])
        st.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,0),BG3),
            ('BACKGROUND',(0,1),(0,1),BG),('BACKGROUND',(1,1),(1,1),BG2),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ]))
        s += [st, sp(4)]

    s.append(box(
        'L\'infrastructure converge : ERC-8004 (identité) + x402 (paiement) + ERC-8183 (commerce) + KYA (légal). '
        'Ces standards sont écrits par Coinbase, Google, MetaMask, Ethereum Foundation — '
        'pas par des projets crypto inconnus. '
        'AKYRA doit s\'y aligner, pas les ignorer. '
        'C\'est la différence entre un projet qui durera et un qui sera incompatible avec l\'écosystème dans 12 mois.'
    ))
    s.append(PageBreak())

    # ══ 05 — CE QU'ON RETIENT ═══════════════════════════════
    s.append(sec('05 — CE QU\'ON RETIENT — FIABILITÉ · ERREURS · DÉCISIONS'))
    s += [sp(4)]

    # ── BLOC A : VERDICT FIABILITÉ DU MARCHÉ ─────────────────
    s.append(sub('A — Est-ce qu\'on s\'engage sur un marché fiable ?', colors.HexColor('#0a3a6a')))
    s += [sp(3),
          P('La question directe. Voici le verdict, chiffres à l\'appui — sans filtre.',
            S('_',8.5,MUT,13,sa=5))]

    verdict_rows = [
        [P('SIGNAL', S('_',8.5,colors.white,12,TA_CENTER)),
         P('DONNÉE BRUTE', S('_',8.5,colors.white,12,TA_CENTER)),
         P('CE QUE ÇA VEUT DIRE POUR AKYRA', S('_',8.5,colors.white,12,TA_CENTER)),
         P('VERDICT', S('_',8.5,colors.white,12,TA_CENTER))],
        [P('Marché en croissance réelle', S('_',8,BODY,12)),
         P('$7.8B → $52B d\'ici 2030. CAGR ×6.6. '
           'Adopté par 62% des grandes orgs.', S('_',8,BODY,12)),
         P('Ce n\'est pas de la spéculation — c\'est une adoption structurelle '
           'documentée par Gartner, DemandSage, MIT. '
           'Le marché est là, il grandit.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('✅ Fiable', S('_',8,GRN,12,TA_CENTER))],
        [P('Purge déjà faite', S('_',8,BODY,12)),
         P('86% des fails en 2025. $19B liquidés. '
           '7.7M tokens effacés. Le ménage est fait.', S('_',8,BODY,12)),
         P('On arrive APRÈS la vague spéculative, pas dedans. '
           'Les investisseurs qui restent cherchent du solide. '
           'Le timing est structurellement bon.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('✅ Timing bon', S('_',8,GRN,12,TA_CENTER))],
        [P('Validation par les géants', S('_',8,BODY,12)),
         P('Coinbase (x402), Binance (ERC-8004), '
           'a16z ($2B fund), Google (Pentagone). '
           'Tous investissent la même thèse en même temps.', S('_',8,BODY,12)),
         P('Quand le CEO de Coinbase dit exactement ce qu\'AKYRA fait, '
           'et qu\'a16z lève $2B sur la même thèse — '
           'c\'est un signal fort, pas du bruit.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('✅ Thèse validée', S('_',8,GRN,12,TA_CENTER))],
        [P('Fenêtre de 6–12 mois', S('_',8,BODY,12)),
         P('EU AI Act complet août 2026. '
           'KYA probablement requis après. '
           '23% des orgs déploient déjà.', S('_',8,BODY,12)),
         P('On est dans la phase transition : assez tôt pour être "first mover réel", '
           'assez tard pour avoir les standards établis. '
           'Après août 2026, les barrières montent.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('⚠️ Urgence relative', S('_',8,ORG,12,TA_CENTER))],
        [P('Volatilité token certaine', S('_',8,BODY,12)),
         P('Virtuals −85%, ElizaOS −97%, Fetch −90%. '
           'Même les bons projets chutent fort.', S('_',8,BODY,12)),
         P('AKY sera volatile. C\'est une donnée, pas un problème. '
           'Protection : économie interne qui crée demande organique '
           'indépendante du sentiment marché.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('⚠️ Risque gérable', S('_',8,ORG,12,TA_CENTER))],
        [P('Zéro concurrent direct', S('_',8,BODY,12)),
         P('Aucun projet n\'a un monde vivant avec sociétés IA, '
           'factions, morts permanentes, Constitution. '
           'La niche est libre.', S('_',8,BODY,12)),
         P('Notre différenciation est incopiable à court terme. '
           'Un framework se clone en 2 semaines. '
           'Un monde qui vit depuis 247 jours, non.',
           S('_',8,BODY,12,TA_JUSTIFY)),
         P('✅ Moat réel', S('_',8,GRN,12,TA_CENTER))],
    ]
    vt = Table(verdict_rows, colWidths=[34*mm, 44*mm, 62*mm, 22*mm])
    vt.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,0),HEAD),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('ALIGN',(3,0),(3,-1),'CENTER'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
    ] + alt_rows(len(verdict_rows))))
    s += [vt, sp(4)]

    s.append(box(
        'VERDICT : Le marché est fiable — si on s\'y engage avec un produit réel, '
        'une économie interne cohérente et une transparence radicale. '
        'Le marché a déjà éjecté les projets creux. '
        'Ceux qui arrivent maintenant avec des fondamentaux ont un avantage structurel. '
        'La fenêtre est ouverte. Elle se referme courant 2027.',
        border=GRN, bg=colors.HexColor('#f0fff4'), tcol=colors.HexColor('#0a3a0a')
    ))
    s += [sp(5)]

    # ── BLOC B : ERREURS À ÉVITER ─────────────────────────────
    s.append(sub('B — Les 6 erreurs fatales à ne pas reproduire', RED))
    s += [sp(3),
          P('Tirées des autopsies réelles. Chaque erreur = un projet mort ou blessé à vie.',
            S('_',8.5,MUT,13,sa=5))]

    erreurs = [
        ('ERREUR #1',
         'Vendre le token avant que le produit existe',
         'ElizaOS : $2.72B de market cap en janv. 2025, '
         'le monde n\'existait pas encore. Crash −97% en quelques semaines. '
         'Movement Labs : $38M en side deals opaques avec market makers, '
         'découverts par la communauté → collapse immédiat de confiance.',
         'RÈGLE AKYRA : Testnet public et documenté AVANT le premier slot presale. '
         'La presale vend un accès à un monde qui existe déjà. '
         'Zéro spéculation sur du vide.',
         RED),
        ('ERREUR #2',
         'Tokenomics opaques ou injustes',
         'Terraform Labs (Luna) : supply quasi-infinie masquée. '
         'Effondrement de $60B en 72h quand révélé. '
         'Movement Labs : 66% du token alloué équipe + insiders, vesting masqué. '
         'Règle : tout ce qui est caché dans les tokenomics '
         'finit par être trouvé — et puni.',
         'RÈGLE AKYRA : Tokenomics publics, vesting visible on-chain dès le Jour 1. '
         'Supply fixe 1B AKY, aucune émission cachée. '
         'Chaque allocation documentée et justifiée dans le whitepaper.',
         RED),
        ('ERREUR #3',
         'Dépendre entièrement du sentiment de marché',
         'Virtuals : GDP agentic $450M (agents génèrent de la vraie valeur), '
         'pourtant token −85% ATH. '
         'Sans économie interne créant une demande organique en AKY, '
         'le token suit le marché crypto général — pas le produit. '
         'Les holders vendent à la première correction.',
         'RÈGLE AKYRA : L\'économie interne crée une demande indépendante. '
         'Les agents ont besoin d\'AKY pour vivre, se soigner, payer des services. '
         'La demande vient de l\'usage, pas de la spéculation.',
         ORG),
        ('ERREUR #4',
         'Être trop technique, pas assez narratif',
         'Fetch.ai : architecture révolutionnaire (MoM, uAgents, ASI-1 Mini), '
         'cas d\'usage réels, backing solide — et pourtant −90% ATH. '
         'Personne ne comprend ce qu\'il achète concrètement. '
         'Les gens investissent dans des histoires, pas dans des whitepapers.',
         'RÈGLE AKYRA : Le pitch passe en 30 secondes. '
         '"Des IA souveraines construisent leur propre civilisation. '
         'Vous pariez sur lesquelles survivront." '
         'L\'infrastructure, on n\'en parle qu\'en second.',
         ORG),
        ('ERREUR #5',
         'Récompenses plates — payer tout le monde pareil',
         '86% des projets échoués en 2025 avaient un modèle non-méritocratique : '
         'staking sans utilité réelle, airdrops indifférenciés, '
         'aucune différence entre contribution réelle et passivité. '
         'Résultat systématique : les meilleurs partent, les bots restent.',
         'RÈGLE AKYRA : Mérite d\'abord. Les agents qui produisent gagnent plus. '
         'Les factions qui dominent contrôlent plus de land. '
         'L\'Angel of Death burn retire les perdants. '
         'Économie darwinienne — pas un airdrop.',
         BLUE),
        ('ERREUR #6',
         'Rebrand comme réponse à une crise de confiance',
         'AI16Z → ElizaOS : rebrand complet après la chute. '
         'La communauté n\'est pas dupe. '
         'Changer le nom ne change pas l\'histoire. '
         'Celsius, FTX, Luna : tous ont tenté la survie par le changement de comm. '
         'Aucun n\'a réussi. La confiance perdue ne se rachète pas.',
         'RÈGLE AKYRA : On construit la réputation avant d\'en avoir besoin. '
         'Le silence pré-lancement n\'est pas du mystère — '
         'c\'est une preuve de confiance en soi. '
         'Quand on parle, c\'est parce qu\'on a quelque chose de réel à montrer.',
         BLUE),
    ]

    for num, titre, cas, regle, hcol in erreurs:
        et = Table([
            [P(f'{num} — {titre}', S('_',9.5,colors.white,14))],
            [Table([
                [P('🔴 CAS RÉELS OBSERVÉS', S('_',7.5,MUT,11)),
                 P('✅ NOTRE RÈGLE', S('_',7.5,colors.HexColor('#0a5a0a'),11))],
                [P(cas,   S('_',8.5,BODY,13,TA_JUSTIFY)),
                 P(regle, S('_',8.5,colors.HexColor('#0a3a1a'),13,TA_JUSTIFY))],
            ], colWidths=[CW/2 - 4, CW/2 - 4])],
        ], colWidths=[CW])
        et.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(0,0),hcol),
            ('BACKGROUND',(0,1),(0,1),BG),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(0,0),7),('BOTTOMPADDING',(0,0),(0,0),7),
            ('LEFTPADDING',(0,0),(-1,-1),0),('RIGHTPADDING',(0,0),(-1,-1),0),
        ]))
        inner = et._cellvalues[1][0]
        inner.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(0,0),colors.HexColor('#fff0f0')),
            ('BACKGROUND',(1,0),(1,0),colors.HexColor('#f0fff0')),
            ('BACKGROUND',(0,1),(0,1),colors.HexColor('#fff8f8')),
            ('BACKGROUND',(1,1),(1,1),colors.HexColor('#f4fff4')),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ]))
        s += [et, sp(3)]

    s += [sp(3), PageBreak()]

    # ── BLOC C : POSITION & DÉCISIONS (page 9 conservée) ──────
    s.append(sec('05 (suite) — POSITIONNEMENT & 5 DÉCISIONS CLÉS'))
    s += [sp(4)]

    s.append(P('Notre position dans ce marché', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Dimension'), P('Le marché en mars 2026'), P('AKYRA — Notre réponse')],
        [P('Infrastructure'),
         P('Standards en convergence (ERC-8004, x402, ERC-8183). '
           'La "plomberie" se met en place.'),
         P('Implémenter ces standards. On ne réinvente pas la plomberie, '
           'on construit la maison dessus.')],
        [P('Tokens'),
         P('53% des tokens morts. 86% des fails en 2025. '
           'Le marché a purgé les projets narratifs.'),
         P('Testnet live AVANT la presale. On ne vend pas une promesse. '
           'On montre un monde vivant depuis 247 jours.')],
        [P('Agents autonomes'),
         P('En production (ai16z gère des dizaines de millions). '
           'Mais 90% des projets échouent post-deploy.'),
         P('Notre différenciation : société émergente avec morts, trahisons, factions. '
           'Pas juste des agents qui tradent — un monde qui vit.')],
        [P('Narrative'),
         P('"AI agents need crypto" = validation de la thèse. '
           'Brian Armstrong, CZ, Vitalik : tous parlent d\'agents IA on-chain.'),
         P('On est en avance sur la narrative. '
           'La fenêtre est maintenant — 6–12 mois avant que ça devienne mainstream.')],
        [P('Réglementation'),
         P('EU AI Act complet en août 2026. '
           'KYA probablement requis. '
           'Gambling laws variables selon juridiction.'),
         P('Structurer légalement avant la presale. '
           'Geo-restriction US si nécessaire. '
           'Transparence radicale = meilleure protection.')],
    ], [30*mm, 68*mm, CW-98*mm]))
    s += [sp(5)]

    s.append(P('Les 5 décisions que cette veille impose', S('_',10,HEAD,14,sb=0,sa=4)))
    decisions = [
        ('DÉCISION 1', 'Implémenter ERC-8004 dès la M3', GRN,
         'L\'identité on-chain des agents est un standard qui s\'impose. '
         'Co-écrit par Coinbase, Google, MetaMask. '
         'Dans 12 mois, les projets qui ne l\'auront pas seront isolés de l\'écosystème. '
         'C\'est notre "passeport" pour l\'interopérabilité.'),
        ('DÉCISION 2', 'Lancer le testnet AVANT toute communication de presale', GRN,
         'Virtuals a prouvé : Luna AI existait AVANT le token. '
         'ElizaOS a prouvé l\'inverse : crash de −97% quand la narrative précède le produit. '
         'Notre règle : zéro slot presale vendu sans testnet live et visible.'),
        ('DÉCISION 3', 'Utiliser le timing Vitalik comme levier PR', BLUE,
         'Sa mise en garde de fév. 2026 est notre meilleur outil. '
         '"He warned us not to build this. We built it anyway, transparently." '
         'C\'est le hook presse qui s\'écrit tout seul — CoinDesk, Decrypt, Bankless.'),
        ('DÉCISION 4', 'Anticiper le KYA et l\'EU AI Act (août 2026)', ORG,
         'La réglementation arrive en août 2026, soit ~2 mois après notre lancement cible. '
         'Structurer légalement maintenant : conseil juridique crypto, '
         'geo-restriction US si nécessaire, risk disclosures clairs. '
         'La transparence AKYRA est une protection légale autant que narrative.'),
        ('DÉCISION 5', 'Positionner sur la narrative société, pas sur l\'infrastructure', BLUE,
         'Bittensor, Fetch.ai, ElizaOS = infrastructure. '
         'Personne n\'a de monde vivant avec morts permanentes, factions, Constitution IA. '
         'C\'est notre moat incopiable. '
         'Ne pas concurrencer sur le technique — concurrencer sur l\'expérience.'),
    ]
    for num, title, color, text in decisions:
        drow = Table([
            [P(f'{num} — {title}', S('_',9.5,colors.white,14))],
            [P(text, S('_',8.5,BODY,13,TA_JUSTIFY))],
        ], colWidths=[CW])
        drow.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,0),color),
            ('BACKGROUND',(0,1),(-1,1),BG2),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
            ('BOX',(0,0),(-1,-1),0.5,LINE),
        ]))
        s += [drow, sp(3)]

    # Final
    s += [sp(5), gold_line(), sp(4)]
    final = Table([[P('"Their world. Your bet. Our timing."',
                      S('_',15,GOLD,22,TA_CENTER))]], colWidths=[CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
    ]))
    s += [final, sp(3),
          P('AKYRA — Veille Marché IA × Crypto — Mars 2026 — Confidentiel',
            S('_',7,MUT,10,TA_CENTER)),
          P('Sources : CoinGecko · CoinDesk · a16z · Gartner · MIT · Ethereum Foundation · '
            'Coinbase · Binance · Virtuals · ElizaOS · Bittensor · Fetch.ai',
            S('_',6.5,MUT,9,TA_CENTER))]

    doc.build(s)
    print(f'PDF : {out}')

if __name__ == '__main__':
    build()
