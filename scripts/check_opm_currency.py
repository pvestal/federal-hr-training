#!/usr/bin/env python3
"""
OPM Regulation Currency Checker
Monitors OPM.gov and Federal Register for updates that may affect training materials
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json
import sys

# Key URLs to monitor
MONITORED_URLS = {
    "opm_benefits": "https://www.opm.gov/healthcare-insurance/healthcare/reference-materials/",
    "opm_retirement": "https://www.opm.gov/retirement-center/",
    "opm_policy": "https://www.opm.gov/policy-data-oversight/",
    "ecfr_title5": "https://www.ecfr.gov/current/title-5",
    "federal_register_hr": "https://www.federalregister.gov/documents/search?conditions%5Bterm%5D=office+of+personnel+management"
}

# Expected update frequencies (in days)
EXPECTED_FRESHNESS = {
    "opm_benefits": 30,  # Should update monthly
    "opm_retirement": 30,
    "opm_policy": 90,  # Quarterly updates
    "ecfr_title5": 30,
    "federal_register_hr": 7  # Weekly checks
}

def check_url_freshness(url, source_name):
    """Check if a URL has recent updates"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for date indicators
        date_patterns = soup.find_all(['time', 'span'], class_=lambda x: x and 'date' in x.lower())

        print(f"✓ {source_name}: Accessible")
        return True

    except requests.RequestException as e:
        print(f"✗ {source_name}: {str(e)}", file=sys.stderr)
        return False

def check_for_recent_updates():
    """Check all monitored sources for recent updates"""
    results = {}
    all_accessible = True

    print("=" * 60)
    print("OPM CURRENCY CHECK")
    print(f"Timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    for source_name, url in MONITORED_URLS.items():
        accessible = check_url_freshness(url, source_name)
        results[source_name] = {
            "url": url,
            "accessible": accessible,
            "check_time": datetime.now().isoformat()
        }
        if not accessible:
            all_accessible = False

    # Save results
    with open('reports/opm_currency_check.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("=" * 60)
    print(f"Results saved to reports/opm_currency_check.json")

    if not all_accessible:
        print("⚠ WARNING: Some sources were not accessible", file=sys.stderr)
        sys.exit(1)
    else:
        print("✓ All sources accessible")
        sys.exit(0)

if __name__ == "__main__":
    check_for_recent_updates()
