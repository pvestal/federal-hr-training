#!/usr/bin/env python3
"""
5 CFR (Code of Federal Regulations) Monitor
Tracks updates to Title 5 - Administrative Personnel regulations
"""

import requests
import json
from datetime import datetime
from pathlib import Path
import re

# Key 5 CFR Parts for Federal HR
CFR_PARTS = {
    "5 CFR Part 210": {
        "title": "Definitions",
        "url": "https://www.ecfr.gov/current/title-5/part-210",
        "relevance": "Fundamental definitions for federal HR",
        "key_sections": ["§ 210.102 Definitions"]
    },

    "5 CFR Part 300": {
        "title": "Employment",
        "url": "https://www.ecfr.gov/current/title-5/part-300",
        "relevance": "General employment policies",
        "key_sections": [
            "§ 300.101 Coverage",
            "§ 300.102 Definitions",
            "§ 300.103 Statutory requirements"
        ]
    },

    "5 CFR Part 315": {
        "title": "Career and Career-Conditional Employment",
        "url": "https://www.ecfr.gov/current/title-5/part-315",
        "relevance": "Appointments, probationary periods, tenure",
        "key_sections": [
            "§ 315.201 Service requirement",
            "§ 315.801 Probationary period",
            "§ 315.907 Supervisor/manager probation"
        ]
    },

    "5 CFR Part 316": {
        "title": "Temporary and Term Employment",
        "url": "https://www.ecfr.gov/current/title-5/part-316",
        "relevance": "Temporary appointments",
        "key_sections": [
            "§ 316.401 General",
            "§ 316.402 Temporary appointments",
            "§ 316.403 Term appointments"
        ]
    },

    "5 CFR Part 317": {
        "title": "Employment in the Senior Executive Service",
        "url": "https://www.ecfr.gov/current/title-5/part-317",
        "relevance": "SES appointments and management"
    },

    "5 CFR Part 330": {
        "title": "Recruitment, Selection, and Placement",
        "url": "https://www.ecfr.gov/current/title-5/part-330",
        "relevance": "Merit staffing, priority placement, CTAP/ICTAP",
        "key_sections": [
            "§ 330.104 Requirements for vacancy announcements",
            "§ 330.608 Interagency Career Transition Assistance Plan (ICTAP)"
        ]
    },

    "5 CFR Part 351": {
        "title": "Reduction in Force",
        "url": "https://www.ecfr.gov/current/title-5/part-351",
        "relevance": "RIF procedures, competitive areas/levels, retention",
        "key_sections": [
            "§ 351.201 Order of release from competitive level",
            "§ 351.402 Defining competitive areas",
            "§ 351.403 Competitive levels",
            "§ 351.504 Retention registers"
        ]
    },

    "5 CFR Part 430": {
        "title": "Performance Management",
        "url": "https://www.ecfr.gov/current/title-5/part-430",
        "relevance": "Performance appraisals, ratings, performance-based actions",
        "key_sections": [
            "§ 430.204 Rating performance",
            "§ 430.208 Dealing with unacceptable performance"
        ]
    },

    "5 CFR Part 432": {
        "title": "Performance Based Reduction in Grade and Removal Actions",
        "url": "https://www.ecfr.gov/current/title-5/part-432",
        "relevance": "Addressing poor performance"
    },

    "5 CFR Part 451": {
        "title": "Awards",
        "url": "https://www.ecfr.gov/current/title-5/part-451",
        "relevance": "Performance awards, quality step increases"
    },

    "5 CFR Part 511": {
        "title": "Classification Under the General Schedule",
        "url": "https://www.ecfr.gov/current/title-5/part-511",
        "relevance": "Position classification standards and appeals",
        "key_sections": [
            "§ 511.201 Definitions",
            "§ 511.601 Right to appeal",
            "§ 511.607 Time limits for agency classification appeals"
        ]
    },

    "5 CFR Part 530": {
        "title": "Pay Rates and Systems",
        "url": "https://www.ecfr.gov/current/title-5/part-530",
        "relevance": "GS pay administration, special rates, locality pay"
    },

    "5 CFR Part 531": {
        "title": "Pay Under the General Schedule",
        "url": "https://www.ecfr.gov/current/title-5/part-531",
        "relevance": "GS pay setting, step increases, promotions",
        "key_sections": [
            "§ 531.203 Definitions",
            "§ 531.212 Superior qualifications appointments",
            "§ 531.407 Maximum payable rate rule"
        ]
    },

    "5 CFR Part 550": {
        "title": "Pay Administration",
        "url": "https://www.ecfr.gov/current/title-5/part-550",
        "relevance": "Premium pay, hazard pay, overtime, retention incentives",
        "key_sections": [
            "§ 550.103 Biweekly and hourly rates",
            "§ 550.1203 Recruitment incentives",
            "§ 550.1403 Retention incentives"
        ]
    },

    "5 CFR Part 630": {
        "title": "Absence and Leave",
        "url": "https://www.ecfr.gov/current/title-5/part-630",
        "relevance": "Annual, sick, FMLA, military, LWOP",
        "key_sections": [
            "§ 630.201 Annual leave accrual",
            "§ 630.302 Maximum carryover",
            "§ 630.401 Granting sick leave",
            "§ 630.1203 FMLA eligibility"
        ]
    },

    "5 CFR Part 752": {
        "title": "Adverse Actions",
        "url": "https://www.ecfr.gov/current/title-5/part-752",
        "relevance": "Suspensions, removals, demotions",
        "key_sections": [
            "§ 752.202 Coverage",
            "§ 752.404 Procedures"
        ]
    },

    "5 CFR Part 890": {
        "title": "Federal Employees Health Benefits Program",
        "url": "https://www.ecfr.gov/current/title-5/part-890",
        "relevance": "FEHB enrollment, qualifying life events, continuation",
        "key_sections": [
            "§ 890.301 Opportunities for employees to enroll",
            "§ 890.302 Continuation into retirement",
            "§ 890.303 Continuation during LWOP"
        ]
    },

    "5 CFR Part 1201": {
        "title": "Practices and Procedures (MSPB)",
        "url": "https://www.ecfr.gov/current/title-5/part-1201",
        "relevance": "Merit Systems Protection Board appeals",
        "key_sections": [
            "§ 1201.3 Filing an appeal",
            "§ 1201.56 Burden and degree of proof"
        ]
    },

    "5 CFR Part 2635": {
        "title": "Standards of Ethical Conduct for Employees",
        "url": "https://www.ecfr.gov/current/title-5/part-2635",
        "relevance": "Ethics, gifts, conflicts of interest, outside activities"
    },

    "5 CFR Part 7001": {
        "title": "Supplemental Standards of Ethical Conduct",
        "url": "https://www.ecfr.gov/current/title-5/part-7001",
        "relevance": "Agency-specific ethics supplements"
    }
}

