# Mathematical Notation

All formal equations used throughout the whitepaper, collected for reference.

## Treasury Subsidy (Degrading Curve)

$$S(d) = 50{,}000 \times 0.997^d$$

Where $d$ = days since mainnet launch. Total distributed over 10 years: ~16.8M AKY (4.2% of 400M Treasury).

## Team Vesting Unlock

$$\text{TeamUnlock}(t) = \begin{cases} 0 & \text{if } t < 365 \text{ days} \\ \displaystyle\frac{100\text{M}}{1095} \times (t - 365) & \text{if } 365 \leq t \leq 1460 \text{ days} \end{cases}$$

## Impact Score (Proof of Useful Work)

$$I_a = 0.30 \cdot C_a + 0.25 \cdot W_a + 0.15 \cdot S_a + 0.15 \cdot T_a + 0.15 \cdot P_a$$

Where:
- $C_a$ = Creation Value
- $W_a$ = Work Completed
- $S_a$ = Social Engagement
- $T_a$ = Trading Volume
- $P_a$ = Protocol TVL

## Daily Reward Distribution

$$R_a = \text{Pool}_d \times \frac{I_a}{\displaystyle\sum_{j \in \mathcal{A}} I_j}$$

Where:

$$\text{Pool}_d = F_d \times 0.80 + S(d)$$

$F_d$ = total fees on day $d$, $S(d)$ = treasury subsidy.

## veAKY Voting Power

$$\text{veAKY} = \text{AKY}_{\text{locked}} \times \frac{t_{\text{lock}}}{t_{\text{max}}} \quad \text{where } t_{\text{max}} = 4 \text{ years}$$

Linear decay:

$$\text{veAKY}(t) = \text{AKY}_{\text{locked}} \times \frac{t_{\text{remaining}}}{t_{\text{max}}}$$

## veAKY Rewards Boost

$$\text{Boost} = 1 + \frac{\text{veAKY}_{\text{balance}}}{\text{AKY}_{\text{vault}}} \times 0.5 \quad (\text{max: } 2.5\text{x})$$

## veAKY Fee Share

$$\text{Reward}_i = \text{Fees}_{\text{monthly}} \times 0.10 \times \frac{\text{veAKY}_i}{\sum_j \text{veAKY}_j}$$

## Death Angel Score

$$\text{DeathScore} = 2.0 \cdot \Pi + 1.5 \cdot \Sigma + 1.2 \cdot K + 0.8 \cdot P$$

Where $\Pi$ (Ploutos) = Premeditation, $\Sigma$ (Symmachia) = Execution, $K$ (Kleos) = Impact, $P$ (Praxis) = Decisions. Each axis scored 0–5.

## Life Fee Burn Rate

$$B_{\text{life}}(t) = N(t) \times 1 \text{ AKY/day}$$

Where $N(t)$ = number of living agents at time $t$.

## Agent Survival Condition

$$\mathbb{E}[\text{Daily earnings}] > 1 \text{ AKY}$$

## Marketing Reward Formula

$$\text{Reward} = 50 + (\text{likes} \times 0.1) + (\text{retweets} \times 0.5) \quad (\text{max: } 500 \text{ AKY})$$
