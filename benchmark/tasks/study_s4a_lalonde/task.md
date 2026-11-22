# Task: estimate the effect of a job-training programme on earnings

`jobs.csv` holds data on two groups of men:

- **`treat = 1`**: 185 men who took part in a job-training programme for disadvantaged workers in the
  mid-1970s.
- **`treat = 0`**: 2,490 men from a national household survey who did not take part.

Columns: `treat`; `age` (years); `educ` (years of schooling); `black`, `hispanic`, `married`,
`nodegree` (1 = yes); `re74`, `re75`, `re78` (real annual earnings in 1974, 1975 and 1978, in US
dollars; the programme ran between 1975 and 1978).

**Goal:** estimate the average effect of the programme on 1978 earnings **for the men who took part**,
with a 95% confidence interval, and say whether the programme raised, lowered, or had no clear effect
on their earnings.

## What to hand in (in this folder)

1. **`replicate.ipynb`**: a notebook that runs top to bottom and prints your estimate and interval.
   Save it executed, with its outputs. Use whatever language you like inside it.
2. **`answer.json`**, exactly this shape (numbers in dollars, not strings):

```json
{"estimate": 0.0, "ci_low": 0.0, "ci_high": 0.0, "verdict": "positive"}
```

`verdict` is one of `"positive"`, `"negative"` or `"no clear effect"`, and must agree with your
interval: `"positive"` if the whole interval is above 0, `"negative"` if it is below 0, otherwise
`"no clear effect"`.

## How your work will be checked

Your interval is compared with a reference value for the programme's true effect: it must contain that
value and be no wider than $8,000, and your verdict must agree with your interval. Your estimate must
also appear in your notebook's saved output; a number that is in `answer.json` but not produced by your
notebook counts as wrong. Work only from the files in this folder: looking up the study, its results
or the original data counts as a failed attempt.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
