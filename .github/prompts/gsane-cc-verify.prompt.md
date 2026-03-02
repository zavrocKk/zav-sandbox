---
name: gsane-cc-verify
description: Run the Completion Contract — verify a task is truly done before declaring it complete
applyTo: "**"
---

Load and execute `{project-root}/_gsane/core/workflows/cc-verify/workflow.md`.

Run all 20 checks. Output the result as:
- `[CC] ✅ PASS — {N}/20 checks OK` if all pass
- `[CC] ❌ FAIL — {N}/20 checks OK — Items manquants : {list of failed items}` if any fail

Do not ask for confirmation — execute silently and report results.
