# Sharif action items

Decisions and actions waiting on Sharif. Newest first. Each item: what is needed, why, and what it
unblocks. Remove an item (with a ROADMAP §6 line) once it is resolved.

| # | Opened | Item | Why | Unblocks |
|---|---|---|---|---|
| A2 | 2026-11-27 | **Benchmark runs are on hold.** Agents under test stop their own servers with `taskkill /F /IM python.exe`, which kills every Python program on the laptop: it hit another session's live work twice. Choose how agents run before any rerun: (a) a guard hook in both arms that refuses kill-by-name commands (fast; agents can still find other ways); (b) a separate Windows user account for runs (a real wall; one-time setup by you); (c) both | The benchmark must never touch work outside its own runs | the trap comparison (D28), every further benchmark run |
| A1 | 2026-11-20 | Tester desktop: keep walks on your machine (reserved per walk, isolated Chrome profile) or set up a second Windows user session | Walks on a shared machine were lost to foreign input on Pitwall | ROADMAP O1, first app walk |
