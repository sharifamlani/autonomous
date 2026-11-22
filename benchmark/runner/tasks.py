"""Load benchmark tasks: one folder per task under benchmark/tasks/, described by its task.toml."""
import tomllib
from pathlib import Path

BENCH = Path(__file__).resolve().parents[1]
ROOT = BENCH.parent
TASKS = BENCH / "tasks"
GROUPS = {"smoke": "smoke_", "study": "study_", "app": "app_"}
DEFAULT_CAPS = {"minutes": 60, "turns": 0, "tokens": 0}       # 0 = no cap (token caps set after step 6)


def load(task_id):
    d = TASKS / task_id
    f = d / "task.toml"
    if not f.exists():
        raise SystemExit(f"no task {task_id!r}: {f} missing")
    cfg = tomllib.loads(f.read_text(encoding="utf-8"))
    cfg["id"], cfg["dir"] = task_id, d
    cfg["caps"] = {**DEFAULT_CAPS, **cfg.get("caps", {})}
    cfg.setdefault("watch", [])
    cfg.setdefault("answer", [])
    cfg.setdefault("grader", "none")
    return cfg


def select(spec):
    """A task id, a group (smoke, study, app), or all / v0.1 (every non-smoke task with a task.toml)."""
    ids = sorted(p.parent.name for p in TASKS.glob("*/task.toml"))
    if spec in GROUPS:
        ids = [i for i in ids if i.startswith(GROUPS[spec])]
    elif spec in ("all", "v0.1"):
        ids = [i for i in ids if not i.startswith("smoke_")]
    else:
        ids = [spec]
    if not ids:
        raise SystemExit(f"no tasks match {spec!r}")
    return [load(i) for i in ids]
