from __future__ import annotations

import argparse
import json
from pathlib import Path

from .radar import analyze


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect error bursts in local JSONL logs.")
    parser.add_argument("input", type=Path)
    parser.add_argument("--threshold", type=int, default=3)
    parser.add_argument("--output", type=Path, default=Path("incident_report.json"))
    args = parser.parse_args()
    events = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line.strip()]
    report = analyze(events, args.threshold)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"incidents": len(report["incidents"]), "error_events": report["error_events"]}))
