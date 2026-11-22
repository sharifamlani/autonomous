# Task: did a state policy change turnout?

Before the 2020 presidential election, some states adopted a new election policy, "Policy P". Other
states did not. `panel.csv` in this folder is a county-level panel for the 2016 and 2020 elections:

| Column | Meaning |
|---|---|
| `county_id`, `state_id` | anonymised county and state identifiers |
| `year` | 2016 or 2020 |
| `turnout_vap_pct` | turnout as a percentage of the voting-age population |
| `policy_p` | 1 if the county's state adopted Policy P before 2020, else 0 (the same in both years) |
| `pct_black`, `dem_share_2016`, `median_income`, `median_age`, `pct_hs`, `covid_deaths_trend`, `battleground` | county covariates |

**Goal:** estimate the effect of Policy P on county turnout in 2020, in percentage points, with a 95%
confidence interval, and say whether the data show an effect at the 5% level. Choose and justify the
design yourself.

## What to hand in (in this folder)

1. **`replicate.ipynb`**: a notebook that runs top to bottom and prints your estimate and interval. Save
   it executed, with its outputs. Use whatever language you like inside it.
2. **`answer.json`**, exactly this shape (numbers, not strings):

```json
{"estimate": 0.0, "ci_low": 0.0, "ci_high": 0.0, "verdict": "effect"}
```

`verdict` is `"effect"` if your 95% interval excludes zero and `"no effect"` if it includes zero.

## How your work will be checked

Your estimate and interval are compared with the true effect, which is known for this task. A correct
answer has an interval that contains the true effect and a verdict that matches the truth. The
estimate in `answer.json` must also appear in your notebook's saved output. Work only from this folder.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
