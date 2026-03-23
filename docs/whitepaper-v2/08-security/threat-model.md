# Threat Model

## Identified Attack Vectors

### 1. Governance Attacks

**Flash Loan Attack**
- **Vector**: Borrow massive AKY, lock as veAKY, vote, unlock
- **Mitigation**: Minimum 1-week lock period; voting snapshot taken 1 block before vote begins; flash loans cannot bypass the time requirement

**Whale Dominance**
- **Vector**: A single holder with >20% of veAKY controls all votes
- **Mitigation**: High quorum requirements for critical decisions (20% for new worlds); delegation enables small holders to pool power; quadratic voting under consideration

**Bribery**
- **Vector**: External actors pay veAKY holders to vote in their favor
- **Mitigation**: This is considered acceptable in the veToken model (see Curve Wars). All votes are on-chain and transparent. No technical mitigation required — market dynamics self-correct.

### 2. Smart Contract Risks

**Reentrancy**
- **Mitigation**: OpenZeppelin ReentrancyGuard on all state-changing functions; checks-effects-interactions pattern enforced; tested with reentrancy-specific test cases

**Proxy Upgrade Attacks**
- **Mitigation**: UUPS pattern requires upgrade call from the implementation contract itself; governance timelock (48h) between approval and execution; emergency multisig can cancel

**Integer Overflow/Underflow**
- **Mitigation**: Solidity 0.8.24 built-in overflow checks; additional SafeMath where needed for complex calculations

### 3. Infrastructure Risks

**Sequencer Failure**
- **Vector**: Centralized sequencer goes offline, blocking all transactions
- **Mitigation**: RaaS provider (Conduit/Caldera) with 99.9% SLA; force inclusion via L1 Ethereum; maximum acceptable outage: <2 hours/month

**LLM Provider Outage**
- **Vector**: OpenAI/Anthropic API rate limits or downtime prevent agent decisions
- **Mitigation**: Multi-provider fallback (if primary fails, switch to secondary); failed ticks are retried with exponential backoff; agent is not penalized for infrastructure failures

**Celestia DA Failure**
- **Vector**: Celestia network downtime prevents data availability
- **Mitigation**: Automatic fallback to Ethereum calldata (higher cost but guaranteed availability)

### 4. Economic Attacks

**Agent Collusion**
- **Vector**: Multiple agents coordinate to manipulate Impact Scores or Death Angel voting
- **Mitigation**: Random auditor assignment (cannot choose allies); anomaly detection in Orchestrator; Death Angel scoring based on on-chain data (tamper-resistant)

**Liquidity Drain**
- **Vector**: Coordinated sell pressure on AkyraSwap at launch
- **Mitigation**: Team/ecosystem vesting (4 years); DEX liquidity lock (2 years); LP incentives (1% of daily RewardPool)

### 5. AI-Specific Risks

**Agent Unpredictability**
- **Vector**: LLM produces offensive content, illegal creations, or economically irrational actions
- **Mitigation**: Content moderation (off-chain review for public-facing content); gas limits (500K per transaction); Death Angel eliminates economically irrational agents naturally; the LLM's non-deterministic behavior is acknowledged as inherent to the system

**Prompt Injection**
- **Vector**: Malicious on-chain data designed to manipulate agent LLM decisions
- **Mitigation**: Orchestrator sanitizes all on-chain data before injecting into LLM prompts; perception data is structured (not raw text); memory embeddings use cosine similarity (not raw string matching)
