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
    echo "  dc           : Delivery Contract — sous-commande : --validate <fichier.md>"
    echo "  flywheel     : Gestion du flywheel — sous-commande : --rollback <tag>"
    echo "  mcp --health     : Vérifie les prérequis MCP (dépendances, imports, schéma)"
    echo "  mcp --smoke-test : Vérifie que tous les outils MCP fonctionnent end-to-end"
    echo "  session --resume : Reprend une session interrompue via le dernier checkpoint"
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
            if run_python -c "import bandit" 2>/dev/null; then
                echo "❌ Bandit Failed : vulnérabilités ou configuration outillage à corriger."
                exit 1
            else
                echo "⚠️  Bandit non installé — skip local. CI Ubuntu valide cette gate."
            fi
        fi

        echo "🔍 Audit dépendances Python (pip-audit)..."
        if ! run_python _gsane/tools/security_gate.py run-pip-audit; then
            if run_python -c "import pip_audit" 2>/dev/null; then
                echo "❌ pip-audit Failed : dépendances vulnérables ou audit non exécutable."
                exit 1
            else
                echo "⚠️  pip-audit non installé — skip local. CI Ubuntu valide cette gate."
            fi
        fi

        echo "🔍 Vérification documentaire..."
        STATUS_OUTPUT="$(git status --porcelain)"
        # Exclure _gsane/_memory/ (fichiers runtime) du gate CHANGELOG
        # || true : grep -v retourne exit 1 quand aucune ligne ne passe le filtre (set -e)
        CODE_CHANGES="$(printf '%s\n' "$STATUS_OUTPUT" | grep -v '_gsane/_memory/' || true)"
        if printf '%s\n' "$CODE_CHANGES" | grep -Eq '^( M| A|AM|A |M |\?\?)' && \
            printf '%s\n' "$CODE_CHANGES" | grep -q "src/\|_gsane/mcp-server/\|_gsane/workflows/\|_gsane/agents/"; then
            if ! printf '%s\n' "$CODE_CHANGES" | grep -q "CHANGELOG.md"; then
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
import re, yaml
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

# P5-E: Métriques par agent
try:
    entries = yaml.safe_load(content)
    if isinstance(entries, list) and entries:
        agent_data = {}
        for e in entries:
            if not isinstance(e, dict):
                continue
            a = str(e.get('agent', '?')).strip()
            if a not in agent_data:
                agent_data[a] = {'count': 0, 'scores': [], 'last_event': '', 'passed': 0, 'failed': 0}
            agent_data[a]['count'] += 1
            agent_data[a]['last_event'] = str(e.get('event', ''))
            ts = e.get('trust_score')
            if ts is not None and str(ts).isdigit():
                agent_data[a]['scores'].append(int(ts))
            ev = str(e.get('event', ''))
            if ev == 'qa_gate_passed':
                agent_data[a]['passed'] += 1
            elif ev == 'qa_gate_failed':
                agent_data[a]['failed'] += 1
        if agent_data:
            print()
            print('📊 Métriques par agent :')
            for a, d in sorted(agent_data.items(), key=lambda x: -x[1]['count']):
                avg = round(sum(d['scores'])/len(d['scores']), 1) if d['scores'] else 'N/A'
                line = f'  {a:<12}: {d["count"]} invocations | trust: {avg} | last: {d["last_event"]}'
                if d['passed'] or d['failed']:
                    total_gates = d['passed'] + d['failed']
                    ratio = round(d['passed'] / total_gates * 100) if total_gates else 0
                    line += f' | pass/fail: {d["passed"]}/{d["failed"]} ({ratio}%)'
                print(line)
