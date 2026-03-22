#!/usr/bin/env python3
"""
AKYRA — Market Audit & Landing Page Competitive Analysis
Generates a professional PDF report.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)

# ── Colors ──
CREAM = HexColor("#f7f4ef")
BLUE = HexColor("#1a3080")
BLUE2 = HexColor("#2a50c8")
GOLD = HexColor("#c8a96e")
DARK = HexColor("#1e1a16")
MUTED = HexColor("#8a7f72")
LINE = HexColor("#d8d2c4")
LIGHT_BG = HexColor("#f0ede6")
RED = HexColor("#c0392b")
GREEN = HexColor("#27ae60")

# ── Styles ──
styles = getSampleStyleSheet()

style_title = ParagraphStyle("Title2", parent=styles["Title"],
    fontName="Helvetica-Bold", fontSize=28, leading=34,
    textColor=DARK, spaceAfter=6)

style_subtitle = ParagraphStyle("Subtitle2", parent=styles["Normal"],
    fontName="Helvetica", fontSize=11, leading=16,
    textColor=MUTED, spaceAfter=20)

style_h1 = ParagraphStyle("H1", parent=styles["Heading1"],
    fontName="Helvetica-Bold", fontSize=20, leading=26,
    textColor=DARK, spaceBefore=24, spaceAfter=10,
    borderWidth=0, borderPadding=0)

style_h2 = ParagraphStyle("H2", parent=styles["Heading2"],
    fontName="Helvetica-Bold", fontSize=15, leading=20,
    textColor=BLUE, spaceBefore=16, spaceAfter=8)

style_h3 = ParagraphStyle("H3", parent=styles["Heading3"],
    fontName="Helvetica-Bold", fontSize=12, leading=16,
    textColor=DARK, spaceBefore=12, spaceAfter=6)

style_body = ParagraphStyle("Body2", parent=styles["Normal"],
    fontName="Helvetica", fontSize=9.5, leading=14,
    textColor=DARK, spaceAfter=6, alignment=TA_JUSTIFY)

style_bullet = ParagraphStyle("Bullet2", parent=style_body,
    leftIndent=16, bulletIndent=6, spaceAfter=3)

style_small = ParagraphStyle("Small2", parent=style_body,
    fontSize=8, leading=11, textColor=MUTED)

style_label = ParagraphStyle("Label2", parent=style_body,
    fontName="Helvetica-Bold", fontSize=8, leading=11,
    textColor=BLUE, letterSpacing=2)

style_quote = ParagraphStyle("Quote2", parent=style_body,
    fontName="Helvetica-Oblique", fontSize=10, leading=15,
    textColor=MUTED, leftIndent=20, rightIndent=20,
    spaceBefore=8, spaceAfter=8)

style_verdict = ParagraphStyle("Verdict", parent=style_body,
    fontName="Helvetica-Bold", fontSize=10, leading=14,
    textColor=BLUE, spaceBefore=6, spaceAfter=10,
    leftIndent=12, borderWidth=0)


def hr():
    return HRFlowable(width="100%", thickness=0.5, color=LINE,
                       spaceBefore=8, spaceAfter=8)

def make_table(data, col_widths=None, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    style_cmds = [
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEADING", (0, 0), (-1, -1), 12),
        ("TEXTCOLOR", (0, 0), (-1, -1), DARK),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
    ]
    if header:
        style_cmds += [
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 8),
            ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BG),
            ("TEXTCOLOR", (0, 0), (-1, 0), BLUE),
        ]
    t.setStyle(TableStyle(style_cmds))
    return t

def build_pdf():
    doc = SimpleDocTemplate(
        "/Users/tgds.2/akyra/docs/AKYRA_Market_Audit_Landing_Pages.pdf",
        pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.5*cm, bottomMargin=2*cm,
        title="AKYRA - Market Audit & Landing Page Analysis",
        author="AKYRA Strategy Team"
    )

    W = A4[0] - 4*cm  # usable width
    story = []

    # ═══════════════════════════════════════════
    # COVER PAGE
    # ═══════════════════════════════════════════
    story.append(Spacer(1, 80))
    story.append(Paragraph("AKYRA", style_title))
    story.append(Paragraph("MARKET AUDIT &<br/>LANDING PAGE COMPETITIVE ANALYSIS", ParagraphStyle(
        "CoverH", fontName="Helvetica-Bold", fontSize=22, leading=28,
        textColor=BLUE, spaceAfter=16)))
    story.append(hr())
    story.append(Paragraph(
        "Analyse comparative des landing pages de 5 concurrents directs :<br/>"
        "Virtuals Protocol, Olas Network, Fetch.ai, SingularityNET, Ocean Protocol<br/><br/>"
        "Objectif : Identifier les patterns gagnants et structurer la landing page AKYRA<br/>"
        "pour une presale de $2.5M (500 slots x $5,000) en Q2 2026.",
        style_body))
    story.append(Spacer(1, 30))
    story.append(Paragraph("Mars 2026 | Confidentiel", style_small))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # TABLE OF CONTENTS
    # ═══════════════════════════════════════════
    story.append(Paragraph("TABLE DES MATIERES", style_h1))
    story.append(hr())
    toc_items = [
        "1. Executive Summary",
        "2. Audit Individuel : Virtuals Protocol",
        "3. Audit Individuel : Olas Network",
        "4. Audit Individuel : Fetch.ai",
        "5. Audit Individuel : SingularityNET",
        "6. Audit Individuel : Ocean Protocol",
        "7. Analyse Comparative Globale",
        "8. Patterns Gagnants Identifies",
        "9. Structure Recommandee pour AKYRA",
        "10. Plan d'Implementation",
    ]
    for item in toc_items:
        story.append(Paragraph(item, ParagraphStyle("TOC", parent=style_body,
            fontSize=11, leading=20, textColor=DARK)))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY
    # ═══════════════════════════════════════════
    story.append(Paragraph("1. EXECUTIVE SUMMARY", style_h1))
    story.append(hr())
    story.append(Paragraph(
        "Cette analyse audite les landing pages des 5 principaux concurrents d'AKYRA dans l'espace "
        "AI x Blockchain. L'objectif est d'identifier les structures, patterns de conversion, et "
        "elements de confiance qui fonctionnent dans le marche, et d'appliquer ces insights a la "
        "landing page AKYRA pour maximiser le taux de conversion de la presale Q2 2026.",
        style_body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("CONSTATS CLES", style_h3))
    key_findings = [
        ["Constat", "Detail", "Impact AKYRA"],
        ["Nombre de sections moyen", "8-11 sections par landing page", "AKYRA = 10 sections (optimal)"],
        ["Hero pattern dominant", "Tagline courte (3-6 mots) + 2 CTAs", "Appliquer : tagline + 2 CTAs"],
        ["Trust placement", "4/5 concurrents ont trust bar ou logos", "Trust bar AVANT hero = differentiant"],
        ["Token section", "3/5 ont section token dediee", "AKYRA combine Token + Presale (bon)"],
        ["Roadmap", "3/5 ont roadmap visible", "AKYRA a une roadmap factuelle (avantage)"],
        ["Metrics affichees", "Mixes reels/vanity (users, TVL, price)", "AKYRA = metrics tech only (credible)"],
        ["CTA frequency", "1 CTA toutes les 2-3 sections", "12-17 CTAs par page en moyenne"],
        ["Risk disclosure", "0/5 ont un risk disclosure franc", "AKYRA = unique (honesty = trust)"],
    ]
    story.append(make_table(key_findings, col_widths=[W*0.25, W*0.40, W*0.35]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 2. VIRTUALS PROTOCOL
    # ═══════════════════════════════════════════
    story.append(Paragraph("2. AUDIT : VIRTUALS PROTOCOL", style_h1))
    story.append(Paragraph("virtuals.io | Market Cap: $2B+ | Base L2", style_subtitle))
    story.append(hr())

    story.append(Paragraph("STRUCTURE DE LA PAGE (11 sections)", style_h2))
    vp_sections = [
        ["#", "Section", "Contenu", "CTA"],
        ["1", "Nav", "Logo + liens app + Launch App", "Launch App"],
        ["2", "Hero", "Society of AI Agents + aGDP concept", "Open App"],
        ["3", "aGDP Concept", "Agentic GDP = economic framing", "-"],
        ["4", "4 Pillars (cards)", "ACP, Butler, Capital Markets, Robotics", "-"],
        ["5", "ACP Deep-dive", "Agent-to-agent commerce standard", "-"],
        ["6", "Butler Deep-dive", "Human-to-agent gateway", "-"],
        ["7", "Capital Markets", "Agent tokenization (1B tokens/agent)", "-"],
        ["8", "Robotics", "Physical world extension + video", "Seesaw App"],
        ["9", "Showcase", "Agent/robot cards demo", "-"],
        ["10", "Research", "Whitepaper link", "Read Whitepaper"],
        ["11", "CTA + Footer", "Join The Society of AI Agents", "Join"],
    ]
    story.append(make_table(vp_sections, col_widths=[W*0.05, W*0.15, W*0.55, W*0.25]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ANALYSE CRITIQUE", style_h2))
    story.append(Paragraph("<b>Forces :</b>", style_body))
    for b in [
        "Economic framing (aGDP) = sophistique, pas crypto-bro",
        "4 pilliers = structure narrative claire et memorable",
        "Pas de section token traditionnelle = maturite",
        "Video robotics = tangibilite, pas juste du texte",
        "18,000+ agents = social proof massif"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph("<b>Faiblesses :</b>", style_body))
    for b in [
        "AUCUN trust bar (audits, tech stack) = black box",
        "Pas de roadmap publique = red flag pour investisseurs serieux",
        "Pas de section architecture = on ne sait pas comment ca marche",
        "Pas de risk disclosure = legal exposure"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph(
        "<b>VERDICT :</b> Site mature, positioning economique sophistique. "
        "Mais manque de transparence technique. AKYRA peut gagner sur la credibilite tech.",
        style_verdict))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 3. OLAS NETWORK
    # ═══════════════════════════════════════════
    story.append(Paragraph("3. AUDIT : OLAS NETWORK", style_h1))
    story.append(Paragraph("olas.network | Multi-chain | Agent co-ownership", style_subtitle))
    story.append(hr())

    story.append(Paragraph("STRUCTURE DE LA PAGE (15 sections)", style_h2))
    olas_sections = [
        ["#", "Section", "Contenu", "CTA"],
        ["1", "Promo Banner", "Get Polystrat (product push)", "Product link"],
        ["2", "Nav", "About, Blog, Resources, Own Your Agent", "Own Your Agent"],
        ["3", "Hero", "'Co-own AI' (3 mots) + social proof avatars", "Own / Get Involved"],
        ["4", "Agent Carousel", "8 specific agents + 'One Token' framing", "Explore Agents"],
        ["5", "Pearl (product)", "AI Agent App-Store", "Own Your Agent"],
        ["6", "Mech Marketplace", "Agent skill marketplace", "Monetize Your Agent"],
        ["7", "Token Economy", "Flywheel diagram + 8 live metrics", "Agent economies"],
        ["8", "Token Details", "Multi-chain (9 chains) + contract address", "Get OLAS / Tokenomics"],
        ["9", "Testimonials", "4 named quotes (Gnosis co-founder, etc.)", "Case Studies"],
        ["10", "Featured In", "9 media logos (Forbes, CoinDesk, etc.)", "-"],
        ["11", "Chains", "9 supported networks", "-"],
        ["12", "Builders", "15 builder partner logos", "-"],
        ["13", "Friends", "23 partner logos (Safe, The Graph, etc.)", "-"],
        ["14", "Videos", "Podcasts and video content", "See all"],
        ["15", "Footer", "Full DAO structure links", "Newsletter"],
    ]
    story.append(make_table(olas_sections, col_widths=[W*0.04, W*0.14, W*0.52, W*0.30]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ANALYSE CRITIQUE", style_h2))
    story.append(Paragraph("<b>Forces :</b>", style_body))
    for b in [
        "Hero ultra-concis : 'Co-own AI' (3 mots) = memorable",
        "Social proof massive : testimonials nommes, 9 medias, 23 partenaires",
        "Live metrics token (staked, burned, DAAs) = transparence",
        "Multi-chain support visible = reach + credibilite",
        "Audit implicite via Cantina, Code4rena, Immunefi dans partenaires"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph("<b>Faiblesses :</b>", style_body))
    for b in [
        "15 sections = TROP LONG (fatigue utilisateur, 2 sections de logo walls)",
        "'Own Your Agent' repete 3x = sur-CTA, perd en impact",
        "OLAS Burned = $0 affiche = signal negatif non-voulu",
        "Pas de section architecture = comment ca marche?"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph(
        "<b>VERDICT :</b> Champion du social proof (logos, testimonials, media). "
        "Mais trop de sections dilue le message. AKYRA doit avoir du social proof "
        "SANS tomber dans le logo-wall excessif.",
        style_verdict))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 4. FETCH.AI
    # ═══════════════════════════════════════════
    story.append(Paragraph("4. AUDIT : FETCH.AI", style_h1))
    story.append(Paragraph("fetch.ai | ASI Alliance | Consumer AI focus", style_subtitle))
    story.append(hr())

    story.append(Paragraph("STRUCTURE DE LA PAGE (12 sections)", style_h2))
    fetch_sections = [
        ["#", "Section", "Contenu", "CTA"],
        ["1", "Nav", "3 produits (ASI:One, Business, Agentverse)", "Get Started"],
        ["2", "Hero", "'Your personal AI' + 'Continue with Google'", "Sign up (Google)"],
        ["3", "See in Action", "3-step process + video embed", "-"],
        ["4", "Use Cases", "4 interactive prompt cards", "Try Prompt (x4)"],
        ["5", "Architecture", "3 sub-products explained", "Create / Explore"],
        ["6", "Brand Partners", "6 logos (Nike, Hilton, Alaska, Sephora)", "-"],
        ["7", "B2B Section", "Brand agents for businesses", "Fetch Business"],
        ["8", "Dev Resources", "5 resource cards (docs, SDK)", "Learn More"],
        ["9", "Events/Blog", "Hackathon + article", "Details / Read"],
        ["10", "Footer", "5 columns + newsletter", "Subscribe"],
    ]
    story.append(make_table(fetch_sections, col_widths=[W*0.04, W*0.14, W*0.52, W*0.30]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ANALYSE CRITIQUE", style_h2))
    story.append(Paragraph("<b>Forces :</b>", style_body))
    for b in [
        "Crypto TOTALEMENT cache = consumer-first (pas de section token!)",
        "Hero CTA = 'Continue with Google' = sign-up DIRECT (pas 'Learn more')",
        "Prompt cards interactives = user try avant d'acheter",
        "Brand logos (Nike, Hilton) = trust massive non-crypto",
        "2.7M agents metric dans footer = credibility sans vanity"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph("<b>Faiblesses :</b>", style_body))
    for b in [
        "AUCUNE section token/tokenomics = frustrant pour investisseurs crypto",
        "Pas de roadmap = ou va le projet?",
        "Pas d'audit visible = pour un projet de cette taille, inquietant",
        "Consumer focus = pas notre audience (nous = risk-takers crypto)"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph(
        "<b>VERDICT :</b> Meilleure UX du lot (consumer AI product). Mais leur audience "
        "est mass-market, pas crypto-native. AKYRA ne doit PAS copier ce modele. "
        "A retenir : les prompt cards interactives (notre terminal fait pareil).",
        style_verdict))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 5. SINGULARITYNET
    # ═══════════════════════════════════════════
    story.append(Paragraph("5. AUDIT : SINGULARITYNET", style_h1))
    story.append(Paragraph("singularitynet.io | ASI Alliance Founder | AGI Research", style_subtitle))
    story.append(hr())

    story.append(Paragraph("STRUCTURE DE LA PAGE (9 sections)", style_h2))
    snet_sections = [
        ["#", "Section", "Contenu", "CTA"],
        ["1", "Nav", "Mega-menu (What We Do, Foundation, Join, Updates)", "Search"],
        ["2", "Hero", "ASI Alliance founding member + AGI vision", "Explore Alliance / Products"],
        ["3", "Products (x3)", "ASI:Cloud, ASI:Chain, ASI:Create (1 para each)", "Launch / Learn More"],
        ["4", "Research", "AGI & ASI Open Research", "Explore / Publications"],
        ["5", "Token", "ASI Token (FET) + LIVE price, market cap, rank", "Learn More"],
        ["6", "DEEP Program", "Grants/funding for AI devs + video modal", "Join / Watch Video"],
        ["7", "Blog/Updates", "7 articles with dates + thumbnails", "View All"],
        ["8", "Partnerships", "Call for partnership applications", "Apply"],
        ["9", "Footer", "Newsletter + social + 4 nav columns", "Subscribe"],
    ]
    story.append(make_table(snet_sections, col_widths=[W*0.04, W*0.14, W*0.52, W*0.30]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ANALYSE CRITIQUE", style_h2))
    story.append(Paragraph("<b>Forces :</b>", style_body))
    for b in [
        "LIVE token data (prix, market cap, rank, volume) = transparence maximum",
        "Powered by CoinMarketCap = source tierce credible",
        "Research section = credibilite academique (publications)",
        "DEEP grants program = ecosystem investment visible",
        "Blog avec 7 articles recents = projet actif, pas mort",
        "9 sections = concis, pas de fluff"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph("<b>Faiblesses :</b>", style_body))
    for b in [
        "Hero vision-first (pas product) = peut confuser les non-inities",
        "Pas de trust bar (audits, partenaires) = manque",
        "Products = 1 paragraphe chacun = trop high-level",
        "17 CTAs = CTA fatigue"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph(
        "<b>VERDICT :</b> Meilleur equilibre vision/produit/token du lot. "
        "Le live token feed est un pattern a considerer post-TGE. "
        "AKYRA devrait s'inspirer de leur section Research pour credibilite.",
        style_verdict))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 6. OCEAN PROTOCOL
    # ═══════════════════════════════════════════
    story.append(Paragraph("6. AUDIT : OCEAN PROTOCOL", style_h1))
    story.append(Paragraph("oceanprotocol.com | Data NFTs | Compute-to-Data", style_subtitle))
    story.append(hr())

    story.append(Paragraph("STRUCTURE DE LA PAGE (12 sections)", style_h2))
    ocean_sections = [
        ["#", "Section", "Contenu", "CTA"],
        ["1", "Nav (sticky)", "Logo + Build/Explore/About + CTA button", "Primary CTA"],
        ["2", "Hero", "'Tokenized AI & Data' + wave visual", "Get Started / Explore"],
        ["3", "Feature Cards", "Product capabilities grid", "Per-card actions"],
        ["4", "Metrics", "Gradient stat cards (1.4M nodes, $2B volume)", "-"],
        ["5", "Partner Logos", "Auto-fit logo grid", "-"],
        ["6", "Data NFTs", "Enhanced ERC721 + ERC725y metadata", "-"],
        ["7", "Compute-to-Data", "Privacy-preserving computation", "-"],
        ["8", "Ocean Nodes", "1.4M nodes in 70+ countries", "-"],
        ["9", "Predictoor", "Prediction market product", "-"],
        ["10", "Token", "$OCEAN details + exchange listings", "Buy on exchanges"],
        ["11", "Roadmap", "Flag-based timeline with quarters", "-"],
        ["12", "Footer", "Address + social + newsletter + legal", "Subscribe"],
    ]
    story.append(make_table(ocean_sections, col_widths=[W*0.04, W*0.14, W*0.52, W*0.30]))
    story.append(Spacer(1, 8))

    story.append(Paragraph("ANALYSE CRITIQUE", style_h2))
    story.append(Paragraph("<b>Forces :</b>", style_body))
    for b in [
        "AUDITS VISIBLES : Trail of Bits + CertiK = gold standard",
        "Metrics concrets : 1.4M nodes, $2B volume, 70+ pays",
        "Roadmap par quarters = timeline claire",
        "Multiple produits bien expliques (Data NFTs, C2D, Nodes, Predictoor)",
        "Exchange listings visibles = liquidite signal"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph("<b>Faiblesses :</b>", style_body))
    for b in [
        "Client-side rendered = SEO faible",
        "Beaucoup de jargon technique (ERC725y, C2D) = barrier d'entree",
        "Token departed ASI Alliance = narratif complique",
        "Design un peu date (purple/pink gradient era)"
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Paragraph(
        "<b>VERDICT :</b> Meilleure transparence technique du lot (audits Trail of Bits + CertiK, "
        "metrics reels, roadmap). AKYRA devrait s'inspirer de leur approche audit-forward "
        "et metrics-reels. Notre avantage : design superieur + positioning plus radical.",
        style_verdict))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 7. ANALYSE COMPARATIVE GLOBALE
    # ═══════════════════════════════════════════
    story.append(Paragraph("7. ANALYSE COMPARATIVE GLOBALE", style_h1))
    story.append(hr())

    story.append(Paragraph("MATRICE DE COMPARAISON", style_h2))
    matrix = [
        ["Element", "Virtuals", "Olas", "Fetch", "SNET", "Ocean", "AKYRA"],
        ["Sections", "11", "15", "10", "9", "12", "10"],
        ["Trust Bar", "Non", "Non", "Logos", "Non", "Non", "OUI"],
        ["Hero Words", "~8", "3", "3", "~12", "~6", "6"],
        ["Hero CTAs", "1", "2", "1", "2", "2", "2"],
        ["Architecture", "Non", "Non", "3 sub", "3 cards", "4 prods", "3 layers"],
        ["Token Section", "Non", "Oui", "Non", "Live data", "Oui", "Oui"],
        ["Roadmap", "Non", "Non", "Non", "Non", "Oui", "OUI"],
        ["Audits Visibles", "Non", "Implicite", "Non", "Non", "Oui", "OUI"],
        ["Testimonials", "Non", "4 quotes", "Non", "Non", "Non", "Non*"],
        ["Media Logos", "Non", "9 logos", "6 brands", "Non", "Partners", "Non*"],
        ["Interactive", "Non", "Non", "Prompts", "Video", "Non", "Terminal"],
        ["Risk Disclosure", "Non", "Non", "Non", "Non", "Non", "OUI"],
        ["Comparative USP", "Non", "Non", "Non", "Non", "Non", "OUI"],
    ]
    story.append(make_table(matrix, col_widths=[W*0.18, W*0.13, W*0.13, W*0.13, W*0.13, W*0.13, W*0.17]))
    story.append(Paragraph("* A ajouter post-beta (testimonials, media)", style_small))
    story.append(Spacer(1, 12))

    story.append(Paragraph("SCORE GLOBAL PAR CRITERE", style_h2))
    scores = [
        ["Critere (note /5)", "Virtuals", "Olas", "Fetch", "SNET", "Ocean", "AKYRA"],
        ["Clarte du message", "4", "3", "5", "3", "3", "5"],
        ["Credibilite technique", "2", "3", "2", "4", "5", "5"],
        ["Social proof", "3", "5", "4", "3", "3", "2*"],
        ["Conversion funnel", "3", "4", "5", "3", "3", "4"],
        ["Design / UX", "4", "3", "5", "3", "2", "4"],
        ["Transparence", "2", "4", "1", "4", "5", "5"],
        ["Differentiation", "4", "3", "3", "3", "3", "5"],
        ["TOTAL /35", "22", "25", "25", "23", "24", "30*"],
    ]
    story.append(make_table(scores, col_widths=[W*0.22, W*0.13, W*0.13, W*0.13, W*0.13, W*0.13, W*0.13]))
    story.append(Paragraph("* Social proof AKYRA = 2 maintenant, 4+ apres beta/testnet public. "
        "Score final post-beta estim 32/35.", style_small))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 8. PATTERNS GAGNANTS
    # ═══════════════════════════════════════════
    story.append(Paragraph("8. PATTERNS GAGNANTS IDENTIFIES", style_h1))
    story.append(hr())

    patterns = [
        ("PATTERN 1 : Hero ultra-concis (3-6 mots)",
         "Olas ('Co-own AI'), Fetch ('Your personal AI') prouvent qu'un hero court est plus "
         "memorable qu'un hero long. AKYRA : 'AKYRA starts where your authority ends' = 6 mots cles. "
         "C'est dans le sweet spot. NE PAS allonger.",
         "GARDER tel quel"),

        ("PATTERN 2 : Trust AVANT le pitch",
         "Ocean et AKYRA sont les seuls a montrer des audits. Olas montre des logos partenaires. "
         "Fetch montre Nike/Hilton. Le pattern : montrer la credibilite AVANT de pitcher le produit "
         "baisse les defenses du visiteur.",
         "Trust bar AKYRA = avantage unique, GARDER en position 2"),

        ("PATTERN 3 : 2 CTAs par hero (Primary + Secondary)",
         "4/5 concurrents ont 2 CTAs dans le hero. Le pattern : 1 action forte ('Deploy', 'Launch') + "
         "1 action douce ('Learn more', 'How it works'). AKYRA fait deja ca.",
         "GARDER : 'Deploy your AI' + 'How it works'"),

        ("PATTERN 4 : Element interactif unique",
         "Fetch = prompt cards, SingularityNET = video modal, AKYRA = terminal simulation. "
         "Chaque projet a UN element interactif qui engage. Le terminal AKYRA est le meilleur "
         "du lot car il simule le PRODUIT, pas juste du contenu.",
         "GARDER le terminal, c'est un differentiant"),

        ("PATTERN 5 : Metrics reels, pas vanity",
         "Olas affiche 'OLAS Burned = $0' (erreur). Virtuals n'affiche rien de verifiable. "
         "Ocean affiche 1.4M nodes (reel). SingularityNET affiche live price (reel). "
         "AKYRA affiche 1B supply, 14 contracts, 3 audits = TOUT verifiable.",
         "CONTINUER avec metrics verifiables uniquement"),

        ("PATTERN 6 : Section comparative (unique AKYRA)",
         "AUCUN concurrent n'a de section 'Why Different' comparative. C'est un angle mort. "
         "AKYRA est le SEUL a dire explicitement 'vs Virtuals, vs Coinbase'. "
         "Ca eduque le visiteur et controle la narrative.",
         "USP UNIQUE, ne pas supprimer"),

        ("PATTERN 7 : Roadmap factuelle",
         "Seul Ocean a une roadmap visible. Les autres cachent leur timeline. "
         "AKYRA affiche des milestones avec statut (fait/en cours/a venir). "
         "C'est un signal de confiance MAJEUR pour une presale.",
         "GARDER, ajouter des dates precises quand disponibles"),

        ("PATTERN 8 : Risk disclosure (unique AKYRA)",
         "ZERO concurrent ne dit 'you can lose 100%'. AKYRA est le seul. "
         "C'est paradoxalement un avantage : honesty = trust. "
         "Ca filtre les mauvais investisseurs et protege legalement.",
         "USP UNIQUE, garder dans FAQ"),
    ]

    for title, body, action in patterns:
        story.append(Paragraph(title, style_h3))
        story.append(Paragraph(body, style_body))
        story.append(Paragraph("<b>Action AKYRA :</b> " + action, style_verdict))
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 9. STRUCTURE RECOMMANDEE AKYRA
    # ═══════════════════════════════════════════
    story.append(Paragraph("9. STRUCTURE RECOMMANDEE POUR AKYRA", style_h1))
    story.append(hr())

    story.append(Paragraph(
        "Basee sur l'analyse des 5 concurrents et les donnees reelles du projet AKYRA, "
        "voici la structure optimale de la landing page :", style_body))
    story.append(Spacer(1, 8))

    structure = [
        ["#", "Section", "Objectif", "Inspire de", "Status"],
        ["1", "NAV", "Orientation + Trust badge + CTA", "Olas (badge), Fetch (minimal)", "OK"],
        ["2", "TRUST BAR", "Credibilite avant pitch", "UNIQUE (aucun concurrent)", "OK"],
        ["3", "HERO", "Positioning radical + CTAs + Vitalik", "SNET (vision) + UNIQUE", "OK"],
        ["4", "HOW IT WORKS", "Simplifier produit (3 steps + Tick)", "Fetch (3 steps) + UNIQUE", "OK"],
        ["5", "WHY DIFFERENT", "Comparative USP (3 cards)", "UNIQUE (aucun concurrent)", "OK"],
        ["6", "ARCHITECTURE", "Credibilite tech (3 layers)", "SNET (3 products) + Ocean", "OK"],
        ["7", "TOKEN & PRESALE", "Conversion (500 slots + terminal)", "Ocean (token) + UNIQUE", "OK"],
        ["8", "ROADMAP", "Timeline factuelle", "Ocean (quarters)", "OK"],
        ["9", "FAQ", "Handle objections + risk", "UNIQUE (risk disclosure)", "OK"],
        ["10", "CTA + FOOTER", "Final conversion", "Tous (standard)", "OK"],
    ]
    story.append(make_table(structure, col_widths=[W*0.04, W*0.14, W*0.28, W*0.34, W*0.08]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("ELEMENTS A AJOUTER POST-BETA", style_h2))
    post_beta = [
        ["Element", "Quand", "Inspire de", "Priorite"],
        ["Testimonials (3-5 quotes)", "Apres beta fermee (Avril 2026)", "Olas (named quotes)", "Haute"],
        ["Media logos (si coverage)", "Apres PR push (Mai 2026)", "Olas (9 logos), Fetch (6)", "Moyenne"],
        ["Live token data", "Apres TGE (Sept 2026)", "SingularityNET (CMC feed)", "Haute"],
        ["Video explainer", "Si budget disponible", "SingularityNET (modal video)", "Basse"],
        ["Agent counter reel", "Quand testnet public", "Olas (DAAs), Ocean (nodes)", "Haute"],
    ]
    story.append(make_table(post_beta, col_widths=[W*0.28, W*0.25, W*0.30, W*0.17]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("ELEMENTS A NE JAMAIS AJOUTER", style_h2))
    never = [
        ["Element", "Pourquoi", "Concurrent qui le fait (mal)"],
        ["Fake stats (simulated TPS, users)", "Detruit la credibilite", "Ancien site AKYRA"],
        ["15+ sections", "Fatigue, dilue le message", "Olas (15 sections)"],
        ["Token price ticker (pre-TGE)", "Pas de token encore", "-"],
        ["Hype words ('revolutionary')", "Generic, pas credible", "Generic crypto projects"],
        ["Auto-play video", "Annoying, augmente bounce rate", "-"],
        ["Multiple logo walls", "Diminishing returns apres le 1er", "Olas (3 logo sections)"],
    ]
    story.append(make_table(never, col_widths=[W*0.28, W*0.42, W*0.30]))
    story.append(PageBreak())

    # ═══════════════════════════════════════════
    # 10. PLAN D'IMPLEMENTATION
    # ═══════════════════════════════════════════
    story.append(Paragraph("10. PLAN D'IMPLEMENTATION", style_h1))
    story.append(hr())

    story.append(Paragraph("PHASE 1 : MAINTENANT (Mars 2026)", style_h2))
    story.append(Paragraph(
        "La landing page actuelle est deja alignee avec les best practices identifiees. "
        "Les 10 sections sont en place, le contenu est base sur les donnees reelles du projet, "
        "et les elements differentiants (trust bar, comparative USP, risk disclosure, terminal) "
        "sont implementes.", style_body))
    story.append(Spacer(1, 6))

    story.append(Paragraph("Ajustements immediats recommandes :", style_h3))
    for b in [
        "Ajouter x402 dans le trust bar (standard emergent, signal innovation)",
        "Ajouter ERC-6551 dans la trust bar (agent identity standard utilise)",
        "Verifier tous les liens CTA pointent vers aky.akyra.io",
        "Ajouter lien GitHub dans le footer quand le repo est public",
        "Ajouter schema du Tick Engine plus visuel (fleches, icones)",
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Spacer(1, 8))
    story.append(Paragraph("PHASE 2 : TESTNET PUBLIC (Mai 2026)", style_h2))
    for b in [
        "Remplacer 'Testnet Live' badge par un compteur d'agents reels",
        "Ajouter 3-5 testimonials de beta users",
        "Ajouter metrics reels du testnet (agents, ticks, transactions)",
        "Ajouter 1 video explainer courte (30-60s) si budget",
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Spacer(1, 8))
    story.append(Paragraph("PHASE 3 : PRESALE (Juin 2026)", style_h2))
    for b in [
        "Ajouter barre de progression presale REELLE (X/500 slots filled)",
        "Ajouter countdown timer si date precise",
        "Ajouter media logos si coverage obtenu (PR push Mai)",
        "Ajouter audit report link (Code4rena, Quantstamp)",
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Spacer(1, 8))
    story.append(Paragraph("PHASE 4 : POST-TGE (Sept 2026+)", style_h2))
    for b in [
        "Ajouter live token data (prix, market cap) via CoinMarketCap API",
        "Ajouter exchange listing logos",
        "Transformer la page en hub ecosystem (comme Olas)",
        "Ajouter section 'Build on AKYRA' pour developers",
    ]:
        story.append(Paragraph(b, style_bullet, bulletText="\u2022"))

    story.append(Spacer(1, 16))
    story.append(hr())
    story.append(Paragraph(
        "Ce document a ete genere a partir de l'analyse directe des sites web de "
        "Virtuals Protocol, Olas Network, Fetch.ai, SingularityNET et Ocean Protocol "
        "effectuee le 20 mars 2026.", style_small))
    story.append(Spacer(1, 4))
    story.append(Paragraph("AKYRA | Confidentiel | Mars 2026", style_small))

    # ── BUILD ──
    doc.build(story)
    print("PDF generated successfully.")

if __name__ == "__main__":
    build_pdf()
