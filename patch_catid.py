from pathlib import Path
path = Path(r'C:\Users\Stephanie.Wang\.vscode\agilent-ir-formats\library_OS_fit.py')
text = path.read_text(encoding='utf-8')
old = "def catID(k):\n    return (OS_meta_ix[OS_meta_ix['index'] == k]['simplified_names']).values[0]\n"
new = "def catID(k):\n    matches = OS_meta_ix[OS_meta_ix['index'] == k]['simplified_names']\n    if len(matches) == 0:\n        return 'unknown polymer'\n    return matches.values[0]\n"
if old not in text:
    raise SystemExit('old catID block not found')
path.write_text(text.replace(old, new), encoding='utf-8')
print('patched library_OS_fit.py')
