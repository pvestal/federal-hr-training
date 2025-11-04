#!/usr/bin/env python3
"""
Monitor Federal Register for HR-related updates

This script checks the Federal Register API for new rules, notices, and proposed rules
related to federal human resources management, benefits, and personnel policies.
"""

import sys
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
import requests

# Federal Register API endpoint
API_BASE = "https://www.federalregister.gov/api/v1"

# HR-related agencies and topics
HR_AGENCIES = [
    "office-of-personnel-management",
    "merit-systems-protection-board",
    "federal-labor-relations-authority",
]

HR_TOPICS = [
    "employee benefits",
    "retirement",
    "health insurance",
    "federal employees",
    "personnel management",
    "position classification",
    "pay administration",
    "leave administration",
]

CACHE_FILE = Path(__file__).parent / ".cache" / "federal_register_last_check.json"


def load_cache():
    """Load the last check date from cache"""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('last_check'), data.get('last_documents', [])
        except Exception as e:
            print(f"Warning: Could not load cache: {e}", file=sys.stderr)
    return None, []


def save_cache(last_check, document_numbers):
    """Save the last check date and document numbers to cache"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({
                'last_check': last_check,
                'last_documents': document_numbers
            }, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}", file=sys.stderr)


def search_federal_register(start_date, end_date):
    """Search Federal Register for HR-related documents"""
    updates = []

    for agency in HR_AGENCIES:
        try:
            params = {
                'conditions[agencies][]': agency,
                'conditions[publication_date][gte]': start_date,
                'conditions[publication_date][lte]': end_date,
                'per_page': 100,
                'order': 'newest'
            }

            response = requests.get(f"{API_BASE}/documents.json", params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            for doc in data.get('results', []):
                # Check if document is relevant to HR topics
                title = doc.get('title', '').lower()
                abstract = doc.get('abstract', '').lower()

                if any(topic.lower() in title or topic.lower() in abstract for topic in HR_TOPICS):
                    updates.append({
                        'title': doc.get('title'),
                        'document_number': doc.get('document_number'),
                        'publication_date': doc.get('publication_date'),
                        'type': doc.get('type'),
                        'abstract': doc.get('abstract', '')[:500],  # Truncate abstract
                        'url': doc.get('html_url'),
                        'agency': agency
                    })

        except requests.exceptions.RequestException as e:
            print(f"Error fetching from Federal Register for {agency}: {e}", file=sys.stderr)
            continue

    return updates


def main():
    """Main function to monitor Federal Register updates"""
    try:
        # Load cache to get last check date
        last_check, last_documents = load_cache()

        # Determine date range
        end_date = datetime.now().strftime('%Y-%m-%d')

        if last_check:
            start_date = last_check
        else:
            # First run - check last 7 days
            start_date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')

        print(f"Checking Federal Register from {start_date} to {end_date}", file=sys.stderr)

        # Search for updates
        updates = search_federal_register(start_date, end_date)

        # Filter out documents we've already seen
        new_updates = [u for u in updates if u['document_number'] not in last_documents]

        if new_updates:
            print(f"Found {len(new_updates)} new HR-related Federal Register entries", file=sys.stderr)

            # Write updates to stdout for capture
            for update in new_updates:
                print(f"\n## {update['title']}")
                print(f"**Type:** {update['type']}")
                print(f"**Published:** {update['publication_date']}")
                print(f"**Document Number:** {update['document_number']}")
                print(f"**Agency:** {update['agency']}")
                print(f"**URL:** {update['url']}")
                print(f"\n**Summary:**")
                print(update['abstract'])
                print("\n---")
        else:
            print("No new Federal Register updates found", file=sys.stderr)

        # Save cache
        all_doc_numbers = [u['document_number'] for u in updates]
        save_cache(end_date, all_doc_numbers[-100:])  # Keep last 100 documents

        # Set GitHub Actions output
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"update_count={len(new_updates)}\n")
                f.write(f"has_updates={'true' if new_updates else 'false'}\n")

        return 0

    except Exception as e:
        print(f"Error in monitor_federal_register: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
