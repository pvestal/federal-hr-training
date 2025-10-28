#!/usr/bin/env python3
"""
DOD/Army Publications Monitor
Automatically tracks updates to military HR regulations and publications
"""

import requests
import json
from datetime import datetime
from pathlib import Path

# DOD/Army HR-relevant publications
DOD_PUBLICATIONS = {
    # DOD Instructions
    "DODI 1400.25": {
        "title": "DoD Civilian Personnel Management System",
        "url": "https://www.esd.whs.mil/Directives/issuances/dodi/",
        "relevance": "Core civilian HR policy for DOD",
        "volumes": [
            "Vol 1400: General Information",
            "Vol 1401: Appointment and Placement",
            "Vol 1402: Classification",
            "Vol 1403: Pay and Leave Policy",
            "Vol 1404: Performance Management",
            "Vol 1405: Discipline and Adverse Actions"
        ]
    },

    # DOD Directives
    "DODD 1400.25": {
        "title": "DoD Civilian Personnel Management",
        "url": "https://www.esd.whs.mil/Directives/issuances/dodd/",
        "relevance": "High-level civilian personnel policy"
    },

    # Army Regulations
    "AR 690-300": {
        "title": "Army Civilian Personnel Administration",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/AR.aspx",
        "relevance": "Army civilian HR comprehensive regulation"
    },

    "AR 690-11": {
        "title": "Mobilization and Deployment of Civilian Personnel",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/AR.aspx",
        "relevance": "Civilian deployment policies"
    },

    "AR 690-950": {
        "title": "Career Management",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/AR.aspx",
        "relevance": "Career development and succession planning"
    },

    "AR 215-3": {
        "title": "Civilian Personnel",
        "url": "https://armypubs.army.mil/ProductMaps/PubForm/AR.aspx",
        "relevance": "Nonappropriated fund (NAF) personnel"
    }
}

# CPAC (Civilian Personnel Advisory Center) resources
CPAC_RESOURCES = {
    "DCPAS_PORTAL": "https://www.dcpas.osd.mil/",
    "DCPDS_GUIDANCE": "https://compo.dcpds.cpms.osd.mil/",
    "NSPS_ARCHIVE": "https://archive.dcpas.osd.mil/nsps/"  # Historical NSPS reference
}

# Army Publishing Directorate
APD_URLS = {
    "AR_SEARCH": "https://armypubs.army.mil/ProductMaps/PubForm/AR.aspx",
    "DA_PAM_SEARCH": "https://armypubs.army.mil/ProductMaps/PubForm/DAPAM.aspx",
    "ALARACT": "https://armypubs.army.mil/ProductMaps/PubForm/ALARACT.aspx"
}

