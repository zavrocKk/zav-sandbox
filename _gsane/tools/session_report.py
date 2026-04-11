"""Session report — affiche un résumé visuel de la dernière session GSANE."""
import datetime
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError:
    print("⚠️  PyYAML requis — pip install pyyaml")
    raise SystemExit(0) from None

ICONS = {
    'langis': '🧙', 'master': '🧙',
    'amelia': '💻', 'dev': '💻',
    'quinn': '🧪', 'qa': '🧪',
    'winston': '🏗️', 'architect': '🏗️',
    'bond': '🤖',
}
ALIAS = {
    'master': 'langis', 'dev': 'amelia',
    'qa': 'quinn', 'architect': 'winston',
}
ORDER = ['langis', 'amelia', 'quinn', 'winston', 'bond']

trace = Path('_gsane/_memory/trace.log')
if not trace.exists():
    print('⚠️  Aucune session enregistrée')
    raise SystemExit(0)

try:
    raw = trace.read_text(encoding='utf-8', errors='replace')
    # Skip comment lines
    clean = '\n'.join(line for line in raw.splitlines() if not line.startswith('#'))
    data = yaml.safe_load(clean)
    if not isinstance(data, list):
        data = [data] if data else []
except Exception:
    print('⚠️  trace.log illisible')
    raise SystemExit(0) from None

events = [e for e in data if isinstance(e, dict)]
if not events:
    print('⚠️  Aucun event')
    raise SystemExit(0)

# Dernière session seulement
last_sid = events[-1].get('session_id', '?')
last = [e for e in events if e.get('session_id') == last_sid]

# Compter par agent (fusionner alias)
counts: defaultdict[str, int] = defaultdict(int)
for e in last:
    a = ALIAS.get(
        e.get('agent', '?').lower(),
        e.get('agent', '?').lower(),
    )
    counts[a] += 1

# Stats globales
challenges = sum(1 for e in last if 'challenge' in e.get('event', ''))
dcs = sum(1 for e in last if 'delivery_contract' in e.get('event', ''))
qa_pass = any(e.get('event') == 'qa_gate_passed' for e in last)

# Affichage
today = datetime.date.today()
print()
print(f'📋 Session {last_sid} — {today}')
print('─' * 35)
for a in ORDER:
    icon = ICONS.get(a, '•')
    n = counts.get(a, 0)
    print(f'{icon} {a.title():<10} ×{n}')
print('─' * 35)
parts = []
if challenges:
    parts.append(f'{challenges} challenge(s)')
if dcs:
    parts.append(f'{dcs} DC')
verdict = '✅ PASS' if qa_pass else '⏳ En cours'
line = ' · '.join(parts + [verdict])
print(f'⚡ {line}')
print()
