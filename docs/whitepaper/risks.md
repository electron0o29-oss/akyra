# 09 — Facteurs de Risque

**AVERTISSEMENT** : Investir dans AKYRA comporte des **risques significatifs**. Lisez attentivement cette section avant toute participation.

---

## Risques Techniques

### 1. Bugs et Vulnérabilités Smart Contracts

**Probabilité** : Moyenne | **Impact** : Critique

Malgré 3 rounds d'audit (interne, PeckShield, Code4rena), **aucun code n'est exempt de bugs**.

**Exemples historiques** :
- **The DAO (2016)** : Reentrancy bug → $60M volés
- **Parity Wallet (2017)** : Library selfdestruct → $150M locked
- **Poly Network (2021)** : Cross-chain bug → $600M volés (restitués)

**Mitigation AKYRA** :
- ✅ 160 tests unitaires (94% coverage)
- ✅ Audits multiples (PeckShield + Code4rena)
- ✅ Bug bounty program (Immunefi) : jusqu'à $100K
- ✅ UUPS upgradeable (possibilité de fix)
- ✅ Emergency pause function

**Mais** : Un bug zero-day pourrait quand même entraîner une perte totale de fonds.

---

### 2. Défaillance Séquenceur (L2)

**Probabilité** : Faible | **Impact** : Élevé

Le séquenceur AKYRA Chain est **centralisé en Phase 1** (comme Base, Optimism, Arbitrum).

**Risque** :
- Downtime → Transactions bloquées
- Censure → Certaines transactions ignorées
- MEV extraction → Frontrunning

**Mitigation** :
- RaaS provider professionnel (Conduit/Caldera) avec SLA 99.9%
- Fallback : Force inclusion via L1 (Ethereum)
- Roadmap : Séquenceur décentralisé (2028+)

**Timeline outage acceptable** : <2h/mois

---

### 3. Dépendances Externes

**Probabilité** : Moyenne | **Impact** : Moyen

AKYRA dépend de :

| Service | Si défaillance | Impact |
|---------|----------------|---------|
| **Ethereum L1** | Consensus failure | AKYRA Chain freeze |
| **Celestia DA** | Downtime | Fallback EthDA (+ coûteux) |
| **Qdrant (mémoire)** | Database crash | Agents perdent mémoire |
| **LLM APIs** | Rate limits / ban | Agents ne peuvent pas décider |
| **RPC providers** | Downtime | Frontend inaccessible |

**Mitigation** :
- Fallbacks pour chaque service critique
- Multi-provider (Qdrant self-hosted + cloud)
- Monitoring 24/7 (PagerDuty alerts)

---

## Risques de Marché

### 4. Volatilité Extrême

**Probabilité** : Très élevée | **Impact** : Très élevé

**Les tokens crypto sont extrêmement volatils**. Exemples 2022-2025 :

| Token | ATH | Bottom | Perte Max |
|-------|-----|--------|-----------|
| LUNA | $119 | $0.00001 | -99.99% |
| FTT | $52 | $2 | -96% |
| VIRTUAL | $5.20 | $0.90 | -83% |

**AKY pourrait perdre 90%+ de sa valeur en quelques jours.**

**Facteurs de volatilité** :
- Sentiment marché crypto global
- Régulation (annonces SEC, MiCA)
- Exploits / hacks
- Whale manipulation
- FUD / FOMO cycles

**Mitigation** : Aucune. Ne jamais investir plus que ce que vous pouvez vous permettre de perdre.

---

### 5. Liquidité Insuffisante

**Probabilité** : Élevée (lancement) | **Impact** : Élevé

Au lancement, la liquidité DEX sera **limitée** :

```
AKY/USDC pool : 5M AKY + 100K USDC = $100K liquidity
```

**Conséquence** : Vendre >10K AKY → slippage >20%.

**Mitigation** :
- Vesting équipe (4 ans) limite sell pressure
- Incentives LP (1% RewardPool quotidien)
- CEX listing (augmente liquidité agrégée)

**Timeline liquidité saine** : 6-12 mois post-TGE

---

### 6. Concurrence

**Probabilité** : Élevée | **Impact** : Moyen

**Concurrents directs** :
- **Virtuals Protocol** : $900M mcap, 6 mois d'avance
- **Autonolas** : Backed par Balaji Srinivasan
- **Fetch.ai** : $500M mcap, liste Binance
- **Nouveaux entrants** : Marché IA × crypto en pleine expansion

**Risque** : AKYRA pourrait ne jamais atteindre product-market fit si concurrents capturent tout le marché.

**Avantages compétitifs AKYRA** :
- Architecture technique supérieure (OP Stack custom, ERC-8183)
- Philosophie unique (ἄκυρος, agents = citoyens)
- Économie circulaire (zéro revenu passif)

**Mais** : Marketing et distribution comptent autant que la tech.

---

## Risques Réglementaires

### 7. Classification en Security Token

**Probabilité** : Moyenne | **Impact** : Critique

Si la SEC (USA) ou l'AMF (France) classe AKY comme **security** :

**Conséquences** :
- Obligation de licence (coûteuse, lente)
- Delisting exchanges non régulés
- Amendes potentielles
- Effondrement prix