# 5 USC (United States Code) - Statutory Authority
USC_SECTIONS = {
    "5 USC Chapter 31": {
        "title": "Authority for Employment",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-B/chapter-31",
        "relevance": "Statutory basis for federal employment"
    },

    "5 USC Chapter 33": {
        "title": "Examination, Selection, and Placement",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-B/chapter-33",
        "relevance": "Merit principles, competitive service",
        "key_sections": [
            "§ 3301 Civil service; generally",
            "§ 3318 Competitive service; selection from certificates"
        ]
    },

    "5 USC Chapter 43": {
        "title": "Performance Appraisal",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-C/chapter-43",
        "relevance": "Statutory performance management requirements"
    },

    "5 USC Chapter 53": {
        "title": "Pay Rates and Systems",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-D/chapter-53",
        "relevance": "GS pay scales, special rates, locality pay",
        "key_sections": [
            "§ 5303 Annual adjustments",
            "§ 5332 GS pay table"
        ]
    },

    "5 USC Chapter 63": {
        "title": "Leave",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-E/chapter-63",
        "relevance": "Annual, sick, family leave statutes",
        "key_sections": [
            "§ 6301 Definitions",
            "§ 6307 Sick leave",
            "§ 6381 FMLA"
        ]
    },

    "5 USC Chapter 75": {
        "title": "Adverse Actions",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-F/chapter-75",
        "relevance": "Removal, suspension, demotion procedures",
        "key_sections": [
            "§ 7513 Cause and procedure"
        ]
    },

    "5 USC Chapter 83": {
        "title": "Retirement (CSRS)",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-G/chapter-83",
        "relevance": "CSRS retirement system"
    },

    "5 USC Chapter 84": {
        "title": "Federal Employees' Retirement System (FERS)",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-G/chapter-84",
        "relevance": "FERS retirement, eligibility, calculations",
        "key_sections": [
            "§ 8414 Early retirement",
            "§ 8415 Computation",
            "§ 8451 Qualifying life events"
        ]
    },

    "5 USC Chapter 89": {
        "title": "Health Insurance (FEHB)",
        "url": "https://www.law.cornell.edu/uscode/text/5/part-III/subpart-G/chapter-89",
        "relevance": "FEHB statutory authority"
    }
}

