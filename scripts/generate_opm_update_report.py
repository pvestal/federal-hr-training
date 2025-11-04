#!/usr/bin/env python3
"""
Generate consolidated OPM update report

This script consolidates outputs from all OPM monitoring scripts
and generates a comprehensive markdown report.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Cache files from monitoring scripts
CACHE_DIR = Path(__file__).parent / ".cache"
FEDERAL_REGISTER_CACHE = CACHE_DIR / "federal_register_last_check.json"
BENEFITS_CACHE = CACHE_DIR / "opm_benefits_checksums.json"
POLICY_CACHE = CACHE_DIR / "opm_policy_checksums.json"


def check_for_updates():
    """Check if any monitoring script detected updates"""
    has_updates = False
    update_details = {
        'federal_register': False,
        'benefits': False,
        'policy': False,
    }

    # Check Federal Register cache
    if FEDERAL_REGISTER_CACHE.exists():
        try:
            with open(FEDERAL_REGISTER_CACHE, 'r') as f:
                data = json.load(f)
                if data.get('last_documents'):
                    update_details['federal_register'] = True
                    has_updates = True
        except Exception:
            pass

    # Check if Benefits cache was recently updated (within last 2 hours)
    if BENEFITS_CACHE.exists():
        cache_age = datetime.now().timestamp() - BENEFITS_CACHE.stat().st_mtime
        if cache_age < 7200:  # 2 hours
            update_details['benefits'] = True
            has_updates = True

    # Check if Policy cache was recently updated (within last 2 hours)
    if POLICY_CACHE.exists():
        cache_age = datetime.now().timestamp() - POLICY_CACHE.stat().st_mtime
        if cache_age < 7200:  # 2 hours
            update_details['policy'] = True
            has_updates = True

    return has_updates, update_details


def generate_report():
    """Generate a consolidated OPM update report"""
    has_updates, update_details = check_for_updates()

    if not has_updates:
        # Output empty report if no updates
        return

    # Generate report header
    print(f"# OPM Update Report")
    print(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")
    print(f"\n---\n")

    print("## Summary")
    print("\nThe automated OPM monitoring system has detected potential updates to federal HR regulations and guidance.\n")

    # Report which sources have updates
    sources_with_updates = []
    if update_details['federal_register']:
        sources_with_updates.append("Federal Register")
    if update_details['benefits']:
        sources_with_updates.append("OPM Benefits Administration")
    if update_details['policy']:
        sources_with_updates.append("OPM Policy & Oversight")

    if sources_with_updates:
        print(f"**Sources with Updates:** {', '.join(sources_with_updates)}\n")

    print("## Action Required")
    print("\nPlease review the following:")
    print("\n1. **Verify Changes:** Review the specific changes detected by each monitoring script")
    print("2. **Impact Assessment:** Determine which training modules are affected")
    print("3. **Update Content:** Revise training materials to reflect new guidance")
    print("4. **Quality Check:** Ensure all references and examples are current")
    print("5. **Document Changes:** Update the curriculum change log")

    print("\n## Monitoring Sources")
    print("\n### Federal Register")
    if update_details['federal_register']:
        print("✅ **Updates Detected** - New HR-related rules or notices published")
        print("\nReview Federal Register monitoring output for details.")
    else:
        print("✓ No new HR-related Federal Register entries")

    print("\n### OPM Benefits Administration")
    if update_details['benefits']:
        print("✅ **Updates Detected** - Changes to OPM Benefits pages")
        print("\nReview OPM Benefits monitoring output for details.")
    else:
        print("✓ No changes to OPM Benefits pages")

    print("\n### OPM Policy & Oversight")
    if update_details['policy']:
        print("✅ **Updates Detected** - Changes to OPM Policy pages")
        print("\nReview OPM Policy monitoring output for details.")
    else:
        print("✓ No changes to OPM Policy pages")

    print("\n## Training Modules to Review")
    print("\nBased on typical update patterns, consider reviewing:")
    print("\n- **Module 2-3:** Federal Benefits Overview & FEHB")
    print("- **Module 4:** FERS Fundamentals")
    print("- **Module 7-8:** Advanced Benefits Counseling")
    print("- **Module 10:** Retirement Benefits Administration")
    print("- **Reference Materials:** 5 CFR Quick Reference")

    print("\n## Next Steps")
    print("\n1. Review the detailed workflow logs for specific changes")
    print("2. Access the monitoring script outputs in the workflow artifacts")
    print("3. Create task tickets for affected modules")
    print("4. Schedule content review with subject matter experts")
    print("5. Update and test revised training materials")

    print("\n---")
    print("\n*This report was automatically generated by the OPM Update Monitor workflow.*")
    print("\n*For questions or issues, please contact the training content team.*")


def main():
    """Main function"""
    try:
        generate_report()
        return 0
    except Exception as e:
        print(f"Error generating OPM update report: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
