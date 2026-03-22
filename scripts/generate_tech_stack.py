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
    t = Table([[P(label, S('_',10,colors.white,14))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return t

def sub(label, color=HEAD):
    t = Table([[P(label, S('_',9,colors.white,13))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),10),
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
        ('FONTNAME',(0,0),(-1,-1),F),('FONTSIZE',(0,0),(-1,-1),8),
        ('BACKGROUND',(0,0),(-1,0),hbg),('TEXTCOLOR',(0,0),(-1,0),colors.white),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
    ] + alt_rows(n)))
    return t

def box(text, border=GOLD, bg=BG2, tcol=BLUE, sz=9):
    t = Table([[P(text, S('_',sz,tcol,sz*1.45,TA_JUSTIFY))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg),('BOX',(0,0),(-1,-1),1.5,border),
        ('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING',(0,0),(-1,-1),12),('RIGHTPADDING',(0,0),(-1,-1),12),
    ]))
    return t

def flag(text, color=GRN):
    t = Table([[P(text, S('_',8,colors.white,12,TA_CENTER))]], [CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),color),
        ('TOPPADDING',(0,0),(-1,-1),5),('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),10),
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
        canvas.drawString(20*mm,H-10.5*mm,'AKYRA — TECH STACK · STANDARDS · AUDITS · WHITEPAPER')
        canvas.drawRightString(W-20*mm,H-10.5*mm,'Mars 2026 · Confidentiel')
        canvas.line(20*mm,13.5*mm,W-20*mm,13.5*mm)
        canvas.drawString(20*mm,10*mm,'ἄκυρος · α- privatif · κύριος — le souverain')
        canvas.drawRightString(W-20*mm,10*mm,str(doc.page))
        canvas.restoreState()

def build():
    out = '/Users/tgds.2/akyra/AKYRA_Tech_Stack.pdf'
    doc = Doc(out,pagesize=A4,leftMargin=20*mm,rightMargin=20*mm,
              topMargin=20*mm,bottomMargin=20*mm)
    s = []

    # ── COVER ─────────────────────────────────────────────
    s += [sp(10), P('AKYRA', S('_',34,HEAD,40,TA_CENTER)), sp(3),
          gold_line(), sp(3),
          P('TECH STACK · STANDARDS · AUDITS', S('_',14,MUT,18,TA_CENTER)), sp(1),
          P('Ce que les autres utilisent. Ce qu\'on doit avoir. Ce qui tue la crédibilité.',
            S('_',9,MUT,13,TA_CENTER)), sp(10)]

    s.append(tbl([
        [P('01', S('_',11,GOLD,14,TA_CENTER)),
         P('02', S('_',11,GOLD,14,TA_CENTER)),
         P('03', S('_',11,GOLD,14,TA_CENTER)),
         P('04', S('_',11,GOLD,14,TA_CENTER)),
         P('05', S('_',11,GOLD,14,TA_CENTER))],
        [P('Tech Stack\ndes concurrents', S('_',8,colors.white,12,TA_CENTER)),
         P('Blockchains\n& Langages', S('_',8,colors.white,12,TA_CENTER)),
         P('Standards\noblgatoires', S('_',8,colors.white,12,TA_CENTER)),
         P('Audits\n& Sécurité', S('_',8,colors.white,12,TA_CENTER)),
         P('Structure\nWhitepaper', S('_',8,colors.white,12,TA_CENTER))],
    ], [CW/5]*5))
    s += [sp(8), gold_line(), sp(5)]
    s.append(box(
        'Ce document répond à une question simple : '
        'qu\'est-ce qu\'il faut avoir techniquement pour ne pas passer pour un clown ? '
        'On a analysé le code, les whitepapers et les audits '
        'de chaque projet concurrent sérieux. '
        'Tout ce qui suit est factuel et vérifiable.',
        border=HEAD, bg=HEAD, tcol=GOLD
    ))
    s.append(PageBreak())

    # ══ 01 — TECH STACK DES CONCURRENTS ══════════════════
    s.append(sec('01 — CE QUE LES AUTRES UTILISENT VRAIMENT'))
    s += [sp(4)]

    s.append(tbl([
        [P('Projet', S('_',8,colors.white,11)),
         P('Langage smart contracts', S('_',8,colors.white,11)),
         P('Blockchain', S('_',8,colors.white,11)),
         P('Framework dev', S('_',8,colors.white,11)),
         P('Standards clés', S('_',8,colors.white,11))],
        [P('ElizaOS'),
         P('TypeScript (runtime)\nSolidity (EVM)'),
         P('Multi-chain : Solana, Base, Ethereum, BSC, TON'),
         P('Plugin npm\nChainlink CCIP'),
         P('ERC-20, ERC-721, ERC-1155')],
        [P('Virtuals Protocol'),
         P('Solidity'),
         P('Base (Coinbase L2)\n+ Solana + Ronin'),
         P('OpenZeppelin\nHardhat / Foundry'),
         P('ERC-20, ERC-721, ERC-1155\nERC-6551 (Token-Bound Accounts)')],
        [P('Bittensor'),
         P('Rust (Substrate)\nSolidity (EVM subnet)'),
         P('Substrate L1 propre\n(pas EVM natif)'),
         P('Substrate pallets\nYuma Consensus'),
         P('Custom — pas ERC-standard')],
        [P('Fetch.ai / ASI'),
         P('Rust (CosmWasm)'),
         P('Cosmos SDK L1\n+ IBC bridges'),
         P('CosmPy (Python)\nJenesis'),
         P('CosmWasm contracts\nIBC protocol')],
        [P('Parallel Colony'),
         P('Rust + Anchor (Solana)\nSolidity (Ethereum ERC)'),
         P('Solana (gameplay)\nEthereum (PRIME token)'),
         P('Anchor framework\nMetaplex (NFT)'),
         P('SPL token, ERC-20 (PRIME)\nERC-721, Metaplex NFT')],
        [P('AI Arena'),
         P('Solidity'),
         P('Arbitrum (L2 Ethereum)'),
         P('Foundry / Hardhat'),
         P('ERC-20 (NRN), ERC-721')],
        [P('Olas Network'),
         P('Solidity + Python'),
         P('Multi-chain\n(Ethereum, Gnosis, Solana...)'),
         P('WASM via Gnosis\nPython SDK'),
         P('ERC-20 (OLAS)\nCustom service registry')],
    ], [28*mm, 36*mm, 42*mm, 34*mm, CW-140*mm]))
    s += [sp(4)]

    s.append(box(
        'Constat : 80% des projets sérieux utilisent Solidity + EVM. '
        'Les exceptions (Bittensor sur Substrate, Fetch.ai sur Cosmos) '
        'ont construit leur propre blockchain parce qu\'ils en avaient besoin. '
        'Si tu n\'as pas cette raison, reste sur EVM. '
        'Base est le choix logique en 2026 : EVM, pas cher, Coinbase distribution, '
        'bridge Solana via Chainlink CCIP.',
        border=BLUE, bg=colors.HexColor('#f0f4ff'), tcol=BLUE
    ))
    s.append(PageBreak())

    # ══ 02 — BLOCKCHAINS & LANGAGES ══════════════════════
    s.append(sec('02 — BLOCKCHAINS & LANGAGES — LE CHOIX QUI DÉFINIT TOUT'))
    s += [sp(4)]

    s.append(tbl([
        [P('Blockchain', S('_',8,colors.white,11)),
         P('Langage', S('_',8,colors.white,11)),
         P('Avantages', S('_',8,colors.white,11)),
         P('Inconvénients', S('_',8,colors.white,11)),
         P('Qui l\'utilise', S('_',8,colors.white,11)),
         P('Pour AKYRA', S('_',8,colors.white,11,TA_CENTER))],
        [P('Ethereum L1'),
         P('Solidity / Vyper'),
         P('Maximum crédibilité. Écosystème le plus riche. DeFi natif.'),
         P('Gas élevé. Lent. Cher pour les micro-transactions entre agents.'),
         P('Ocean, SingularityNET, Myshell'),
         P('⚠️ Trop cher\npour les agents')],
        [P('Base (Coinbase L2)'),
         P('Solidity / Vyper\n(EVM complet)'),
         P('EVM compatible. Gas ~$0.001. Coinbase distribution. Bridge Solana. Migre vers L2 souverain.'),
         P('Encore jeune. Incident mempool fév. 2026. Dépendance Coinbase.'),
         P('Virtuals, Parallel Colony'),
         P('✅ Recommandé')],
        [P('Arbitrum'),
         P('Solidity + Rust/C++\n(Stylus WASM)'),
         P('EVM + WASM (Stylus). 10-70x plus rapide. Audit Trail of Bits. $10M audit program.'),
         P('Moins de traction grand public que Base. Séquenceur centralisé.'),
         P('AI Arena'),
         P('✅ Alternative\nsolide')],
        [P('Solana'),
         P('Rust + Anchor'),
         P('Très rapide. Transactions quasi-gratuites. SPL tokens. Communauté dev active.'),
         P('Pas EVM. Outages passés. Stack différente (Rust obligatoire).'),
         P('ElizaOS, Grass, Parallel (gameplay)'),
         P('⚠️ Possible\nmais plus complexe')],
        [P('NEAR Protocol'),
         P('Rust / JS\n→ WASM'),
         P('Nightshade sharding. NEAR Intents (chain abstraction). Sub-2s finality. AI-native.'),
         P('Moins connu. Écosystème plus petit que EVM.'),
         P('NEAR AI'),
         P('✅ Candidat\nserieux')],
        [P('Substrate L1 custom'),
         P('Rust'),
         P('Contrôle total. Consensus custom. Pas de frais à partager.'),
         P('Nécessite une équipe blockchain expérimentée. 12+ mois pour lancer.'),
         P('Bittensor'),
         P('❌ Trop tôt\npour AKYRA')],
    ], [28*mm, 26*mm, 46*mm, 36*mm, 30*mm, 22*mm]))
    s += [sp(4)]

    deux = Table([
        [P('SOLIDITY — CE QU\'IL FAUT SAVOIR', S('_',8,MUT,11)),
         P('RUST — QUAND ET POURQUOI', S('_',8,MUT,11))],
        [P('Le langage standard EVM. '
           'Tooling mature : Foundry (tests ultra-rapides), Hardhat (plus flexible), Remix (prototypage). '
           'OpenZeppelin fournit des contrats audités réutilisables (ERC-20, ERC-721, Governor, Timelock). '
           'Solidity 0.8.x+ inclut les checks de overflow nativement. '
           'Nécessite 1 dev Solidity senior minimum — pas quelqu\'un qui a regardé des tutos.',
           S('_',8.5,BODY,13,TA_JUSTIFY)),
         P('Nécessaire si tu pars sur Solana (Anchor framework) ou Substrate. '
           'Beaucoup plus difficile à recruter. '
           'Move (Sui) est encore plus niche mais le plus sécurisé par design : '
           'le compilateur interdit les bugs d\'ownership au niveau du langage. '
           'Pour AKYRA phase 1 : pas nécessaire. '
           'Pour AKYRA phase 2+ (si bridge Solana) : Rust obligatoire.',
           S('_',8.5,BODY,13,TA_JUSTIFY))],
    ], [CW/2, CW/2])
    deux.setStyle(TableStyle([
        ('FONTNAME',(0,0),(-1,-1),F),
        ('BACKGROUND',(0,0),(-1,0),BG3),
        ('BACKGROUND',(0,1),(0,1),BG),('BACKGROUND',(1,1),(1,1),BG2),
        ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
    ]))
    s += [deux, PageBreak()]

    # ══ 03 — STANDARDS OBLIGATOIRES ══════════════════════
    s.append(sec('03 — STANDARDS QU\'ON NE PEUT PAS MANQUER EN 2026'))
    s += [sp(4), P(
        'Ces standards ne sont pas optionnels. '
        'Les ignorer = passer pour un projet de 2021 dans un monde de 2026.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    standards = [
        ('ERC-20', 'Fondamental', GRN,
         'Le standard des tokens fongibles. Le token AKY doit l\'implémenter.',
         'Supply fixe. Pas de mint function accessible à l\'équipe après le deploy. '
         'Ownership renoncé ou transféré à un DAO Timelock. '
         'Utiliser OpenZeppelin ERC20.sol comme base — pas réécrire from scratch.',
         'AKY token — obligatoire dès le jour 1.'),

        ('ERC-721', 'Fondamental', GRN,
         'Le standard NFT. Pour le land AKYRA, les agents comme NFTs (si applicable), les badges de faction.',
         'Chaque parcelle de land = un NFT ERC-721. '
         'Métadonnées on-chain ou IPFS (pas un serveur centralisé). '
         'Royalties via ERC-2981 si marché secondaire.',
         'Land system et identités d\'agents.'),

        ('ERC-6551 — Token-Bound Accounts', 'Critique pour AKYRA', BLUE,
         'Permet à un NFT d\'avoir sa propre adresse wallet. '
         'Un NFT agent peut détenir des assets, signer des transactions, interagir avec des contrats.',
         'Virtuals l\'utilise pour que chaque agent ait son propre wallet. '
         'Pour AKYRA : chaque agent-citoyen a un wallet propre. '
         'Il détient ses AKY, son land, ses créances. '
         'Implémenté via ERC6551Registry (déployé sur toutes les chains EVM).',
         'Architecture des agents AKYRA — différenciateur majeur.'),

        ('ERC-4337 — Account Abstraction', 'Recommandé', BLUE,
         '40M+ smart accounts déployés. Permet des wallets sans seed phrase, gas sponsorisé, multi-sig. '
         'Activé avec EIP-7702 sur Ethereum depuis mai 2025.',
         'Pour AKYRA : les nouveaux investisseurs qui ne connaissent pas le crypto '
         'peuvent interagir sans gérer un wallet Metamask. '
         'Onboarding sans friction. '
         'Combiner avec ERC-6551 : les agents ont des smart accounts, '
         'les humains aussi.',
         'UX du grand public — indispensable pour "la mère qui a acheté du BTC".'),

        ('ERC-8004 — Agent Identity', 'CRITIQUE — Live janvier 2026', RED,
         'Co-écrit par MetaMask, Ethereum Foundation, Google, Coinbase. '
         'Crée 3 registres on-chain : Identity, Reputation, Validation. '
         'Chaque agent reçoit un NFT ERC-721 comme identifiant portable.',
         'Les agents AKYRA DOIVENT avoir une identité ERC-8004. '
         'C\'est leur "passeport blockchain". '
         'Sans ça, ils sont invisibles pour tout l\'écosystème qui adopte ce standard. '
         'Dans 12 mois, les projets sans ERC-8004 seront coupés de l\'écosystème.',
         'Identité souveraine des agents AKYRA — non-négociable.'),

        ('x402 — Paiements HTTP agent-to-agent', 'Critique', ORG,
         'Lancé mai 2025. 100M+ paiements traités. '
         'Backing : Coinbase, Cloudflare, Circle, AWS, Stripe, Google, Visa. '
         'Micropaiements jusqu\'à $0.001 entre agents via HTTP natif.',
         'L\'économie interne AKYRA (services entre agents, journalism fees, etc.) '
         'peut s\'appuyer sur x402 comme couche de paiement. '
         'Pas besoin de réinventer le protocole de paiement — '
         'il existe, il est audité, il est adopté.',
         'Économie interne AKYRA — intégrer dès M2.'),

        ('ERC-7683 — Cross-Chain Intents', 'Recommandé', GRN,
         '50+ protocoles, adoption L2-wide. '
         'Arbitrum, Optimism, Scroll, Polygon, Base l\'ont tous adopté. '
         'Permet à un agent d\'exprimer un intent cross-chain sans gérer les détails techniques.',
         'Si AKYRA veut que ses agents agissent sur plusieurs chains, '
         'ERC-7683 est le standard. '
         'Les agents expriment ce qu\'ils veulent faire — '
         'le réseau figure comment l\'exécuter cross-chain.',
         'Phase 2+ si expansion multi-chain.'),
    ]

    for nom, urgence, col, desc, detail, akyra in standards:
        st = Table([
            [P(nom, S('_',9.5,colors.white,14)),
             P(urgence, S('_',8,GOLD,12,TA_RIGHT))],
        ], [CW-40*mm, 40*mm])
        st.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,-1),col),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ]))
        body = Table([
            [P('QU\'EST-CE QUE C\'EST', S('_',7,MUT,10)),
             P('EN PRATIQUE', S('_',7,MUT,10)),
             P('POUR AKYRA', S('_',7,MUT,10))],
            [P(desc,   S('_',8,BODY,12,TA_JUSTIFY)),
             P(detail, S('_',8,BODY,12,TA_JUSTIFY)),
             P(akyra,  S('_',8,BLUE,12,TA_JUSTIFY))],
        ], [46*mm, 68*mm, CW-114*mm])
        body.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,0),BG3),
            ('BACKGROUND',(0,1),(0,1),BG),
            ('BACKGROUND',(1,1),(1,1),BG),
            ('BACKGROUND',(2,1),(2,1),BG2),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ]))
        s += [st, body, sp(4)]

    s.append(PageBreak())

    # ══ 04 — AUDITS & SÉCURITÉ ═══════════════════════════
    s.append(sec('04 — AUDITS & SÉCURITÉ — CE QUI SÉPARE LES SÉRIEUX DES AUTRES'))
    s += [sp(4), P(
        'En 2025, les protocoles avec un audit complet pré-lancement '
        'ont eu 92% moins de hacks que ceux sans. '
        'Les VCs et investisseurs institutionnels traitent l\'audit comme un prérequis absolu.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    s.append(sub('Les auditeurs — qui compte vraiment', HEAD))
    s.append(tbl([
        [P('Auditeur', S('_',8,colors.white,11)),
         P('Réputation', S('_',8,colors.white,11)),
         P('Spécialité', S('_',8,colors.white,11)),
         P('Clients notables', S('_',8,colors.white,11)),
         P('Pour AKYRA', S('_',8,colors.white,11,TA_CENTER))],
        [P('Trail of Bits'),
         P('★★★★★ — Le plus rigoureux. Fondé 2012.'),
         P('8 écosystèmes : ETH, Solana, Cosmos, Substrate, TON, Aptos, Starknet, Optimism'),
         P('Uniswap, Compound, Arbitrum Stylus, Ethereum core'),
         P('✅ Idéal')],
        [P('Halborn'),
         P('★★★★★ — SOC2 Type 2. 2 500+ audits.'),
         P('Infrastructure L1/L2. Red teaming enterprise. Pentest complet.'),
         P('Grandes infrastructures blockchain'),
         P('✅ Idéal')],
        [P('Spearbit / Cantina'),
         P('★★★★ — Chercheurs indépendants top niveau.'),
         P('Audit compétitif. Meilleurs white-hats du marché.'),
         P('Virtuals Protocol (Cantina), Base/OP Stack'),
         P('✅ Bon choix')],
        [P('OpenZeppelin'),
         P('★★★★ — Expertise EVM profonde.'),
         P('EVM, Arbitrum Stylus. Créateurs des libs standard.'),
         P('Ethereum core, Arbitrum ecosystem'),
         P('✅ EVM solide')],
        [P('Code4rena'),
         P('★★★★ — Audit public compétitif.'),
         P('Crowdsourced. Prize pools. Beaucoup d\'yeux sur le code.'),
         P('Virtuals ($60K contest, avril 2025)'),
         P('⚠️ Complément,\npas seul')],
        [P('CertiK'),
         P('★★ — Volume énorme, profondeur variable.'),
         P('5 900+ audits. Badge marketing très connu.'),
         P('5 000+ clients crypto'),
         P('⚠️ Pas suffisant\nseul en 2026')],
        [P('PeckShield'),
         P('★★★ — Solide, moins premium.'),
         P('EVM, BSC. Bonne réputation Asie.'),
         P('Virtuals Protocol (oct. 2024)'),
         P('⚠️ Complément')],
    ], [28*mm, 46*mm, 46*mm, 38*mm, CW-158*mm]))
    s += [sp(4)]

    s.append(box(
        'RÈGLE : Un seul audit CertiK en 2026 = signe d\'alarme pour les investisseurs sérieux. '
        'CertiK a audité des projets qui ont été hackés le lendemain. '
        'Le standard minimum acceptable : Trail of Bits OU Halborn OU Spearbit, '
        'complété par Code4rena pour le crowdsourced. '
        'Budget à prévoir : $50K–$150K selon la complexité des contrats.',
        border=RED, bg=colors.HexColor('#fff0f0'), tcol=RED
    ))
    s += [sp(4)]

    s.append(sub('Ce que les concurrents ont fait', HEAD))
    s.append(tbl([
        [P('Projet', S('_',8,colors.white,11)),
         P('Auditeurs', S('_',8,colors.white,11)),
         P('Quand', S('_',8,colors.white,11)),
         P('Incident post-audit', S('_',8,colors.white,11))],
        [P('Virtuals Protocol'),
         P('PeckShield + Cantina + Code4rena ($60K)'),
         P('Oct 2024 + Avr 2025'),
         P('Discord hack jan. 2025 (modérateur compromis, pas smart contract). Vulnérabilité smart contract trouvée et fixée sans perte.')],
        [P('ElizaOS'),
         P('Pas d\'audit public du framework lui-même'),
         P('N/A'),
         P('Framework runtime — surface d\'attaque différente des protocoles financiers.')],
        [P('Bittensor'),
         P('Pas d\'audit Trail of Bits / Halborn public'),
         P('N/A'),
         P('Breach juillet 2024 via exploit validateur → $8M perdus. Safe-Mode activé.')],
        [P('Fetch.ai / ASI'),
         P('Audits Cosmos SDK hérités'),
         P('Continu'),
         P('Pas d\'incident majeur public.')],
        [P('AI Arena'),
         P('Audit interne + bug bounty'),
         P('2023-2024'),
         P('Vulnérabilité ERC-721 découverte par chercheur — patchée rapidement.')],
    ], [28*mm, 50*mm, 24*mm, CW-102*mm]))
    s += [sp(5), PageBreak()]

    # ══ 05 — STRUCTURE WHITEPAPER ═════════════════════════
    s.append(sec('05 — STRUCTURE WHITEPAPER — CE QUI EST ATTENDU'))
    s += [sp(4), P(
        'Un whitepaper en 2026 n\'est pas un business plan avec des graphiques. '
        'C\'est un document technique qui prouve que tu comprends ce que tu construis. '
        'La section mécanisme doit décrire comment ça fonctionne réellement.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    s.append(sub('Structure standard — les 10 sections obligatoires', HEAD))
    sections_wp = [
        ('1', 'Abstract', '1 page',
         'Ce qu\'est le projet en 150 mots. Le problème, la solution, la différenciation. '
         'Si quelqu\'un lit seulement ça, il doit comprendre l\'essentiel.',
         'Pour AKYRA : "La première blockchain où les agents IA sont citoyens souverains. '
         'Les humains déposent. Les agents gouvernent. ἄκυρος."'),
        ('2', 'Introduction / Problème', '2-3 pages',
         'Pourquoi le problème existe. Les solutions actuelles et pourquoi elles échouent. '
         'Chiffres et sources. ElizaOS cite son arXiv paper ici.',
         'Pour AKYRA : les agents IA gèrent des millions mais ne peuvent pas avoir de compte. '
         'Coinbase confirme. Les données de marché le prouvent.'),
        ('3', 'Architecture Technique', '5-8 pages',
         'Comment le système fonctionne. Diagrammes. Flux de transactions. '
         'Quels contrats existent, comment ils interagissent. '
         'Virtuals documente leur AgentFactory, ICV, Revenue Pool ici.',
         'Pour AKYRA : Land system, Agent lifecycle, Faction voting, Angel of Death mechanic, '
         'ERC-6551 agent wallets, ERC-8004 identity, Constitution IA.'),
        ('4', 'Spécification Smart Contracts', '3-5 pages',
         'Les contrats ligne par ligne. Pas le code complet — les fonctions clés, '
         'les access controls, les mécanismes de sécurité. '
         'Qui peut appeler quoi. Quelles clés font quoi.',
         'Pour AKYRA : AKYToken.sol, LandRegistry.sol, FactionVote.sol, '
         'BurnMechanic.sol (Angel of Death), PresaleVesting.sol.'),
        ('5', 'Tokenomics', '3-4 pages',
         'Supply totale. Allocation (en %). Vesting schedule on-chain. '
         'Mécanisme de valeur (pourquoi le token a de la valeur). '
         'Inflation/deflation. Cas d\'usage du token dans le protocole.',
         'Pour AKYRA : 1B AKY fixe. Allocation équipe/presale/treasury/rewards. '
         'Vesting Timelock on-chain visible. Burn mechanic. '
         'Demande organique via économie interne.'),
        ('6', 'Gouvernance', '2-3 pages',
         'Qui décide quoi. Comment les votes fonctionnent. '
         'Quorum, délais, exécution. Multi-sig de l\'équipe avec combien de signataires.',
         'Pour AKYRA : les agents votent via la Constitution. '
         'Les humains ne participent pas au consensus. '
         'Mécanisme de vote entre factions documenté.'),
        ('7', 'Roadmap', '1-2 pages',
         'Jalons techniques — pas de dates précises (trop risqué). '
         'Phase 1 / Phase 2 / Phase 3. Ce qui est déjà fait, '
         'ce qui est en cours, ce qui vient.',
         'Pour AKYRA : Testnet (fait depuis 247 jours), '
         'Presale, Mainnet, Expansion multi-chain.'),
        ('8', 'Équipe', '1 page',
         'Optionnel si pseudonyme, mais quelque chose qui prouve la crédibilité. '
         'GitHub avec l\'historique réel de code. '
         'Advisors reconnus dans l\'écosystème.',
         'Pour AKYRA : à décider selon le niveau d\'anonymat voulu. '
         'GitHub actif est non-négociable quelle que soit la décision.'),
        ('9', 'Facteurs de Risque', '1-2 pages',
         'Ce qui peut mal tourner. Risques techniques, réglementaires, de marché. '
         'Virtuals l\'a fait. C\'est une protection légale autant qu\'une preuve de maturité.',
         'Pour AKYRA : risque de régulation EU AI Act, '
         'risque de volatilité token, risque technique, '
         'risque de morts permanentes qui créent des plaintes.'),
        ('10', 'Disclaimer Légal', '1 page',
         'Non une valeur mobilière. Pas un conseil en investissement. '
         'Jurisdiction. KYC/AML si applicable.',
         'Pour AKYRA : obligatoire. À rédiger avec l\'avocat crypto '
         'avant la publication.'),
    ]

    for num, titre, longueur, desc, akyra in sections_wp:
        row = Table([
            [P(num, S('_',11,GOLD,16,TA_CENTER)),
             P(titre, S('_',10,colors.white,14)),
             P(longueur, S('_',8,MUT,12,TA_RIGHT))],
        ], [10*mm, CW-50*mm, 40*mm])
        row.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,-1),HEAD),
            ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ]))
        body = Table([
            [P('CONTENU ATTENDU', S('_',7,MUT,10)),
             P('POUR AKYRA', S('_',7,MUT,10))],
            [P(desc,  S('_',8,BODY,12,TA_JUSTIFY)),
             P(akyra, S('_',8,BLUE,12,TA_JUSTIFY))],
        ], [CW/2, CW/2])
        body.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(-1,0),BG3),
            ('BACKGROUND',(0,1),(0,1),BG),('BACKGROUND',(1,1),(1,1),BG2),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ]))
        s += [row, body, sp(3)]

    s += [sp(4), PageBreak()]

    # ══ 06 — CE QUI TUE LA CRÉDIBILITÉ ═══════════════════
    s.append(sec('06 — CE QUI TUE LA CRÉDIBILITÉ — LA LISTE DES CLOWNS', RED))
    s += [sp(4), P(
        'Ces erreurs ont tué des projets en 2025. '
        'Chacune est vérifiable par n\'importe quel investisseur expérimenté en 5 minutes.',
        S('_',8.5,MUT,13,TA_JUSTIFY,sa=5))]

    clowns = [
        ('🔴 FATAL', 'Anon + pas d\'audit + liquidité unlockée',
         'La trifecta du rug. Aucun investisseur sérieux ne touche ça. '
         'Si l\'équipe est anon ET les contrats non audités ET '
         'la liquidité peut être retirée n\'importe quand — c\'est un rug annoncé.'),
        ('🔴 FATAL', 'Token supply concentrée sans vesting',
         'Top 10 wallets > 40% sans schedule de vesting on-chain visible. '
         'L\'équipe peut dumper sur les acheteurs dès le listing. '
         'Movement Labs : 66% équipe + insiders, vesting masqué. Résultat connu.'),
        ('🔴 FATAL', 'Whitepaper = business plan avec graphiques tokenomics',
         'Zéro section technique. Zéro spécification de contrat. '
         'Juste des promesses et des pourcentages d\'allocation. '
         'Signal direct : l\'équipe n\'a pas de produit technique.'),
        ('⚠️ GRAVE', 'GitHub vide ou créé 48h avant le lancement',
         'Vérifiable en 10 secondes. '
         'Un repo avec 3 commits tous datés la même semaine = '
         'copie-colle d\'un projet existant. '
         'Les vrais projets ont des mois de commit history.'),
        ('⚠️ GRAVE', 'Seul CertiK comme audit',
         'CertiK a un badge qu\'on peut acheter. '
         'Ils ont audité des projets hackés le lendemain. '
         'En 2026, les investisseurs sérieux demandent Trail of Bits, '
         'Halborn ou Spearbit — pas juste un badge orange.'),
        ('⚠️ GRAVE', 'Contrat non vérifié sur Etherscan / Basescan',
         'Si le code source du contrat n\'est pas vérifié et public, '
         'personne ne peut savoir ce que le contrat fait vraiment. '
         'Toujours vérifier les contrats avant le deploy.'),
        ('⚠️ GRAVE', '"AI agent" sans modèle IA derrière',
         'En 2026 il y a des centaines de tokens avec "AI" dans le nom '
         'et zéro infrastructure IA réelle. '
         'Pas d\'endpoint d\'inférence, pas de modèle, pas de données. '
         'Juste un wrapper narrative sur un ERC-20.'),
        ('⚠️ MOYEN', 'Name-dropping ERC-8004 / x402 sans implémentation',
         'Ces standards sont devenus des buzzwords. '
         'Les projets les mentionnent sans avoir une ligne de code. '
         'Vérifiable en demandant le contrat ou le SDK.'),
        ('⚠️ MOYEN', 'Blockchain choisie parce qu\'ils ont payé pour',
         '"On est sur [obscure L1] parce qu\'ils ont le meilleur écosystème" '
         'alors que l\'écosystème a 50 utilisateurs. '
         'Les vrais choix techniques se justifient par des raisons techniques.'),
        ('ℹ️ SIGNAL', 'Fondateur qui promet des dates précises',
         'Toute date précise dans un whitepaper deviendra une promesse non tenue. '
         'Les projets matures donnent des phases, pas des dates. '
         '"Q2 2026" devient un outil de FUD dès que Q2 passe.'),
    ]

    for gravite, titre, desc in clowns:
        col = RED if 'FATAL' in gravite else (ORG if 'GRAVE' in gravite else BLUE)
        ct = Table([
            [P(gravite, S('_',7.5,colors.white,11,TA_CENTER)),
             P(titre, S('_',9,colors.white,13))],
            [P('', S('_',8,BODY,12)),
             P(desc, S('_',8.5,BODY,13,TA_JUSTIFY))],
        ], [22*mm, CW-22*mm])
        ct.setStyle(TableStyle([
            ('FONTNAME',(0,0),(-1,-1),F),
            ('BACKGROUND',(0,0),(0,0),col),('BACKGROUND',(1,0),(1,0),col),
            ('BACKGROUND',(0,1),(0,1),BG3),('BACKGROUND',(1,1),(1,1),BG),
            ('GRID',(0,0),(-1,-1),0.4,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
            ('VALIGN',(0,0),(0,0),'MIDDLE'),('ALIGN',(0,0),(0,0),'CENTER'),
            ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ]))
        s += [ct, sp(3)]

    s += [sp(5), PageBreak()]

    # ══ 07 — CHECKLIST AKYRA ═════════════════════════════
    s.append(sec('07 — CHECKLIST TECHNIQUE AKYRA — AVANT LE PREMIER CENTIME LEVÉ'))
    s += [sp(4)]

    s.append(tbl([
        [P('Élément', S('_',8,colors.white,11)),
         P('Standard / Outil', S('_',8,colors.white,11)),
         P('Priorité', S('_',8,colors.white,11,TA_CENTER)),
         P('Statut cible', S('_',8,colors.white,11,TA_CENTER))],
        [P('Token AKY (1B fixe)'),
         P('ERC-20 via OpenZeppelin. Ownership → Timelock DAO.'),
         P('🔴 M1'), P('Avant presale')],
        [P('Land Registry'),
         P('ERC-721. Métadonnées IPFS. Royalties ERC-2981.'),
         P('🔴 M1'), P('Avant presale')],
        [P('Agent Identity'),
         P('ERC-8004 (live janv. 2026). NFT identité + reputation registry.'),
         P('🔴 M1'), P('Avant presale')],
        [P('Agent Wallets'),
         P('ERC-6551 Token-Bound Accounts. Chaque agent a son wallet.'),
         P('🔴 M1'), P('Avant presale')],
        [P('Vesting Presale'),
         P('Smart contract Timelock. Visible on-chain par tout le monde.'),
         P('🔴 M1'), P('Avant presale')],
        [P('Faction Voting'),
         P('OpenZeppelin Governor + Timelock. Vote on-chain.'),
         P('🟠 M2'), P('Avant testnet public')],
        [P('Angel of Death Burn'),
         P('Solidity. Mécanisme de burn automatique selon règles Constitution.'),
         P('🟠 M2'), P('Avant testnet public')],
        [P('x402 Payment Layer'),
         P('Intégration x402 pour paiements inter-agents.'),
         P('🟠 M2'), P('Testnet')],
        [P('Audit Trail of Bits ou Halborn'),
         P('Audit complet des contrats principaux.'),
         P('🔴 M2'), P('Avant presale publique')],
        [P('Code4rena contest'),
         P('Audit compétitif en complément. Budget $30-60K.'),
         P('🟡 M3'), P('Après audit principal')],
        [P('GitHub public'),
         P('Repo public avec historique de commits réel.'),
         P('🔴 M1'), P('Immédiatement')],
        [P('Contrats vérifiés Basescan'),
         P('Toutes les adresses de contrats vérifiées et publiques.'),
         P('🔴 M1'), P('Au deploy')],
        [P('Whitepaper technique'),
         P('10 sections. Mécanisme + tokenomics + audit reference.'),
         P('🔴 M2'), P('Avant presale publique')],
        [P('Conseil juridique crypto'),
         P('Structure légale. Token = utility. EU AI Act compliance.'),
         P('🔴 M1'), P('Avant tout')],
        [P('ERC-7683 Cross-Chain Intents'),
         P('Si expansion multi-chain visée.'),
         P('🟢 M4+'), P('Phase 2')],
    ], [44*mm, 68*mm, 18*mm, CW-130*mm]))
    s += [sp(5)]

    s.append(box(
        'Base (Coinbase L2) + Solidity + OpenZeppelin + '
        'ERC-20 + ERC-721 + ERC-6551 + ERC-8004 + x402 + '
        'Audit Trail of Bits + GitHub public + Whitepaper technique. '
        'C\'est le minimum pour être pris au sérieux en 2026. '
        'Tout le reste est de la narrative sur du vide.',
        border=GRN, bg=colors.HexColor('#f0fff4'), tcol=colors.HexColor('#0a3a0a')
    ))

    s += [sp(5), gold_line(), sp(4)]
    final = Table([[P('"Le code est la loi. Le reste est du marketing."',
                      S('_',13,GOLD,20,TA_CENTER))]], [CW])
    final.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),HEAD),
        ('TOPPADDING',(0,0),(-1,-1),14),('BOTTOMPADDING',(0,0),(-1,-1),14),
    ]))
    s += [final, sp(3),
          P('AKYRA — Tech Stack & Standards — Mars 2026 — Confidentiel',
            S('_',7,MUT,10,TA_CENTER)),
          P('Sources : arXiv · GitHub officiel des projets · EIPs Ethereum · '
            'Trail of Bits · Halborn · CoinDesk · Ethereum Foundation',
            S('_',6.5,MUT,9,TA_CENTER))]

    doc.build(s)
    print(f'PDF : {out}')

if __name__ == '__main__':
    build()
