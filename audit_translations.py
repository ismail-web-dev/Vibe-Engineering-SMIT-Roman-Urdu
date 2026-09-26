#!/usr/bin/env python3
"""
Audit Urdu translations by checking if actual content is in Roman Urdu or still English.
"""
import os
import re
from pathlib import Path

def extract_main_content(html_file):
    """Extract the main text content from HTML, excluding code/technical elements."""
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove script tags
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        # Remove style tags
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
        # Remove code blocks
        content = re.sub(r'<pre>.*?</pre>', '', content, flags=re.DOTALL)
        content = re.sub(r'<code[^>]*>.*?</code>', '', content, flags=re.DOTALL)
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', ' ', content)
        # Remove URLs
        content = re.sub(r'https?://\S+', '', content)

        return content
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return ""

def is_urdu_content(text):
    """
    Check if text contains Roman Urdu indicators.
    Roman Urdu uses specific words and patterns.
    """
    # Common Roman Urdu words/patterns
    urdu_indicators = [
        'hai', 'hain', 'ka', 'ke', 'ki', 'ko', 'se', 'mein', 'par', 'aur',
        'yeh', 'woh', 'kya', 'kaise', 'kyun', 'jab', 'tab', 'agar',
        'hum', 'aap', 'apna', 'apne', 'humara', 'humare', 'aapka', 'aapke',
        'karna', 'karte', 'karein', 'kiya', 'hota', 'hoti', 'hote',
        'liye', 'sath', 'darmiyan', 'baad', 'pehle', 'tak', 'bhi',
        'nahi', 'nahin', 'tha', 'thi', 'the', 'tha',
        'ab', 'phir', 'yahaan', 'wahaan', 'kahan', 'jahan',
        'dekhen', 'dekhein', 'samjhen', 'samjhein', 'poochein', 'karein',
        'banayein', 'banayen', 'shuru', 'khatam', 'zyada', 'kam',
        'achha', 'accha', 'bura', 'theek', 'bilkul', 'sirf', 'bas'
    ]

    # English-specific indicators that should NOT appear in Urdu content
    english_indicators = [
        'the ', 'and ', 'you ', 'are ', 'this ', 'that ', 'have ', 'with ',
        'from ', 'they ', 'will ', 'would ', 'should ', 'could ', 'been ',
        'were ', 'what ', 'when ', 'where ', 'which ', 'their ', 'there ',
        'before ', 'after ', 'about ', 'because ', 'through ', 'during ',
        'without ', 'between ', 'under ', 'over ', 'again ', 'while '
    ]

    text_lower = text.lower()

    # Count Urdu indicators
    urdu_count = sum(1 for word in urdu_indicators if f' {word} ' in text_lower or text_lower.startswith(f'{word} '))

    # Count English indicators
    english_count = sum(1 for phrase in english_indicators if phrase in text_lower)

    # Simple heuristic: if we see more English than Urdu indicators, it's English
    return urdu_count > english_count

def audit_file(english_file, urdu_file):
    """Audit a single Urdu file against its English source."""
    if not urdu_file.exists():
        return 'MISSING'

    urdu_content = extract_main_content(urdu_file)

    # Check if there's substantial content
    words = urdu_content.split()
    if len(words) < 50:  # Too little content to judge
        return 'UNKNOWN'

    if is_urdu_content(urdu_content):
        return 'URDU'
    else:
        return 'ENGLISH'

def main():
    root = Path('.')
    ur_dir = root / 'ur'

    english_files = sorted([f for f in root.glob('*.html')
                           if f.name.startswith(('class', 'day', 'lab', 'index'))])

    results = {
        'URDU': [],
        'ENGLISH': [],
        'MISSING': [],
        'UNKNOWN': []
    }

    for eng_file in english_files:
        urdu_file = ur_dir / eng_file.name
        status = audit_file(eng_file, urdu_file)
        results[status].append(eng_file.name)
        print(f"{status:8} {eng_file.name}")

    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print(f"Already in Urdu:  {len(results['URDU'])}")
    print(f"Still in English: {len(results['ENGLISH'])}")
    print(f"Missing files:    {len(results['MISSING'])}")
    print(f"Unknown status:   {len(results['UNKNOWN'])}")
    print(f"Total files:      {len(english_files)}")

    if results['ENGLISH']:
        print("\nFiles still in English:")
        for f in results['ENGLISH']:
            print(f"  - {f}")

if __name__ == '__main__':
    main()