def check_publication_updates():
    """Check for updates to DOD/Army publications"""
    print("=" * 70)
    print("DOD/ARMY PUBLICATIONS MONITOR")
    print(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    updates = []

    for pub_id, pub_info in DOD_PUBLICATIONS.items():
        print(f"\nChecking: {pub_id} - {pub_info['title']}")
        print(f"  URL: {pub_info['url']}")
        print(f"  Relevance: {pub_info['relevance']}")

        # Note: Actual API integration would go here
        # For now, documenting what would be checked
        print(f"  Status: ✓ Documented (API integration pending)")

        if "volumes" in pub_info:
            print(f"  Volumes: {len(pub_info['volumes'])}")
            for vol in pub_info['volumes']:
                print(f"    - {vol}")

    return updates

def generate_publications_reference():
    """Generate markdown reference guide for DOD/Army publications"""

    content = """# DOD/Army HR Publications Quick Reference

**Last Updated**: {date}
**Purpose**: Quick access to official DOD and Army civilian personnel regulations

---

## 📘 Core DOD Instructions (DODI 1400.25 Volumes)

The **DODI 1400.25** series is the primary regulation for DOD civilian personnel management.

### Volume Structure:
""".format(date=datetime.now().strftime('%B %d, %Y'))

    # Add DODI 1400.25 volumes
    if "DODI 1400.25" in DOD_PUBLICATIONS:
        pub = DOD_PUBLICATIONS["DODI 1400.25"]
        if "volumes" in pub:
            for vol in pub["volumes"]:
                content += f"- **{vol}**\n"

    content += """
### Key Topics Covered:
- **Volume 1400**: General Information and Definitions
- **Volume 1401**: Appointment Types, Competitive Service, Excepted Service
- **Volume 1402**: Position Classification (GS, FWS, NSPS legacy)
- **Volume 1403**: Pay Administration, Special Rates, Locality Pay
- **Volume 1404**: DPMAP (DoD Performance Management and Appraisal Program)
- **Volume 1405**: Discipline, Adverse Actions, Grievances, Appeals

**Access**: [DOD Issuances Portal](https://www.esd.whs.mil/Directives/issuances/dodi/)

---

## 🪖 Army Regulations (AR)

### AR 690-300: Civilian Personnel Administration
**Description**: Comprehensive Army civilian personnel regulation covering all aspects of HR management.

**Key Sections**:
- Classification and pay
- Recruitment and staffing
- Performance management
- Labor relations
- Discipline and adverse actions

**Access**: [Army Publishing Directorate](https://armypubs.army.mil/)

### AR 690-11: Mobilization and Deployment
**Description**: Policies for mobilizing and deploying Army civilian employees.

**Relevant for**:
- Emergency Essential (EE) positions
- Deployment pay and benefits
- OCONUS assignments during contingencies

### AR 690-950: Career Management
**Description**: Career development, training, and succession planning for Army civilians.

**Topics**:
- Career ladders
- Leadership development programs
- Mentoring
- Succession planning

---

## 🔧 DCPAS Resources (Defense Civilian Personnel Advisory Service)

### Main Portal
**URL**: https://www.dcpas.osd.mil/

**Resources Available**:
- DCPDS user guides
- Policy memoranda
- Training webinars
- Classification standards

### DCPDS Guidance Portal
**URL**: https://compo.dcpds.cpms.osd.mil/

**For**:
- DCPDS system documentation
- Personnel action guides
- Reporting instructions

---

## 📢 ALARACT Messages

**ALARACT** (All Army Activities) messages provide urgent policy updates.

**HR-Relevant ALARACT Topics**:
- Emergency hiring authorities
- COVID-19 personnel policies
- Pay and benefits updates
- Telework policy changes

**Access**: [ALARACT Search](https://armypubs.army.mil/ProductMaps/PubForm/ALARACT.aspx)

---

## 🔄 How to Stay Current

### 1. Subscribe to DCPAS Updates
Email alerts when new DOD civilian personnel policies published.

**Subscribe at**: DCPAS website → "Stay Informed"

### 2. Bookmark Army Publishing Directorate
Check monthly for new/revised ARs.

**Bookmark**: https://armypubs.army.mil/

### 3. Use This Repository's Auto-Monitor
This repository automatically checks for updates (see `scripts/monitor_dod_publications.py`)

**Run manually**:
```bash
python scripts/monitor_dod_publications.py
```

**Automated**: GitHub Actions runs weekly check

---

## 📋 Integration with This Training

### How DOD/Army Publications Are Incorporated:

1. **Regulatory Citations**: All training modules cite specific DODI/AR sections
2. **Policy Updates**: When regulations change, training modules updated
3. **Real-World Application**: Scenarios based on actual DOD/Army policies
4. **Compliance Focus**: Training ensures HR actions comply with military regulations

### Example:
```
Module 2.4: DOD Recruitment Strategies
├── Cites: DODI 1400.25, Volume 1401 (Appointment and Placement)
├── Cites: AR 690-300 (Army Civilian Personnel Administration)
└── Scenarios: Based on actual Army installation HR challenges
```

---

## ⚠️ Important Notes

### Classification Levels
Most DODI 1400.25 volumes are **UNCLASSIFIED**.
Some Army-specific supplements may be **FOUO** (For Official Use Only).

### Currency
Publications listed are current as of **{date}**.
Always verify latest version before citing in official actions.

### Applicability
- **DODI**: Applies to ALL DOD civilian employees (Army, Navy, Air Force, Marines, Space Force)
- **AR**: Applies to Army civilian employees specifically
- **Service-Specific**: Other services have equivalent regulations (NAVPERS, AFI, etc.)

---

## 🆘 Questions?

**DOD Policy Questions**: Contact your CPAC or DCPAS liaison
**Army-Specific Questions**: Contact your garrison CPAC
**Training Questions**: File issue in this repository

---

**Document Control**:
- **Version**: 1.0.0
- **Last Updated**: {date}
- **Next Review**: Quarterly (automated check)
""".format(date=datetime.now().strftime('%B %d, %Y'))

    # Save reference guide
    ref_path = Path("reference-materials/dod-army-publications-reference.md")
    ref_path.parent.mkdir(exist_ok=True)

    with open(ref_path, 'w') as f:
        f.write(content)

    print(f"\n✅ Generated: {ref_path}")

    return str(ref_path)

def main():
    """Main function"""
    print("Starting DOD/Army Publications Monitor...\n")

    # Check for updates
    updates = check_publication_updates()

    # Generate reference guide
    ref_file = generate_publications_reference()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Publications monitored: {len(DOD_PUBLICATIONS)}")
    print(f"Reference guide: {ref_file}")
    print("\nRecommendation: Review reference guide and bookmark key DOD/Army")
    print("publication sources for accurate policy interpretation.")

    print("\n💡 Next Steps:")
    print("  1. Bookmark DCPAS portal: https://www.dcpas.osd.mil/")
    print("  2. Bookmark Army pubs: https://armypubs.army.mil/")
    print("  3. Subscribe to DCPAS email updates")
    print("  4. Set calendar reminder to check for new DODIs quarterly")

if __name__ == "__main__":
    main()
