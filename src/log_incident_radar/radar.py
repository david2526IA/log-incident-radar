"""Aggregate structured error logs into transparent time buckets."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any


def _minute(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except ValueError as error:
        raise ValueError(f"invalid timestamp: {value!r}") from error
    return parsed.strftime("%Y-%m-%dT%H:%MZ")


def analyze(events: list[dict[str, Any]], threshold: int = 3) -> dict[str, Any]:
    """Find service/minute buckets containing at least ``threshold`` errors."""
    if threshold < 1:
        raise ValueError("threshold must be at least 1")
    buckets: Counter[tuple[str, str]] = Counter()
    services: Counter[str] = Counter()
    invalid = []
    for index, event in enumerate(events, start=1):
        if not {"timestamp", "service", "level"} <= event.keys():
            invalid.append({"line": index, "reason": "timestamp, service and level are required"})
            continue
        if str(event["level"]).upper() not in {"ERROR", "CRITICAL"}:
            continue
        try:
            minute = _minute(str(event["timestamp"]))
        except ValueError as error:
            invalid.append({"line": index, "reason": str(error)})
            continue
        service = str(event["service"])
        buckets[(service, minute)] += 1
        services[service] += 1
    incidents = [{"service": service, "minute": minute, "error_events": count} for (service, minute), count in buckets.items() if count >= threshold]
    incidents.sort(key=lambda item: (-item["error_events"], item["service"], item["minute"]))
    return {"events": len(events), "error_events": sum(services.values()), "threshold": threshold, "incidents": incidents, "errors_by_service": dict(sorted(services.items())), "invalid_events": invalid, "scope": "triage signal only; inspect source logs and system context before declaring an incident"}
