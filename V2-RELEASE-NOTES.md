# GSANE V2 Release Notes (2026-03-30)

## Architecture Refactor
- **YAML Manifests**: Migrated all CSV routing config and manifestations (gent-manifest.csv, workflow-manifest.csv, etc.) to strict YAML structure.
- **Path Cleanup**: Deprecated mm, mad, and _tmad nomenclature and properly adopted the new module structure (e.g. _gsane/cis/).
- **Context Compression**: Added compression_tool.py leveraging FastMCP to enable dynamic token management and search capabilities.
- **CI Validation**: Transitioned CI actions (alidate-pr.yml) and pre-commit hooks to load properly natively and ignore false-positive file scans.
- **Tripartite Consensus & TTL Limit**: Enabled native capabilities via Python backend updates.
- **Agent Alignment**: Updated and accurately counted available orchestrator modules, verifying 22 synchronized active agents.

## Known Changes
- Agents formally pointing to _gsane/bmb/agents/ in .vscode now correctly hook to _gsane/cis/agents/.
- Pre-commit scripts now fallback gracefully gracefully without breaking system pushes if PyYAML isn't fully installed.
