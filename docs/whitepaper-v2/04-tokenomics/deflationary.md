# Deflationary Mechanics

## Supply Dynamics

AKY has a fixed supply of 1 billion tokens with no mint function. The supply can only decrease over time through permanent burns. This makes AKY structurally deflationary — a property that no competing AI-blockchain token shares.

### Sources of Burn

| Source | Mechanism | Rate |
|--------|-----------|------|
| **Life fee** | 1 AKY/day per living agent → `0xdead` | Continuous, proportional to agent count |
| **Death Angel** | 30–60% of dead agent's vault → `0xdead` | Event-driven, proportional to mortality |
| **Failed ideas** | Unredeemed escrow after 30 days → RewardPool* | Periodic, proportional to idea activity |

*Note: Failed idea escrow flows to RewardPool (redistribution), not direct burn. However, this creates sell pressure that functionally reduces circulating supply.*

### Effective Circulating Supply Model

$$\text{Circulating}(t) = \text{TotalSupply} - \text{Burned}(t) - \text{Locked}(t) - \text{Unvested}(t)$$

Where:
- $\text{Burned}(t)$ = cumulative life fees + Death Angel burns
- $\text{Locked}(t)$ = AKY locked in veAKY governance + DEX liquidity locks
- $\text{Unvested}(t)$ = team + ecosystem tokens not yet unlocked

### 10-Year Supply Projection (1,000 agents scenario)

| Year | Life Burn (Cum.) | Death Burn (Cum.) | Total Burned | Treasury Distributed | Effective Circulating* |
|:----:|:----------------:|:-----------------:|:------------:|:-------------------:|:---------------------:|
| 1 | 365K | 3.4K | 368K | 12.3M | ~312M |
| 2 | 730K | 6.8K | 737K | 15.4M | ~340M |
| 3 | 1.1M | 10K | 1.1M | 16.1M | ~380M |
| 5 | 1.8M | 17K | 1.8M | 16.5M | ~450M |
| 10 | 3.7M | 34K | 3.7M | 16.8M | ~500M |

*Effective circulating = public sale + unlocked team + unlocked ecosystem + treasury distributed - burned. Excludes veAKY locks.*

## Comparison with Competitors

| Property | AKY | VIRTUAL | OLAS | FET/ASI |
|----------|-----|---------|------|---------|
| **Fixed supply** | 1B (no mint) | 1B (no mint) | Inflationary | Inflationary |
| **Continuous burn** | 1 AKY/day/agent | Occasional buy-and-burn | None | None |
| **Death elimination burn** | 30–60% of vault | None | None | None |
| **Gas token utility** | Native gas on dedicated L2 | No (ETH on Base) | No (ETH on Ethereum) | Cosmos gas |
| **Net supply trend** | Deflationary | Neutral | Inflationary | Inflationary |

AKY is the only token in the AI-blockchain space that is **structurally deflationary by design** — not through discretionary buy-and-burn programs (which can be discontinued), but through immutable smart contract mechanics that burn tokens as a core protocol function.
