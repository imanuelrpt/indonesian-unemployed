import nbformat
from nbclient import NotebookClient
import os

os.chdir(r'C:\DA_file\Voicelove\pengangguran-pendidikan-indonesia')
p = 'notebooks/02_eda.ipynb'
nb = nbformat.read(p, as_version=4)
nc = NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': 'notebooks'}})
nc.execute()
nbformat.write(nb, p)
print('Notebook executed successfully, errors:', sum(1 for c in nb.cells if c.cell_type == 'code' for o in c.get('outputs', []) if o.get('output_type') == 'error'))