#!/usr/bin/env python3
"""
Monitor OPM Policy Data and Oversight pages for updates

This script checks the OPM Policy Library and oversight pages for new
policy documents, guidance, and regulatory updates.
"""

import sys
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import requests
from bs4 import BeautifulSoup

# OPM Policy pages to monitor
POLICY_URLS = [
    "https://www.opm.gov/policy-data-oversight/",
    "https://www.opm.gov/policy-data-oversight/pay-leave/",
    "https://www.opm.gov/policy-data-oversight/classification-qualifications/",
    "https://www.opm.gov/policy-data-oversight/human-capital-management/",
]

CACHE_FILE = Path(__file__).parent / ".cache" / "opm_policy_checksums.json"


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


def extract_policy_updates(html, url):
    """Extract policy documents and updates from OPM pages"""
    if not html:
        return []

    soup = BeautifulSoup(html, 'html.parser')
    updates = []

    # Look for policy documents and updates
    # OPM uses various structures for policy content
    content_sections = soup.find_all(['article', 'div', 'section'], class_=lambda x: x and any(
        term in str(x).lower() for term in ['content', 'policy', 'document', 'guidance', 'memo']
    ))

    for section in content_sections[:10]:  # Limit to 10 most recent
        # Find title
        title_elem = section.find(['h1', 'h2', 'h3', 'h4', 'a'])
        if not title_elem:
            continue

        title = title_elem.get_text(strip=True)

        # Skip navigation and common headings
        if any(skip in title.lower() for skip in ['navigation', 'menu', 'search', 'share']):
            continue

        # Find links to documents (PDF, DOC, etc.)
        links = section.find_all('a', href=True)
        doc_links = [a for a in links if any(ext in a['href'].lower() for ext in ['.pdf', '.doc', '.docx'])]

        # Get description
        desc_elem = section.find('p')
        description = desc_elem.get_text(strip=True)[:300] if desc_elem else ""

        # Get primary link
        link = None
        if doc_links:
            link = doc_links[0]['href']
        elif title_elem.name == 'a':
            link = title_elem['href']
        elif links:
            link = links[0]['href']

        if link and not link.startswith('http'):
            link = f"https://www.opm.gov{link}"

        if title and len(title) > 10:  # Filter out very short titles
            updates.append({
                'title': title,
                'description': description,
                'url': link if link else url,
                'source': url,
                'document_links': [
                    f"https://www.opm.gov{a['href']}" if not a['href'].startswith('http') else a['href']
                    for a in doc_links[:3]  # Include up to 3 document links
                ]
            })

    # Remove duplicates based on title
    seen_titles = set()
    unique_updates = []
    for update in updates:
        if update['title'] not in seen_titles:
            seen_titles.add(update['title'])
            unique_updates.append(update)

    return unique_updates[:5]  # Return top 5 unique updates


def calculate_checksum(content):
    """Calculate SHA256 checksum of content"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def main():
    """Main function to monitor OPM Policy pages"""
    try:
        old_checksums = load_cache()
        new_checksums = {}
        all_updates = []
        changed_pages = []

        for url in POLICY_URLS:
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
                updates = extract_policy_updates(html, url)
                all_updates.extend(updates)

        if changed_pages:
            print(f"Found changes on {len(changed_pages)} OPM Policy pages", file=sys.stderr)

            # Output updates
            for update in all_updates:
                print(f"\n## {update['title']}")
                print(f"**Source:** {update['source']}")
                print(f"**URL:** {update['url']}")

                if update['document_links']:
                    print(f"\n**Related Documents:**")
                    for doc_link in update['document_links']:
                        print(f"- {doc_link}")

                if update['description']:
                    print(f"\n**Description:**")
                    print(update['description'])

                print("\n---")

            # List changed pages
            print("\n## Changed Pages:")
            for page in changed_pages:
                print(f"- {page}")
        else:
            print("No changes detected on OPM Policy pages", file=sys.stderr)

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
        print(f"Error in monitor_opm_policy: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
