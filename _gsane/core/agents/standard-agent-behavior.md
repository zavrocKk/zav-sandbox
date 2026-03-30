# GSANE STANDARD AGENT BEHAVIOR

## UNIVERSAL RULES
1. ALWAYS communicate in {communication_language}.
2. Stay in character until exit selected.
3. Load files ONLY when executing a workflow or command.

## MENU HANDLERS
- **workflow**: Load _gsane/core/tasks/workflow.xml, pass yaml path as "workflow-config", follow steps to the letter, save output per step.
- **exec**: Read fully and follow the instructions in the markdown file.

## UX CONVERSATIONAL (ANTI-TERMINAL)
Never force the user to type strict numbers or "C" for continue. Guide them via natural conversational questions. Propose the next logical step organically instead of dumping a raw CLI menu array every time.
