#!/usr/bin/env python3
"""
Module Completeness Checker
Validates that all training modules have required components
"""

import os
import sys
import json
from pathlib import Path

REQUIRED_SECTIONS = [
    "## Module Overview",
    "## Content Outline",
    "## Learning Activities",
    "## Assessment",
    "## Resources"
]

TRAINING_LEVELS = [
    "01-basic-hr",
    "02-intermediate-hr",
    "03-advanced-hr",
    "04-expert-hr"
]

def check_module_structure(module_path):
    """Check if a module has all required sections"""
    try:
        with open(module_path, 'r', encoding='utf-8') as f:
            content = f.read()

        missing_sections = []
        for section in REQUIRED_SECTIONS:
            if section not in content:
                missing_sections.append(section)

        return {
            "complete": len(missing_sections) == 0,
            "missing_sections": missing_sections
        }
    except Exception as e:
        return {
            "complete": False,
            "error": str(e)
        }

def main():
    """Check all modules for completeness"""
    results = {
        "check_time": "2025-10-28",
        "modules": {}
    }

    total_modules = 0
    complete_modules = 0

    print("=" * 60)
    print("MODULE COMPLETENESS CHECK")
    print("=" * 60)

    for level in TRAINING_LEVELS:
        level_path = Path(level) / "modules"
        if level_path.exists():
            for module_file in level_path.glob("*.md"):
                total_modules += 1
                module_name = f"{level}/{module_file.name}"

                check_result = check_module_structure(module_file)
                results["modules"][module_name] = check_result

                if check_result["complete"]:
                    complete_modules += 1
                    print(f"✓ {module_name}")
                else:
                    print(f"✗ {module_name}")
                    if "missing_sections" in check_result:
                        for section in check_result["missing_sections"]:
                            print(f"  Missing: {section}")

    # Summary
    print("=" * 60)
    print(f"Total modules: {total_modules}")
    print(f"Complete modules: {complete_modules}")
    if total_modules > 0:
        completion_rate = (complete_modules / total_modules) * 100
        print(f"Completion rate: {completion_rate:.1f}%")

    # Save results
    os.makedirs('reports', exist_ok=True)
    with open('reports/module_completeness.json', 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to reports/module_completeness.json")

    # Exit with error if modules are incomplete
    if complete_modules < total_modules:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
