#!/usr/bin/env python3
"""Generate a self-contained HTML trace report from _gsane/_memory/trace.log."""

import sys
from datetime import datetime
from html import escape
from pathlib import Path

import yaml  # type: ignore[import-untyped]

SCRIPT_DIR = Path(__file__).resolve().parent
GSANE_DIR = SCRIPT_DIR.parent
PROJECT_ROOT = GSANE_DIR.parent
TRACE_FILE = GSANE_DIR / "_memory" / "trace.log"
OUTPUT_DIR = PROJECT_ROOT / "_gsane-output"


def _load_entries() -> list[dict]:
    if not TRACE_FILE.exists():
        return []
    content = TRACE_FILE.read_text(encoding="utf-8", errors="replace")
    if not content.strip():
        return []
    try:
        entries = yaml.safe_load(content)
        if not isinstance(entries, list):
            return []
        return [e for e in entries if isinstance(e, dict)]
    except Exception:
        return []


def _build_html(entries: list[dict]) -> str:
    today = datetime.now().strftime("%Y-%m-%d")

    if not entries:
        return _wrap_html(
            today,
            "<div class='card'><h2>Aucune donnée de session</h2>"
            "<p>trace.log est vide ou absent.</p></div>",
        )

    # Summary
    total = len(entries)
    sessions = set()
    scores = []
    agent_data: dict[str, dict] = {}

    for e in entries:
        sid = str(e.get("session_id", ""))
        if sid:
            sessions.add(sid)
        ts_val = e.get("trust_score")
        if ts_val is not None and str(ts_val).isdigit():
            scores.append(int(ts_val))

        agent = str(e.get("agent", "?")).strip()
        if agent not in agent_data:
            agent_data[agent] = {
                "count": 0,
                "scores": [],
                "last_event": "",
                "last_ts": "",
            }
        agent_data[agent]["count"] += 1
        agent_data[agent]["last_event"] = str(e.get("event", ""))
        agent_data[agent]["last_ts"] = str(e.get("timestamp", ""))
        if ts_val is not None and str(ts_val).isdigit():
            agent_data[agent]["scores"].append(int(ts_val))

    avg_score = round(sum(scores) / len(scores), 1) if scores else "N/A"

    # Alerts
    events_list = [str(e.get("event", "")) for e in entries]
    hup_rouge = events_list.count("hup_rouge")
    circuit_breakers = events_list.count("circuit_breaker_triggered")
    low_trust = [
        e
        for e in entries
        if e.get("trust_score") is not None
        and str(e.get("trust_score")).isdigit()
        and int(str(e.get("trust_score"))) < 3
    ]

    # Build HTML sections
    summary_html = f"""
    <div class='card'>
        <h2>Résumé</h2>
        <div class='metrics'>
            <div class='metric'>
                <span class='metric-value'>{total}</span>
                <span class='metric-label'>Events total</span>
            </div>
            <div class='metric'>
                <span class='metric-value'>{len(sessions)}</span>
                <span class='metric-label'>Sessions</span>
            </div>
            <div class='metric'>
                <span class='metric-value'>{avg_score}</span>
                <span class='metric-label'>Trust score moyen</span>
            </div>
        </div>
    </div>
    """

    # Agent table
    rows = ""
    for agent, data in sorted(agent_data.items(), key=lambda x: -x[1]["count"]):
        avg = (
            round(sum(data["scores"]) / len(data["scores"]), 1)
            if data["scores"]
            else "N/A"
        )
        rows += (
            f"<tr><td>{escape(agent)}</td><td>{data['count']}</td>"
            f"<td>{avg}</td><td>{escape(data['last_ts'][:19])}</td></tr>\n"
        )
    agent_table_html = f"""
    <div class='card'>
        <h2>Agents</h2>
        <table>
            <thead><tr><th>Agent</th><th>Invocations</th><th>Trust score moy</th><th>Dernière activité</th></tr></thead>
            <tbody>{rows}</tbody>
        </table>
    </div>
    """

    # Timeline (last 10)
    timeline_rows = ""
    for e in entries[-10:]:
        ts = escape(str(e.get("timestamp", "?"))[:19])
        ag = escape(str(e.get("agent", "?")))
        ev = escape(str(e.get("event", "?")))
        timeline_rows += f"<tr><td>{ts}</td><td>{ag}</td><td>{ev}</td></tr>\n"
    timeline_html = f"""
    <div class='card'>
        <h2>Timeline — 10 derniers events</h2>
        <table>
            <thead><tr><th>Timestamp</th><th>Agent</th><th>Event type</th></tr></thead>
            <tbody>{timeline_rows}</tbody>
        </table>
    </div>
    """

    # Alerts
    alert_items = ""
    if hup_rouge > 0:
        alert_items += f"<li class='alert-critical'>HUP Rouge : {hup_rouge}</li>"
    if circuit_breakers > 0:
        alert_items += f"<li class='alert-critical'>Circuit breakers : {circuit_breakers}</li>"
    if low_trust:
        alert_items += f"<li class='alert-warning'>Trust &lt; 3 : {len(low_trust)} events</li>"
    if not alert_items:
        alert_items = "<li class='alert-ok'>Aucune alerte</li>"
    alerts_html = f"""
    <div class='card'>
        <h2>Alertes</h2>
        <ul class='alerts'>{alert_items}</ul>
    </div>
    """

    body = summary_html + agent_table_html + timeline_html + alerts_html
    return _wrap_html(today, body)


def _wrap_html(date: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GSANE Trace Report — {date}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
         background: #f0f2f5; color: #1a1a2e; padding: 2rem; }}
  h1 {{ text-align: center; margin-bottom: 2rem; color: #16213e; }}
  .card {{ background: #fff; border-radius: 8px; padding: 1.5rem; margin-bottom: 1.5rem;
           box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .card h2 {{ margin-bottom: 1rem; color: #0f3460; font-size: 1.2rem; }}
  .metrics {{ display: flex; gap: 2rem; flex-wrap: wrap; }}
  .metric {{ text-align: center; flex: 1; min-width: 120px; }}
  .metric-value {{ display: block; font-size: 2rem; font-weight: bold; color: #e94560; }}
  .metric-label {{ display: block; font-size: 0.85rem; color: #666; margin-top: 0.3rem; }}
  table {{ width: 100%; border-collapse: collapse; }}
  th, td {{ padding: 0.6rem 1rem; text-align: left; border-bottom: 1px solid #eee; }}
  th {{ background: #f8f9fa; font-weight: 600; color: #333; }}
  tr:hover {{ background: #f0f7ff; }}
  .alerts {{ list-style: none; }}
  .alerts li {{ padding: 0.5rem 1rem; margin-bottom: 0.5rem; border-radius: 4px; }}
  .alert-critical {{ background: #ffe6e6; color: #c0392b; border-left: 4px solid #e74c3c; }}
  .alert-warning {{ background: #fff3cd; color: #856404; border-left: 4px solid #ffc107; }}
  .alert-ok {{ background: #d4edda; color: #155724; border-left: 4px solid #28a745; }}
  footer {{ text-align: center; margin-top: 2rem; color: #999; font-size: 0.8rem; }}
</style>
</head>
<body>
<h1>📊 GSANE Trace Report — {date}</h1>
{body}
<footer>Généré par GSANE trace-report.py — {date}</footer>
</body>
</html>"""


def main() -> int:
    entries = _load_entries()
    html = _build_html(entries)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    output_path = OUTPUT_DIR / f"trace-report-{today}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Rapport HTML généré : {output_path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
