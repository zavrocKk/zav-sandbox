#!/bin/bash
# ----------------------------------------------------------------------------- 
# GSANE Core CLI Router (Zero-Touch Edition)
# ----------------------------------------------------------------------------- 

ACTION=$1

if [ -z "$ACTION" ]; then
    echo "Usage: bash gsane.sh <command>"
    echo "Commands:"
    echo "  doctor       : Vérifie l'intégrité de l'environnement (session-start + YAML validation)"
    echo "  validate     : Exécution de la Quality Gate (pytest + qa-linter + CHANGELOG check)"
    echo "  trace        : Observabilité — sous-commandes : --tail N | --summary | --p2p"
    echo "  mcp --health     : Vérifie les prérequis MCP (dépendances, imports, schéma)"
    echo "  mcp --smoke-test : Vérifie que tous les outils MCP fonctionnent end-to-end"
    exit 1
fi

case $ACTION in
    doctor|health-check)
        echo "🩺 GSANE Doctor - Health Check global"
        echo "----------------------------------------"
        echo "1️⃣  Validation des liens morts (via session-start)..."
        if [ -f .github/hooks/session-start.sh ]; then
            bash .github/hooks/session-start.sh
        fi
        echo "----------------------------------------"
        echo "2️⃣  Validation hiérarchique des YAML..."
        python -c "
import yaml, glob, sys
files = glob.glob('_gsane/_config/*.yaml')
errors = 0
for f in files:
    try:
        yaml.safe_load(open(f, encoding='utf-8'))
        print(f'  ✅ {f} : OK')
    except Exception as e:
        print(f'  ❌ {f} : ERREUR ({e})')
        errors += 1
