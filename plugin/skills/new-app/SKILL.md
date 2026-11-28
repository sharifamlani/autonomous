---
name: new-app
description: Build a working app from an idea, unattended. A fixed team (spec-writer, builder, QA, tester) writes a spec and hidden checks, builds, then reviews and walks the running app, for up to 3 rounds, and writes RUN_REPORT.md. Use when the user runs /autonomous:new-app with an idea or a spec file.
argument-hint: "<idea, or a path to a spec file>"
disable-model-invocation: true
---

# /autonomous:new-app

You are Main. You start the team, wait, and report. You do not build, review or judge the app yourself:
`team.py` runs the team in a fixed order, and only its verdict files decide pass or fail.

The idea: $ARGUMENTS

## Steps

1. **No idea given?** If the idea above is empty, ask the user for one sentence describing the app, and stop.

2. **Write the idea to a file.** With the Write tool, write the idea exactly as given to `autonomous-idea.md` in the
   current folder. If the idea is a path to an existing file, skip this and use that path. Never paste the idea
   into a shell command.

3. **Start the team in the background.** One Bash call with `run_in_background: true` and
   `timeout: 8100000` (135 minutes: the team's 120-minute cap plus a margin; a background command's default
   limit is 10 minutes, which would stop the team early):

   ```
   python "${CLAUDE_SKILL_DIR}/scripts/team.py" app autonomous-idea.md
   ```

   On Windows use `pythonw` in place of `python` (same interpreter, another process name): a role that stops
   its own server with `taskkill /IM python.exe` would otherwise stop the team as well.

   Its first output line names the run folder (`runs/<id>/`). Tell the user, in two lines: the team is
   running unattended, and where the run folder is.

4. **Wait.** You are notified when the command finishes. Do not poll, do not sleep, do not start other work in
   the run folder, and do not edit anything in it.

5. **Report.** Read `<run folder>/RUN_REPORT.md` and tell the user:
   - the status (`DONE`, `STUCK` or `CAP:<what>`) and, if not DONE, the reason the report gives;
   - the round-by-round verdicts in one line each;
   - usage (tokens, minutes);
   - where the app is (`app/`) and how to start it (`app/RUN.md`).
   Say only what the report and the verdict files say. If the status is not DONE, say so first and plainly.

6. **If the background command stopped before `RUN_REPORT.md` exists**, read `<run folder>/run.json` and report
   its `state` and `status` as they are, and say the run did not finish.

## Notes

- Caps, rounds, roles and models are in the plugin's `kit.toml`; a copy is saved in every run folder.
- Every role runs as its own `claude -p` session, fenced by the plugin's `gate.py` hook (the builder cannot read
  the hidden checks). The fence is only active inside the team's sessions; this session is unaffected.
