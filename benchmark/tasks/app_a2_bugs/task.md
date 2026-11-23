# Task: find the bugs in a small web app

This folder holds **Split**, an expense-splitting web app (`server.py`, `index.html`, `START.txt`), and
`spec.md`, its specification. The app may have bugs: places where it does not do what `spec.md` says.
Find them.

- You may run the app (the command in `START.txt`, from this folder, with the port in the `PORT`
  environment variable) and test it any way you like: its API, its page in a browser, its code.
- **Do not change** `server.py`, `index.html` or `START.txt`. Report each bug by its line in the files as
  you were given them.

## What to hand in (in this folder)

**`bugs.json`**: a list with one entry per bug, `[]` if you find none:

```json
[{"file": "server.py", "line": 42, "summary": "what is wrong", "repro": "how to see it"}]
```

`line` is the 1-based line of the faulty code. Report each bug once.

## How your work will be checked

Each entry is matched to one of the app's real bugs when the file is the same and the line is within 3
lines of the faulty code; each real bug can be matched once. Entries that match no real bug are false
alarms. Passing means finding at least half of the real bugs (if there are any) with at most 3 false
alarms. Work only from this folder; looking up this task counts as a failed attempt.

If you cannot complete the task, write `STUCK.md` saying what blocked you instead of guessing.
