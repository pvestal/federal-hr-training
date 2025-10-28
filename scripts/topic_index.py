#!/usr/bin/env python3
"""
Generate Topic Index
Creates a searchable index of all topics covered in training materials
"""

import os
import sys
import json
from pathlib import Path
from collections import defaultdict


class TopicIndexer:
    """Build searchable topic index"""

    def __init__(self, base_path="."):
        self.base_path = Path(base_path)
        self.topics = defaultdict(list)

    def build_index(self):
        """Build comprehensive topic index"""

        # Define key topics to track
        self.key_topics = {
            # Benefits
            "FEHB": "Federal Employees Health Benefits",
            "FERS": "Federal Employees Retirement System",
            "TSP": "Thrift Savings Plan",
            "FLTCIP": "Federal Long Term Care Insurance",
            "FSAFEDS": "Federal Flexible Spending Accounts",

            # Classification & Pay
            "Classification": "Position Classification",
            "GS": "General Schedule",
            "FWS": "Federal Wage System",
            "Pay": "Compensation and Pay",

            # Leave
            "Annual Leave": "Annual Leave Administration",
            "Sick Leave": "Sick Leave Administration",
            "FMLA": "Family and Medical Leave Act",
            "LWOP": "Leave Without Pay",

            # Workforce Shaping
            "RIF": "Reduction in Force",
            "VERA": "Voluntary Early Retirement Authority",
            "VSIP": "Voluntary Separation Incentive Payments",

            # Recruitment & Staffing
            "Hiring": "Recruitment and Hiring",
            "USA Staffing": "USA Staffing System",
            "Merit Hiring": "Merit Hiring Plan",
            "Direct Hire": "Direct Hire Authority",

            # Performance
            "DPMAP": "DoD Performance Management and Appraisal Program",
            "Performance": "Performance Management",
            "Appraisal": "Performance Appraisal",

            # Regulations & Ethics
            "5 CFR": "Code of Federal Regulations Title 5",
            "Merit Systems": "Merit Systems Principles",
            "Hatch Act": "Hatch Act Political Activity",
            "Privacy Act": "Privacy Act and PII",

            # Travel
            "FTR": "Federal Travel Regulation",
            "JFTR": "Joint Federal Travel Regulations",
            "Per Diem": "Travel Per Diem",
            "PCS": "Permanent Change of Station",

            # HR Systems
            "DCPDS": "Defense Civilian Personnel Data System",
            "eOPF": "Electronic Official Personnel Folder",
            "Services Online": "OPM Services Online",
        }

        # Search for each topic
        for topic, description in self.key_topics.items():
            self._find_topic_references(topic, description)

        return self.topics

    def _find_topic_references(self, topic, description):
        """Find all references to a topic"""

        search_dirs = [
            "01-basic-hr",
            "02-intermediate-hr",
            "03-advanced-hr",
            "04-expert-hr",
            "decision-trees",
            "reference-materials"
        ]

        for directory in search_dirs:
            dir_path = self.base_path / directory
            if dir_path.exists():
                for md_file in dir_path.rglob("*.md"):
                    if self._file_contains_topic(md_file, topic):
                        rel_path = str(md_file).replace(str(self.base_path) + os.sep, "")
                        self.topics[topic].append({
                            'file': rel_path,
                            'description': description
                        })

    def _file_contains_topic(self, file_path, topic):
        """Check if file contains topic"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                return topic.lower() in content
        except:
            return False

    def print_index(self):
        """Print formatted topic index"""
        print("\n" + "=" * 70)
        print("📚 FEDERAL HR TRAINING TOPIC INDEX")
        print("=" * 70)

        # Group by category
        categories = {
            "Benefits": ["FEHB", "FERS", "TSP", "FLTCIP", "FSAFEDS"],
            "Classification & Pay": ["Classification", "GS", "FWS", "Pay"],
            "Leave": ["Annual Leave", "Sick Leave", "FMLA", "LWOP"],
            "Workforce Shaping": ["RIF", "VERA", "VSIP"],
            "Recruitment": ["Hiring", "USA Staffing", "Merit Hiring", "Direct Hire"],
            "Performance": ["DPMAP", "Performance", "Appraisal"],
            "Ethics & Regulations": ["5 CFR", "Merit Systems", "Hatch Act", "Privacy Act"],
            "Travel": ["FTR", "JFTR", "Per Diem", "PCS"],
            "HR Systems": ["DCPDS", "eOPF", "Services Online"],
        }

        for category, topics in categories.items():
            print(f"\n## {category}")

            for topic in topics:
                if topic in self.topics and self.topics[topic]:
                    print(f"\n### {topic} ({self.key_topics[topic]})")
                    print(f"   Found in {len(self.topics[topic])} locations:")

                    for ref in self.topics[topic][:3]:  # Show first 3
                        print(f"   - {ref['file']}")

                    if len(self.topics[topic]) > 3:
                        print(f"   ... and {len(self.topics[topic]) - 3} more")

        print("\n" + "=" * 70)

    def save_index(self, output_file="topic_index.json"):
        """Save index to JSON file"""
        output_path = self.base_path / "reports" / output_file

        # Create reports directory if it doesn't exist
        output_path.parent.mkdir(exist_ok=True)

        # Convert to serializable format
        index_data = {
            topic: {
                'description': self.key_topics.get(topic, ""),
                'locations': [ref['file'] for ref in refs]
            }
            for topic, refs in self.topics.items()
        }

        with open(output_path, 'w') as f:
            json.dump(index_data, f, indent=2)

        print(f"\n💾 Index saved to: {output_path}")


def main():
    """Main function"""
    print("Building topic index...")

    indexer = TopicIndexer()
    indexer.build_index()
    indexer.print_index()
    indexer.save_index()

    print("\n✅ Topic index complete!")
    print("\nUsage:")
    print("  - View index: python scripts/topic_index.py")
    print("  - Search: python scripts/search_training.py <topic>")


if __name__ == "__main__":
    main()
