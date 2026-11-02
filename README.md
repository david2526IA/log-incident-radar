# Log Incident Radar

Local, explainable error-burst analysis for JSONL application logs. It groups `ERROR` and `CRITICAL` events by service and UTC minute, then highlights buckets that reach a declared threshold.

## Run

```bash
pip install .
log-incident-radar app.jsonl --threshold 3 --output incident_report.json
```

Input rows need `timestamp`, `service` and `level`. Invalid error rows are retained in the report instead of being silently discarded.

## Scope

This is a local triage signal, not an alerting platform or root-cause analysis system. It does not upload logs, page anyone or decide whether an operational incident exists.

## Development

```bash
pip install ".[dev]"
pytest -q
```

## License

MIT
