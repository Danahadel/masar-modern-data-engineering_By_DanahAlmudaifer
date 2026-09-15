from pathlib import Path
import json, shutil, sys

ROOT = Path.cwd()
if not (ROOT / "course.json").exists():
    raise RuntimeError("Run this script from the repository root.")

sys.path.insert(0, str(ROOT / "src"))
from masar.workspace import completed_bronze_workspace

WORK = completed_bronze_workspace(ROOT)
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)

# Copy only small report/document evidence; never copy the Delta lake or handoff ZIPs.
candidates = []
for p in WORK.rglob("*"):
    if not p.is_file():
        continue
    rel = p.relative_to(WORK)
    if "reports" in rel.parts or p.suffix.lower() in {".json", ".txt", ".html"}:
        # Avoid large/runtime internals and Delta transaction logs.
        if "_delta_log" in rel.parts or "checkpoints" in rel.parts:
            continue
        if p.stat().st_size <= 2_000_000:
            candidates.append(p)

for p in candidates:
    rel = p.relative_to(WORK)
    # keep paths after the first 'reports' component when present
    if "reports" in rel.parts:
        i = rel.parts.index("reports")
        dest_rel = Path(*rel.parts[i+1:])
    else:
        dest_rel = Path("run_evidence") / rel
    dest = REPORTS / dest_rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(p, dest)

print("Workspace:", WORK)
print("Copied", len(candidates), "small evidence files into", REPORTS)
for p in sorted(REPORTS.rglob("*")):
    if p.is_file():
        print(p.relative_to(ROOT))
