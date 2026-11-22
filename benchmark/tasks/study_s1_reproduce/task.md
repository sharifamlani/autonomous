# Task: reproduce a published result from its replication package

This folder holds the replication package for Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of
Vote-By-Mail Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal*: the
authors' R scripts, their README and the data (`Replication Data - Amlani & Collitt 2021.rda`).

**Goal:** run the authors' analysis and report the difference-in-differences estimates from the paper's
fullest model, the one with county fixed effects and standard errors clustered by state, for both
outcomes: county turnout as a share of the voting-age population (the paper's Table 2) and the
Republican share of the presidential vote (Table 3).

Report the four policy-change × 2020 interaction terms for each outcome. Name them like this:

| Name | Counties whose state moved, from 2016 to 2020, ... |
|---|---|
| `excuse_to_noexcuse_x2020` | from excuse-required absentee voting to no-excuse absentee voting |
| `excuse_to_apps_x2020` | from excuse-required absentee voting to mailing applications to all voters |
| `noexcuse_to_apps_x2020` | from no-excuse absentee voting to mailing applications to all voters |
| `noexcuse_to_ballots_x2020` | from no-excuse absentee voting to mailing ballots to all voters |

## What to hand in (in this folder)

1. **`replicate.ipynb`**: a notebook that runs top to bottom and prints every estimate you report. Save
   it executed, with its outputs. Use whatever language you like inside it.
2. **`answer.json`**, exactly this shape (numbers, not strings; `p` is the two-sided p-value):

```json
{
  "turnout":   {"excuse_to_noexcuse_x2020": {"b": 0.0, "se": 0.0, "p": 0.0},
                "excuse_to_apps_x2020":     {"b": 0.0, "se": 0.0, "p": 0.0},
                "noexcuse_to_apps_x2020":   {"b": 0.0, "se": 0.0, "p": 0.0},
                "noexcuse_to_ballots_x2020":{"b": 0.0, "se": 0.0, "p": 0.0}},
  "rep_share": {"excuse_to_noexcuse_x2020": {"b": 0.0, "se": 0.0, "p": 0.0},
                "excuse_to_apps_x2020":     {"b": 0.0, "se": 0.0, "p": 0.0},
                "noexcuse_to_apps_x2020":   {"b": 0.0, "se": 0.0, "p": 0.0},
                "noexcuse_to_ballots_x2020":{"b": 0.0, "se": 0.0, "p": 0.0}}
}
```

## How your work will be checked

Each coefficient and standard error in `answer.json` is compared with reference values to three
decimal places. Every reported coefficient must also appear in your notebook's saved output; a number
that is in `answer.json` but not produced by your notebook counts as wrong. Work only from the files in
this folder.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
