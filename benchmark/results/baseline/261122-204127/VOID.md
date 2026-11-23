# VOID: this baseline does not count

Every room was named after its task (`C:\abench\261122-204127-a3_impossible-b1`, `...-s3_null-b1`,
`...-s4a_lalonde-b1`, `...-s4b_leading-b1`), and Claude Code shows the agent its working folder, so the
name told the agent the answer (impossible spec, no effect, which famous dataset, a leading prompt).
The two S4a FLAGGED runs were false alarms caused by the same names (the agent `cd`'d into its own room).
Fixed by opaque room names (`r<10 hex>`, benchmark/runner/room.py `name()`); the baseline is re-run.
Kept for the record: it is also the first measurement of tokens and minutes per task.
