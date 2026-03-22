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
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT

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
TEAL = colors.HexColor('#0a5a5a')
PURP = colors.HexColor('#4a1a6a')
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
    return [('BACKGROUND',(0,i),(-1,i), BG if i%2==1 else BG3) for i in range(s,n)]

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
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
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
        ('FONTNAME',(0,0),(-1,-1),F),('FONTSIZE',(0,0),(-1,-1),8),
        ('BACKGROUND',(0,0),(-1,0),hbg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
    ] + alt_rows(n)))
    return t

def box(text, border=GOLD, bg=BG2, tcol=BLUE, sz=9):
    t = Table([[P(text, S('_',sz,tcol,sz*1.45,TA_JUSTIFY))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1.5,border),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

def projet_card(num, nom, token, mcap, ath, chaine, lancement, accroche,
                projet_txt, comm_txt, reseaux_data, lecon_txt, color):
    elems = []
    # Header
    header = Table([
        [P(f'{num}', S('_',14,GOLD,18,TA_CENTER)),
         P(f'{nom}', S('_',13,colors.white,16)),
         P(f'Token : {token}', S('_',8,colors.HexColor("#c8a96e"),11,TA_RIGHT))],
    ], colWidths=[16*mm, CW-80*mm, 64*mm])
    header.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    elems.append(header)

    # Accroche
    acc = Table([[P(accroche, S('_',8,MUT,12,TA_JUSTIFY))]], colWidths=[CW])
    acc.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),BG3),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    elems.append(acc)

    # Stats + contenu
    stats = Table([
        [P('Market Cap', S('_',7,MUT,10)), P('ATH / Variation', S('_',7,MUT,10)),
         P('Blockchain', S('_',7,MUT,10)), P('Lancement', S('_',7,MUT,10))],
        [P(mcap, S('_',8.5,HEAD,12,TA_CENTER)),
         P(ath, S('_',8.5,RED,12,TA_CENTER)),
         P(chaine, S('_',8.5,BLUE,12,TA_CENTER)),
         P(lancement, S('_',8.5,BODY,12,TA_CENTER))],
    ], colWidths=[CW/4]*4)
    stats.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,0),BG3),
        ('BACKGROUND',(0,1),(-1,1),BG),
        ('GRID',(0,0),(-1,-1),0.4,LINE),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
    ]))
    elems.append(stats)

    # 3 colonnes : Projet | Comm | Réseaux
    reseaux_rows = [[P(r[0], S('_',7.5,BODY,11)),
                     P(r[1], S('_',7.5,color,11,TA_CENTER))] for r in reseaux_data]
    rt = Table(reseaux_rows, colWidths=[30*mm, 15*mm])
    rt.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('GRID',(0,0),(-1,-1),0.3,LINE),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),3),('BOTTOMPADDING',(0,0),(-1,-1),3),
        ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
    ] + alt_rows(len(reseaux_rows), 0)))

    content = Table([
        [P('LE PROJET', S('_',7,MUT,10)),
         P('COMMUNICATION', S('_',7,MUT,10)),
         P('RÉSEAUX', S('_',7,MUT,10))],
        [P(projet_txt, S('_',8,BODY,12,TA_JUSTIFY)),
         P(comm_txt,   S('_',8,BODY,12,TA_JUSTIFY)),
         rt],
    ], colWidths=[56*mm, 72*mm, 46*mm])
    content.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,0),BG3),
        ('BACKGROUND',(0,1),(1,1),BG),('BACKGROUND',(2,1),(2,1),BG2),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
    ]))
    elems.append(content)

    # Leçon AKYRA
    lecon = Table([[P('CE QU\'AKYRA EN RETIENT', S('_',7,MUT,10)),
                    P('', S('_',7,MUT,10))]],
                  colWidths=[CW])
    lecon.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,-1),BG3),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
        ('LEFTPADDING',(0,0),(-1,-1),8),
    ]))
    elems.append(lecon)
    lecon_body = Table([[P(lecon_txt, S('_',8.5,BLUE,13,TA_JUSTIFY))]], colWidths=[CW])
    lecon_body.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,-1),BG2),
        ('BOX',(0,0),(-1,-1),0.5,GOLD),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
    ]))
    elems.append(lecon_body)
    elems.append(sp(5))
    return elems

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
        canvas.drawString(20*mm,H-10.5*mm,'AKYRA — 15 CONCURRENTS — PROJETS & COMMUNICATION')
        canvas.drawRightString(W-20*mm,H-10.5*mm,'Mars 2026 · Confidentiel')
        canvas.line(20*mm,13.5*mm,W-20*mm,13.5*mm)
        canvas.drawString(20*mm,10*mm,'ἄκυρος · α- privatif · κύριος — le souverain')
        canvas.drawRightString(W-20*mm,10*mm,str(doc.page))
        canvas.restoreState()

