import json
from pathlib import Path
p = Path(r'C:\Users\Stephanie.Wang\.vscode\agilent-ir-formats\simplified_morphology_analysis.ipynb')
data = json.loads(p.read_text(encoding='utf-8'))
for cell in data['cells']:
    if cell.get('cell_type') == 'code' and any('def analyze_particle' in line for line in cell['source']):
        for line in cell['source']:
            if 'representative = cpca' in line or 'np.interp' in line or 'processed = spec_p.proc' in line:
                print(line, end='')
        break
