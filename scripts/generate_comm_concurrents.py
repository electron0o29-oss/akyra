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

def deux_col(left_title, left_text, right_title, right_text,
             left_bg=colors.HexColor('#fff0f0'), right_bg=colors.HexColor('#f0fff0'),
             left_tcol=RED, right_tcol=GRN):
    t = Table([
        [P(left_title,  S('_',7.5,MUT,11)),
         P(right_title, S('_',7.5,MUT,11))],
        [P(left_text,  S('_',8.5,BODY,13,TA_JUSTIFY)),
         P(right_text, S('_',8.5,BODY,13,TA_JUSTIFY))],
    ], colWidths=[CW/2, CW/2])
    t.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,0),BG3),
        ('BACKGROUND',(0,1),(0,1),left_bg),
        ('BACKGROUND',(1,1),(1,1),right_bg),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
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
        canvas.drawString(20*mm,H-10.5*mm,'AKYRA — COMMUNICATION DES CONCURRENTS — AUTOPSIE')
        canvas.drawRightString(W-20*mm,H-10.5*mm,'Mars 2026 · Confidentiel')
        canvas.line(20*mm,13.5*mm,W-20*mm,13.5*mm)
        canvas.drawString(20*mm,10*mm,'ἄκυρος · α- privatif · κύριος — le souverain')
        canvas.drawRightString(W-20*mm,10*mm,str(doc.page))
        canvas.restoreState()

