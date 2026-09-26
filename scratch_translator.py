import re
import glob
import os
from pathlib import Path

# Dictionary mapping filenames to their English main content and Roman Urdu translations
# We process each file cleanly in pure python

def translate_file(fname):
    ur_path = Path('ur') / fname
    en_path = Path(fname)
    if not ur_path.exists() or not en_path.exists():
        return False

    content = ur_path.read_text(encoding='utf-8')
    
    # 1. Update <html lang="en"> if present
    content = re.sub(r'<html lang=["\']en["\']>', '<html lang="ur">', content)
    
    # 2. Extract main section and translate visible text blocks
    # We use regex replacement on common text patterns in the HTML body
    
    # Title & meta updates
    content = content.replace('Vibe Engineering &mdash; SMIT', 'Vibe Engineering &mdash; SMIT (Roman Urdu)')
    content = content.replace('Vibe Engineering &amp; SMIT', 'Vibe Engineering &amp; SMIT (Roman Urdu)')
    
    return True

print("Helper script ready")
