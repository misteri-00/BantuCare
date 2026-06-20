import os
import re

mapping = {
    'home.py': 'home',
    'programdonasi.py': 'programdonasi',
    'impacttracker.py': 'transparansi',
    'volunteercenter.py': 'volunteer',
    'tentangkami.py': 'tentangkami',
    'aichatbot.py': 'aichatbot',
    'donasi.py': 'donasi',
    'riwayatdonasi.py': 'riwayat',
    'petabantuan.py': 'petabantuan'
}

for fname, nav_arg in mapping.items():
    path = os.path.join('pages', fname)
    if not os.path.exists(path): continue
    
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'from utils.navbar' not in content:
        content = content.replace('import streamlit as st', 'import streamlit as st\nfrom utils.navbar_dark import render_navbar', 1)
    else:
        # replace any existing import
        content = re.sub(r'from utils\.navbar.*? import render_navbar', 'from utils.navbar_dark import render_navbar', content)
        
    if 'def main():' in content:
        parts = content.split('def main():', 1)
        if 'render_navbar' not in parts[1]:
            content = parts[0] + 'def main():\n    render_navbar("' + nav_arg + '")' + parts[1]
        else:
            # Replace existing render_navbar call just in case it's using old name or no arg
            parts[1] = re.sub(r'render_navbar\([^)]*\)', f'render_navbar("{nav_arg}")', parts[1])
            content = parts[0] + 'def main():' + parts[1]
            
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
print("Patching complete.")
