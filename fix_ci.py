import sys
with open('.github/workflows/validate-pr.yml', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('import csv, sys, os', 'import yaml, sys, os')
text = text.replace("with open('_gsane/_config/workflow-manifest.csv'", "with open('_gsane/_config/workflow-manifest.yaml'")
text = text.replace('reader = csv.DictReader(f)', 'reader = yaml.safe_load(f)')
text = text.replace('workflow-manifest.csv', 'workflow-manifest.yaml')

text = text.replace('import csv, sys', 'import yaml, sys')
text = text.replace("with open('_gsane/_config/agent-manifest.csv'", "with open('_gsane/_config/agent-manifest.yaml'")
text = text.replace('reader = csv.DictReader(f)', 'reader = yaml.safe_load(f)')
text = text.replace('agent-manifest.csv', 'agent-manifest.yaml')

text = text.replace('echo "🔍 Checking workflow manifest file integrity..."', 'pip3 install pyyaml\n          echo "🔍 Checking workflow manifest file integrity..."')

with open('.github/workflows/validate-pr.yml', 'w', encoding='utf-8') as f:
    f.write(text)