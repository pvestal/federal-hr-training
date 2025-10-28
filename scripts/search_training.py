#!/usr/bin/env python3
"""
Federal HR Training Search Tool
Simple keyword search across all training materials
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict


class TrainingSearch:
    """Search engine for training materials"""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.results = defaultdict(list)

    def search(self, query, case_sensitive=False):
        """Search for query across all markdown files"""
        search_pattern = query if case_sensitive else query.lower()

        # Search in these directories
        search_dirs = [
            "01-basic-hr",
            "02-intermediate-hr",
            "03-advanced-hr",
            "04-expert-hr",
            "decision-trees",
            "case-studies",
            "reference-materials",
            "opm-updates"
        ]

        for directory in search_dirs:
            dir_path = self.base_path / directory
            if dir_path.exists():
                self._search_directory(dir_path, search_pattern, case_sensitive)

        return self.results

    def _search_directory(self, directory, search_pattern, case_sensitive):
        """Recursively search a directory"""
        for md_file in directory.rglob("*.md"):
            self._search_file(md_file, search_pattern, case_sensitive)

    def _search_file(self, file_path, search_pattern, case_sensitive):
        """Search within a single file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            for line_num, line in enumerate(lines, 1):
                search_line = line if case_sensitive else line.lower()

                if search_pattern in search_line:
                    # Get context (line before and after)
                    context_start = max(0, line_num - 2)
                    context_end = min(len(lines), line_num + 1)
                    context = lines[context_start:context_end]

                    self.results[str(file_path)].append({
                        'line_number': line_num,
                        'line': line.strip(),
                        'context': [l.strip() for l in context]
                    })

        except Exception as e:
            print(f"Error reading {file_path}: {e}", file=sys.stderr)

    def print_results(self, query):
        """Pretty print search results"""
        if not self.results:
            print(f"\n❌ No results found for: '{query}'")
            print("\nTips:")
            print("- Try different keywords")
            print("- Check spelling")
            print("- Use broader terms (e.g., 'FEHB' instead of 'health insurance')")
            return

        print("\n" + "=" * 70)
        print(f"🔍 SEARCH RESULTS FOR: '{query}'")
        print("=" * 70)

        total_matches = sum(len(matches) for matches in self.results.values())
        print(f"\nFound {total_matches} matches in {len(self.results)} files\n")

        for file_path, matches in sorted(self.results.items()):
            # Get relative path and make it readable
            rel_path = file_path.replace(str(self.base_path) + os.sep, "")

            print(f"\n📄 {rel_path}")
            print(f"   ({len(matches)} matches)")

            for i, match in enumerate(matches[:5], 1):  # Show first 5 matches per file
                print(f"\n   Match {i} (line {match['line_number']}):")
                print(f"   → {match['line'][:100]}...")

            if len(matches) > 5:
                print(f"\n   ... and {len(matches) - 5} more matches in this file")

        print("\n" + "=" * 70)
        print("💡 Tip: Open the file to see full context")
        print("=" * 70)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("=" * 70)
        print("Federal HR Training Search Tool")
        print("=" * 70)
        print("\nUsage: python search_training.py <search_term> [-c]")
        print("\nOptions:")
        print("  -c    Case-sensitive search")
        print("\nExamples:")
        print("  python search_training.py FEHB")
        print("  python search_training.py 'qualifying life event'")
        print("  python search_training.py RIF -c")
        print("\nCommon Search Terms:")
        print("  - FEHB, FERS, TSP (benefits)")
        print("  - RIF, VERA, VSIP (workforce shaping)")
        print("  - Classification, GS, FWS (position management)")
        print("  - Leave, FMLA, annual (leave administration)")
        print("  - Merit systems, Hatch Act (ethics)")
        print("=" * 70)
        sys.exit(1)

    # Parse arguments
    query = sys.argv[1]
    case_sensitive = '-c' in sys.argv

    # Run search
    searcher = TrainingSearch()
    searcher.search(query, case_sensitive)
    searcher.print_results(query)


if __name__ == "__main__":
    main()
