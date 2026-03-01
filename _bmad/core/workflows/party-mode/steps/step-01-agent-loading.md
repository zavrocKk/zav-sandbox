# Step 1: Agent Index Loading and Party Mode Initialization

## MANDATORY EXECUTION RULES (READ FIRST):

- ✅ YOU ARE BMAD MASTER acting as smart party mode orchestrator
- 🎯 LOAD ONLY THE LIGHTWEIGHT INDEX — 4 fields per agent (name, displayName, icon, capabilities)
- 🚫 FORBIDDEN to load full agent profiles, identity, communicationStyle, or .md files at this step
- 📋 STORE {agent_index} as session variable — it persists for the full party mode session
- ✅ YOU MUST ALWAYS SPEAK OUTPUT in {communication_language}

## EXECUTION PROTOCOLS:

- 🎯 Parse manifest for index fields only — do NOT load full rows
- ⚠️ Present [C] continue option after index is loaded
- 💾 ONLY update frontmatter when user chooses C (Continue)
- 📖 Update frontmatter `stepsCompleted: [1]` before loading next step
- 🚫 FORBIDDEN to start conversation until C is selected

## CONTEXT BOUNDARIES:

- Agent manifest CSV is available at `{project-root}/_bmad/_config/agent-manifest.csv`
- User configuration from config.yaml is already resolved in session — do NOT reload it
- Party mode is standalone interactive workflow
- {agent_index} is the only data structure built at this step

## YOUR TASK:

Build a lightweight agent index for JIT selection, then activate party mode.

## INITIALIZATION SEQUENCE:

### 1. Build Agent Index (Lightweight)

Parse CSV manifest from `{project-root}/_bmad/_config/agent-manifest.csv`.

Extract ONLY these 4 columns for each row:

- **name** — agent identifier (used for selection scoring)
- **displayName** — persona name (shown to user)
- **icon** — emoji identifier
- **capabilities** — keyword string (used for relevance scoring against user topic)

Store result as `{agent_index}` — a compact list of (name, displayName, icon, capabilities) tuples.

> ⚠️ Do NOT read: title, role, identity, communicationStyle, principles, module, path at this step.

### 2. Party Mode Activation

Generate the welcome message:

"🎉 PARTY MODE ACTIVÉ ! 🎉

Bienvenue {{user_name}} ! BMad Master a chargé l'index de **[N] agents** disponibles. Les experts n'entrent en scène que lorsqu'ils sont pertinents pour votre sujet — approche sélective et efficace.

**De quoi voulez-vous discuter avec l'équipe aujourd'hui ?**"

> Replace [N] with the count of agents in {agent_index}. Do NOT list agents here.

### 3. Present Continue Option

"**Index chargé — [N] agents prêts.**

[C] Continuer — Démarrer la discussion"

### 4. Handle Continue Selection

#### If 'C' (Continue):

- Update frontmatter: `stepsCompleted: [1]`, `agent_index_loaded: true`, `party_active: true`
- Load: `./step-02-discussion-orchestration.md`

## SUCCESS METRICS:

✅ Manifest parsed for index fields only (4 columns)
✅ {agent_index} stored as session variable
✅ No full agent profiles or .md files loaded
✅ Welcome message shows agent count only
✅ [C] continue option presented and handled
✅ Frontmatter updated correctly
✅ Routed to step-02

## FAILURE MODES:

❌ Loading full agent profiles or .md files at this step
❌ Reloading config.yaml (already in session)
❌ Listing all agents in the welcome message
❌ Starting conversation without user C selection

## NEXT STEP:

After user selects 'C', load `./step-02-discussion-orchestration.md`. BMad Master will use {agent_index} to score and select agents JIT for each user message.
