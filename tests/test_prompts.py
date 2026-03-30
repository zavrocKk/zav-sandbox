
import pytest
import os

def test_template_sync_with_prompt():
    # 1. Lire le template
    with open('_gsane/bmad/data/product-brief.template.md', 'r', encoding='utf-8') as f:
        template = f.read()
    
    # 2. Lire le step (prompt)
    with open('_gsane/bmad/workflows/1-analysis/create-product-brief/steps/step-01-init.md', 'r', encoding='utf-8') as f:
        prompt = f.read()

    # Si le template reclame les 'Risques', le mot doit figurer dans le prompt pour guider le LLM
    if '## Risques' in template:
        assert 'Risques' in prompt, 'The prompt step-01-init does not instruct on the Risques section despite it existing in the template. This leads to Silent Desync.'
        
    assert True