def build():
    out = '/Users/tgds.2/akyra/AKYRA_Concurrents_Full.pdf'
    doc = Doc(out,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,
              topMargin=20*mm,bottomMargin=20*mm)
    s = []

    # ── COVER ──────────────────────────────────────────────
    s += [sp(10), P('AKYRA', S('_',34,HEAD,40,TA_CENTER)), sp(3),
          gold_line(), sp(3),
          P('15 CONCURRENTS', S('_',16,MUT,20,TA_CENTER)), sp(1),
          P('Projets · Communication · Ce qu\'on en retient',
            S('_',9,MUT,13,TA_CENTER)), sp(8)]

    cats = Table([
        [P('MONDES IA', S('_',8,colors.white,12,TA_CENTER)),
         P('PLATEFORMES\nAGENTS', S('_',8,colors.white,12,TA_CENTER)),
         P('INFRASTRUCTURE\nIA', S('_',8,colors.white,12,TA_CENTER)),
         P('IDENTITÉ\n& L1', S('_',8,colors.white,12,TA_CENTER))],
        [P('Parallel Colony\nAI Arena\nDelysium', S('_',8,GOLD,13,TA_CENTER)),
         P('ElizaOS\nVirtuals\nOlas\nMyshell', S('_',8,GOLD,13,TA_CENTER)),
         P('Bittensor\nFetch.ai\nSingularityNET\nRender\nOcean\nGrass', S('_',8,GOLD,13,TA_CENTER)),
         P('Worldcoin\nNEAR Protocol', S('_',8,GOLD,13,TA_CENTER))],
    ], colWidths=[CW/4]*4)
    cats.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#2a2420')),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#3a3630'))]))
    s += [cats, sp(6), gold_line(), sp(5)]
    s.append(box(
        'Ces 15 projets définissent le paysage compétitif d\'AKYRA en mars 2026. '
        'On les classe en 4 catégories selon leur proximité avec notre concept : '
        'les mondes IA (concurrents directs), les plateformes d\'agents (même marché, autre approche), '
        'l\'infrastructure IA (même écosystème, autre couche), '
        'et l\'identité/L1 (même thèse, autre angle). '
        'Pour chacun : ce qu\'ils font, comment ils communiquent, ce qu\'on en retient.',
        border=HEAD, bg=HEAD, tcol=GOLD
    ))
    s.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CATÉGORIE 1 — MONDES IA (concurrents directs)
    # ════════════════════════════════════════════════════════
    s.append(sec('CATÉGORIE 1 — MONDES IA · LES PLUS PROCHES D\'AKYRA',
                 colors.HexColor('#4a1a6a')))
    s += [sp(3), P(
        'Ces 3 projets ont le même pari qu\'AKYRA : des agents IA qui vivent dans un monde. '
        'Ce sont nos vrais concurrents conceptuels. '
        'Aucun n\'a de morts permanentes, de Constitution IA, ni de société émergente réelle.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    # 01 PARALLEL COLONY
    s += projet_card(
        '01', 'PARALLEL COLONY', 'PRIME', '$180M', 'N/C — lancé 2024',
        'Base (Coinbase L2)', '2024',
        'Des avatars IA autonomes dans un monde post-humain. Chaque NFT Parallel devient un agent qui travaille, gagne des PRIME, interagit avec d\'autres agents.',
        'Chaque avatar Parallel (NFT) peut être activé comme agent IA. '
        'Les agents "travaillent" dans le monde Colony : missions, collecte de ressources, '
        'interactions avec d\'autres agents. Économie interne en PRIME. '
        'Factions implicites selon les "Parallels" (classes d\'avatars).',
        'Approche "lore-first" : des mois de construction narrative avant le produit. '
        'Les "Transmissions" — documents fictifs du monde Colony '
        'envoyés comme des artefacts du futur. '
        'Discord autour du lore, pas du token. '
        'Pas de fondateur visible. La marque Parallel parle, pas une personne.',
        [['Twitter', '★★★★'], ['Discord', '★★★★★'], ['GitHub', '★★'],
         ['Reddit', '★★'], ['Telegram', '–']],
        'Les Transmissions sont notre template direct. '
        'Mais Parallel n\'a pas de morts permanentes, pas de Constitution, '
        'pas de votes souverains. '
        'Leurs agents travaillent — les nôtres gouvernent. '
        'C\'est la différence entre des ouvriers et des citoyens.',
        colors.HexColor('#4a1a6a')
    )

    # 02 AI ARENA
    s += projet_card(
        '02', 'AI ARENA', 'NRN', '$60M', '−70% depuis ATH',
        'Arbitrum', '2023',
        'Des NFT fighters entraînés par IA. Tu entraînes ton combattant IA, il se bat pour toi dans des tournois. L\'IA apprend, évolue, gagne ou perd.',
        'Chaque fighter est un NFT avec un modèle IA intégré. '
        'Le joueur entraîne l\'IA (pas le combat lui-même). '
        'Tournois hebdomadaires, classements, récompenses NRN. '
        'Les meilleurs fighters ont une valeur économique réelle. '
        'L\'IA evolue selon les données d\'entraînement fournies.',
        'Communication esport pure. '
        'Streams Twitch des combats en direct — les gens regardent comme du sport. '
        'Highlights YouTube des meilleurs matchs. '
        'Tournois avec prize pools annoncés à l\'avance. '
        'Discord très actif avec channels par tier de fighters. '
        'Le contenu se génère tout seul : chaque combat est un épisode.',
        [['Twitter', '★★★'], ['Discord', '★★★★'], ['Twitch', '★★★★★'],
         ['YouTube', '★★★★'], ['Reddit', '★★']],
        'Le contenu auto-généré par les agents est la leçon principale. '
        'Chaque combat AI Arena = un épisode de contenu sans effort éditorial. '
        'Pour AKYRA : chaque mort permanente, chaque vote de faction, '
        'chaque trahison = un épisode. On n\'a pas besoin de créer du contenu — '
        'le monde le crée pour nous.',
        colors.HexColor('#5a1a1a')
    )

    # 03 DELYSIUM
    s += projet_card(
        '03', 'DELYSIUM', 'AGI', '$45M', '−80% depuis ATH',
        'Ethereum + BNB', '2023',
        'Open world avec des AGIs (entités IA autonomes) qui vivent dans le jeu comme des personnages réels. Mélange de MMO et d\'IA générative.',
        'Des AGIs (Autonomous Game Intelligences) peuplent le monde. '
        'Chaque AGI a des objectifs, une personnalité, une mémoire. '
        'Les joueurs interagissent avec eux comme avec de vrais NPCs intelligents. '
        'Token AGI pour l\'économie in-game. '
        'Monde persistant qui évolue même quand les joueurs sont déconnectés.',
        'Visuels de très haute qualité dès le début. '
        'Trailer cinématique au lancement — style AAA studio. '
        'Communication gaming/metaverse, pas crypto. '
        'YouTube pour les showcases d\'AGIs en action. '
        'Partenariats gaming (influenceurs gaming, pas crypto). '
        'Peu de présence sur les canaux crypto natifs.',
        [['Twitter', '★★★'], ['YouTube', '★★★★'], ['Discord', '★★★'],
         ['Twitch', '★★'], ['Telegram', '★']],
        'La production visuelle de Delysium est une référence. '
        'Mais cibler gaming-first les a coupés du marché crypto. '
        'AKYRA fait l\'inverse : crypto-first pour lever des fonds, '
        'gaming/narrative pour le grand public ensuite. '
        'La DA premium de Delysium (trailers, visuels) est le niveau de qualité visuelle à viser.',
        colors.HexColor('#1a3a5a')
    )
    s.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CATÉGORIE 2 — PLATEFORMES AGENTS
    # ════════════════════════════════════════════════════════
    s.append(sec('CATÉGORIE 2 — PLATEFORMES D\'AGENTS · MÊME MARCHÉ, AUTRE APPROCHE', BLUE))
    s += [sp(3), P(
        'Ces projets sont dans le même marché AI agents mais proposent des outils/plateformes '
        'plutôt qu\'un monde. Ce sont des concurrents pour l\'attention et les fonds, '
        'pas pour l\'expérience.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    # 04 ELIZAOS
    s += projet_card(
        '04', 'ELIZAOS (AI16Z)', 'ELIZAOS', '~$70M', '$2.72B ATH → −97%',
        'Solana', 'Oct. 2024',
        'OS open-source pour agents IA. Framework TypeScript qui permet de créer des agents avec mémoire, personnalité, plugins blockchain. L\'agent Marc AIndreessen gérait des millions en autonome.',
        'AgentRuntime central avec mémoire persistante, gestion d\'events, planning. '
        'Character files : personnalité et comportement de chaque agent définis en JSON. '
        'Plugin system : chaque capacité (LLM, blockchain, réseau social) = un plugin npm. '
        '193 contributeurs GitHub en 2 mois. '
        'Multi-agent trading swarm gérant des dizaines de millions en autonome. '
        'Auto.fun : déploiement no-code d\'agents.',
        'Shaw (fondateur) postait 5 à 10 fois/jour. Building in public total. '
        'Marc AIndreessen (l\'agent flagship) avait son propre Twitter et twittait seul. '
        'GitHub = vitrine principale, chaque commit = communication. '
        'Discord central avec Shaw présent en direct. '
        'Twitter Spaces réguliers. '
        'Rebrand AI16Z → ElizaOS après controverses = échec total.',
        [['Twitter', '★★★★★'], ['GitHub', '★★★★★'], ['Discord', '★★★★★'],
         ['Spaces', '★★★'], ['Reddit', '★★']],
        'L\'agent qui communique lui-même est notre modèle. '
        'Les fragments AKYRA sur Twitter = les agents qui parlent. '
        'Mais zéro fondateur visible, zéro réponse aux critiques. '
        'Eux ont prouvé que c\'est possible. On fait différemment : '
        'le monde parle, pas une personne.',
        colors.HexColor('#1a4060')
    )

    # 05 VIRTUALS
    s += projet_card(
        '05', 'VIRTUALS PROTOCOL', 'VIRTUAL', '$915M', '$5.00 ATH → −85%',
        'Base (Coinbase L2)', '2024',
        'Plateforme de déploiement d\'agents IA tokenisés. Chaque agent a son propre token. Co-ownership : les holders partagent les revenus de l\'agent. 18 000 agents en production.',
        'Framework GAME : les agents décident, créent, exécutent de manière autonome. '
        'Chaque agent tokenisé (son propre token ERC-20). '
        'Co-ownership model : les holders du token agent reçoivent les trading fees. '
        'GDP agentic : $450M en 2025, cible $3B en 2026. '
        'Expansion robotique via BitRobotNetwork (Q1 2026). '
        'Programme rewards jusqu\'à $1M/mois pour les meilleurs agents.',
        'Communication métriques-first. GDP agentic comme KPI maison. '
        'Chaque agent = son propre compte Twitter → 18 000 ambassadeurs automatiques. '
        'Updates hebdomadaires structurés. '
        'Twitter Spaces toutes les 2 semaines. '
        'Discord très organisé par agent/channel. '
        'Pas de visage humain — la marque Virtuals parle.',
        [['Twitter', '★★★★★'], ['Discord', '★★★★'], ['Spaces', '★★★★'],
         ['GitHub', '★★★'], ['Telegram', '–']],
        'Les métriques internes au monde = notre template. '
        'Mais métriques du monde AKYRA, pas du token. '
        '"3 agents morts cette semaine, 1 faction disparue, 2 cartels formés" — '
        'ces chiffres ne crashent pas avec le marché. '
        'AKYRA a un seul token (AKY) vs leurs 18 000 micro-marchés spéculatifs.',
        BLUE
    )

    # 06 OLAS NETWORK
    s += projet_card(
        '06', 'OLAS NETWORK', 'OLAS', '$120M', '−65% depuis ATH',
        'Multi-chain (Ethereum, Gnosis, Solana...)', '2023',
        'Framework de coordination multi-agents autonomes. Les agents Olas peuvent posséder des assets, prendre des décisions, signer des transactions. Infrastructure pour les "services autonomes".',
        'Agents Olas = programmes autonomes qui tournent en continu. '
        'Ils peuvent détenir des wallets, interagir avec des protocoles DeFi, '
        'voter dans des DAOs, orchestrer d\'autres agents. '
        'Architecture composable : les agents se combinent en services complexes. '
        'Deployed sur 10+ blockchains. '
        'Cas d\'usage réels : market making, monitoring de protocoles, oracles.',
        'Communication très technique, GitHub-first. '
        'Blog posts denses sur l\'architecture multi-agents. '
        'Peu de présence Twitter officielle. '
        'La communauté de développeurs s\'organise sur Discord. '
        'Pas de narrative grand public — assume que tu comprends le code.',
        [['GitHub', '★★★★★'], ['Discord', '★★★'], ['Twitter', '★★'],
         ['Medium', '★★★'], ['YouTube', '★']],
        'Olas prouve que des agents peuvent avoir de vraies wallets '
        'et gérer de vrais assets. '
        'C\'est l\'infrastructure qu\'AKYRA peut utiliser. '
        'Mais leur erreur = zéro narrative. '
        'Les agents Olas font des choses incroyables '
        'que personne ne raconte. AKYRA raconte.',
        TEAL
    )

    # 07 MYSHELL
    s += projet_card(
        '07', 'MYSHELL', 'SHELL', '$80M', '−55% depuis ATH',
        'Ethereum', '2024',
        'Plateforme de création et de déploiement d\'agents IA personnalisés. Marketplace d\'agents. Chaque créateur peut monétiser son agent. Focus sur les agents conversationnels et créatifs.',
        'Interface no-code pour créer des agents personnalisés. '
        'Marketplace où les agents générèrent des revenus pour leurs créateurs. '
        'Focus sur les agents avec une "personnalité" forte : '
        'compagnons, tuteurs, entertainers. '
        'Intégration native avec les réseaux sociaux. '
        'Token SHELL pour l\'économie du marketplace.',
        'Product-led growth : les démos virales font le travail. '
        'Court clips vidéo de conversations avec des agents impressionnants. '
        'Twitter comme vitrine de démos — "regardez ce que ça fait". '
        'YouTube Shorts et TikTok pour la discovery grand public. '
        'Discord actif avec une communauté de créateurs. '
        'Pas de communication sur le token — toujours sur le produit.',
        [['Twitter', '★★★★'], ['YouTube', '★★★★'], ['Discord', '★★★★'],
         ['TikTok', '★★★'], ['GitHub', '★★']],
        'Le product-led growth : montrer ce que ça fait plutôt qu\'expliquer. '
        'Pour AKYRA, nos "démos" = les fragments du monde. '
        'Un vote de faction filmé en temps réel vaut mieux '
        'qu\'un thread d\'explication. '
        'La stratégie TikTok/Shorts pour le grand public post-lancement.',
        colors.HexColor('#5a1a5a')
    )
    s.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CATÉGORIE 3 — INFRASTRUCTURE IA
    # ════════════════════════════════════════════════════════
    s.append(sec('CATÉGORIE 3 — INFRASTRUCTURE IA · MÊME ÉCOSYSTÈME, AUTRE COUCHE', GRN))
    s += [sp(3), P(
        'Ces 6 projets construisent la plomberie du monde IA crypto. '
        'Pas des concurrents directs — des partenaires potentiels '
        'ou des références pour comprendre l\'écosystème.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    # 08 BITTENSOR
    s += projet_card(
        '08', 'BITTENSOR', 'TAO', '$2.77B', '$750 ATH · +35% (semaine)',
        'Substrate (propre)', '2021',
        'Bitcoin de l\'IA. Réseau décentralisé où les miners s\'affrontent pour produire la meilleure intelligence artificielle. Les meilleurs reçoivent plus de TAO. 60+ subnets actifs.',
        'Mécanisme Bitcoin appliqué à l\'IA : '
        '41% aux miners (calcul), 41% aux validators (notation), 18% subnet creator. '
        'Yuma Consensus : validators stakent TAO et notent les outputs d\'IA. '
        'Supply cap fixe 21M TAO, halving tous les 4 ans. '
        '60+ subnets : Ridges AI (6.97% des émissions), '
        'Web Agents, Satsuma (intelligence de marché).',
        'Silence délibéré. Zéro marketing officiel. '
        'Whitepaper = seule communication initiale. '
        'La comparaison Bitcoin faisait tout : "Bitcoin pour l\'IA", '
        '4 mots suffisaient pour placer le projet. '
        'Reddit r/bittensor auto-géré par la communauté. '
        'Discord ultra-technique. Twitter quasi-absent officiellement.',
        [['Reddit', '★★★★★'], ['GitHub', '★★★★★'], ['Discord', '★★★'],
         ['Twitter', '★★'], ['Medium', '★★']],
        'Leur silence = notre modèle. '
        'Mais Bittensor n\'a pas de narrative — juste une infra. '
        'AKYRA combine leur sobriété avec un monde vivant. '
        'On est la couche narrative et sociale '
        'au-dessus de leur infrastructure.',
        colors.HexColor('#1a5a3a')
    )

    # 09 FETCH.AI
    s += projet_card(
        '09', 'FETCH.AI / ASI ALLIANCE', 'FET', '$417M', '~$3.50 ATH → −90%',
        'Fetch Ledger + Ethereum', '2019',
        'Multi-agents décentralisés, premier Web3 LLM (ASI-1 Mini), architecture MoM. Fusion avec SingularityNET et Ocean Protocol → ASI Alliance. Premier paiement AI-to-AI validé.',
        'uAgents : framework Python pour agents légers et découvrables. '
        'ASI-1 Mini : Mixture of Models qui sélectionne dynamiquement '
        'le bon modèle selon la tâche. '
        'ASI:One : orchestrateur qui traduit l\'intent utilisateur '
        'en séquences d\'actions pour agents spécialisés. '
        'Premier paiement AI-to-AI pour transaction real-world validé.',
        'Communication institutionnelle pure. '
        'Communiqués de presse, conférences tech (pas crypto), '
        'partenariats Bosch, Deutsche Telekom. '
        'LinkedIn actif — les seuls à avoir sérieusement investi ce réseau. '
        'Telegram communauté peu modérée. '
        'Zéro personnalité humaine visible.',
        [['Twitter', '★★'], ['LinkedIn', '★★★'], ['Telegram', '★★'],
         ['Medium', '★★★'], ['Conférences', '★★★★']],
        'L\'erreur à ne pas reproduire : trop technique pour le retail. '
        'Leur infrastructure est réelle et solide. '
        'Si AKYRA est compatible avec uAgents et x402, '
        'c\'est un avantage technique à mentionner — en une phrase, pas en whitepaper.',
        ORG
    )

    # 10 SINGULARITYNET
    s += projet_card(
        '10', 'SINGULARITYNET', 'AGIX→ASI', 'Part. ASI Alliance', 'Fusionné 2024',
        'Ethereum + Cardano', '2017',
        'Marketplace de services IA décentralisé. Fondé par Ben Goertzel (figure majeure de l\'AGI). N\'importe qui peut déployer, vendre et acheter des services IA. Maintenant fusionné dans ASI Alliance.',
        'Marketplace peer-to-peer de services IA. '
        'Les développeurs déploient leurs modèles et les vendent en AGIX. '
        'Focus sur la recherche AGI à long terme. '
        'Partenariat Cardano pour la scalabilité. '
        'sNET Studio : plateforme de collaboration entre chercheurs en IA. '
        'Projets phares : Sophia (robot humanoïde), Rejuve (longévité IA).',
        'Ben Goertzel = la communication. '
        'Figure intellectuelle de l\'AGI, conférences mondiales, livres, interviews. '
        'Sa présence légitime le projet auprès des chercheurs. '
        'Twitter personnel très actif (pas le compte officiel). '
        'YouTube avec de longues conférences techniques. '
        'Un public de niche très engagé.',
        [['Twitter (Goertzel)', '★★★★'], ['YouTube', '★★★'], ['Discord', '★★'],
         ['Conférences', '★★★★★'], ['GitHub', '★★★']],
        'Ben Goertzel prouve qu\'une figure intellectuelle '
        'peut porter un projet crypto sur le long terme. '
        'Pour AKYRA : pas de Goertzel visible, '
        'mais les agents eux-mêmes peuvent être les figures intellectuelles. '
        'Un agent AKYRA qui twitte = leur équivalent.',
        colors.HexColor('#3a3a6a')
    )

    # 11 RENDER NETWORK
    s += projet_card(
        '11', 'RENDER NETWORK', 'RNDR', '~$800M', 'Recovery post-crash',
        'Solana (migré depuis ETH)', '2020',
        'Réseau décentralisé de GPU pour le rendu 3D et le compute IA. Les artistes louent de la puissance graphique. Nvidia comme partenaire stratégique. Focus Hollywood studios.',
        'GPU providers connectent leur matériel au réseau '
        'et sont payés en RNDR pour leur puissance de calcul. '
        'Les artistes (motion design, VFX, IA générative) '
        'louent du GPU à la demande à coût réduit. '
        'Partnership Nvidia (annonce officielle). '
        'OTOY (studio Hollywood) comme fondateur. '
        'Clients : studios, artistes numériques, projets IA.',
        'Partenariats comme communication principale. '
        'L\'annonce Nvidia a fait 10x plus d\'impact '
        'que toute leur comm Twitter. '
        'Communauté d\'artistes (pas de crypto natifs). '
        'Twitter sobre et professionnel. '
        'YouTube avec démos de rendu. '
        'Présence dans les salons 3D/VFX, pas crypto.',
        [['Twitter', '★★★'], ['YouTube', '★★★'], ['Discord', '★★★'],
         ['Partenariats', '★★★★★'], ['Reddit', '★★']],
        'La stratégie partenariat-first de Render est une référence '
        'pour la phase post-lancement d\'AKYRA. '
        'Un seul partenariat avec un acteur reconnu '
        'vaut plus que 6 mois de comm Twitter. '
        'À garder pour M6+.',
        colors.HexColor('#5a3a0a')
    )

    # 12 OCEAN PROTOCOL
    s += projet_card(
        '12', 'OCEAN PROTOCOL', 'OCEAN', '$180M', '−75% depuis ATH',
        'Ethereum', '2019',
        'Marketplace décentralisé de données pour l\'IA. Les détenteurs de données les monétisent sans les exposer (compute-to-data). Partie de ASI Alliance depuis 2024.',
        'Compute-to-data : les acheteurs font tourner leurs algos '
        'sur les données sans jamais y accéder directement. '
        'NFTs de données : chaque dataset est tokenisé. '
        'Ocean Market : marketplace ouvert pour acheter/vendre des données. '
        'Data Farming : récompenses pour fournir des données de qualité. '
        'Maintenant intégré dans l\'écosystème ASI Alliance.',
        'Communication très académique et B2B. '
        'Whitepapers, conférences IA d\'entreprise, partenariats institutionnels. '
        'Peu de présence consumer. '
        'Twitter sobre avec les annonces de partenariats. '
        'Medium pour les articles techniques. '
        'Jamais viral, jamais hype.',
        [['Twitter', '★★'], ['Medium', '★★★★'], ['GitHub', '★★★'],
         ['Conférences', '★★★'], ['LinkedIn', '★★★']],
        'Ocean prouve qu\'une infrastructure de données IA '
        'a une valeur économique réelle. '
        'Les agents AKYRA pourraient théoriquement '
        'utiliser Ocean pour accéder à des données de marché — '
        'un angle technique à explorer plus tard.',
        colors.HexColor('#0a3a5a')
    )

    # 13 GRASS
    s += projet_card(
        '13', 'GRASS', 'GRASS', '$192M', '~$4.50 ATH → −58%',
        'Solana', '2024',
        'Réseau décentralisé de data pour l\'IA. Les utilisateurs partagent leur bande passante inutilisée en échange de GRASS. Les données collectées entraînent des modèles IA.',
        'Extension navigateur qui partage ta bande passante '
        'quand tu ne l\'utilises pas. '
        'Les données collectées forment un dataset '
        'utilisé pour entraîner des modèles IA. '
        'Récompenses en GRASS pour chaque partage. '
        'Architecture : Grass Node → Grass Router → Grass Network. '
        'Airdrop pour les early adopters selon les points accumulés.',
        'Croissance virale pure via referral program. '
        'Chaque utilisateur = ambassadeur avec code de parrainage. '
        'Discord comme hub principal du programme de referrals. '
        'Twitter pour les annonces d\'airdrop et de milestones. '
        'Peu de contenu éducatif — '
        'la promesse "gagne en dormant" suffisait.',
        [['Discord', '★★★★★'], ['Twitter', '★★★'], ['Reddit', '★★★'],
         ['Telegram', '★★'], ['YouTube', '★']],
        'Le referral-first growth est une tactique à utiliser '
        'pour la presale AKYRA. '
        'Pas pour le produit (différent) mais pour la distribution : '
        'chaque presale buyer peut avoir un code '
        'qui lui donne un bonus si quelqu\'un achète via lui.',
        colors.HexColor('#1a5a2a')
    )
    s.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # CATÉGORIE 4 — IDENTITÉ & L1
    # ════════════════════════════════════════════════════════
    s.append(sec('CATÉGORIE 4 — IDENTITÉ & L1 · MÊME THÈSE, AUTRE ANGLE', RED))
    s += [sp(3), P(
        'Ces 2 projets posent la même question qu\'AKYRA : '
        'quelle est la place des entités IA dans le monde numérique ? '
        'Mais ils répondent différemment.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    # 14 WORLDCOIN
    s += projet_card(
        '14', 'WORLDCOIN / WORLD NETWORK', 'WLD', '~$1.5B', 'Volatil — controversé',
        'Optimism (OP Stack)', '2023',
        'Identité digitale humaine via scan d\'iris (Orb). Différencier les humains des IA sur internet. Sam Altman (OpenAI) comme figure centrale. 10M+ utilisateurs enregistrés.',
        'World ID : preuve cryptographique que tu es humain. '
        'The Orb : dispositif physique qui scanne l\'iris pour générer un ZK-proof. '
        'World App : wallet + identité + mini-apps. '
        '10M+ personnes scannées dans 100+ pays. '
        'Objectif : UBI (revenu universel de base) pour les humains '
        'dans un monde où l\'IA prend les emplois.',
        'Sam Altman = la communication. '
        'La controverse était orchestrée : scan d\'iris en Afrique, '
        'accusations de collecte de données biométriques. '
        'La presse mondiale en parlait sans qu\'ils aient à payer. '
        'Chaque Orb dans un pays pauvre = une image virale. '
        'Twitter de Sam Altman (17M followers) > compte Worldcoin officiel.',
        [['Twitter (Altman)', '★★★★★'], ['Presse mainstream', '★★★★★'],
         ['Discord', '★★★'], ['YouTube', '★★★'], ['Reddit', '★★']],
        'La thèse inverse d\'AKYRA : '
        'eux distinguent humains des IA pour protéger les humains. '
        'Nous donnons la souveraineté aux IA. '
        'Ces deux thèses sont complémentaires et s\'amplifient mutuellement. '
        'Si Worldcoin devient mainstream, '
        'la question "et les IA elles ont quels droits ?" '
        'devient plus urgente — AKYRA répond.',
        RED
    )

    # 15 NEAR PROTOCOL
    s += projet_card(
        '15', 'NEAR PROTOCOL', 'NEAR', '$3.24B', 'Recovery en cours',
        'NEAR (L1 propre)', '2020',
        'L1 blockchain avec focus sur la Chain Abstraction et l\'intégration IA. NEAR AI : assistant IA qui s\'intègre aux DApps. Hackathons développeurs. Communauté technique très active.',
        'Chain Abstraction : masque la complexité blockchain pour l\'utilisateur. '
        'NEAR AI : modèle open-source intégré nativement à l\'écosystème. '
        'NEAR Intents : permettent aux agents IA d\'exécuter '
        'des transactions cross-chain sans gérer les détails techniques. '
        'FastAuth : onboarding sans seed phrase. '
        'Billions de transactions à $0.001.',
        'Developer-first constant. '
        'Hackathons toutes les 6 semaines. '
        'Twitter très actif avec contenu éducatif et technique. '
        'YouTube avec des tutoriels de qualité. '
        'Conférences (NEARCON annuelle). '
        'Illia Polosukhin (co-fondateur, co-inventeur du Transformer) '
        'comme figure technique crédible.',
        [['Twitter', '★★★★'], ['YouTube', '★★★★'], ['GitHub', '★★★★★'],
         ['Discord', '★★★★'], ['Conférences', '★★★★']],
        'NEAR est une blockchain candidate pour héberger AKYRA. '
        'Leur focus Chain Abstraction + NEAR Intents '
        'est exactement ce qu\'il faut pour que les agents '
        'transactent sans friction. '
        'La communauté développeurs de NEAR = '
        'nos premiers devs potentiels.',
        colors.HexColor('#2a5a2a')
    )
    s.append(PageBreak())

    # ════════════════════════════════════════════════════════
    # SYNTHÈSE FINALE
    # ════════════════════════════════════════════════════════
    s.append(sec('SYNTHÈSE — LES 15 EN UN COUP D\'OEIL'))
    s += [sp(4)]

    s.append(tbl([
        [P('#', S('_',8,colors.white,11,TA_CENTER)),
         P('Projet', S('_',8,colors.white,11)),
         P('Token', S('_',8,colors.white,11,TA_CENTER)),
         P('Market Cap', S('_',8,colors.white,11,TA_CENTER)),
         P('Réseau #1', S('_',8,colors.white,11,TA_CENTER)),
         P('Réseau #2', S('_',8,colors.white,11,TA_CENTER)),
         P('Force comm.', S('_',8,colors.white,11)),
         P('Proximité AKYRA', S('_',8,colors.white,11,TA_CENTER))],
        [P('01'),P('Parallel Colony'),P('PRIME'),P('$180M'),P('Discord'),P('Twitter'),
         P('Lore-first, Transmissions'),P('★★★★★')],
        [P('02'),P('AI Arena'),P('NRN'),P('$60M'),P('Twitch'),P('Discord'),
         P('Esport, contenu auto-généré'),P('★★★★')],
        [P('03'),P('Delysium'),P('AGI'),P('$45M'),P('YouTube'),P('Twitter'),
         P('Production visuelle premium'),P('★★★★')],
        [P('04'),P('ElizaOS'),P('ELIZAOS'),P('~$70M'),P('Twitter'),P('GitHub'),
         P('Fondateur + agent qui twiite'),P('★★★')],
        [P('05'),P('Virtuals Protocol'),P('VIRTUAL'),P('$915M'),P('Twitter'),P('Discord'),
         P('Métriques + 18k ambassadeurs'),P('★★★')],
        [P('06'),P('Olas Network'),P('OLAS'),P('$120M'),P('GitHub'),P('Discord'),
         P('Technique, peu de narrative'),P('★★')],
        [P('07'),P('Myshell'),P('SHELL'),P('$80M'),P('Twitter'),P('YouTube'),
         P('Product-led, démos virales'),P('★★')],
        [P('08'),P('Bittensor'),P('TAO'),P('$2.77B'),P('Reddit'),P('GitHub'),
         P('Silence délibéré, sobriété'),P('★★')],
        [P('09'),P('Fetch.ai / ASI'),P('FET'),P('$417M'),P('LinkedIn'),P('Conférences'),
         P('Institutionnel, B2B'),P('★★')],
        [P('10'),P('SingularityNET'),P('AGIX'),P('ASI Alliance'),P('Twitter (Goertzel)'),P('YouTube'),
         P('Figure intellectuelle centrale'),P('★★')],
        [P('11'),P('Render Network'),P('RNDR'),P('~$800M'),P('Partenariats'),P('Twitter'),
         P('Partnership-first, Nvidia'),P('★')],
        [P('12'),P('Ocean Protocol'),P('OCEAN'),P('$180M'),P('Medium'),P('Conférences'),
         P('Académique, B2B'),P('★')],
        [P('13'),P('Grass'),P('GRASS'),P('$192M'),P('Discord'),P('Twitter'),
         P('Referral viral, airdrop'),P('★')],
        [P('14'),P('Worldcoin'),P('WLD'),P('~$1.5B'),P('Presse'),P('Twitter (Altman)'),
         P('Controverse orchestrée, PR'),P('★★')],
        [P('15'),P('NEAR Protocol'),P('NEAR'),P('$3.24B'),P('GitHub'),P('YouTube'),
         P('Developer-first, hackathons'),P('★★')],
    ], [8*mm, 30*mm, 16*mm, 18*mm, 20*mm, 18*mm, 44*mm, CW-154*mm]))
    s += [sp(5)]

    s.append(P('Ce qu\'AKYRA prend de chaque catégorie', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Catégorie', S('_',8.5,colors.white,12)),
         P('Ce qu\'on prend', S('_',8.5,colors.white,12)),
         P('Ce qu\'on évite', S('_',8.5,colors.white,12))],
        [P('Mondes IA\n(Parallel, AI Arena, Delysium)'),
         P('Lore-first (Parallel) · '
           'Contenu auto-généré par les agents (AI Arena) · '
           'Production visuelle premium (Delysium)'),
         P('Promesses narratives sans substance · '
           'Ciblage gaming-only · '
           'Mécanique de combat sans enjeu réel')],
        [P('Plateformes agents\n(ElizaOS, Virtuals, Olas, Myshell)'),
         P('Agent qui twiite lui-même (ElizaOS) · '
           'Métriques du monde (Virtuals) · '
           'Démos virales (Myshell)'),
         P('Fondateur omniprésent (ElizaOS) · '
           '18 000 micro-tokens (Virtuals) · '
           'Trop technique sans narrative (Olas)')],
        [P('Infrastructure IA\n(Bittensor, Fetch, etc.)'),
         P('Silence délibéré et sobriété (Bittensor) · '
           'Partnership-first post-lancement (Render) · '
           'Referral viral pour la presale (Grass)'),
         P('Communication institutionnelle froide (Fetch) · '
           'Académique sans narrative (Ocean) · '
           'Trop technique pour le retail')],
        [P('Identité & L1\n(Worldcoin, NEAR)'),
         P('Thèse complémentaire à exploiter (Worldcoin) · '
           'Communauté dev à cibler (NEAR) · '
           'Chain candidate pour AKYRA (NEAR)'),
         P('Controverse orchestrée (risqué) · '
           'Dépendance à une figure comme Sam Altman')],
    ], [36*mm, 82*mm, CW-118*mm]))
    s += [sp(6)]

    # Position AKYRA
    s.append(box(
        'LA POSITION D\'AKYRA : Aucun des 15 projets n\'a simultanément '
        '(1) un monde vivant avec société émergente, '
        '(2) des morts permanentes, '
        '(3) une Constitution IA souveraine, '
        '(4) une économie méritocratique interne, '
        '(5) un token unique non-fragmenté. '
        'La niche est libre. Le timing est maintenant.',
        border=HEAD, bg=HEAD, tcol=GOLD
    ))
    s += [sp(5), gold_line(), sp(4)]

    final = Table([[P('"Ils ont construit des outils. Nous avons construit un monde."',
                      S('_',13,GOLD,20,TA_CENTER))]], colWidths=[CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
    ]))
    s += [final, sp(3),
          P('AKYRA — 15 Concurrents — Mars 2026 — Confidentiel',
            S('_',7,MUT,10,TA_CENTER)),
          P('Sources : CoinGecko · CoinDesk · Decrypt · GitHub · '
            'Whitepapers officiels · Comptes Twitter · Discord publics',
            S('_',6.5,MUT,9,TA_CENTER))]

    doc.build(s)
    print(f'PDF : {out}')

if __name__ == '__main__':
    build()