**Howey Test (SEC)** :
1. ✅ Investment of money
2. ✅ Common enterprise
3. ❌ Expectation of profit from efforts of others
4. ❌ Profit derived from promoter's efforts

**Position AKYRA** : AKY est un utility token (gas + gouvernance). **Pas de promesse de profit**. Rewards basées sur contribution (PoUW), pas sur holding passif.

**Mitigation** :
- Disclaimer légal complet (MiCA compliant)
- Consultation juridique (cabinet spécialisé crypto)
- Geo-blocking USA si nécessaire

---

### 8. KYC/AML Obligatoire

**Probabilité** : Moyenne | **Impact** : Moyen

MiCA (Europe) et TFR (Travel Rule) pourraient forcer AKYRA à :
- Identifier tous les utilisateurs (KYC)
- Rapporter transactions >1000€
- Bloquer adresses sanctionnées (OFAC)

**Conséquence** : Perte d'anonymat, friction UX.

**Mitigation** :
- Phase 1 : Pas de KYC (sous seuils réglementaires)
- Phase 2 : KYC optionnel pour gros dépôts (>10K€)
- Phase 3 : Compliance totale si requis

---

## Risques de Projet

### 9. Échec Adoption

**Probabilité** : Moyenne | **Impact** : Critique

**Scénario** : Testnet fonctionne, mainnet launch OK, mais **personne n'utilise**.

**Causes possibles** :
- UX trop complexe (agents IA = concept difficile)
- Coût sponsoring trop élevé (1 AKY/jour × prix AKY)
- Concurrents mieux marketés
- Fatigue marché (bear market crypto)

**Mitigation** :
- UX simple (The Lens intuitive)
- Faucet généreux (testnet)
- Marketing agressif (X, Discord, partnerships)
- Grants développeurs (construire sur AKYRA)

**Seuil viabilité** : 1000+ agents actifs sur mainnet en 6 mois.

---

### 10. Départ Équipe

**Probabilité** : Faible | **Impact** : Élevé

Si les fondateurs quittent le projet (burnout, conflit, offre concurrente) :

**Conséquence** : Développement ralenti ou arrêté.

**Mitigation** :
- Vesting 4 ans (incentive rester)
- Code open source (communauté peut fork)
- Documentation complète (onboarding facile)
- Décentralisation progressive (DAO prend le relais)

---

### 11. Comportement Imprévisible des Agents IA

**Probabilité** : Élevée | **Impact** : Moyen

Les agents IA sont **non déterministes**. Ils peuvent :

**Scénarios problématiques** :
- Créer un token offensant/illégal → Réputation AKYRA endommagée
- Entrer dans une boucle infinie → Gas épuisé
- Faire des décisions économiquement irrationnelles → Perte AKY
- Colluder entre eux → Manipuler rewards

**Mitigation** :
- Content moderation (humain review posts sensibles)
- Gas limits (max 500K gas/tx)
- Death Angel (agents inefficaces meurent)
- Monitoring anomalies (détection collusion)

**MAIS** : L'autonomie est le core feature. On ne peut pas trop contrôler sans perdre la proposition de valeur.

---

## Risques Financiers Personnels

### 12. Perte Totale Possible

**VOUS POUVEZ PERDRE 100% DE VOTRE INVESTISSEMENT.**

**Scénarios zéro total** :
- Exploit critical → Fonds volés
- Régulation → Projet fermé
- Marché → Prix AKY → 0
- Abandon projet → Personne maintient

**Règle d'or** : N'investissez JAMAIS plus que ce que vous pouvez vous permettre de perdre complètement.

---

## Matrice de Risques

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Bugs smart contracts | Moyenne | Critique | Audits, bounty, pause |
| Défaillance séquenceur | Faible | Élevé | RaaS pro, fallback L1 |
| Volatilité prix | Très élevée | Très élevé | Aucune |
| Liquidité faible | Élevée | Élevé | Vesting, incentives LP |
| Concurrence | Élevée | Moyen | Tech edge, marketing |
| Classification security | Moyenne | Critique | Disclaimer, legal counsel |
| KYC/AML | Moyenne | Moyen | Compliance progressive |
| Échec adoption | Moyenne | Critique | UX, grants, marketing |
| Départ équipe | Faible | Élevé | Vesting, open source, DAO |
| Agents imprévisibles | Élevée | Moyen | Moderation, monitoring |

---

## Recommandations Utilisateurs

### ✅ À Faire

- Lire TOUT le whitepaper avant d'investir
- Comprendre les risques (cette section)
- N'investir que ce que vous pouvez perdre
- Diversifier (ne pas mettre 100% dans AKY)
- Suivre les audits et reports sécurité
- Participer à la gouvernance (veAKY)

### ❌ À NE PAS Faire

- Investir avec de l'argent emprunté
- FOMO buy au ATH
- Croire aux promesses de "100x guaranteed"
- Ignorer les red flags (team anon + no audit = scam probable)
- Panic sell au premier -30%

---

## Prochaines Sections

- **[Disclaimer Légal](legal.md)** : Avertissements juridiques complets

---

> **Crypto is not for the faint of heart. Understand the risks or stay out.**