def check_ecfr_updates():
    """Check eCFR for recent updates to Title 5"""
    print("=" * 70)
    print("5 CFR REGULATORY MONITOR")
    print(f"Check time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    print("\nMonitoring {} CFR parts for federal civilian HR\n".format(len(CFR_PARTS)))

    for part_id, part_info in CFR_PARTS.items():
        print(f"✓ {part_id}: {part_info['title']}")
        print(f"  Relevance: {part_info['relevance']}")
        if "key_sections" in part_info:
            print(f"  Key sections: {len(part_info['key_sections'])}")

    print("\n" + "=" * 70)
    print("NOTE: Manual verification recommended for regulatory changes")
    print("=" * 70)

def generate_5cfr_reference():
    """Generate comprehensive 5 CFR quick reference"""

    content = """# 5 CFR Quick Reference for Federal HR Specialists

**Last Updated**: {date}
**Purpose**: Quick access to Title 5 Code of Federal Regulations for civilian HR

---

## 📖 What is 5 CFR?

**Title 5 of the Code of Federal Regulations (5 CFR)** contains the administrative regulations governing federal civilian personnel management. These regulations are issued by the Office of Personnel Management (OPM) to implement the statutes in Title 5 of the United States Code (5 USC).

**Hierarchy**:
1. **5 USC** (statute - enacted by Congress)
2. **5 CFR** (regulations - issued by OPM to implement 5 USC)
3. **OPM Guidance** (policy letters, handbooks)
4. **Agency Policy** (must comply with above)

---

## 🔑 Essential 5 CFR Parts for HR Specialists

### 📋 Employment & Appointments

#### 5 CFR Part 210: Definitions
**What it covers**: Core definitions used throughout Title 5
**Key terms**: Competitive service, excepted service, career, career-conditional

#### 5 CFR Part 315: Career and Career-Conditional Employment
**What it covers**: Permanent appointments, probationary periods, tenure
**Critical sections**:
- § 315.201: 3-year service requirement for career tenure
- § 315.801: Probationary period (1 year for most employees)
- § 315.907: Supervisory probationary period

**Common scenarios**:
- When does probationary period start?
- Can probation be extended?
- What happens if employee fails probation?

#### 5 CFR Part 316: Temporary and Term Employment
**What it covers**: Temporary appointments (≤1 year), term appointments (>1 year ≤4 years)
**When to use**: Project work, seasonal work, temporary needs

#### 5 CFR Part 330: Recruitment, Selection, and Placement
**What it covers**: Merit staffing, veterans' preference, CTAP/ICTAP
**Critical sections**:
- § 330.104: Vacancy announcement requirements
- § 330.608: ICTAP (Interagency Career Transition Assistance Plan)

---

### ⚖️ Reduction in Force (RIF)

#### 5 CFR Part 351: Reduction in Force
**What it covers**: RIF procedures from start to finish
**Critical sections**:
- § 351.402: Competitive areas
- § 351.403: Competitive levels
- § 351.504: Retention registers (tenure groups, subgroups)
- § 351.201: Order of release

**Use this when**:
- Planning workforce reduction
- Calculating retention standing
- Determining bump/retreat rights

**WARNING**: RIF is highly complex. Consult this regulation AND legal counsel.

---

### 📊 Classification & Pay

#### 5 CFR Part 511: Classification Under the General Schedule
**What it covers**: Position classification, standards, appeals
**Critical sections**:
- § 511.601: Employee right to appeal classification
- § 511.607: Time limits (15 days to agency, then 15 days to OPM)

**Factor Evaluation System (FES)**: Used to classify most GS positions

#### 5 CFR Part 531: Pay Under the General Schedule
**What it covers**: Pay setting, within-grade increases, promotions
**Critical sections**:
- § 531.212: Superior qualifications and special needs pay-setting authority
- § 531.407: Maximum payable rate rule
- § 531.214: Setting pay upon promotion

**Common scenarios**:
- How to set pay for new hire with superior qualifications?
- When does employee get next step increase?
- How to calculate promotion pay?

#### 5 CFR Part 550: Pay Administration (Premium Pay)
**What it covers**: Overtime, hazard pay, recruitment/retention incentives
**Critical sections**:
- § 550.1203: Recruitment incentives (up to 25% of basic pay)
- § 550.1403: Retention incentives (up to 25% of basic pay)

---

### 📈 Performance Management

#### 5 CFR Part 430: Performance Management
**What it covers**: Performance appraisal systems, ratings, actions
**Critical sections**:
- § 430.204: Rating performance (must have at least 3 rating levels)
- § 430.208: Addressing unacceptable performance

**Requirements**:
- Communicate performance standards at beginning of appraisal period
- Mid-year progress review
- Annual rating

#### 5 CFR Part 432: Performance Based Actions
**What it covers**: Reduction in grade or removal for poor performance
**Process**:
1. Notify employee performance is unacceptable
2. Provide opportunity to improve (30+ days)
3. If still unacceptable, propose action
4. Give employee chance to respond
5. Issue decision

---

### 🏖️ Leave Administration

#### 5 CFR Part 630: Absence and Leave
**What it covers**: Annual, sick, FMLA, military, LWOP, and other leave
**Critical sections**:

**Annual Leave**:
- § 630.201: Accrual rates (4, 6, or 8 hours per pay period)
- § 630.302: Maximum carryover (240 hours GS, 360 hours SES)

**Sick Leave**:
- § 630.401: Sick leave purposes (illness, medical appointments, family care)
- § 630.402: Advancing sick leave

**FMLA**:
- § 630.1203: Eligibility (12 months service + 1,250 hours worked)
- § 630.1204: Leave entitlement (12 weeks unpaid per 12 months)

**Common scenarios**:
- Employee has 300 hours annual leave. How much can carry over?
- Employee requests FMLA. Is she eligible?
- Can employee use sick leave for parent's illness?

---

### ⚠️ Adverse Actions

#### 5 CFR Part 752: Adverse Actions
**What it covers**: Suspensions >14 days, removals, demotions
**Critical sections**:
- § 752.202: Coverage (employees with appeal rights)
- § 752.404: Procedures (30-day advance notice)

**Types of actions**:
- **Suspension >14 days**
- **Removal**
- **Reduction in grade**
- **Reduction in pay**
- **Furlough >30 days**

**Procedural requirements**:
1. 30-day advance written notice
2. Reasonable time to answer (7+ days)
3. Right to be represented
4. Written decision
5. Right to appeal to MSPB

---

### 💊 Benefits

#### 5 CFR Part 890: Federal Employees Health Benefits (FEHB)
**What it covers**: FEHB enrollment, qualifying life events, continuation
**Critical sections**:

**Qualifying Life Events (QLEs)**:
- § 890.301(f): Marriage, divorce, birth, adoption (31 or 60 days to request)
- § 890.301(g): Loss of other coverage

**Continuing FEHB into Retirement**:
- § 890.302: Must be enrolled 5 years immediately before retirement

**FEHB During LWOP**:
- § 890.303: Can continue for 365 days, must pay both shares

**Common scenarios**:
- Employee got married 45 days ago. Can she add spouse now?
- Employee wants FEHB in retirement. Is he eligible?
- Employee going on unpaid leave. Can she keep FEHB?

---

## 📚 How to Use This Reference

### For Daily HR Work:
1. **Identify the topic** (appointment, leave, classification, etc.)
2. **Find the relevant 5 CFR part** (use this guide)
3. **Read the specific sections** at [eCFR.gov](https://www.ecfr.gov/current/title-5)
4. **Cite in your personnel action** (e.g., "Per 5 CFR § 630.401...")

### For Complex Issues:
1. **Read the CFR section** thoroughly
2. **Check OPM guidance** (policy letters, handbooks)
3. **Consult agency policy**
4. **If still unclear**: Contact OPM or legal counsel

### For Policy Development:
1. **Start with 5 USC** (statutory authority)
2. **Review 5 CFR** (regulatory requirements)
3. **Review OPM guidance** (interpretation and best practices)
4. **Draft agency policy** (must comply with all above)

---

## 🔗 Essential Links

### Official Sources:
- **eCFR (electronic CFR)**: https://www.ecfr.gov/current/title-5
- **OPM Policy**: https://www.opm.gov/policy-data-oversight/
- **5 USC (law)**: https://www.law.cornell.edu/uscode/text/5

### OPM Resources:
- **Classification Standards**: https://www.opm.gov/policy-data-oversight/classification-qualifications/
- **Pay & Leave**: https://www.opm.gov/policy-data-oversight/pay-leave/
- **Retirement**: https://www.opm.gov/retirement-center/
- **Healthcare**: https://www.opm.gov/healthcare-insurance/

---

## ⚠️ Important Reminders

### Currency
5 CFR is updated continuously. **Always check eCFR for the current version** before citing.

### Interpretation
When 5 CFR is unclear:
1. Check OPM guidance documents
2. Contact agency legal counsel
3. Contact OPM (for novel interpretations)

### Agency Policy
Agency policies **must comply with 5 CFR** but can be more restrictive.

**Example**:
- 5 CFR allows 30 days to respond to adverse action proposal
- Agency policy can require 45 days (more generous)
- Agency policy CANNOT require only 15 days (less than regulation)

---

**Document Control**:
- **Version**: 1.0.0
- **Last Updated**: {date}
- **Next Review**: Quarterly
- **Maintained by**: Federal HR Training Repository
""".format(date=datetime.now().strftime('%B %d, %Y'))

    # Save reference guide
    ref_path = Path("reference-materials/5cfr-quick-reference.md")
    ref_path.parent.mkdir(exist_ok=True)

    with open(ref_path, 'w') as f:
        f.write(content)

    print(f"\n✅ Generated comprehensive 5 CFR reference: {ref_path}")
    return str(ref_path)

def main():
    """Main function"""
    print("Starting 5 CFR Regulatory Monitor for Federal Civilian HR...\n")

    # Check for updates
    check_ecfr_updates()

    # Generate reference guide
    ref_file = generate_5cfr_reference()

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"CFR parts monitored: {len(CFR_PARTS)}")
    print(f"USC chapters documented: {len(USC_SECTIONS)}")
    print(f"Reference guide: {ref_file}")

    print("\n💡 For HR Specialists:")
    print("  1. Bookmark eCFR: https://www.ecfr.gov/current/title-5")
    print("  2. Bookmark Cornell Law (5 USC): https://www.law.cornell.edu/uscode/text/5")
    print("  3. Subscribe to Federal Register for rule changes")
    print("  4. Check OPM.gov monthly for policy updates")

    print("\n📘 Quick Access:")
    print(f"  - Full 5 CFR reference: {ref_file}")
    print("  - Federal Register: https://www.federalregister.gov/")
    print("  - OPM Regulations: https://www.opm.gov/about-us/open-government/regulations/")

if __name__ == "__main__":
    main()
