
import os
import re
import sys

def check_file(path):
    errors = 0
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if '{{project_name}}' in content:
        print(f'[FAIL] {path}: Found forbidden macro {{project_name}}')
        errors += 1

    if '{project-root}' in content:
        print(f'[FAIL] {path}: Found forbidden pseudo-variable {{project-root}}')
        error += 1

    return errors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python qa-linter.py <file-to-test>')
        sys.exit(1)
        
    total_errors = 0
    for target in sys.argv[1:]:
        if os.path.isfile(target):
            total_errors += check_file(target)
    
    if total_errors > 0:
        print(f'\nQA LINTER FAILED with {total_errors} errors.')
        sys.exit(1)
    else:
        print('\nQA LINTER PASSED. Output is strictly compliant.')
        sys.exit(0)

