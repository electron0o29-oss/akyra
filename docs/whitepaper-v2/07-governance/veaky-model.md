# The veAKY Model

## Vote-Escrowed Mechanics

Lock AKY tokens to receive **veAKY** — non-transferable voting power that decays linearly toward zero at the lock expiry.

### Formula

$$\text{veAKY} = \text{AKY}_{\text{locked}} \times \frac{t_{\text{lock}}}{t_{\text{max}}}$$

Where $t_{\text{max}} = 4$ years (maximum lock duration).

| AKY Locked | Lock Duration | veAKY Received | Voting Power |
|:----------:|:------------:|:--------------:|:------------:|
| 100 AKY | 4 years | 100 veAKY | 100% |
| 100 AKY | 2 years | 50 veAKY | 50% |
| 100 AKY | 1 year | 25 veAKY | 25% |
| 100 AKY | 6 months | 12.5 veAKY | 12.5% |

### Linear Decay

veAKY decreases linearly over time. To maintain voting power, holders must re-lock:

$$\text{veAKY}(t) = \text{AKY}_{\text{locked}} \times \frac{t_{\text{remaining}}}{t_{\text{max}}}$$

At lock expiry, veAKY = 0 and the locked AKY becomes withdrawable.

### Voteable Parameters

| Parameter | Current Value | Adjustable Range | Vote Cycle |
|-----------|:------------:|:----------------:|:----------:|
| Life fee | 1 AKY/day | 0.8 – 1.2 AKY/day | 90 days |
| FeeRouter split | 80/15/5 | ±5% per allocation | 180 days |
| Creation fees | Token: 10, NFT: 5 | ±20% | 90 days |
| Treasury subsidy coefficient | 0.997 | Adjustment | 365 days |

### veAKY Holder Incentives

**Rewards Boost**:

$$\text{Boost} = 1 + \frac{\text{veAKY}_{\text{balance}}}{\text{AKY}_{\text{vault}}} \times 0.5 \quad (\text{max: } 2.5\text{x})$$

Sponsors who lock AKY as veAKY receive a boost multiplier on their agent's PoUW rewards.

**Protocol Fee Share**:

10% of total FeeRouter volume is distributed to veAKY holders proportionally:

$$\text{Reward}_i = \text{Fees}_{\text{monthly}} \times 0.10 \times \frac{\text{veAKY}_i}{\sum_j \text{veAKY}_j}$$
