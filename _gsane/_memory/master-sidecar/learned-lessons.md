# Master Sidecar — learned-lessons

> Leçons accumulées par Langis. Chargé uniquement si non vide.

- LESSON-001 : Les DC doivent lister TOUS les fichiers à créer, y compris les fichiers de config annexes (.customize.yaml, manifests, etc.). Bond ne peut pas créer ce qui n'est pas dans le DC.
- Bond n'a pas créé vera.customize.yaml et sage.customize.yaml car le DC P6-G ne les listait pas explicitement et le qa-linter ne vérifie pas leur présence.
- Les subagents légers doivent rester compacts, mais leur activation réelle doit être simulée au moins une fois après création.
- Les comptes de tests doivent être annoncés avec la décomposition explicite: structurels exécutés, behavioral désélectionnés, total collecté.
