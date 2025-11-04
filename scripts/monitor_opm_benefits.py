#!/usr/bin/env python3
"""
Monitor OPM Benefits Officers Center for updates

This script checks the OPM Benefits Administration pages for new bulletins,
fact sheets, and guidance documents relevant to federal benefits administration.
"""

import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# OPM Benefits pages to monitor
BENEFITS_URLS = [
    "https://www.opm.gov/healthcare-insurance/",
    "https://www.opm.gov/retirement-center/",
    "https://www.opm.gov/healthcare-insurance/healthcare/benefits-officers/",
]

CACHE_FILE = Path(__file__).parent / ".cache" / "opm_benefits_checksums.json"


def load_cache():
    """Load the last checksums from cache"""
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not load cache: {e}", file=sys.stderr)
    return {}


def save_cache(checksums):
    """Save checksums to cache"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(checksums, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save cache: {e}", file=sys.stderr)


def get_page_content(url):
    """Fetch and parse a web page"""
    try:
        headers = {
            'User-Agent': 'Federal-HR-Training-Monitor/1.0 (Educational Purpose)'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def extract_updates(html, url):
    """Extract key information from OPM Benefits pages"""
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    updates = []

    # Look for common update indicators
    update_sections = soup.find_all(['article', 'div'], class_=lambda x: x and any(
        term in str(x).lower() for term in ['news', 'update', 'bulletin', 'announcement']
    ))

    for section in update_sections[:5]:  # Limit to 5 most recent
        title_elem = section.find(['h1', 'h2', 'h3', 'h4'])
        if title_elem:
            title = title_elem.get_text(strip=True)

            # Find date if available
            date_elem = section.find(['time', 'span'], class_=lambda x: x and 'date' in str(x).lower())
            date_text = date_elem.get_text(strip=True) if date_elem else "Date not specified"

            # Get summary
            summary_elem = section.find('p')
            summary = summary_elem.get_text(strip=True)[:300] if summary_elem else ""

            # Get link
            link_elem = section.find('a', href=True)
            link = link_elem['href'] if link_elem else url
            if link and not link.startswith('http'):
                link = f"https://www.opm.gov{link}"

            updates.append({
                'title': title,
                'date': date_text,
                'summary': summary,
                'url': link,
                'source': url
            })

    return updates


def calculate_checksum(content):
    """Calculate SHA256 checksum of content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def main():
    """Main function to monitor OPM Benefits pages"""
    try:
        old_checksums = load_cache()
        new_checksums = {}
        all_updates = []
        changed_pages = []

        for url in BENEFITS_URLS:
            print(f"Checking {url}", file=sys.stderr)

            html = get_page_content(url)
            if not html:
                continue

            # Calculate checksum
            checksum = calculate_checksum(html)
            new_checksums[url] = checksum

            # Check if page changed
            if url not in old_checksums or old_checksums[url] != checksum:
                changed_pages.append(url)
                updates = extract_updates(html, url)
                all_updates.extend(updates)

        if changed_pages:
            print(f"Found changes on {len(changed_pages)} OPM Benefits pages", file=sys.stderr)

            # Output updates
            for update in all_updates:
                print(f"\n## {update['title']}")
                print(f"**Date:** {update['date']}")
                print(f"**Source:** {update['source']}")
                print(f"**URL:** {update['url']}")
                print(f"\n**Summary:**")
                print(update['summary'])
                print("\n---")

            # List changed pages
            print("\n## Changed Pages:")
            for page in changed_pages:
                print(f"- {page}")
        else:
            print("No changes detected on OPM Benefits pages", file=sys.stderr)

        # Save cache
        save_cache(new_checksums)

        # Set GitHub Actions output
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"update_count={len(all_updates)}\n")
                f.write(f"has_updates={'true' if changed_pages else 'false'}\n")

        return 0

    except Exception as e:
        print(f"Error in monitor_opm_benefits: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
