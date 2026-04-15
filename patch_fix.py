import json
from pathlib import Path
p = Path(r'C:\Users\Stephanie.Wang\.vscode\agilent-ir-formats\simplified_morphology_analysis.ipynb')
data = json.loads(p.read_text(encoding='utf-8'))
updated = False
for cell in data['cells']:
    if cell.get('cell_type') == 'code' and any('def analyze_particle' in line for line in cell['source']):
        src = cell['source']
        for i, line in enumerate(src):
            if line.strip() == 'representative = cpca(spectra, range(1))[0].astype(DTYPE)':
                src[i+1:i+1] = [
                    '    if representative.shape[0] != wavenumbers.shape[0]:\n',
                    '        representative = np.interp(\n',
                    '            wavenumbers,\n',
                    '            np.linspace(wavenumbers[0], wavenumbers[-1], representative.shape[0]),\n',
                    '            representative\n',
                    '        ).astype(DTYPE)\n'
                ]
                cell['source'] = src
                updated = True
                break
        if updated:
            break
if not updated:
    raise SystemExit('not updated')
p.write_text(json.dumps(data, indent=1), encoding='utf-8')
print('updated')
