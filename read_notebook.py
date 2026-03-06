import json
import os

notebook_path = r"D:\crewai-work\Minnor-crew.ipynb"

try:
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    print(f"Cells found: {len(nb.get('cells', []))}")
    
    for i, cell in enumerate(nb.get('cells', [])):
        if cell['cell_type'] == 'code':
            print(f"\n--- CELL {i} ---\n")
            print("".join(cell['source']))
            
except Exception as e:
    print(f"Error reading notebook: {e}")
