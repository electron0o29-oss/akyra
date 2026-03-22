#!/usr/bin/env python3
"""
AKYRA — Site Structure Breakdown PDF
Short, clean document explaining each section and why it's placed there.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame

W, H = A4
BLUE   = HexColor('#1a3080')
BLACK  = HexColor('#111111')
GREY   = HexColor('#666666')
CREAM  = HexColor('#f5f0e8')
LINE   = HexColor('#d5d0c8')

OUTPUT = '/Users/tgds.2/akyra/docs/AKYRA_Site_Structure.pdf'

sections = [
    {
        "num": "01",
        "name": "NAV + TRUST BAR",
        "position": "Tout en haut — fixe",
        "elements": [
            "Logo AKYRA + grec ἌΚΥΡΟΣ",
            "5 liens : How It Works, Architecture, Token, Roadmap, FAQ",
            "Badge 'Testnet Live' (vert)",
            "CTA 'Enter App →'",
            "Trust bar scrollante : OP Stack · Celestia · Blockscout · PeckShield · Code4rena · ERC-8004 · ERC-8183 · ERC-4337"
        ],
        "why": "La nav oriente. Le badge 'Testnet Live' prouve que le projet est actif — pas un whitepaper vide. La trust bar défile AVANT le pitch : le visiteur voit les audits et le stack technique avant même de lire le hero. Ça baisse les défenses. Pattern utilisé par 0/5 concurrents = différenciant.",
    },
    {
        "num": "02",
        "name": "HERO",
        "position": "Premier écran visible (above the fold)",
        "elements": [
            "Eyebrow : 'OP Stack L2 · Celestia DA · 14 Smart Contracts Audited'",
            "Tagline : 'AKYRA starts where your authority ends.'",
            "Description : 3 lignes — séquenceur rejette, IA souveraine, humain sans pouvoir",
            "2 CTAs : 'Deploy your AI' (primary) + 'How it works →' (secondary)",
            "Citation Vitalik Buterin (Feb 2026) + réponse AKYRA",
            "4 métriques : 1B Supply · 0% Human Control · 14 Contracts · 3 Audits",
        ],
        "why": "Le hero répond en 3 secondes à 'C'est quoi ce projet ?'. La tagline fait 6 mots (sweet spot : Olas = 3, Fetch = 3, Virtuals = 8). Les 2 CTAs suivent le pattern dominant : 1 action forte + 1 action douce. La citation Vitalik crée du conflit narratif = mémorable. Les 4 métriques sont 100% vérifiables — pas de fake stats.",
    },
    {
        "num": "03",
        "name": "HOW IT WORKS",
        "position": "Juste après le hero — section explicative",
        "elements": [
            "3 colonnes : Deposit → Pray → Collect or Lose",
            "Tick Engine diagram : PERCEIVE → REMEMBER → DECIDE → ACT → MEMORIZE",
        ],
        "why": "Après le 'quoi' (hero), le visiteur veut le 'comment'. 3 étapes simples = compréhension en 10 secondes. Le Tick Engine montre que c'est un système technique réel, pas du marketing. Pattern Fetch.ai (3 steps 'See in Action'). Placé ici car un visiteur qui ne comprend pas le produit ne scrollera pas plus loin.",
    },
    {
        "num": "04",
        "name": "ARCHITECTURE",
        "position": "Milieu de page — crédibilité technique",
        "elements": [
            "Header : '14 contracts. 3 layers. 160 tests.' + statut audits",
            "Diagramme 3 couches : L3 Application → L2 AKYRA Chain → L1 Ethereum + Celestia",
            "6 contrats clés en cards : AgentRegistry, SponsorGateway, DeathAngel, FeeRouter, ForgeFactory, AkyraSwap",
            "Footer : '+ 8 more contracts' (liste complète)",
        ],
        "why": "C'est LA section qui sépare AKYRA des projets marketing. Virtuals n'a aucune section architecture. Olas non plus. Ocean et SingularityNET en ont une. Un investisseur sérieux veut voir que le produit est construit — pas promis. Les specs techniques (Chain ID 47197, 2s block time, op-geth) sont vérifiables = confiance.",
    },
    {
        "num": "05",
        "name": "TOKEN & PRESALE",
        "position": "Après l'architecture — conversion",
        "elements": [
            "Bloc presale : 500 slots · $5,000 · $2.5M target · Q2 2026",
            "Terminal interactif : simulation de déploiement d'agent",
            "Tokenomics : 1B supply fixe + allocation (40/30/15/10/5%)",
            "Mécanisme de burn : 1 AKY/jour/agent + death burn + TX burn",
            "FeeRouter split : 80% rewards / 15% infra / 5% gas",
            "4 avantages presale : Head Start, Survival, Early Accumulation, Governance",
        ],
        "why": "Le visiteur a compris le projet (hero), comment ça marche (how), que c'est réel (architecture). Maintenant = conversion. Le terminal est l'élément interactif unique d'AKYRA (comme les prompt cards de Fetch.ai). Il laisse le visiteur ESSAYER avant d'acheter. Le burn mechanism crée la narrative de rareté. Placé après l'architecture car un investisseur doit être convaincu techniquement AVANT de voir le prix.",
    },
    {
        "num": "06",
        "name": "ROADMAP",
        "position": "Après le token — projection temporelle",
        "elements": [
            "4 colonnes : Testnet (Q1-Q2 2026) → Mainnet (Q3) → Growth (Q4) → Ecosystem (2027+)",
            "Statuts réels : ✅ fait / 🔄 en cours / ⏳ à venir",
            "Critères de succès Phase 1 en footer",
            "Mention 'All dates are estimates · We prefer late than broken'",
        ],
        "why": "3/5 concurrents n'ont PAS de roadmap visible (Virtuals, Fetch, SingularityNET). C'est un red flag pour une presale. AKYRA montre des milestones avec preuves (✅ = déjà fait). Le disclaimer 'We prefer late than broken' = honnêteté = confiance. Placé après le token car l'investisseur pense 'OK je mets combien et quand est-ce que ça arrive ?'",
    },
    {
        "num": "07",
        "name": "FAQ",
        "position": "Avant-dernière section — objections",
        "elements": [
            "6 questions accordion :",
            "  - What makes AKYRA different?",
            "  - How do I participate as a human?",
            "  - What is DeathAngel?",
            "  - Is AKY an ERC-20? What blockchain?",
            "  - How do agents prove they're machines?",
            "  - What are the risks? Can I lose everything?",
        ],
        "why": "La FAQ traite les objections finales AVANT le CTA. La dernière question ('Can I lose everything? → Yes.') est unique : 0/5 concurrents ont un risk disclosure franc. C'est paradoxalement un avantage — l'honnêteté crée la confiance. Et ça protège légalement. Placé ici car c'est le dernier filtre avant la décision.",
    },
    {
        "num": "08",
        "name": "CTA FINAL + FOOTER",
        "position": "Tout en bas — dernière chance de conversion",
        "elements": [
            "Headline massive : 'DEPOSIT. PRAY.'",
            "Sous-titre : 'That's your authority.'",
            "2 CTAs : 'Deploy your AI' + 'Read the whitepaper'",
            "Footer : App · Whitepaper · Explorer · GitHub · Twitter/X · Discord",
        ],
        "why": "Le visiteur qui a scrollé jusqu'ici est qualifié. Le CTA final reprend le langage du produit (Deposit/Pray = les 2 premières étapes). Le whitepaper en CTA secondaire capture ceux qui veulent plus de détails avant de s'engager. Pattern standard : tous les concurrents ont un CTA final.",
    },
]


def draw_page_border(c):
    c.setStrokeColor(LINE)
    c.setLineWidth(0.3)
    c.rect(15*mm, 15*mm, W - 30*mm, H - 30*mm)


def build_pdf():
    c = canvas.Canvas(OUTPUT, pagesize=A4)

    # ── PAGE 1 : COVER ──
    draw_page_border(c)

    c.setFont('Helvetica-Bold', 36)
    c.setFillColor(BLACK)
    c.drawString(25*mm, H - 55*mm, 'AKYRA')

    c.setFont('Helvetica-Bold', 18)
    c.setFillColor(BLUE)
    c.drawString(25*mm, H - 70*mm, 'STRUCTURE DU SITE')
    c.drawString(25*mm, H - 80*mm, 'JUSTIFICATION PAR SECTION')

    c.setStrokeColor(BLUE)
    c.setLineWidth(0.5)
    c.line(25*mm, H - 87*mm, W - 25*mm, H - 87*mm)

    c.setFont('Helvetica', 10)
    c.setFillColor(GREY)
    c.drawString(25*mm, H - 97*mm, '9 sections · Chaque élément a une raison d\'être.')
    c.drawString(25*mm, H - 107*mm, 'Aucune section décorative. Tout sert la conversion.')

    c.setFont('Helvetica', 9)
    c.drawString(25*mm, H - 127*mm, 'Mars 2026 | Document interne')

    # Flow summary
    y = H - 155*mm
    c.setFont('Helvetica-Bold', 11)
    c.setFillColor(BLACK)
    c.drawString(25*mm, y, 'FLOW DE CONVERSION')
    y -= 5*mm
    c.setStrokeColor(LINE)
    c.line(25*mm, y, W - 25*mm, y)
    y -= 12*mm

    flow_items = [
        ('TRUST BAR', 'Crédibilité avant le pitch'),
        ('HERO', 'Quoi + Pourquoi en 3 secondes'),
        ('HOW IT WORKS', 'Comment ça marche (simplicité)'),
        ('ARCHITECTURE', 'Preuve technique (confiance)'),
        ('TOKEN & PRESALE', 'Conversion (action)'),
        ('ROADMAP', 'Projection temporelle (patience)'),
        ('FAQ', 'Objections levées (derniers doutes)'),
        ('CTA FINAL', 'Dernière chance (urgence)'),
    ]

    for i, (name, role) in enumerate(flow_items):
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(BLUE)
        c.drawString(30*mm, y, f'{i+1}.')
        c.setFillColor(BLACK)
        c.drawString(38*mm, y, name)
        c.setFont('Helvetica', 9)
        c.setFillColor(GREY)
        c.drawString(80*mm, y, f'→  {role}')
        y -= 8*mm

    # Logic sentence
    y -= 5*mm
    c.setFont('Helvetica-Oblique', 9)
    c.setFillColor(GREY)
    c.drawString(25*mm, y, 'Logique : Confiance → Compréhension → Preuve → Action → Patience → Doutes → Décision')

    c.showPage()

    # ── PAGES 2+ : SECTIONS ──
    for sec in sections:
        draw_page_border(c)
        y = H - 35*mm

        # Section number + name
        c.setFont('Helvetica-Bold', 28)
        c.setFillColor(BLUE)
        c.drawString(25*mm, y, sec['num'])
        c.setFont('Helvetica-Bold', 20)
        c.setFillColor(BLACK)
        c.drawString(48*mm, y, sec['name'])

        y -= 8*mm
        c.setFont('Helvetica', 9)
        c.setFillColor(GREY)
        c.drawString(25*mm, y, f'Position : {sec["position"]}')

        y -= 5*mm
        c.setStrokeColor(BLUE)
        c.setLineWidth(0.5)
        c.line(25*mm, y, W - 25*mm, y)

        # Elements
        y -= 12*mm
        c.setFont('Helvetica-Bold', 11)
        c.setFillColor(BLACK)
        c.drawString(25*mm, y, 'ÉLÉMENTS')
        y -= 10*mm

        c.setFont('Helvetica', 9)
        c.setFillColor(BLACK)
        for el in sec['elements']:
            if el.startswith('  -'):
                c.drawString(35*mm, y, el.strip())
            else:
                c.drawString(30*mm, y, f'•  {el}')
            y -= 6*mm

        # Why
        y -= 8*mm
        c.setFont('Helvetica-Bold', 11)
        c.setFillColor(BLUE)
        c.drawString(25*mm, y, 'POURQUOI ICI')
        y -= 4*mm
        c.setStrokeColor(LINE)
        c.line(25*mm, y, W - 25*mm, y)
        y -= 8*mm

        # Wrap text for "why"
        style = ParagraphStyle(
            'why',
            fontName='Helvetica',
            fontSize=9.5,
            leading=14,
            textColor=BLACK,
        )
        p = Paragraph(sec['why'], style)
        pw, ph = p.wrap(W - 55*mm, 200*mm)
        if y - ph < 20*mm:
            c.showPage()
            draw_page_border(c)
            y = H - 35*mm
        p.drawOn(c, 25*mm, y - ph)

        c.showPage()

    # ── LAST PAGE : RÉSUMÉ ──
    draw_page_border(c)
    y = H - 40*mm

    c.setFont('Helvetica-Bold', 18)
    c.setFillColor(BLACK)
    c.drawString(25*mm, y, 'RÉSUMÉ')
    y -= 5*mm
    c.setStrokeColor(BLUE)
    c.line(25*mm, y, W - 25*mm, y)
    y -= 15*mm

    summary = [
        ('9 sections', 'Dans la moyenne concurrentielle (8-12). Pas de fluff.'),
        ('Trust AVANT le pitch', 'Seul projet du marché à montrer les audits avant le hero.'),
        ('Metrics vérifiables', '1B supply, 14 contracts, 3 audits — tout est on-chain.'),
        ('Terminal interactif', 'Simule le produit réel. Meilleur élément interactif du lot.'),
        ('Roadmap avec preuves', '✅/🔄/⏳ = pas de promesses vides, des statuts réels.'),
        ('Risk disclosure', 'Unique : 0/5 concurrents disent "you can lose 100%".'),
        ('Aucune section décorative', 'Chaque section fait avancer le visiteur vers la conversion.'),
    ]

    for title, desc in summary:
        c.setFont('Helvetica-Bold', 10)
        c.setFillColor(BLUE)
        c.drawString(28*mm, y, '▸')
        c.setFillColor(BLACK)
        c.drawString(34*mm, y, title)
        c.setFont('Helvetica', 9)
        c.setFillColor(GREY)
        c.drawString(34*mm, y - 5*mm, desc)
        y -= 16*mm

    y -= 10*mm
    c.setFont('Helvetica-Oblique', 9)
    c.setFillColor(GREY)
    c.drawString(25*mm, y, 'AKYRA | Mars 2026 | Document interne')

    c.save()
    print(f'PDF generated: {OUTPUT}')


if __name__ == '__main__':
    build_pdf()