except Exception:
    pass
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
                echo "📊 Generating trace report..."
                run_python _gsane/tools/trace-report.py
                ;;
            *)
                echo "Usage: bash gsane.sh trace --tail N | --summary | --p2p | --report"
                exit 1
                ;;
        esac
        ;;
    dc)
        DCCMD="${2:-}"
        case $DCCMD in
            --validate)
                DC_FILE="${3:-}"
                if [ -z "$DC_FILE" ]; then
                    echo "Usage: bash gsane.sh dc --validate <fichier.md>"
                    exit 1
                fi
                if [ ! -f "$DC_FILE" ]; then
                    echo "❌ Fichier introuvable : $DC_FILE"
                    exit 1
                fi
                run_python _gsane/tools/dc-validator.py "$DC_FILE"
                ;;
            *)
                echo "Usage: bash gsane.sh dc --validate <fichier.md>"
                exit 1
                ;;
        esac
        ;;
    flywheel)
        FLYCMD="${2:-}"
        case $FLYCMD in
            --rollback)
                TAG="${3:-}"
                if [ -z "$TAG" ]; then
                    echo "Usage: bash gsane.sh flywheel --rollback <tag>"
                    echo "Tags disponibles:"
                    git tag -l "gsane-flywheel-pre-*" 2>/dev/null || echo "  (aucun tag trouvé)"
                    exit 1
                fi
                bash _gsane/tools/flywheel-rollback.sh rollback "$TAG"
                ;;
            *)
                echo "Usage: bash gsane.sh flywheel --rollback <tag>"
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
                # 1. Dépendances — fallback gracieux si le Python résolu n'a pas mcp
                MCP_DEP_OK=false
                if run_python -c "from mcp.server.fastmcp import FastMCP; import yaml; print('  [OK] Dépendances MCP : OK')" 2>/dev/null; then
                    MCP_DEP_OK=true
                fi
                if [ "$MCP_DEP_OK" = false ]; then
                    echo "  ⚠️ mcp --health: module mcp non trouvé dans cet environnement."
                    echo "     Installer via : pip install mcp[cli]"
                    echo "     CI Ubuntu reste la référence pour ce check."
                    echo "---"
                    echo "⚠️ MCP Health : SKIP (module mcp absent — non bloquant)"
                    exit 0
                fi
                # 2. Import des outils
                run_python -c "
import sys; sys.path.insert(0, '_gsane/mcp-server'); sys.path.insert(0, '_gsane/tools')
from compression_tool import gsane_read_canonical_brief, gsane_read_active_delivery_contract, gsane_read_project_snapshot, gsane_fetch_compressed_memory, gsane_write_session_checkpoint, gsane_read_checkpoint, gsane_route, gsane_memory_fetch, gsane_search_memory, gsane_emit_event
from security_gate import load_security_gate_config
load_security_gate_config()
assert callable(gsane_read_canonical_brief)
assert callable(gsane_read_active_delivery_contract)
assert callable(gsane_read_project_snapshot)
assert callable(gsane_search_memory)
assert callable(gsane_emit_event)
print('  [OK] Outils MCP importables : OK (10/10) + security_gate')
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

r = gsane_search_memory('agent', 'all')
assert isinstance(r, str) and len(r) > 0
print('  [OK] gsane_search_memory : OK')

r = gsane_search_memory('xyz_inexistant_99999')
assert 'Aucun résultat' in r
print('  [OK] gsane_search_memory (no result) : OK')

r = gsane_emit_event('qa_gate_passed', 'Quinn', {'tests': 155})
assert '✅' in r and 'qa_gate_passed' in r
print('  [OK] gsane_emit_event : OK')

r = gsane_emit_event('custom_nonstandard', 'Test', {'x': 1})
assert '⚠️' in r
print('  [OK] gsane_emit_event (non-standard warning) : OK')

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
    session)
        SESSIONCMD="${2:-}"
        case $SESSIONCMD in
            --resume)
                echo "🔄 GSANE Session Resume"
                echo "---"
                run_python -c "
import sys
sys.path.insert(0, '_gsane/mcp-server')
sys.path.insert(0, '_gsane/tools')
from compression_tool import gsane_read_checkpoint
result = gsane_read_checkpoint()
if 'SESSION INTERROMPUE' in result:
    print(result)
else:
    print('Aucune session interrompue. Prêt pour une nouvelle session.')
"
                ;;
            *)
                echo "Usage: bash gsane.sh session --resume"
                exit 1
                ;;
        esac
        ;;
    *)
        echo "❌ Commande '$ACTION' non reconnue."
        exit 1
        ;;
esac
