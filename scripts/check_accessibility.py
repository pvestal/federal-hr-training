#!/usr/bin/env python3
"""
Section 508 Accessibility Compliance Checker for Federal HR Training Materials
Checks markdown files for basic accessibility compliance
"""

import os
import re
from pathlib import Path

def check_headings_structure(content, filename):
    """Check if headings follow proper hierarchy"""
    issues = []
    lines = content.split('\n')

    heading_levels = []
    for i, line in enumerate(lines, 1):
        if line.startswith('#'):
            level = len(line.split()[0])  # Count # characters
            if level > 6:
                issues.append(f"{filename}:{i} - Heading level too deep (h{level})")
            heading_levels.append(level)

    # Check for skipped heading levels
    for i in range(1, len(heading_levels)):
        if heading_levels[i] - heading_levels[i-1] > 1:
            issues.append(f"{filename} - Skipped heading level (h{heading_levels[i-1]} to h{heading_levels[i]})")

    return issues

def check_alt_text_images(content, filename):
    """Check if images have alt text"""
    issues = []
    # Find markdown images ![alt](src)
    image_pattern = r'!\[([^\]]*)\]\([^)]+\)'
    matches = re.finditer(image_pattern, content)

    for match in matches:
        alt_text = match.group(1)
        if not alt_text.strip():
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"{filename}:{line_num} - Image missing alt text")
        elif len(alt_text.strip()) < 3:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"{filename}:{line_num} - Alt text too short: '{alt_text}'")

    return issues

def check_links_descriptive(content, filename):
    """Check if links have descriptive text"""
    issues = []
    # Find markdown links [text](url)
    link_pattern = r'\[([^\]]+)\]\([^)]+\)'
    matches = re.finditer(link_pattern, content)

    non_descriptive = ['click here', 'here', 'link', 'read more', 'more', 'this']

    for match in matches:
        link_text = match.group(1).lower().strip()
        if link_text in non_descriptive:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"{filename}:{line_num} - Non-descriptive link text: '{link_text}'")

    return issues

def check_table_headers(content, filename):
    """Check if tables have proper headers"""
    issues = []
    lines = content.split('\n')

    in_table = False
    table_start_line = 0

    for i, line in enumerate(lines, 1):
        if '|' in line and not in_table:
            in_table = True
            table_start_line = i
            # Check if next line has header separator
            if i < len(lines) and '|' in lines[i]:
                if not re.search(r'\|[-\s:]+\|', lines[i]):
                    issues.append(f"{filename}:{table_start_line} - Table missing header row separator")
        elif in_table and '|' not in line:
            in_table = False

    return issues

def check_color_contrast_references(content, filename):
    """Check for potential color-only information"""
    issues = []
    color_words = ['red', 'green', 'blue', 'yellow', 'orange', 'purple', 'pink']

    for word in color_words:
        if re.search(rf'\b{word}\b', content, re.IGNORECASE):
            issues.append(f"{filename} - Warning: Contains color reference '{word}' - ensure information is not conveyed by color alone")

    return issues

def run_accessibility_checks():
    """Run all accessibility checks on markdown files"""
    all_issues = []

    # Find all markdown files
    md_files = list(Path('.').glob('**/*.md'))

    for md_file in md_files:
        if 'node_modules' in str(md_file) or '.git' in str(md_file):
            continue

        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()

            filename = str(md_file)

            # Run checks
            all_issues.extend(check_headings_structure(content, filename))
            all_issues.extend(check_alt_text_images(content, filename))
            all_issues.extend(check_links_descriptive(content, filename))
            all_issues.extend(check_table_headers(content, filename))
            all_issues.extend(check_color_contrast_references(content, filename))

        except Exception as e:
            all_issues.append(f"{md_file} - Error reading file: {e}")

    return all_issues

def main():
    print("🔍 Running Section 508 Accessibility Checks...")
    print("=" * 60)

    issues = run_accessibility_checks()

    if not issues:
        print("✅ No accessibility issues found!")
        print("\n📊 Checks performed:")
        print("  • Heading structure hierarchy")
        print("  • Image alt text presence")
        print("  • Descriptive link text")
        print("  • Table header markup")
        print("  • Color-only information warnings")

    else:
        print(f"⚠️  Found {len(issues)} accessibility issues:")
        print()

        for issue in issues:
            if "Warning:" in issue:
                print(f"⚠️  {issue}")
            else:
                print(f"❌ {issue}")

        print(f"\n📊 Total issues: {len(issues)}")

        # Don't exit with error code for warnings
        warnings_only = all("Warning:" in issue for issue in issues)
        if not warnings_only:
            exit(1)

if __name__ == "__main__":
    main()