if errors > 0: sys.exit(1)
"
        if [ $? -eq 0 ]; then
            echo "✅ GSANE est sain."
        else
            echo "❌ Erreurs détectées par le Doctor."
            exit 1
        fi
        ;;

    validate)
        echo "🔍 Quality Gate : Exécution de la suite de tests Python..."       

        python -m pytest tests/ -m "not behavioral"
        EXIT_CODE=$?

        if [ $EXIT_CODE -ne 0 ]; then
            echo "❌ Quality Gate Failed : Des tests ont échoué ! (Code: $EXIT_CODE)"
            exit 1
        fi

        echo "🔍 QA Linter (Zero-Touch validation)..."
        python tests/qa-linter.py _gsane/agents/*.md
        if [ $? -ne 0 ]; then
            echo "❌ QA Linter Failed : Non-compliance détectée dans les fichiers des agents."
            exit 1
        fi

        echo "🔍 Vérification documentaire..."
        if git status --porcelain | grep -E '^ M|^ A|^AM|^A |^M |^\?\?' | grep -q "src/"; then
            if ! git status --porcelain | grep -E '^ M|^ A|^AM|^A |^M |^\?\?' | grep -q "CHANGELOG.md"; then
                echo "❌ ERREUR: Code source modifié mais CHANGELOG.md ignoré." 
                echo "➡️ Règle de la Strike Team : Tout nouveau code exige une ligne de changelog."
                exit 1
            fi
        fi

        echo "🔍 Validation schéma execution-plan.yaml (sessions)..."
        PLAN_COUNT=0
        for f in $(find _gsane-output/sessions -name "execution-plan.yaml" 2>/dev/null); do
            PLAN_COUNT=$((PLAN_COUNT + 1))
            python -c "
import sys
sys.path.insert(0, 'tests')
import qa_linter
exit(qa_linter.validate_execution_plan_schema('$f'))
"
            if [ $? -ne 0 ]; then
                echo "❌ Schéma invalide : $f"
                exit 1
            fi
        done
        if [ $PLAN_COUNT -eq 0 ]; then
            echo "   (aucun execution-plan.yaml trouvé — skip)"
        fi

        echo "✅ Quality Gate Passed : Tous les tests sont validés !"
        exit 0
        ;;

    trace)
        TRACE_FILE="_gsane/_memory/trace.log"
        SUBCMD=$2

        case $SUBCMD in
            --tail)
                N=${3:-10}
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "⚠️  trace.log not found. No events yet."
                    exit 0
                fi
                echo "📋 Last $N trace events:"
                echo "---"
                # Each YAML entry starts with "- timestamp:", split on those
                python -c "
import sys
content = open('$TRACE_FILE', encoding='utf-8').read()
entries = [e.strip() for e in content.split('- timestamp:') if e.strip()]
entries = entries[-${N}:]
for e in entries:
    print('- timestamp:' + e)
    print()
" 2>/dev/null || tail -n $((N * 10)) "$TRACE_FILE"
                ;;
            --summary)
                if [ ! -f "$TRACE_FILE" ]; then
                    echo "⚠️  trace.log not found."
                    exit 0
                fi
                echo "📊 Trace Summary:"
                python -c "
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
                python -c "
import re, yaml
content = open('$TRACE_FILE', encoding='utf-8', errors='replace').read()
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
            *)
                echo "Usage: bash gsane.sh trace --tail N | --summary | --p2p"
                exit 1
                ;;
        esac
        ;;
    mcp)
        MCPCMD=$2
        case $MCPCMD in
            --health)
                echo "🔌 GSANE MCP Health Check"
                echo "---"
                # 1. Dépendances
                python -c "from mcp.server.fastmcp import FastMCP; import yaml; print('  ✅ Dépendances MCP : OK')" 2>/dev/null || { echo "  ❌ Dépendances manquantes — pip install -r _gsane/mcp-server/requirements.txt"; exit 1; }
                # 2. Import des outils
                python -c "
import sys; sys.path.insert(0, '_gsane/mcp-server')
from compression_tool import gsane_fetch_compressed_memory, gsane_write_session_checkpoint, gsane_read_checkpoint, gsane_route, gsane_memory_fetch
print('  ✅ Outils MCP importables : OK (5/5)')
" 2>/dev/null || { echo "  ❌ Erreur d'import des outils MCP"; exit 1; }
                # 3. Schéma delegation-matrix.yaml
                python -c "
import yaml, sys
with open('_gsane/_config/delegation-matrix.yaml', encoding='utf-8') as f:
    data = yaml.safe_load(f)
rules = data.get('rules', [])
for r in rules:
    assert 'trigger' in r, f'Clé manquante trigger: {r}'
    assert 'agent' in r, f'Clé manquante agent: {r}'
print(f'  ✅ delegation-matrix.yaml schéma OK ({len(rules)} règles)')
" 2>/dev/null || { echo "  ❌ Schema mismatch dans delegation-matrix.yaml"; exit 1; }
                echo "---"
                echo "✅ MCP Health : TOUS LES CHECKS PASSÉS"
                ;;
            --smoke-test)
                echo "🔬 GSANE MCP Smoke Test"
                echo "---"
                python -c "
import sys, os
sys.path.insert(0, '_gsane/mcp-server')
from compression_tool import (gsane_fetch_compressed_memory, gsane_write_session_checkpoint,
    gsane_read_checkpoint, gsane_route, gsane_memory_fetch)

r = gsane_fetch_compressed_memory('master')
assert r is not None
print('  ✅ gsane_fetch_compressed_memory : OK')

r = gsane_write_session_checkpoint('plan test', 'next step', 'decision A', 'item B', 'risk C', 1)
assert '✅' in r, f'Echec write: {r}'
print('  ✅ gsane_write_session_checkpoint : OK')

r = gsane_read_checkpoint()
assert r is not None
print('  ✅ gsane_read_checkpoint : OK')

r = gsane_route('implement a new feature with code')
assert r is not None
print(f'  ✅ gsane_route : OK — {r[:60]}')

r = gsane_memory_fetch('master', '')
assert r is not None
print(f'  ✅ gsane_memory_fetch : OK — {len(r)} chars')

print('---')
print('✅ MCP Smoke Test : TOUS LES CHECKS PASSÉS')
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