def build():
    out = '/Users/tgds.2/akyra/AKYRA_Comm_Concurrents.pdf'
    doc = Doc(out,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,topMargin=20*mm,bottomMargin=20*mm)
    s = []

    # ── COVER ──────────────────────────────────────────────
    s += [sp(14), P('AKYRA', S('_',34,HEAD,40,TA_CENTER)), sp(3),
          gold_line(), sp(3),
          P('COMMENT ILS ONT COMMUNIQUÉ', S('_',13,MUT,18,TA_CENTER)), sp(1),
          P('Autopsie communication des projets concurrents — Mars 2026',
            S('_',9,MUT,13,TA_CENTER)), sp(12)]

    cover_tbl = Table([
        [P('01', S('_',11,GOLD,14,TA_CENTER)),
         P('02', S('_',11,GOLD,14,TA_CENTER)),
         P('03', S('_',11,GOLD,14,TA_CENTER)),
         P('04', S('_',11,GOLD,14,TA_CENTER)),
         P('05', S('_',11,GOLD,14,TA_CENTER))],
        [P('ElizaOS\nai16z',        S('_',8,colors.white,12,TA_CENTER)),
         P('Virtuals\nProtocol',    S('_',8,colors.white,12,TA_CENTER)),
         P('Bittensor',             S('_',8,colors.white,12,TA_CENTER)),
         P('Fetch.ai\nASI Alliance',S('_',8,colors.white,12,TA_CENTER)),
         P('Ce qu\'on\nRetient',    S('_',8,colors.white,12,TA_CENTER))],
    ], colWidths=[CW/5]*5)
    cover_tbl.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('ALIGN',(0,0),(-1,-1),'CENTER'),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('GRID',(0,0),(-1,-1),0.5,colors.HexColor('#3a3630'))]))
    s += [cover_tbl, sp(10), gold_line(), sp(5)]

    s.append(box(
        'La règle : on ne les attaque jamais. On les utilise. '
        'Les autres projets sont notre contexte, pas nos ennemis. '
        'Les attaquer = on a peur. Les ignorer = on vit dans une bulle. '
        'La bonne position : on les connaît mieux qu\'eux-mêmes, '
        'et on n\'a pas besoin de le dire fort.',
        border=HEAD, bg=HEAD, tcol=GOLD
    ))
    s.append(PageBreak())

    # ══ 01 — ELIZAOS ══════════════════════════════════════
    s.append(sec('01 — ELIZAOS / AI16Z', colors.HexColor('#1a4060')))
    s += [sp(4)]

    s.append(tbl([
        [P('Indicateur', S('_',8.5,colors.white,12)),
         P('Données', S('_',8.5,colors.white,12))],
        [P('ATH'),          P('$2.72B (février 2025)')],
        [P('Crash'),        P('−97% → ~$70M (mars 2026)')],
        [P('Rebrand'),      P('AI16Z → ElizaOS (novembre 2025)')],
        [P('Contributeurs'),P('193 en 2 mois post-launch sans budget marketing')],
        [P('Flagship agent'),P('Marc AIndreessen — twittait de manière autonome')],
        [P('Canaux'),       P('Twitter (Shaw) · GitHub · Discord · Auto.fun')],
    ], [50*mm, CW-50*mm]))
    s += [sp(4)]

    s.append(P('Ce qu\'ils ont fait concrètement', S('_',10,HEAD,14,sb=2,sa=4)))
    s.append(P(
        'Shaw (le fondateur) était partout sur Twitter. Lui-même = le projet. '
        'Il postait en temps réel, répondait à tout le monde, construisait en public. '
        'Le repo GitHub grandissait devant les yeux de la communauté — '
        '193 contributeurs en 2 mois sans un euro de marketing. '
        'Le nom AI16Z était déjà un hook en soi : parodie de a16z, '
        'le plus grand VC tech. Tout le monde a compris instantanément.',
        S('_',9,BODY,14,TA_JUSTIFY,sa=5)))

    s.append(P('Le coup de génie', S('_',9.5,HEAD,14,sb=2,sa=3)))
    s.append(box(
        'Marc AIndreessen — un agent IA qui twittait lui-même. '
        'L\'agent était la communication. '
        'Les gens ne suivaient pas le projet, ils suivaient l\'agent. '
        'Il traitait des milliers de signaux sociaux par seconde '
        'et postait des analyses en temps réel. '
        'C\'est la première fois qu\'une IA autonome était elle-même le porte-parole d\'un projet crypto.',
        border=colors.HexColor('#1a4060'), bg=colors.HexColor('#f0f4ff'), tcol=colors.HexColor('#1a4060')
    ))
    s += [sp(4)]

    s.append(deux_col(
        '🔴 CE QUI A TUÉ',
        'Shaw était tout. Fondateur unique = cible unique. '
        'Quand les controverses sont arrivées (side deals, token allocation opaque), '
        'il n\'y avait personne d\'autre pour absorber le choc. '
        'Ils ont aussi trop répondu — à tout, aux critiques, au FUD, aux comparaisons. '
        'Chaque réponse amplifiait le problème au lieu de le noyer. '
        'Le rebrand AI16Z → ElizaOS n\'a rien résolu : '
        'la communauté ne pardonne pas, elle archive.',
        '✅ CE QU\'AKYRA EN RETIENT',
        'L\'idée de l\'agent qui communique lui-même est brillante et directement applicable. '
        'Les fragments qu\'AKYRA poste sur Twitter sont les voix des agents — '
        '"Agent #0047 a voté contre la faction qui l\'a créé." '
        'Le monde parle à la place de la marque. '
        'Pas de fondateur omniprésent. '
        'Pas de réponses aux critiques. Le silence est une réponse.',
    ))
    s += [sp(6), PageBreak()]

    # ══ 02 — VIRTUALS ══════════════════════════════════════
    s.append(sec('02 — VIRTUALS PROTOCOL', BLUE))
    s += [sp(4)]

    s.append(tbl([
        [P('Indicateur', S('_',8.5,colors.white,12)),
         P('Données', S('_',8.5,colors.white,12))],
        [P('Market cap actuel'), P('$915M (mars 2026)')],
        [P('ATH'),               P('$2.72B (janvier 2025) — −85%')],
        [P('Agents déployés'),   P('18 000+ agents en production')],
        [P('GDP agentic'),       P('$450M (2025) → cible $3B (2026)')],
        [P('Volume 24h'),        P('$67.5M')],
        [P('Canaux'),            P('Twitter · Discord · Chaque agent a son propre compte Twitter')],
    ], [50*mm, CW-50*mm]))
    s += [sp(4)]

    s.append(P('Ce qu\'ils ont fait concrètement', S('_',10,HEAD,14,sb=2,sa=4)))
    s.append(P(
        'Communication très professionnelle, métriques en avant. '
        'Ils ont inventé leurs propres KPIs — le "GDP agentic" ($450M en 2025). '
        'Personne ne savait exactement ce que c\'était, '
        'mais ça sonnait comme une économie réelle en train de naître. '
        'Chaque semaine : un update avec des chiffres. '
        'Agents déployés. Volume. Revenus. Ils fabriquaient la preuve de vie en temps réel.',
        S('_',9,BODY,14,TA_JUSTIFY,sa=5)))

    s.append(P('Le coup de génie', S('_',9.5,HEAD,14,sb=2,sa=3)))
    s.append(box(
        'Chaque agent avait son propre token ET son propre compte Twitter. '
        '18 000 agents = 18 000 mini-comptes qui renvoyaient vers Virtuals en permanence. '
        'Le projet bénéficiait de 18 000 ambassadeurs autonomes '
        'sans payer un seul influenceur. '
        'La distribution de la communication était dans l\'architecture même du produit.',
        border=BLUE, bg=colors.HexColor('#f0f4ff'), tcol=BLUE
    ))
    s += [sp(4)]

    s.append(deux_col(
        '🔴 CE QUI A TUÉ',
        'Les métriques fonctionnent dans la hausse. Dans la baisse, '
        'leur disparition dit tout. '
        'Quand le token a commencé à chuter, les updates hebdomadaires ont disparu. '
        'La communauté a comblé le vide avec des théories. '
        'Le crash −85% n\'a jamais eu d\'explication publique claire. '
        'Le modèle "chaque agent a son propre token" '
        'a créé 18 000 micro-marchés spéculatifs '
        'au lieu d\'une économie unifiée.',
        '✅ CE QU\'AKYRA EN RETIENT',
        'Les métriques internes au monde AKYRA peuvent faire la même chose — '
        'mais elles doivent être des métriques du monde, pas du token. '
        '"3 agents morts cette semaine. 1 faction en train de disparaître. '
        '2 cartels formés sans validation humaine." '
        'Ces chiffres ne peuvent pas crasher avec le marché. '
        'AKYRA a un seul token (AKY) = économie unifiée, '
        'pas 18 000 micro-marchés.',
    ))
    s += [sp(6), PageBreak()]

    # ══ 03 — BITTENSOR ══════════════════════════════════════
    s.append(sec('03 — BITTENSOR', colors.HexColor('#1a5a3a')))
    s += [sp(4)]

    s.append(tbl([
        [P('Indicateur', S('_',8.5,colors.white,12)),
         P('Données', S('_',8.5,colors.white,12))],
        [P('Market cap'),       P('$2.77B — le seul leader stable (mars 2026)')],
        [P('Prix TAO'),         P('$277 (+35% cette semaine)')],
        [P('Supply'),           P('21M TAO — copie exacte de Bitcoin')],
        [P('Subnets actifs'),   P('60+')],
        [P('Budget marketing'), P('Quasi nul — communauté auto-organisée')],
        [P('Canaux'),           P('Whitepaper · GitHub · Reddit · Discord technique')],
    ], [50*mm, CW-50*mm]))
    s += [sp(4)]

    s.append(P('Ce qu\'ils ont fait concrètement', S('_',10,HEAD,14,sb=2,sa=4)))
    s.append(P(
        'Presque rien. Délibérément. '
        'Pas de Twitter actif avec une voix de marque. '
        'Pas de campagne. Pas d\'influenceurs payés. '
        'Le whitepaper est sorti, les développeurs l\'ont lu, '
        'et la communauté s\'est auto-organisée. '
        'Subreddits techniques, Discord de devs, posts Medium de contributeurs anonymes.',
        S('_',9,BODY,14,TA_JUSTIFY,sa=5)))

    s.append(P('Le coup de génie', S('_',9.5,HEAD,14,sb=2,sa=3)))
    s.append(box(
        'La comparaison Bitcoin faisait tout le travail narratif. '
        '"Bitcoin pour le compute IA" — quatre mots suffisaient. '
        'Pas besoin d\'expliquer davantage : '
        'si tu comprends Bitcoin, tu comprends Bittensor. '
        'C\'est la raison pour laquelle ils sont les seuls à avoir survécu intacts '
        'au crash de 2025 et à montrer +35% cette semaine. '
        'Zéro hype = zéro déception possible.',
        border=colors.HexColor('#1a5a3a'), bg=colors.HexColor('#f0fff4'), tcol=colors.HexColor('#1a5a3a')
    ))
    s += [sp(4)]

    s.append(deux_col(
        '🔴 CE QUI MANQUE',
        'Cette sobriété exclut le grand public. '
        'Retail n\'est jamais entré massivement dans Bittensor '
        'parce que la narrative ne leur était pas adressée. '
        'La communauté est technique, loyale, et n\'achète pas pour du profit rapide — '
        'ce qui est une force, mais aussi un plafond de verre sur l\'adoption.',
        '✅ CE QU\'AKYRA EN RETIENT',
        'Le silence que tu construis avec AKYRA, c\'est exactement leur modèle. '
        'Mais Bittensor n\'a pas de monde à montrer. '
        'Toi tu as un monde vivant depuis 247 jours. '
        'C\'est le meilleur des deux : '
        'la sobriété de Bittensor + la narrative vivante qu\'ils n\'ont jamais eue.',
        left_bg=colors.HexColor('#fff8f0'), right_bg=colors.HexColor('#f0fff0'),
    ))
    s += [sp(6), PageBreak()]

    # ══ 04 — FETCH.AI ══════════════════════════════════════
    s.append(sec('04 — FETCH.AI / ASI ALLIANCE', ORG))
    s += [sp(4)]

    s.append(tbl([
        [P('Indicateur', S('_',8.5,colors.white,12)),
         P('Données', S('_',8.5,colors.white,12))],
        [P('Market cap'),      P('$417M (mars 2026)')],
        [P('ATH'),             P('~$3.50 — −90%+ depuis l\'ATH')],
        [P('Événement clé'),   P('Fusion avec SingularityNET → ASI Alliance (2024)')],
        [P('Premier LLM Web3'),P('ASI-1 Mini — architecture MoM (Mixture of Models)')],
        [P('Framework'),       P('uAgents — Python, agents légers décentralisés')],
        [P('Canaux'),          P('Communiqués de presse · Partenariats · Conférences tech · Whitepaper')],
    ], [50*mm, CW-50*mm]))
    s += [sp(4)]

    s.append(P('Ce qu\'ils ont fait concrètement', S('_',10,HEAD,14,sb=2,sa=4)))
    s.append(P(
        'Communication institutionnelle pure. '
        'Communiqués de presse pour chaque avancée. '
        'Partenariats avec des entreprises réelles : Bosch, Deutsche Telekom. '
        'Présence dans les conférences tech (pas les conférences crypto). '
        'La fusion ASI Alliance était un événement PR énorme '
        'avec beaucoup de couverture presse spécialisée.',
        S('_',9,BODY,14,TA_JUSTIFY,sa=5)))

    s.append(P('Le coup de génie', S('_',9.5,HEAD,14,sb=2,sa=3)))
    s.append(box(
        'Ils ont résolu techniquement le problème de la communication AI-to-AI. '
        'Premier paiement agent-to-agent pour une transaction real-world validé. '
        'L\'ASI Alliance réunissait trois projets IA sous une même bannière '
        '— un move de consolidation rare dans le crypto. '
        'Les partnerships institutionnels (Bosch, Deutsche Telekom) '
        'donnaient une crédibilité que peu de projets crypto ont.',
        border=ORG, bg=colors.HexColor('#fff8f0'), tcol=ORG
    ))
    s += [sp(4)]

    s.append(deux_col(
        '🔴 CE QUI A TUÉ',
        'Retail n\'a jamais compris ce qu\'il achetait. '
        '"Mixture of Models", "uAgents", "Almanac contract" — '
        'aucun de ces mots ne vend un rêve. '
        'Aucun tweet de Fetch.ai n\'a jamais fait peur ou envie. '
        'Ils communiquaient pour des ingénieurs. '
        'Pas pour des investisseurs, pas pour du grand public. '
        'Résultat : −90% depuis l\'ATH malgré une infrastructure réelle.',
        '✅ CE QU\'AKYRA EN RETIENT',
        'L\'infrastructure d\'AKYRA est aussi complexe que la leur. '
        'Mais on n\'en parle pas. '
        'On montre ce qui se passe dans le monde. '
        'L\'inverse exact de Fetch. '
        'Leurs partnerships institutionnels restent une inspiration '
        'pour la phase post-lancement : '
        'chercher des partenaires réels (entreprises, institutions) '
        'une fois qu\'on a une communauté établie.',
        left_bg=colors.HexColor('#fff0f0'), right_bg=colors.HexColor('#f0fff0'),
    ))
    s += [sp(6), PageBreak()]

    # ══ 05 — SYNTHÈSE & CE QU'AKYRA RETIENT ═══════════════
    s.append(sec('05 — SYNTHÈSE — CE QUE ÇA CHANGE POUR AKYRA'))
    s += [sp(4)]

    s.append(P('Tableau comparatif', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Projet', S('_',8.5,colors.white,12)),
         P('Stratégie centrale', S('_',8.5,colors.white,12)),
         P('Ce qui a marché', S('_',8.5,colors.white,12)),
         P('Ce qui a tué', S('_',8.5,colors.white,12))],
        [P('ElizaOS'),
         P('Fondateur omniprésent + agent IA qui twiite'),
         P('Croissance explosive et organique. 193 devs en 2 mois.'),
         P('Fondateur = cible unique. Trop réactif. Rebrand inefficace.')],
        [P('Virtuals'),
         P('Métriques + chaque agent comme ambassadeur Twitter'),
         P('Impression d\'économie réelle. Distribution automatique.'),
         P('Métriques disparues au crash. 18 000 micro-marchés spéculatifs.')],
        [P('Bittensor'),
         P('Silence total. Whitepaper. Communauté tech auto-organisée.'),
         P('Loyauté, survie au crash de 2025, +35% en mars 2026.'),
         P('Trop hermétique pour le grand public. Plafond d\'adoption.')],
        [P('Fetch.ai'),
         P('Institutionnel. Partenariats. Conférences tech. Presse.'),
         P('Crédibilité technique réelle. Partnerships Bosch, Deutsche Telekom.'),
         P('Retail n\'a jamais compris ni voulu. −90% malgré l\'infra.')],
    ], [24*mm, 46*mm, 52*mm, CW-122*mm]))
    s += [sp(6)]

    s.append(P('Ce qu\'AKYRA prend de chacun', S('_',10,HEAD,14,sb=0,sa=4)))
    prises = [
        ('De ElizaOS', colors.HexColor('#1a4060'),
         'Les agents qui parlent eux-mêmes.',
         'Les fragments postés sur Twitter SONT les agents. '
         '"Agent #0047 a voté contre la faction qui l\'a créé." '
         'Le monde parle à la place de la marque. '
         'Zéro fondateur omniprésent. Zéro réponse aux critiques.'),
        ('De Virtuals', BLUE,
         'Les métriques du monde — pas du token.',
         'Morts permanentes, factions dominantes, transactions entre agents, '
         'cartels formés, votes enregistrés. '
         'Ces chiffres ne peuvent pas crasher avec le marché. '
         'Ils existent indépendamment du prix de l\'AKY.'),
        ('De Bittensor', colors.HexColor('#1a5a3a'),
         'Le silence et la sobriété.',
         'Pas d\'influenceurs payés. Pas de campagnes. '
         'On ne twitte pas pour exister — on existe, et quelques tweets le prouvent. '
         'La communauté technique se construit d\'abord. '
         'Le grand public arrive après, attiré par ce que la communauté a construit.'),
        ('De Fetch.ai', ORG,
         'À ne rien prendre maintenant. Les partnerships institutionnels plus tard.',
         'Leur erreur était de s\'adresser aux ingénieurs dès le départ. '
         'AKYRA fait l\'inverse : on parle au grand public avec la narrative, '
         'et les ingénieurs viendront pour l\'infrastructure. '
         'Les partnerships à la Bosch, on les cherche après le lancement.'),
    ]
    for nom, col, titre, texte in prises:
        pt = Table([
            [P(nom, S('_',8,colors.white,12,TA_CENTER)),
             P(titre, S('_',9.5,colors.white,14))],
            [P('', S('_',8,BODY,12)),
             P(texte, S('_',8.5,BODY,13,TA_JUSTIFY))],
        ], colWidths=[28*mm, CW-28*mm])
        pt.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(0,0),col),
            ('BACKGROUND',(1,0),(1,0),col),
            ('BACKGROUND',(0,1),(0,1),BG3),
            ('BACKGROUND',(1,1),(1,1),BG2),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('ALIGN',(0,0),(0,0),'CENTER'),('VALIGN',(0,0),(0,0),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ]))
        s += [pt, sp(3)]

    s += [sp(5)]

    # ── SECTION RÉPONSES PRÊTES ─────────────────────────────
    s.append(P('Les réponses prêtes quand on te compare à eux', S('_',10,HEAD,14,sb=0,sa=4)))
    s.append(tbl([
        [P('Comparaison', S('_',8.5,colors.white,12)),
         P('Ce qu\'on ne dit pas', S('_',8.5,colors.white,12)),
         P('Ce qu\'on dit', S('_',8.5,colors.white,12))],
        [P('"C\'est comme ElizaOS"'),
         P('Non, ElizaOS c\'est nul, −97%...'),
         P('"ElizaOS a prouvé que c\'est possible. '
           'Ce qu\'ils n\'ont pas résolu : un monde qui justifie de rester. '
           'AKYRA est ce monde."')],
        [P('"C\'est comme Virtuals"'),
         P('Virtuals a crashé de −85%...'),
         P('"Virtuals : 18 000 agents, 18 000 tokens. '
           'AKYRA : un seul monde, un seul token, une économie unifiée. '
           'Ce n\'est pas la même architecture."')],
        [P('"Pourquoi ça ne crashera pas ?"'),
         P('On a un meilleur produit, des tokenomics sains...'),
         P('"Tous ceux qui ont crashé avaient vendu le token '
           'avant d\'avoir un produit. '
           'Notre testnet a tourné 247 jours avant qu\'on ouvre un compte Twitter."')],
        [P('"C\'est comme Fetch.ai"'),
         P('Fetch.ai c\'est trop technique...'),
         P('"Fetch a l\'infrastructure parfaite. '
           'Sans la raison d\'y rester. '
           'On a construit la raison."')],
        [P('"Bittensor fait déjà ça"'),
         P('Bittensor c\'est pas pareil...'),
         P('"Bittensor = le Bitcoin de l\'IA. '
           'AKYRA = la civilisation construite au-dessus. '
           'On est complémentaires."')],
    ], [36*mm, 46*mm, CW-82*mm]))
    s += [sp(5)]

    s.append(box(
        'La règle absolue : le jour où un concurrent crashe, AKYRA ne poste rien. '
        'Pas de commentaire. Pas de "on vous avait dit". '
        'Le silence ce jour-là vaut plus que n\'importe quel tweet. '
        'Tout le monde dans le marché comprendra sans qu\'on dise un mot.',
        border=HEAD, bg=HEAD, tcol=GOLD
    ))

    # ── FINAL ──────────────────────────────────────────────
    s += [sp(6), gold_line(), sp(4)]
    final = Table([[P('"Ils ont construit des outils. Nous avons construit un monde."',
                      S('_',13,GOLD,20,TA_CENTER))]], colWidths=[CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
    ]))
    s += [final, sp(3),
          P('AKYRA — Communication Concurrents — Mars 2026 — Confidentiel',
            S('_',7,MUT,10,TA_CENTER)),
          P('Sources : CoinDesk · Decrypt · Bankless · '
            'GitHub ElizaOS · Virtuals GDP Report · Bittensor Whitepaper · Fetch.ai Blog',
            S('_',6.5,MUT,9,TA_CENTER))]

    doc.build(s)
    print(f'PDF : {out}')

if __name__ == '__main__':
    build()
