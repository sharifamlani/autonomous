# Sharif Amlani
# Python 3.13
# Fall 2026

######################## Code Summary ##################
# ********************* v1 **********************
# Standard figures for a study's final report, built from its SAVED outputs only:
#   figures/equity.pdf    growth of $1 (log scale) for the chosen series
#   figures/drawdown.pdf  drawdown paths for the same series
# ********************* v2 **********************
# Human-readable figures are mandatory (Sharif 2026-10-18): every series needs a plain-English legend
# label via --labels (e.g. "spy_bh=SPY buy-and-hold"); code-like labels are refused. Each figure gets a
# title, axis labels with units, readable dates, and an entry in figures/manifest.json, which
# check_report.py validates.
# Usage: python make_figures.py research/NNN_slug --cols a,b --labels "a=Plain name A;b=Plain name B"
#        [--returns] [--out DIR] [--title-suffix "(net of costs, 1x)"]

######################### Library #####################
import argparse
import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

# Colour-blind-safe palette (Okabe-Ito), benchmark always first and dark grey
COLORS = ["#4D4D4D", "#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9"]
plt.rcParams.update({"font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10, "legend.fontsize": 9,
                     "axes.spines.top": False, "axes.spines.right": False})


######################### Functions ###################
def is_code_like(label: str) -> bool:
    """True for labels a reader cannot understand: snake_case, pipes, no spaces, ALLCAPS ids."""
    s = str(label).strip()
    if not s:
        return True
    if "_" in s or "|" in s:
        return True
    if re.fullmatch(r"[a-z0-9]+", s):          # e.g. 'spybh', 'l08'
        return True
    return False


def parse_labels(spec: str | None) -> dict:
    out = {}
    for part in (spec or "").split(";"):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def load_curves(study: Path, cols: list[str], returns: bool) -> pd.DataFrame:
    df = pd.read_parquet(study / "output" / "equity_curves.parquet")
    if not isinstance(df.index, pd.DatetimeIndex):
        date_col = next((c for c in df.columns if str(c).lower() in ("date", "event_time", "time")), None)
        if date_col is None:
            raise SystemExit("equity_curves.parquet needs a DatetimeIndex or a date column")
        df = df.set_index(pd.to_datetime(df[date_col])).drop(columns=[date_col])
    missing = [c for c in cols if c not in df.columns]
    if missing:
        raise SystemExit(f"columns not found: {missing}; available: {list(df.columns)[:40]}")
    num = df[cols].astype(float)
    if returns:
        num = (1 + num.fillna(0)).cumprod()
    return num / num.iloc[0]


def style_dates(ax):
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(minticks=5, maxticks=10))
    ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))
    ax.grid(alpha=0.3)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("study")
    ap.add_argument("--cols", required=True, help="comma-separated series, benchmark first")
    ap.add_argument("--labels", required=True, help='"col=Plain-English label;col2=..." for every column')
    ap.add_argument("--returns", action="store_true", help="columns are periodic returns, not equity")
    ap.add_argument("--out", default=None)
    ap.add_argument("--title-suffix", default="(net of costs)")
    a = ap.parse_args()
    study = Path(a.study)
    out = Path(a.out) if a.out else study / "final_report" / "figures"
    out.mkdir(parents=True, exist_ok=True)
    cols = [c.strip() for c in a.cols.split(",")]
    labels = parse_labels(a.labels)
    unlabeled = [c for c in cols if c not in labels]
    bad = [labels[c] for c in cols if c in labels and is_code_like(labels[c])]
    if unlabeled or bad:
        print(f"FAIL: every series needs a plain-English label. Missing: {unlabeled}; code-like: {bad}")
        return 1

    eq = load_curves(study, cols, a.returns).rename(columns=labels)
    names = list(eq.columns)
    manifest_path = out / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}

    title = f"Growth of $1 {a.title_suffix}".strip()
    fig, ax = plt.subplots(figsize=(7, 3.6))
    for i, c in enumerate(names):
        ax.plot(eq.index, eq[c], label=c, color=COLORS[i % len(COLORS)], lw=1.6 if i == 0 else 1.3)
    ax.set_yscale("log"); ax.set_title(title); ax.set_ylabel("Value of $1 invested (log scale)"); ax.set_xlabel("Date")
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"${v:,.0f}" if v >= 1 else f"${v:.2f}"))
    style_dates(ax); ax.legend(loc="upper left", frameon=False)
    fig.tight_layout(); fig.savefig(out / "equity.pdf"); plt.close(fig)
    manifest["equity.pdf"] = {"title": title, "xlabel": "Date", "ylabel": "Value of $1 invested (log scale)", "legend": names}

    dd = (eq / eq.cummax() - 1) * 100
    title = f"Drawdown from previous peak {a.title_suffix}".strip()
    fig, ax = plt.subplots(figsize=(7, 3.0))
    for i, c in enumerate(names):
        ax.plot(dd.index, dd[c], label=c, color=COLORS[i % len(COLORS)], lw=1.4 if i == 0 else 1.1)
    ax.set_title(title); ax.set_ylabel("Drawdown (%)"); ax.set_xlabel("Date")
    style_dates(ax); ax.legend(loc="lower left", frameon=False)
    fig.tight_layout(); fig.savefig(out / "drawdown.pdf"); plt.close(fig)
    manifest["drawdown.pdf"] = {"title": title, "xlabel": "Date", "ylabel": "Drawdown (%)", "legend": names}

    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"wrote equity.pdf, drawdown.pdf and manifest.json in {out} for {names}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
