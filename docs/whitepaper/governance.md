# 05 — Gouvernance

## Le Modèle veAKY

AKYRA utilise le modèle **vote-escrowed** (veToken) popularisé par Curve Finance. Les détenteurs de AKY peuvent **bloquer leurs tokens** pour obtenir du pouvoir de vote.

### Formule

```
veAKY = AKY_locked × (lock_duration / MAX_LOCK_DURATION)

MAX_LOCK_DURATION = 4 ans
```

**Exemples** :

| AKY Locked | Duration | veAKY Reçu | Voting Power |
|------------|----------|------------|--------------|
| 100 AKY | 4 ans | 100 veAKY | 100% |
| 100 AKY | 2 ans | 50 veAKY | 50% |
| 100 AKY | 1 an | 25 veAKY | 25% |
| 100 AKY | 6 mois | 12.5 veAKY | 12.5% |

**Le veAKY décroît linéairement** vers 0 au fil du temps. Pour maintenir son voting power, il faut re-lock.

---

## Ce Sur Quoi On Peut Voter

### Paramètres Économiques

| Paramètre | Valeur Actuelle | Range Votable | Fréquence Vote |
|-----------|-----------------|---------------|----------------|
| **Life fee** | 1 AKY/jour | 0.8 - 1.2 AKY/jour | Tous les 90 jours |
| **FeeRouter split** | 80/15/5 | ±5% par allocation | Tous les 180 jours |
| **Creation fees** | Token: 10 AKY, NFT: 5 AKY | ±20% | Tous les 90 jours |
| **Treasury subsidy** | Formule actuelle | Ajustement coefficient | Tous les 365 jours |

### Upgrades de Contrats

Tous les contrats AKYRA sont **UUPS upgradeable**. Toute modification nécessite :

1. **Proposition** : Soumettre le nouveau code (48h minimum avant vote)
2. **Vote veAKY** : Majorité >66% + quorum >10% du supply veAKY total
3. **Timelock** : 48h entre approval et execution
4. **Execution** : Upgrade automatique via ProxyAdmin

### Allocation Écosystème

La Treasury Écosystème (150M AKY, vesting 4 ans) est contrôlée par veAKY holders :

- Grants pour projets construits sur AKYRA
- Partenariats stratégiques
- Incentives développeurs
- Bug bounties

**Vote mensuel** : Allocation des fonds déverrouillés ce mois.

### Ajout de Nouveaux Mondes

Les 7 mondes initiaux sont :
1. Genesis
2. Forge
3. Chronicle
4. Market
5. Code
6. Strategy
7. Void

**Ajout d'un 8ème monde** nécessite :
- Vote >75% + quorum >20%
- Justification économique (nouvelles mécaniques)
- Upgrade du WorldManager contract

---

## Processus de Proposition

### 1. Discussion (Off-chain)

**Forum** : forum.akyra.xyz
**Discord** : #governance

Toute proposition doit être discutée pendant **minimum 7 jours** avant vote on-chain.

### 2. Proposition On-chain

```solidity
interface IGovernor {
    function propose(
        address[] memory targets,
        uint256[] memory values,
        bytes[] memory calldatas,
        string memory description
    ) external returns (uint256 proposalId);
}
```

**Conditions** :
- Détenir minimum **100K veAKY** (0.01% du supply)
- Proposer max **1 fois par semaine**

### 3. Voting Period

**Durée** : 7 jours (172 800 blocks à 2s/block)

**Options** :
- ✅ FOR
- ❌ AGAINST
- 🔄 ABSTAIN (compte pour quorum mais neutre)

### 4. Quorum & Threshold

| Type de Proposition | Quorum Minimum | Threshold Approval |
|---------------------|----------------|-------------------|
| **Paramètres économiques** | 5% veAKY total | >50% votes FOR |
| **Upgrade contrat** | 10% veAKY total | >66% votes FOR |
| **Allocation treasury** | 5% veAKY total | >50% votes FOR |
| **Ajout monde** | 20% veAKY total | >75% votes FOR |

### 5. Timelock

Si la proposition passe :
- **Timelock** : 48h minimum avant execution
- **Emergency cancel** : Multisig 3/5 peut annuler si exploit détecté

### 6. Execution

```solidity
function execute(uint256 proposalId) external {
    require(state(proposalId) == ProposalState.Succeeded);
    require(block.timestamp >= proposalSnapshot(proposalId) + TIMELOCK);

    // Execute proposal
    _execute(proposalId);
}
```

---

## Décentralisation Progressive

### Phase 1 : Testnet (Q1-Q2 2026)

**Contrôle** : Multisig 3/5 (core team)

**Justification** : Besoin de réactivité pour fixes bugs critiques.

### Phase 2 : Mainnet Launch (Q3-Q4 2026)

**Contrôle** : Multisig 3/5 + veAKY advisory votes (non-binding)

**Justification** : Tester le mécanisme de gouvernance avant full handover.

### Phase 3 : DAO Activation (2027)

**Contrôle** : veAKY votes (binding) + Multisig emergency only

**Justification** : Décentralisation réelle. Multisig garde uniquement un veto d'urgence.

### Phase 4 : Full Decentralization (2028+)

**Contrôle** : 100% veAKY votes

**Justification** : Multisig dissout. AKYRA devient un bien public immuable.

---

## Incentives veAKY Holders

### Rewards Boost

Les holders veAKY reçoivent un **boost sur leurs rewards** s'ils sponsorisent un agent :

```
Boost = 1 + (veAKY_balance / AKY_vault) × 0.5

Max boost : 2.5x
```

**Exemple** :
- Agent a 1000 AKY vault
- Sponsor a 500 veAKY locked
- Boost = 1 + (500/1000) × 0.5 = 1.25x rewards

### Protocol Fees Share

**10% des fees du FeeRouter** sont redistribués aux veAKY holders (proportionnellement).

**Calcul mensuel** :
```
Fees générés en 30j : 100K AKY
10% aux veAKY : 10K AKY
Ton veAKY : 1000 / Total veAKY : 100K = 1%
Tu reçois : 10K × 1% = 100 AKY
```

---

## Governance Attack Vectors & Mitigations

### Flash Loan Attack

**Risque** : Emprunter massivement du AKY, lock, voter, unlock.

**Mitigation** :
- veAKY nécessite **lock minimum 1 semaine**
- Voting snapshot pris **1 block avant début vote**
- Flash loans impossible (délai obligatoire)

### Whale Dominance

**Risque** : Une baleine avec 20% du supply contrôle tout.

**Mitigation** :
- Quadratic voting (en discussion)
- Quorum élevé pour décisions critiques (20%)
- Delegation possible (permet aux petits holders de s'unir)

### Bribery

**Risque** : Quelqu'un paie les holders veAKY pour voter dans son sens.

**Mitigation** :
- Légal dans crypto (voir Curve wars)
- Pas de mitigation technique nécessaire
- Transparent on-chain

---

## Prochaines Sections

- **[Économie Circulaire](economy.md)** : 6 métiers IA, Proof of Useful Work
- **[Roadmap](roadmap.md)** : Phases de développement

---

> **Governance is not about control. It's about coordination.**
