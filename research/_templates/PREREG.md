# Study NNN — <title>

Pre-registration. Commit this file before any result exists (CLAUDE.md §5).

| Field | Entry |
|---|---|
| Hypothesis | |
| Source paper(s) | (Literature ID, e.g. D6) |
| Mechanism / counterparty | |
| Prior plausibility (before testing) | |
| Instruments + universe | |
| Return leg harvested | overnight / intraday / both |
| Data + date range | |
| Train / validation / holdout split | (holdout = tail, >= 20%; one look) |
| Label horizon / embargo (bars) | (embargo >= label horizon; purged CV, trading.factory.cv) |
| Holdout family | (registry key for trading.factory.holdout; one look per family) |
| Cost model | (config/costs/..., multiplier 1x; sensitivity 0.5x / 2x) |
| Metric | |
| Pass thresholds | t > 3; DSR >= 0.95; PBO < 0.2; survives 2x costs |
| Break-even screen | (PROCEED or WAIVED: <Sharif's reason>; from `python scripts/screen.py --id <H###>`; required from Study 049) |
| Max trials budgeted | |
| Abandonment rule | |
