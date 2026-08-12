import json
from pathlib import Path
p = Path(r'C:\Users\Stephanie.Wang\.vscode\agilent-ir-formats\simplified_morphology_analysis.ipynb')
data = json.loads(p.read_text(encoding='utf-8'))
replaced = False
for cell in data['cells']:
    if cell.get('cell_type')=='code':
        src = ''.join(cell['source'])
        old = "def match_library(spectrum):\n    spectrum = (spectrum - np.mean(spectrum)) / (np.std(spectrum) + 1e-8)\n    library_norm = (library_spectra - np.mean(library_spectra, axis=1, keepdims=True)) / (np.std(library_spectra, axis=1, keepdims=True) + 1e-8)\n    correlations = np.dot(library_norm, spectrum) / spectrum.shape[0]\n    best_ix = int(np.argmax(correlations))\n    return best_ix, float(correlations[best_ix])\n"
        new = "def match_library(spectrum):\n    spectrum = (spectrum - np.mean(spectrum)) / (np.std(spectrum) + 1e-8)\n    library_norm = (library_spectra - np.mean(library_spectra, axis=1, keepdims=True)) / (np.std(library_spectra, axis=1, keepdims=True) + 1e-8)\n    correlations = np.dot(library_norm, spectrum) / spectrum.shape[0]\n    if not np.isfinite(correlations).any():\n        return -1, 0.0\n    best_ix = int(np.nanargmax(correlations))\n    best_pr = float(correlations[best_ix])\n    return best_ix, best_pr\n"
        if old in src:
            cell['source'] = src.replace(old, new).splitlines(keepends=True)
            replaced = True
            break
if not replaced:
    raise SystemExit('old function block not found')
p.write_text(json.dumps(data, indent=1), encoding='utf-8')
print('replaced', replaced)
