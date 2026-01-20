import csv
import json
from datetime import datetime
from pathlib import Path


def _timestamp():
    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")


def save_json(data, out_dir="reports"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    filename = f"report_{_timestamp()}.json"
    path = Path(out_dir) / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return str(path)


def save_csv(rows, out_dir="reports"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    filename = f"report_{_timestamp()}.csv"
    path = Path(out_dir) / filename

    keys = set()
    for r in rows:
        keys.update(r.keys())
    fieldnames = sorted(keys)

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    return str(path)
