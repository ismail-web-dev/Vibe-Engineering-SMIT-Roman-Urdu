#!/usr/bin/env python3
"""
Validate all links across English and Roman Urdu versions
"""

import glob
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def extract_links(filepath):
    """Extract all href links from an HTML file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all href attributes
    links = re.findall(r'href=["\']([^"\']+)["\']', content)
    return links

def validate_site():
    """Validate all links in both English and Urdu versions"""

    errors = []

    # Get all HTML files
    english_files = glob.glob('*.html')
    urdu_files = glob.glob('ur/*.html')

    print("=" * 60)
    print("LINK VALIDATION REPORT")
    print("=" * 60)

    # Check English files
    print("\n[1] Validating English files...")
    for filepath in english_files:
        links = extract_links(filepath)
        basename = os.path.basename(filepath)

        for link in links:
            # Skip external links, anchors, and mailto
            if link.startswith(('http://', 'https://', '#', 'mailto:')):
                continue

            # Check if it's a language switcher to ur/
            if link.startswith('ur/'):
                target = link  # ur/filename.html
                if not os.path.exists(target):
                    errors.append(f"  {filepath} -> {link} [MISSING]")

            # Check relative links to other pages
            elif link.endswith('.html'):
                if not os.path.exists(link):
                    errors.append(f"  {filepath} -> {link} [MISSING]")

    if not errors:
        print("  OK All English file links valid")
    else:
        print(f"  Found {len(errors)} broken links in English files")

    # Check Urdu files
    print("\n[2] Validating Urdu files...")
    urdu_errors = []
    for filepath in urdu_files:
        links = extract_links(filepath)
        basename = os.path.basename(filepath)

        for link in links:
            # Skip external links, anchors, and mailto
            if link.startswith(('http://', 'https://', '#', 'mailto:')):
                continue

            # Check if it's a language switcher back to English
            if link.startswith('../'):
                # This should point to English version
                target = link.replace('../', '')
                if not os.path.exists(target):
                    urdu_errors.append(f"  {filepath} -> {link} [MISSING: {target}]")

            # Check relative links to other Urdu pages
            elif link.endswith('.html'):
                target = os.path.join('ur', link)
                if not os.path.exists(target):
                    urdu_errors.append(f"  {filepath} -> {link} [MISSING: {target}]")

    if not urdu_errors:
        print("  OK All Urdu file links valid")
    else:
        print(f"  Found {len(urdu_errors)} broken links in Urdu files")
        errors.extend(urdu_errors)

    # Check bidirectional language switching
    print("\n[3] Validating bidirectional language switching...")
    switch_errors = []

    for eng_file in english_files:
        basename = os.path.basename(eng_file)
        urdu_file = os.path.join('ur', basename)

        # Check if English file has correct switch to Urdu
        eng_content = open(eng_file, 'r', encoding='utf-8').read()
        if f'href="ur/{basename}"' not in eng_content:
            switch_errors.append(f"  {eng_file}: Language switcher not pointing to ur/{basename}")

        # Check if Urdu file has correct switch back to English
        if os.path.exists(urdu_file):
            urdu_content = open(urdu_file, 'r', encoding='utf-8').read()
            if f'href="../{basename}"' not in urdu_content:
                switch_errors.append(f"  {urdu_file}: Language switcher not pointing to ../{basename}")

    if not switch_errors:
        print("  OK All language switchers are bidirectional")
    else:
        print(f"  Found {len(switch_errors)} language switch issues")
        errors.extend(switch_errors)

    # Final summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"English files: {len(english_files)}")
    print(f"Urdu files: {len(urdu_files)}")
    print(f"Total errors: {len(errors)}")

    if errors:
        print("\nERRORS FOUND:")
        for error in errors:
            print(error)
        return False
    else:
        print("\nSUCCESS: All links are valid!")
        return True

if __name__ == '__main__':
    success = validate_site()
    sys.exit(0 if success else 1)
