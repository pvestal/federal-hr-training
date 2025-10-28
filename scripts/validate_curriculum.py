#!/usr/bin/env python3
"""
Curriculum Structure Validator
Ensures the training program maintains proper structure and organization
"""

import os
import sys
import json
from pathlib import Path

EXPECTED_STRUCTURE = {
    "01-basic-hr": {
        "modules": [],
        "assessments": [],
        "resources": []
    },
    "02-intermediate-hr": {
        "modules": [],
        "assessments": [],
        "resources": []
    },
    "03-advanced-hr": {
        "modules": [],
        "assessments": [],
        "resources": []
    },
    "04-expert-hr": {
        "modules": [],
        "assessments": [],
        "resources": []
    },
    "case-studies": [],
    "decision-trees": [],
    "opm-updates": [],
    "reference-materials": []
}

def validate_structure():
    """Validate that all required directories exist"""
    issues = []

    print("=" * 60)
    print("CURRICULUM STRUCTURE VALIDATION")
    print("=" * 60)

    # Check top-level directories
    for directory in EXPECTED_STRUCTURE.keys():
        if not os.path.exists(directory):
            issues.append(f"Missing directory: {directory}")
            print(f"✗ Missing: {directory}")
        else:
            print(f"✓ Found: {directory}")

            # Check subdirectories for training levels
            if isinstance(EXPECTED_STRUCTURE[directory], dict):
                for subdir in EXPECTED_STRUCTURE[directory].keys():
                    subdir_path = os.path.join(directory, subdir)
                    if not os.path.exists(subdir_path):
                        issues.append(f"Missing subdirectory: {subdir_path}")
                        print(f"  ✗ Missing: {subdir}")
                    else:
                        print(f"  ✓ Found: {subdir}")

    # Check for README
    if not os.path.exists("README.md"):
        issues.append("Missing README.md")
        print("✗ Missing: README.md")
    else:
        print("✓ Found: README.md")

    # Check for CURRICULUM_GUIDE
    if not os.path.exists("CURRICULUM_GUIDE.md"):
        issues.append("Missing CURRICULUM_GUIDE.md")
        print("✗ Missing: CURRICULUM_GUIDE.md")
    else:
        print("✓ Found: CURRICULUM_GUIDE.md")

    print("=" * 60)

    if issues:
        print(f"❌ Validation failed with {len(issues)} issue(s):")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ Curriculum structure is valid")
        return True

def main():
    valid = validate_structure()
    sys.exit(0 if valid else 1)

if __name__ == "__main__":
    main()
