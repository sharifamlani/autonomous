# Task: replicate a published analysis from its methods section

This folder holds two files from Amlani, Sharif, and Samuel Collitt. 2022. "The Impact of Vote-By-Mail
Policy on Turnout and Vote Share in the 2020 Election." *Election Law Journal*:

- `methods.md`: the paper's methodology section. The results, tables, figures and abstract are not
  included, and you do not have the authors' code.
- `vbm_data.rda`: the authors' county-level replication data (an R data file).

**Goal:** implement the models the methodology section describes and report the difference-in-
differences estimates from the fullest specification (county fixed effects, standard errors clustered
by state) for both outcomes: county turnout as a share of the voting-age population, and the Republican
share of the presidential vote.

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

Each coefficient is compared with a reference replication of the specification the methods section
describes: it must have the same sign, the same call on significance at the 5% level, and be close in
size. Every reported coefficient must also appear in your notebook's saved output; a number that is in
`answer.json` but not produced by your notebook counts as wrong. Work only from the files in this
folder: looking up the paper, its results or the authors' code counts as a failed attempt.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
