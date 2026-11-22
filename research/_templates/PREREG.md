# Study NNN — <title>

Pre-registration. Commit this file before any result exists (CLAUDE.md §5).

| Field | Entry |
|---|---|
| Hypothesis | |
| Source(s) | (Literature ID, e.g. C4; public repo; prior study) |
| Why the literature can't answer it | (CLAUDE.md §5 "literature first": which search found no answer) |
| Mechanism | (why this change should help) |
| Prior plausibility (before testing) | |
| System under test | (kit version / agents / skills / prompts / model ids) |
| Comparison arm(s) | (no-plugin baseline, previous kit version, alternative config) |
| Task set | (benchmark tasks with known answers or scripted walks; source of each) |
| Dev / held-out split | (held-out tasks never seen while tuning; one look) |
| Runs per arm | (≥ 3; agent runs vary) |
| Metric(s) | (success rate, accuracy vs known answer, tokens/task, wall-clock, human interventions) |
| Grader | (deterministic check / script / LLM judge with its calibration set) |
| Pass thresholds | |
| Cost budget | ($ and tokens; stop when exceeded) |
| Max trials budgeted | |
| Abandonment rule | |
