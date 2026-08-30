import json
from pathlib import Path
p = Path(r'C:\Users\Stephanie.Wang\.vscode\agilent-ir-formats\simplified_morphology_analysis.ipynb')
d = json.loads(p.read_text(encoding='utf-8'))
for cell in d['cells']:
    if cell.get('cell_type') == 'code' and any('def analyze_particle' in line for line in cell['source']):
        for i, line in enumerate(cell['source']):
            if 31 <= i <= 50:
                print(i, repr(line))
        break
