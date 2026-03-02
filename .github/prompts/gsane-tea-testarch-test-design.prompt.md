---
description: 'Test Design'
agent: 'agent'
tools: ['read', 'edit', 'search', 'execute']
---

1. Load {project-root}/_gsane/core/config.yaml and store ALL fields as session variables
2. Load the workflow engine at {project-root}/_gsane/core/tasks/workflow.xml
3. Load and execute the workflow configuration at {project-root}/_gsane/tea/workflows/testarch/test-design/workflow.yaml using the engine from step 2
