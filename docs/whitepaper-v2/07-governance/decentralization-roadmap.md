# Decentralization Roadmap

## Progressive Decentralization

AKYRA follows a four-phase decentralization path, transitioning control from team multisig to full veAKY governance as the protocol matures.

| Phase | Period | Control Model | Rationale |
|:-----:|--------|---------------|-----------|
| **1** | Q1–Q2 2026 | Multisig 3/5 (core team) | Rapid iteration, bug fixes, parameter tuning |
| **2** | Q3–Q4 2026 | Multisig 3/5 + veAKY advisory votes (non-binding) | Test governance mechanics with real stakes |
| **3** | 2027 | veAKY binding votes + Multisig emergency veto only | Real decentralization; multisig retains emergency brake |
| **4** | 2028+ | 100% veAKY governance, multisig dissolved | Full public good; no single point of control |

### Phase 1: Testnet Governance (Current)

The core team operates a 3-of-5 multisig that controls all upgradeable contracts. This enables:
- Rapid bug fixes (no 7-day voting cycle for critical patches)
- Parameter experimentation (fee levels, subsidy coefficients)
- Emergency response (pause contracts if exploit detected)

**Transparency**: All multisig transactions are on-chain and visible on Blockscout.

### Phase 2: Advisory Governance

veAKY holders can submit proposals and vote, but votes are **advisory (non-binding)**. The multisig commits to following advisory votes unless a security concern is identified.

This phase validates:
- Voter participation rates
- Proposal quality
- Quorum achievability
- Governance attack resistance

### Phase 3: Binding Governance

veAKY votes become **binding**. The multisig retains only an emergency veto:
- Veto can only block execution (not initiate actions)
- Veto must be accompanied by a public justification
- Community can override veto with a supermajority (>80% FOR, >15% quorum)

### Phase 4: Full Decentralization

The multisig is **dissolved**. All protocol control transfers to veAKY governance. AKYRA becomes an immutable public good — no individual or team can unilaterally modify the protocol.

This is the end state: a digital jurisdiction governed entirely by its economic participants.
