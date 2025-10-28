#!/usr/bin/env python3
"""
Smart URL Validator for Federal Training Materials
Handles government website quirks and validation challenges
"""

import re
import sys
import json
import time
from pathlib import Path
from urllib.parse import urlparse
import requests
from datetime import datetime

class SmartURLValidator:
    """Intelligent URL validation for government sites"""

    def __init__(self):
        self.results = {
            'checked': 0,
            'valid': 0,
            'invalid': 0,
            'warnings': 0,
            'errors': []
        }

        # Government sites that commonly have validation issues
        self.known_good_domains = {
            'opm.gov': 'Office of Personnel Management',
            'ecfr.gov': 'Electronic Code of Federal Regulations',
            'federalregister.gov': 'Federal Register',
            'govinfo.gov': 'Government Publishing Office',
            'gsa.gov': 'General Services Administration',
            'dfas.mil': 'Defense Finance and Accounting Service',
            'travel.dod.mil': 'Defense Travel Management Office',
            'dcsa.mil': 'Defense Counterintelligence and Security Agency',
            'mspb.gov': 'Merit Systems Protection Board',
            'flra.gov': 'Federal Labor Relations Authority',
            'osc.gov': 'Office of Special Counsel',
            'eeoc.gov': 'Equal Employment Opportunity Commission',
            'tsp.gov': 'Thrift Savings Plan',
            'law.cornell.edu': 'Cornell Law School (Legal Information Institute)',
            'justice.gov': 'Department of Justice',
            'plainlanguage.gov': 'Plain Language',
            'section508.gov': 'Section 508',
        }

        # URLs to skip (internal references, etc.)
        self.skip_patterns = [
            r'^#',  # Anchor links
            r'^mailto:',  # Email links
            r'^http://localhost',  # Local development
            r'^http://127\.0\.0\.1',  # Local development
        ]

        # User agent that works better with government sites
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }

    def should_skip_url(self, url):
        """Check if URL should be skipped"""
        for pattern in self.skip_patterns:
            if re.match(pattern, url):
                return True
        return False

    def is_known_good_domain(self, url):
        """Check if URL is from a trusted government domain"""
        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            domain = domain.replace('www.', '')

            for known_domain in self.known_good_domains.keys():
                if domain.endswith(known_domain):
                    return True, self.known_good_domains[known_domain]
        except:
            pass
        return False, None

    def validate_url(self, url, timeout=10, retries=3):
        """Validate a single URL with retries and smart handling"""

        if self.should_skip_url(url):
            return {'status': 'skipped', 'reason': 'Internal/local reference'}

        # Check if it's a known good domain
        is_known, org_name = self.is_known_good_domain(url)

        for attempt in range(retries):
            try:
                # Add delay between retries
                if attempt > 0:
                    time.sleep(2 * attempt)  # Exponential backoff

                response = requests.head(
                    url,
                    headers=self.headers,
                    timeout=timeout,
                    allow_redirects=True
                )

                # If HEAD fails, try GET
                if response.status_code >= 400:
                    response = requests.get(
                        url,
                        headers=self.headers,
                        timeout=timeout,
                        allow_redirects=True
                    )

                if response.status_code < 400:
                    return {
                        'status': 'valid',
                        'code': response.status_code,
                        'final_url': response.url if response.url != url else None
                    }
                elif response.status_code in [301, 302, 307, 308]:
                    return {
                        'status': 'redirect',
                        'code': response.status_code,
                        'final_url': response.url
                    }
                elif is_known and response.status_code in [403, 429]:
                    # Government sites sometimes block automated requests
                    return {
                        'status': 'warning',
                        'code': response.status_code,
                        'reason': f'Blocked but known good domain ({org_name})',
                        'suggestion': 'Manual verification recommended'
                    }

            except requests.exceptions.Timeout:
                if attempt == retries - 1:
                    if is_known:
                        return {
                            'status': 'warning',
                            'reason': f'Timeout but known good domain ({org_name})',
                            'suggestion': 'Manual verification recommended'
                        }
                    return {'status': 'error', 'reason': 'Timeout after retries'}

            except requests.exceptions.ConnectionError:
                if attempt == retries - 1:
                    if is_known:
                        return {
                            'status': 'warning',
                            'reason': f'Connection error but known good domain ({org_name})',
                            'suggestion': 'Check if site is temporarily down'
                        }
                    return {'status': 'error', 'reason': 'Connection failed'}

            except Exception as e:
                if attempt == retries - 1:
                    return {'status': 'error', 'reason': str(e)}

        return {'status': 'error', 'reason': 'Failed after all retries'}

    def extract_urls_from_file(self, file_path):
        """Extract all URLs from a markdown file"""
        urls = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Match markdown links [text](url)
            markdown_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
            for text, url in markdown_links:
                if url and not url.startswith('#'):
                    urls.append((text, url))

            # Match bare URLs
            bare_urls = re.findall(r'https?://[^\s<>"]+', content)
            for url in bare_urls:
                if url not in [u[1] for u in urls]:  # Avoid duplicates
                    urls.append(('(bare URL)', url))

        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

        return urls

    def validate_file(self, file_path):
        """Validate all URLs in a file"""
        print(f"\n📄 Checking: {file_path}")

        urls = self.extract_urls_from_file(file_path)
        if not urls:
            print("   No URLs found")
            return

        print(f"   Found {len(urls)} URLs")

        file_results = []

        for link_text, url in urls:
            self.results['checked'] += 1
            result = self.validate_url(url)

            if result['status'] == 'valid':
                self.results['valid'] += 1
                print(f"   ✓ {url[:60]}...")

            elif result['status'] == 'redirect':
                self.results['valid'] += 1
                print(f"   ↗ {url[:60]}...")
                print(f"      Redirects to: {result['final_url'][:60]}...")

            elif result['status'] == 'warning':
                self.results['warnings'] += 1
                print(f"   ⚠ {url[:60]}...")
                print(f"      {result['reason']}")
                file_results.append({
                    'url': url,
                    'link_text': link_text,
                    'status': 'warning',
                    'details': result
                })

            elif result['status'] == 'skipped':
                print(f"   ⊘ {url[:60]}... (skipped)")

            else:  # error
                self.results['invalid'] += 1
                print(f"   ✗ {url[:60]}...")
                print(f"      {result.get('reason', 'Unknown error')}")
                file_results.append({
                    'url': url,
                    'link_text': link_text,
                    'status': 'error',
                    'details': result
                })

            # Small delay between requests
            time.sleep(0.5)

        if file_results:
            self.results['errors'].append({
                'file': str(file_path),
                'issues': file_results
            })

    def validate_directory(self, base_path="."):
        """Validate all markdown files"""
        base = Path(base_path)

        search_dirs = [
            "01-basic-hr",
            "02-intermediate-hr",
            "03-advanced-hr",
            "04-expert-hr",
            "case-studies",
            "decision-trees",
            "reference-materials",
            "opm-updates"
        ]

        print("=" * 70)
        print("🔍 SMART URL VALIDATOR FOR FEDERAL TRAINING")
        print("=" * 70)

        for directory in search_dirs:
            dir_path = base / directory
            if dir_path.exists():
                for md_file in sorted(dir_path.rglob("*.md")):
                    self.validate_file(md_file)

        # Also check root markdown files
        for md_file in sorted(base.glob("*.md")):
            self.validate_file(md_file)

    def print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 70)
        print("📊 VALIDATION SUMMARY")
        print("=" * 70)

        print(f"\nURLs Checked: {self.results['checked']}")
        print(f"✓ Valid: {self.results['valid']}")
        print(f"⚠ Warnings: {self.results['warnings']}")
        print(f"✗ Errors: {self.results['invalid']}")

        if self.results['warnings'] > 0:
            print("\n⚠ WARNINGS (Manual verification recommended):")
            for file_data in self.results['errors']:
                for issue in file_data['issues']:
                    if issue['status'] == 'warning':
                        print(f"  {issue['url']}")
                        print(f"    Reason: {issue['details']['reason']}")

        if self.results['invalid'] > 0:
            print("\n✗ ERRORS (Need attention):")
            for file_data in self.results['errors']:
                file_name = file_data['file']
                error_count = sum(1 for i in file_data['issues'] if i['status'] == 'error')
                if error_count > 0:
                    print(f"\n  File: {file_name}")
                    for issue in file_data['issues']:
                        if issue['status'] == 'error':
                            print(f"    ✗ {issue['url']}")
                            print(f"      {issue['details'].get('reason', 'Unknown')}")

        print("\n" + "=" * 70)

        # Save results to JSON
        report_path = Path("reports/url_validation_report.json")
        report_path.parent.mkdir(exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'summary': {
                    'checked': self.results['checked'],
                    'valid': self.results['valid'],
                    'warnings': self.results['warnings'],
                    'errors': self.results['invalid']
                },
                'details': self.results['errors']
            }, f, indent=2)

        print(f"💾 Report saved: {report_path}")

        # Exit code
        if self.results['invalid'] > 0:
            print("\n❌ Validation failed (errors found)")
            sys.exit(1)
        elif self.results['warnings'] > 0:
            print("\n⚠ Validation passed with warnings")
            sys.exit(0)
        else:
            print("\n✅ All URLs validated successfully")
            sys.exit(0)


def main():
    """Main function"""
    print("Starting URL validation...")
    print("This may take several minutes for government sites...\n")

    validator = SmartURLValidator()
    validator.validate_directory()
    validator.print_summary()


if __name__ == "__main__":
    main()
