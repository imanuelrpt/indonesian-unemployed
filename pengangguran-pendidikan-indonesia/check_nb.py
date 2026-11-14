import nbformat
import sys
sys.path.insert(0, '.')

try:
    nb = nbformat.read('notebooks/02_eda.ipynb', as_version=4)
    print('Read OK, cells:', len(nb.cells))
    for i, c in enumerate(nb.cells):
        print(f'Cell {i}: type={c.cell_type}', end='')
        if hasattr(c, 'source'):
            src = c.source if isinstance(c.source, str) else ''.join(c.source)
            print(f', source_len={len(src)}', end='')
        print()
except Exception as e:
    print('Error reading:', e)
    import traceback
    traceback.print_exc()