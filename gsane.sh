#!/bin/bash
# ----------------------------------------------------------------------------- 
# GSANE Core CLI Router (Zero-Touch Edition)
# ----------------------------------------------------------------------------- 

set -euo pipefail
IFS=$'\n\t'

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ACTION="${1:-}"
PYTHON_CMD=()

is_non_negative_integer() {
    case "$1" in
        ''|*[!0-9]*)
            return 1
            ;;
        *)
            return 0
            ;;
    esac
}

resolve_python_cmd() {
    if command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(python3)
        return 0
    fi
    if command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(python)
        return 0
    fi
    if command -v py >/dev/null 2>&1 && py -3 -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(py -3)
        return 0
    fi
    return 1
}

run_python() {
    if [ ${#PYTHON_CMD[@]} -eq 0 ]; then
        if ! resolve_python_cmd; then
            echo "❌ Python exécutable introuvable. Installe Python ou active un interpréteur réel (python, python3 ou py -3)." >&2
            return 127
        fi
    fi
    "${PYTHON_CMD[@]}" "$@"
}

validate_config_yaml_tree() {
    run_python - <<'PY'
from pathlib import Path
import sys

import yaml

files = sorted(Path("_gsane/_config").rglob("*.yaml"))
errors = 0

if not files:
    print("  [FAIL] _gsane/_config/: aucun fichier YAML trouvé")
    sys.exit(1)

for file_path in files:
    try:
        with file_path.open(encoding="utf-8") as handle:
            yaml.safe_load(handle)
        print(f"  [OK] {file_path.as_posix()} : OK")
    except Exception as error:
        print(f"  [FAIL] {file_path.as_posix()} : ERREUR ({error})")
        errors += 1

if errors > 0:
    sys.exit(1)
PY
}

if [ -z "$ACTION" ]; then
    echo "Usage: bash gsane.sh <command>"
    echo "Commands:"
    echo "  doctor       : Vérifie l'intégrité de l'environnement (session-start + YAML validation)"
    echo "  validate     : Exécution de la Quality Gate (pytest + YAML + qa-linter + security gate + CHANGELOG)"
    echo "  trace        : Observabilité — sous-commandes : --tail N | --summary | --p2p | --report"
    echo "  mcp --health     : Vérifie les prérequis MCP (dépendances, imports, schéma)"
    echo "  mcp --smoke-test : Vérifie que tous les outils MCP fonctionnent end-to-end"
    exit 1
fi

case $ACTION in
    doctor|health-check)
        echo "🩺 GSANE Doctor - Health Check global"
        echo "----------------------------------------"

        # Détection Windows sans WSL natif
        if [ "$(uname -s 2>/dev/null)" = "MINGW64_NT"* ] || [ "$(uname -s 2>/dev/null)" = "MSYS_NT"* ] || [ -n "${MSYSTEM:-}" ]; then
            echo "⚠️  Environnement Windows détecté (Git Bash / MSYS2)."
            echo "   gsane.sh fonctionne partiellement sous Git Bash."
            echo "   Pour un environnement aligné avec le CI : wsl --install -d Ubuntu"
            echo "   Alternative sans Bash : python -m pytest tests/ -m 'not behavioral'"
            echo "----------------------------------------"
        fi

        echo "1️⃣  Validation des liens morts (via session-start)..."
        if [ -f .github/hooks/session-start.sh ]; then
            bash .github/hooks/session-start.sh
        fi
        echo "----------------------------------------"
        echo "2️⃣  Validation récursive des YAML..."
        if validate_config_yaml_tree; then
            echo "✅ GSANE est sain."
        else
            echo "❌ Erreurs détectées par le Doctor."
            exit 1
        fi
        ;;

    validate)
        echo "🔍 Quality Gate : Exécution de la suite de tests Python..."       

        if run_python -m pytest tests/ -m "not behavioral"; then
            :
        else
            EXIT_CODE=$?
            echo "❌ Quality Gate Failed : Des tests ont échoué ! (Code: $EXIT_CODE)"
            exit 1
        fi

        echo "🔍 Vérification récursive de la syntaxe YAML..."
        if ! validate_config_yaml_tree; then
            echo "❌ Quality Gate Failed : YAML invalide dans _gsane/_config/**."
            exit 1
        fi

        echo "🔍 QA Linter (Zero-Touch validation)..."
        if ! run_python tests/qa-linter.py _gsane/agents/*.md; then
            echo "❌ QA Linter Failed : Non-compliance détectée dans les fichiers des agents."
            exit 1
        fi

        echo "🔍 Scan secrets bloquant..."
        if ! run_python _gsane/tools/security_gate.py scan-secrets; then
            echo "❌ Secret Scan Failed : signatures fortes détectées."
            exit 1
        fi

        echo "🔍 SAST Python léger (Bandit)..."
        if ! run_python _gsane/tools/security_gate.py run-bandit; then
            echo "❌ Bandit Failed : vulnérabilités ou configuration outillage à corriger."
            exit 1
        fi

        echo "🔍 Audit dépendances Python (pip-audit)..."
        if ! run_python _gsane/tools/security_gate.py run-pip-audit; then
            echo "❌ pip-audit Failed : dépendances vulnérables ou audit non exécutable."
            exit 1
        fi

        echo "🔍 Vérification documentaire..."
        STATUS_OUTPUT="$(git status --porcelain)"
        if printf '%s\n' "$STATUS_OUTPUT" | grep -Eq '^( M| A|AM|A |M |\?\?)' && \
            printf '%s\n' "$STATUS_OUTPUT" | grep -q "src/\|_gsane/mcp-server/\|_gsane/workflows/\|_gsane/agents/"; then
            if ! printf '%s\n' "$STATUS_OUTPUT" | grep -q "CHANGELOG.md"; then
                echo "❌ ERREUR: Code source modifié mais CHANGELOG.md ignoré." 
                echo "➡️ Règle de la Strike Team : Tout nouveau code exige une ligne de changelog."
                exit 1
            fi
        fi

        echo "🔍 Validation schéma execution-plan.yaml (sessions)..."
        PLAN_COUNT=0
        if [ -d "_gsane-output/sessions" ]; then
            while IFS= read -r -d '' f; do
                PLAN_COUNT=$((PLAN_COUNT + 1))
                if run_python - "$f" <<'PY'
import sys
sys.path.insert(0, 'tests')
import qa_linter
sys.exit(qa_linter.validate_execution_plan_schema(sys.argv[1]))
PY
                then
                    :
                else
                    echo "❌ Schéma invalide : $f"
                    exit 1
                fi
            done < <(find "_gsane-output/sessions" -name "execution-plan.yaml" -print0 2>/dev/null)
        fi
        if [ $PLAN_COUNT -eq 0 ]; then
            echo "   (aucun execution-plan.yaml trouvé — skip)"
        fi

        echo "✅ Quality Gate Passed : Tous les tests sont validés !"
        exit 0
        ;;

    trace)
        TRACE_FILE="_gsane/_memory/trace.log"
        SUBCMD="${2:-}"

        case $SUBCMD in
            --tail)
                N="${3:-10}"
                if ! is_non_negative_integer "$N"; then
                    echo "❌ Valeur invalide pour --tail: '$N'"
                    exit 1
                fi
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "⚠️  trace.log not found. No events yet."
                    exit 0
                fi
                echo "📋 Last $N trace events:"
                echo "---"
                run_python -c "
import yaml
try:
    entries = yaml.safe_load(open('$TRACE_FILE', encoding='utf-8').read())
    if not isinstance(entries, list):
        raise ValueError('Not a list')
    entries = entries[-${N}:]
    for e in entries:
        print(yaml.safe_dump([e], default_flow_style=False, allow_unicode=True))
except Exception:
    print('⚠️ trace.log corrompu — fallback lecture Python')
    line_count = ${N} * 10
    lines = open('$TRACE_FILE', encoding='utf-8', errors='replace').read().splitlines()
    for line in lines[-line_count:]:
        print(line)
" 2>/dev/null
                ;;
            --summary)
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "⚠️  trace.log not found."
                    exit 0
                fi
                echo "📊 Trace Summary:"
                run_python -c "
import re
content = open('$TRACE_FILE', encoding='utf-8', errors='replace').read()
agents = re.findall(r'  agent: (.+)', content)
events = re.findall(r'  event: (.+)', content)
scores = [int(x) for x in re.findall(r'  trust_score: (\d+)', content)]
rouge = events.count('hup_rouge')
jaune = events.count('hup_jaune')
huddles = events.count('huddle_opened')
cb = events.count('circuit_breaker_triggered')
agent_counts = {}
for a in agents:
    agent_counts[a.strip()] = agent_counts.get(a.strip(), 0) + 1
avg_score = round(sum(scores)/len(scores), 1) if scores else 'N/A'
print(f'  Events total    : {len(events)}')
print(f'  Agents actifs   : {dict(agent_counts)}')
print(f'  Trust score moy : {avg_score}')
print(f'  HUP rouge       : {rouge}')
print(f'  HUP jaune       : {jaune}')
print(f'  Huddles ouverts : {huddles}')
print(f'  Circuit breakers: {cb}')
"
                ;;
            --p2p)
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "⚠️  trace.log not found."
                    exit 0
                fi
                echo "🔗 P2P Messages:"
                echo "---"
                run_python -c "
import re, yaml
content = open('$TRACE_FILE', encoding='utf-8', errors='replace').read()
try:
    entries = yaml.safe_load(content)
    if not isinstance(entries, list):
        raise ValueError('Not a list')
    for e in entries:
        if isinstance(e, dict) and 'p2p_message_sent' in str(e.get('event', '')):
            ts_val = e.get('timestamp', '?')
            ag_val = e.get('agent', '?')
            det_val = e.get('details', '?')
            print(f'[{ts_val}] {ag_val} → {det_val}')
except Exception:
    entries = [e.strip() for e in content.split('- timestamp:') if e.strip()]
    for e in entries:
        if 'p2p_message_sent' in e:
            ts = re.search(r'(\S+)', e)
            agent = re.search(r'agent: (.+)', e)
            details = re.search(r'details: (.+)', e)
            ts_val = ts.group(1) if ts else '?'
            ag_val = agent.group(1).strip() if agent else '?'
            det_val = details.group(1).strip() if details else '?'
            print(f'[{ts_val}] {ag_val} → {det_val}')
"
                ;;
            --report)
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "ℹ️  trace.log not found. No events yet."
                    exit 0
                fi
                echo "📊 Generating trace report..."
                run_python -c "
import yaml
from datetime import datetime

TRACE_FILE = '$TRACE_FILE'

try:
    with open(TRACE_FILE, encoding='utf-8', errors='replace') as f:
        entries = yaml.safe_load(f.read())
    if not isinstance(entries, list):
        raise ValueError('Not a list')
except Exception:
    # Fallback regex
    import re
    content = open(TRACE_FILE, encoding='utf-8', errors='replace').read()
    agents = re.findall(r'  agent: (.+)', content)
    events = re.findall(r'  event: (.+)', content)
    scores = [int(x) for x in re.findall(r'  trust_score: (\d+)', content)]
    rouge = events.count('hup_rouge')
    jaune = events.count('hup_jaune')
    cb = events.count('circuit_breaker_triggered')
    huddles = events.count('huddle_opened')
    p2p = events.count('p2p_message_sent')
    avg_score = round(sum(scores)/len(scores), 1) if scores else 'N/A'
    agent_counts = {}
    for a in agents:
        a = a.strip()
        agent_counts[a] = agent_counts.get(a, 0) + 1
    print('# 📊 GSANE Trace Report')
    print()
    print('⚠️ Parsing YAML échoué — rapport partiel (regex fallback)')
    print()
    print(f'## Activité globale')
    print(f'- Events total : {len(events)}')
    print()
    print('## Top Agents')
    print('| Agent | Events | Trust Score Moyen |')
    print('|-------|--------|-------------------|')
    for a, c in sorted(agent_counts.items(), key=lambda x: -x[1]):
        print(f'| {a} | {c} | {avg_score} |')
    print()
    print('## Alertes')
    print(f'- HUP Rouge : {rouge}')
    print(f'- HUP Jaune : {jaune}')
    print(f'- Circuit Breakers : {cb}')
    print(f'- Huddles ouverts : {huddles}')
    print()
    print(f'## Events P2P')
    print(f'- Messages P2P : {p2p}')
    import sys; sys.exit(0)

# YAML parsed OK
timestamps = [e.get('timestamp', '') for e in entries if isinstance(e, dict)]
first_ts = timestamps[0] if timestamps else '?'
last_ts = timestamps[-1] if timestamps else '?'

agent_data = {}
for e in entries:
    if not isinstance(e, dict):
        continue
    a = str(e.get('agent', '?')).strip()
    if a not in agent_data:
        agent_data[a] = {'count': 0, 'scores': []}
    agent_data[a]['count'] += 1
    ts = e.get('trust_score')
    if ts is not None and str(ts).isdigit():
        agent_data[a]['scores'].append(int(ts))

events_list = [str(e.get('event', '')) for e in entries if isinstance(e, dict)]
rouge = events_list.count('hup_rouge')
jaune = events_list.count('hup_jaune')
cb = events_list.count('circuit_breaker_triggered')
huddles = events_list.count('huddle_opened')
p2p = events_list.count('p2p_message_sent')

today = datetime.now().strftime('%Y-%m-%d')
print(f'# 📊 GSANE Trace Report — {today}')
print()
print('## Activité globale')
print(f'- Events total : {len(entries)}')
print(f'- Période : {first_ts} → {last_ts}')
print()
print('## Top Agents (par nombre d\\'events)')
print('| Agent | Events | Trust Score Moyen |')
print('|-------|--------|-------------------|')
for a, d in sorted(agent_data.items(), key=lambda x: -x[1]['count']):
    avg = round(sum(d['scores'])/len(d['scores']), 1) if d['scores'] else 'N/A'
    print('| {} | {} | {} |'.format(a, d['count'], avg))
print()
print('## Alertes')
print(f'- HUP Rouge : {rouge}')
print(f'- HUP Jaune : {jaune}')
print(f'- Circuit Breakers : {cb}')
print(f'- Huddles ouverts : {huddles}')
print()
print('## Events P2P')
print(f'- Messages P2P : {p2p}')
print()
print('## Derniers 5 events')
for e in entries[-5:]:
    if isinstance(e, dict):
        ts = e.get('timestamp', '?')
        ag = e.get('agent', '?')
        ev = e.get('event', '?')
        det = str(e.get('details', ''))[:60]
        print(f'- {ts} | {ag} | {ev} | {det}')
"
                ;;
            *)
                echo "Usage: bash gsane.sh trace --tail N | --summary | --p2p | --report"
                exit 1
                ;;
        esac
        ;;
    mcp)
        MCPCMD="${2:-}"
        case $MCPCMD in
            --health)
                echo "🔌 GSANE MCP Health Check"
                echo "---"
                # 1. Dépendances
                run_python -c "from mcp.server.fastmcp import FastMCP; import yaml; print('  [OK] Dépendances MCP : OK')" 2>/dev/null || { echo "  ❌ Dépendances manquantes — pip install -r _gsane/mcp-server/requirements.txt"; exit 1; }
                # 2. Import des outils
                run_python -c "
import sys; sys.path.insert(0, '_gsane/mcp-server'); sys.path.insert(0, '_gsane/tools')
from compression_tool import gsane_read_canonical_brief, gsane_read_active_delivery_contract, gsane_read_project_snapshot, gsane_fetch_compressed_memory, gsane_write_session_checkpoint, gsane_read_checkpoint, gsane_route, gsane_memory_fetch
from security_gate import load_security_gate_config
load_security_gate_config()
assert callable(gsane_read_canonical_brief)
assert callable(gsane_read_active_delivery_contract)
assert callable(gsane_read_project_snapshot)
print('  [OK] Outils MCP importables : OK (8/8) + security_gate')
" 2>/dev/null || { echo "  ❌ Erreur d'import des outils MCP"; exit 1; }
                # 3. Schéma delegation-matrix.yaml
                run_python -c "
import yaml, sys
with open('_gsane/_config/delegation-matrix.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
rules = data.get('rules', [])
for r in rules:
    assert 'trigger' in r, f'Clé manquante trigger: {r}'
    assert 'agent' in r, f'Clé manquante agent: {r}'
print(f'  [OK] delegation-matrix.yaml schéma OK ({len(rules)} règles)')
" 2>/dev/null || { echo "  ❌ Schema mismatch dans delegation-matrix.yaml"; exit 1; }
                echo "---"
                echo "✅ MCP Health : TOUS LES CHECKS PASSÉS"
                ;;
            --smoke-test)
                echo "🔬 GSANE MCP Smoke Test"
                echo "---"
                run_python -c "
import sys, os
sys.path.insert(0, '_gsane/mcp-server')
from compression_tool import (gsane_fetch_compressed_memory, gsane_write_session_checkpoint,
    gsane_read_checkpoint, gsane_route, gsane_memory_fetch,
    gsane_read_canonical_brief, gsane_read_active_delivery_contract,
    gsane_read_project_snapshot)

r = gsane_read_canonical_brief()
assert 'canonical_human_brief' in r and 'project-context.md' in r
print('  [OK] gsane_read_canonical_brief : OK')

r = gsane_read_active_delivery_contract()
assert 'active_delivery_contract' in r and 'current-delivery-contract.md' in r
print('  [OK] gsane_read_active_delivery_contract : OK')

r = gsane_read_project_snapshot()
assert 'canonical_project_snapshot' in r and 'audit-only' in r
print('  [OK] gsane_read_project_snapshot : OK')

r = gsane_fetch_compressed_memory('master')
assert r is not None
print('  [OK] gsane_fetch_compressed_memory : OK')

r = gsane_write_session_checkpoint('plan test', 'next step', 'decision A', 'item B', 'risk C', 1)
assert 'Checkpoint sauvegardé' in r, f'Echec write: {r}'
print('  [OK] gsane_write_session_checkpoint : OK')

r = gsane_read_checkpoint()
assert r is not None
print('  [OK] gsane_read_checkpoint : OK')

r = gsane_route('implement a new feature with code')
assert r is not None
print('  [OK] gsane_route : OK')

r = gsane_route('security hardening for GSANE MCP sandbox guardrail')
assert 'ESCALADE SÉCURITÉ' in r and 'Winston' in r and 'Quinn' in r
print('  [OK] gsane_route security_gate : OK')

r = gsane_memory_fetch('master', '')
assert r is not None
print(f'  [OK] gsane_memory_fetch : OK — {len(r)} chars')

print('---')
print('[OK] MCP Smoke Test : TOUS LES CHECKS PASSÉS')
"
                ;;
            *)
                echo "Usage: bash gsane.sh mcp --health | --smoke-test"
                exit 1
                ;;
        esac
        ;;
    *)
        echo "❌ Commande '$ACTION' non reconnue."
        exit 1
        ;;
esac
