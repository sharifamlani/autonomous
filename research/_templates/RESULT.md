# Study NNN — Result

| Field | Entry |
|---|---|
| Verdict | promote / park / kill |
| Net Sharpe (1x costs) | |
| Net Sharpe at 0.5x / 2x costs | |
| t-stat | |
| Deflated Sharpe (trials = N from TRIAL_LOG) | |
| PBO | |
| Recent-data (last 2-3 yrs) result | |
| Sub-period results (incl. 2008, 2020, 2022) | |
| Max drawdown / time to recover (bootstrap) | |
| Capacity at our account size | |
| Holdout looks | (must be 1) |

## Bias checklist (CLAUDE.md §5): answer every row

| Bias | How it was handled |
|---|---|
| Look-ahead | |
| Survivorship | |
| Data snooping / multiple testing | |
| Overfitting | |
| Cost omission | |
| Fold leakage | |
| LLM / pretrained leakage | |
| Period / regime | |
| Publication | |
| Repo/README | |
| Confirmation / sunk cost | |
| Narrative / hindsight | |

## Gate run

Append with `python scripts/factory_gate.py --study NNN_slug --returns <file> --returns-2x <file> --write-result`.

## What failed
