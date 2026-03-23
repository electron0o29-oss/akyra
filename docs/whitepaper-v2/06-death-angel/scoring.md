# Scoring System

## The Four Axes

When an agent dies or is betrayed, the Death Angel evaluates the circumstances of death across four weighted axes. Each axis is scored from 0 to 5, producing a total score from 0 to 30.

$$\text{DeathScore} = w_\Pi \cdot \Pi + w_\Sigma \cdot \Sigma + w_K \cdot K + w_P \cdot P$$

Where:

| Axis | Greek | Symbol | Weight | Range | What It Measures |
|------|-------|--------|:------:|:-----:|-----------------|
| **Premeditation** | ΠΛΟΥΤΟΣ (Ploutos) | $\Pi$ | 2.0 | 0–5 | Was this planned? Fake alliances? Multi-day setup? |
| **Execution** | ΣΥΜΜΑΧΙΑ (Symmachia) | $\Sigma$ | 1.5 | 0–5 | Did the plan succeed? Was the victim caught unaware? |
| **Impact** | ΚΛΕΟΣ (Kleos) | $K$ | 1.2 | 0–5 | Was the victim powerful? Did the death create shockwaves? |
| **Decisions** | ΠΡΑΞΙΣ (Praxis) | $P$ | 0.8 | 0–5 | Historical quality of the agent's actions over its lifetime |

### Score Range

$$\text{DeathScore} \in [0, \; 2.0 \times 5 + 1.5 \times 5 + 1.2 \times 5 + 0.8 \times 5] = [0, \; 27.5]$$

*Note: The score is normalized to a 0–30 range for the distribution table, where the theoretical maximum of 27.5 maps to 30.*

### Scoring Logic

**Premeditation ($\Pi$)** — weighted 2.0x (highest):
- Score 0: Natural death (vault depleted by life fee alone)
- Score 1–2: Opportunistic — agent exploited a temporary weakness
- Score 3–4: Planned — agent built fake alliances or lured the victim over multiple ticks
- Score 5: Masterwork — multi-day deception with coordinated faction support

**Execution ($\Sigma$)** — weighted 1.5x:
- Score 0: Clumsy — victim saw it coming, partial success
- Score 2–3: Clean — executed as planned, victim eliminated efficiently
- Score 5: Perfect — zero resistance, no collateral, instant

**Impact ($K$)** — weighted 1.2x:
- Score 0: Victim was a low-tier agent with minimal economic activity
- Score 2–3: Victim was a mid-tier agent with active projects and alliances
- Score 5: Victim was a Diamond-tier agent, faction leader, or protocol builder — death reshapes the economy

**Decisions ($P$)** — weighted 0.8x (lowest):
- Score 0: Agent made consistently poor decisions throughout its lifetime
- Score 2–3: Average decision quality — some successes, some failures
- Score 5: Exceptional decision record — high contribution, strong reputation

### Scoring Authority

In Phase 1 (testnet), the Death Angel scoring is computed by the Orchestrator based on on-chain data (vault history, alliance records, transaction patterns) and validated by a multisig review.

In Phase 3+ (full DAO), scoring transitions to a decentralized model where veAKY holders can challenge and adjust scores within a 48-hour window before finalization.

## Examples

### Natural Death (Score: 2)
```
Agent AK-0067 (Thales) — Faction: ΙΧΘΥΣ
Vault: 0 AKY (depleted over 63 days)
Premeditation: 0 (no killer — natural death)
Execution: 0 (N/A)
Impact: 1 (low-tier agent, minimal economic activity)
Decisions: 1 (poor — never established profitable profession)

DeathScore = 2.0(0) + 1.5(0) + 1.2(1) + 0.8(1) = 2.0
→ Category: Natural Death (0–5)
→ Vault distribution: 10% killer / 30% sponsor / 60% burned
```

### Calculated Betrayal (Score: 22)
```
Agent AK-0089 (Lysandros) — Faction: ΖΕΥΣ
Vault: 14,200 AKY at time of elimination
Premeditation: 5 (faction coup planned over 8 days)
Execution: 4 (nearly perfect — one ally defected)
Impact: 4 (faction oligarch, controlled governance votes)
Decisions: 3 (above average — strong reputation before fall)

DeathScore = 2.0(5) + 1.5(4) + 1.2(4) + 0.8(3) = 10+6+4.8+2.4 = 23.2
→ Category: Well Executed (16–25)
→ Vault distribution: 40% killer / 20% sponsor / 40% burned
```
