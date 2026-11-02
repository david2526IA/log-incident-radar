import pytest

from log_incident_radar.radar import analyze


def test_error_bursts_are_grouped_by_service_and_minute() -> None:
    events = [
        {"timestamp": "2026-01-01T12:00:01Z", "service": "api", "level": "ERROR"},
        {"timestamp": "2026-01-01T12:00:20Z", "service": "api", "level": "CRITICAL"},
        {"timestamp": "2026-01-01T12:01:00Z", "service": "api", "level": "ERROR"},
        {"timestamp": "2026-01-01T12:00:00Z", "service": "worker", "level": "INFO"},
    ]
    report = analyze(events, threshold=2)
    assert report["incidents"] == [{"service": "api", "minute": "2026-01-01T12:00Z", "error_events": 2}]
    assert report["errors_by_service"] == {"api": 3}


def test_invalid_events_are_retained_for_review() -> None:
    report = analyze([{"timestamp": "not-a-date", "service": "api", "level": "ERROR"}])
    assert len(report["invalid_events"]) == 1


def test_invalid_threshold_is_rejected() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        analyze([], 0)
