#!/usr/bin/env python3
"""
Smart Module Quality Checker
Validates training modules have essential content without rigid templates
"""

import os
import sys
import json
import re
from pathlib import Path

TRAINING_LEVELS = [
    "01-basic-hr",
    "02-intermediate-hr",
    "03-advanced-hr",
    "04-expert-hr"
]

def check_module_quality(module_path):
    """Check if module meets quality standards"""
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

        issues = []

        # 1. Must have title (# Module X.X: Title)
        if not re.search(r'^#\s+Module\s+\d+\.\d+:', content, re.MULTILINE):
            issues.append("Missing module title (should be: # Module X.X: Title)")

        # 2. Must have Learning Objectives
        if "Learning Objectives" not in content and "learning objectives" not in content.lower():
            issues.append("Missing Learning Objectives section")

        # 3. Must have substantial content (minimum 2000 words)
        word_count = len(content.split())
        if word_count < 2000:
            issues.append(f"Content too short ({word_count} words, minimum 2000)")

        # 4. Must have at least one example or scenario
        has_example = any(word in content.lower() for word in ["example", "scenario", "practice"])
        if not has_example:
            issues.append("No examples or practice scenarios found")

        # 5. Must have regulatory citations (5 CFR or 5 USC)
        has_citations = bool(re.search(r'5\s+(CFR|USC)', content))
        if not has_citations:
            issues.append("No regulatory citations (5 CFR or 5 USC) found")

        # 6. Must have document control footer
        if "Document Control" not in content:
            issues.append("Missing Document Control section at end")

        return {
            "quality": "good" if len(issues) == 0 else "needs_improvement",
            "word_count": word_count,
            "issues": issues
        }

    except Exception as e:
        return {
            "quality": "error",
            "error": str(e)
        }

def main():
    """Check all modules for quality"""
    results = {
        "check_time": "2025-10-28",
        "modules": {}
    }

    total_modules = 0
    good_modules = 0

    print("=" * 70)
    print("TRAINING MODULE QUALITY CHECK")
    print("Validating essential content without rigid templates")
    print("=" * 70)

    for level in TRAINING_LEVELS:
        level_path = Path(level) / "modules"
        if level_path.exists():
            for module_file in level_path.glob("module-*.md"):
                total_modules += 1
                module_name = f"{level}/{module_file.name}"

                check_result = check_module_quality(module_file)
                results["modules"][module_name] = check_result

                if check_result["quality"] == "good":
                    good_modules += 1
                    print(f"✓ {module_name} ({check_result.get('word_count', 0)} words)")
                else:
                    print(f"⚠ {module_name}")
                    if "issues" in check_result:
                        for issue in check_result["issues"]:
                            print(f"    - {issue}")
                    if "error" in check_result:
                        print(f"    ERROR: {check_result['error']}")

    # Summary
    print("=" * 70)
    print(f"Total modules: {total_modules}")
    print(f"Good quality: {good_modules}")
    if total_modules > 0:
        quality_rate = (good_modules / total_modules) * 100
        print(f"Quality rate: {quality_rate:.1f}%")

    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/module_quality.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to reports/module_quality.json")

    # Success if at least 80% good quality (allows some work-in-progress)
    if total_modules > 0 and quality_rate >= 80.0:
        print("\n✅ Quality check PASSED (≥80% good quality)")
        sys.exit(0)
    elif total_modules == 0:
        print("\n⚠️  No modules found")
        sys.exit(0)
    else:
        print(f"\n⚠️  Quality check needs improvement (<80% good quality)")
        sys.exit(1)

if __name__ == "__main__":
    main()
