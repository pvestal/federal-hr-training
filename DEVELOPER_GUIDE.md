# Federal HR Training Program - Developer Guide

**For**: Content Developers, Technical Contributors, Training Coordinators
**Version**: 1.0.0
**Last Updated**: October 28, 2025

---

## 📚 Table of Contents

1. [Development Environment Setup](#development-environment-setup)
2. [Repository Structure](#repository-structure)
3. [Content Development Standards](#content-development-standards)
4. [Creating Training Modules](#creating-training-modules)
5. [Building Decision Trees](#building-decision-trees)
6. [Working with Automation Scripts](#working-with-automation-scripts)
7. [Testing and Quality Assurance](#testing-and-quality-assurance)
8. [Git Workflow](#git-workflow)
9. [CI/CD Pipeline](#cicd-pipeline)
10. [Release Process](#release-process)
11. [Troubleshooting](#troubleshooting)

---

## 🛠️ Development Environment Setup

### Prerequisites

**Required**:
- Git (2.30+)
- Text editor or IDE (VS Code recommended)
- GitHub account

**Optional but Recommended**:
- Python 3.11+ (for automation scripts)
- Node.js 18+ (for future interactive tools)
- Markdown linter extension
- GitHub CLI (`gh`)

### Initial Setup

#### 1. Fork and Clone Repository

```bash
# Fork on GitHub first, then:
git clone https://github.com/YOUR-USERNAME/federal-hr-training.git
cd federal-hr-training

# Add upstream remote
git remote add upstream https://github.com/pvestal/federal-hr-training.git

# Verify remotes
git remote -v
```

#### 2. Install Development Tools

**Python Tools** (for scripts):
```bash
# Create virtual environment
python3 -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install requests beautifulsoup4 pyyaml
```

**VS Code Extensions** (recommended):
- Markdown All in One
- markdownlint
- Spell Checker
- GitLens
- Python (if developing scripts)

#### 3. Configure Git

```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Optional: Set up commit signing
git config commit.gpgsign true
```

---

## 📁 Repository Structure

### Directory Layout

```
federal-hr-training/
│
├── .github/                        # GitHub configuration
│   ├── workflows/                  # CI/CD pipelines
│   │   ├── quality-check.yml      # Content quality automation
│   │   └── opm-update-monitor.yml # Regulatory monitoring
│   ├── ISSUE_TEMPLATE/            # Issue templates
│   │   ├── bug_report.yml
│   │   ├── content-update.yml
│   │   └── feedback.yml
│   └── PULL_REQUEST_TEMPLATE/     # PR template
│       └── pull_request_template.md
│
├── 01-basic-hr/                   # Level 1 training
│   ├── modules/                   # Training modules
│   ├── assessments/               # Quizzes and exams
│   └── resources/                 # Additional materials
│
├── 02-intermediate-hr/            # Level 2 training
│   ├── modules/
│   ├── assessments/
│   └── resources/
│
├── 03-advanced-hr/                # Level 3 training
│   ├── modules/
│   ├── assessments/
│   └── resources/
│
├── 04-expert-hr/                  # Level 4 training
│   ├── modules/
│   ├── assessments/
│   └── resources/
│
├── case-studies/                  # Real-world scenarios
├── decision-trees/                # Interactive guidance
├── opm-updates/                   # Regulatory tracking
│   └── 2025/
│       └── CHANGELOG-2025.md
│
├── reference-materials/           # Quick references
├── scripts/                       # Automation scripts
│   ├── check_opm_currency.py     # OPM monitoring
│   ├── check_module_completeness.py
│   └── validate_curriculum.py
│
├── reports/                       # Generated reports (not in git)
│
├── README.md                      # Program overview
├── USER_GUIDE.md                  # End-user documentation
├── DEVELOPER_GUIDE.md             # This document
├── CURRICULUM_GUIDE.md            # Detailed curriculum
├── CONTRIBUTING.md                # Contribution guidelines
├── CHANGELOG.md                   # Version history
├── LICENSE                        # Public domain dedication
├── .gitignore                     # Git ignore rules
└── .markdownlint.json            # Linting configuration
```

### File Naming Conventions

**Training Modules**:
```
module-<level>.<number>-<topic-slug>.md

Examples:
- module-1.1-intro-to-federal-hr.md
- module-2.3-classification-deep-dive.md
- module-3.5-rif-planning-execution.md
```

**Decision Trees**:
```
<topic-slug>-decision-tree.md

Examples:
- fehb-qualifying-life-event.md
- leave-approval-decision.md
- rif-retention-determination.md
```

**Case Studies**:
```
case-<number>-<topic-slug>.md

Examples:
- case-001-complex-retirement-calculation.md
- case-042-rif-competitive-area-analysis.md
```

**Reference Materials**:
```
<topic>-quick-reference.md
<regulation>-summary.md

Examples:
- fehb-plans-quick-reference.md
- 5cfr-part-630-summary.md
```

---

## 📝 Content Development Standards

### Writing Style Guidelines

#### Plain Language Requirements

Follow [PlainLanguage.gov](https://www.plainlanguage.gov/) principles:

**DO**:
- Use active voice: "Submit your application" (not "Your application should be submitted")
- Use short sentences (15-20 words average)
- Use common words: "use" not "utilize", "help" not "facilitate"
- Define acronyms on first use: "Federal Employees Health Benefits (FEHB)"
- Use "you" to address the reader

**DON'T**:
- Use jargon without explanation
- Write overly long paragraphs (5-7 sentences max)
- Use bureaucratic language
- Assume prior knowledge

#### Markdown Formatting Standards

**Headers**:
```markdown
# Level 1 - Main Title
## Level 2 - Major Section
### Level 3 - Subsection
#### Level 4 - Minor Point
```

**Emphasis**:
```markdown
**Bold** for key terms on first use
*Italics* for emphasis
`Code formatting` for system names (DCPDS, FEHB)
```

**Lists**:
```markdown
Unordered:
- First item
- Second item
  - Nested item (2 spaces)

Ordered:
1. First step
2. Second step
3. Third step
```

**Links**:
```markdown
[Descriptive Text](https://www.opm.gov/exact-url/)

Examples:
[5 CFR § 630.201](https://www.ecfr.gov/current/title-5/section-630.201)
[OPM Benefits Administration Letters](https://www.opm.gov/healthcare-insurance/healthcare/reference-materials/)
```

**Tables**:
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
| Data     | Data     | Data     |
```

**Code Blocks**:
````markdown
```bash
# Bash commands
git clone https://github.com/repo.git
```

```python
# Python code
def function():
    return "value"
```
````

### Citation Requirements

**Always cite official sources**:

```markdown
According to 5 CFR § 630.201, annual leave accrues based on years of service.

**Reference**: [5 CFR § 630.201](https://www.ecfr.gov/current/title-5/section-630.201)
```

**Source Priority**:
1. 5 CFR (Code of Federal Regulations)
2. OPM policy guidance (BALs, CHCO memos)
3. Federal Register notices
4. OPM handbooks and manuals
5. Agency-specific guidance (if applicable)

### Accessibility Standards

**Section 508 Compliance**:
- Use descriptive link text (not "click here")
- Provide alt text for images: `![Description](image.png)`
- Use proper heading hierarchy (don't skip levels)
- Ensure tables have headers
- Keep contrast ratios accessible
- Test with screen readers

---

## 📚 Creating Training Modules

### Module Template

Create new module from this template:

```markdown
# Module X.Y: [Module Title]

**Level**: [Basic/Intermediate/Advanced/Expert] (Level X)
**Duration**: X hours
**Prerequisites**: [None or list prerequisites]
**Last Updated**: [Date]

---

## Module Overview

[2-3 paragraph overview of what this module covers and why it's important]

**Terminal Learning Objective**:
Upon completion, learners will be able to [specific, measurable objective].

**Enabling Learning Objectives**:
1. [Specific objective 1]
2. [Specific objective 2]
3. [Specific objective 3]

---

## Content Outline

### 1. [Major Topic] (XX minutes)

#### Subsection
[Content here]

**Reference**: [Official source with link]

---

## Learning Activities

### Activity 1: [Activity Name] (XX minutes)

**Scenario**: [Description]

**Questions**:
1. [Question]
2. [Question]

**Answers**:
[Provide answers with explanation]

---

## Assessment

### Knowledge Check Quiz (XX questions, XX% passing)

**Multiple Choice**:

1. [Question]
   - a) [Option]
   - b) [Option]
   - c) [Option]
   - d) [Option]

   **Answer**: [Correct answer with brief explanation]

### Practical Exercise

[Hands-on activity description]

---

## Resources

### Official References
- [Link with description]
- [Link with description]

### Additional Reading
- [Optional resources]

### Videos
- [OPM or training videos]

### Job Aids
- [Quick references, checklists]

---

**Module Complete**

**Next Module**: X.Y - [Next Module Title]

**Questions or Feedback**: Submit via GitHub Issues

---

**Document Control**:
- **Version**: X.Y.Z
- **Author**: [Name]
- **Last Review**: [Date]
- **Next Review**: [Date]
```

### Module Development Checklist

Before submitting a new module, verify:

**Content Quality**:
- [ ] Learning objectives are clear and measurable
- [ ] Content is accurate and cited
- [ ] Examples are relevant and realistic
- [ ] Plain language is used throughout
- [ ] Acronyms are defined on first use

**Structure**:
- [ ] Follows template format
- [ ] All required sections present
- [ ] Proper heading hierarchy
- [ ] Consistent formatting

**Citations**:
- [ ] All regulations cited with links
- [ ] OPM guidance referenced
- [ ] Sources are current (2025-2026)
- [ ] Effective dates included

**Learning Components**:
- [ ] Learning activities included
- [ ] Assessment questions provided
- [ ] Practice exercises realistic
- [ ] Resources list is comprehensive

**Technical**:
- [ ] Markdown syntax correct
- [ ] Links tested and working
- [ ] File named correctly
- [ ] No sensitive information

---

## 🌲 Building Decision Trees

### Decision Tree Template

```markdown
# [Topic] Decision Tree

**Purpose**: [What this decision tree helps determine]
**Authority**: [5 CFR citation or OPM guidance]
**Last Updated**: [Date]

---

## How to Use This Decision Tree

1. Start at the beginning
2. Answer each question YES or NO
3. Follow the path to the determination
4. Note the action required and timeframe

---

## Decision Tree

\```
START: [Initial situation]
│
├─► Q1: [First decision point]
│   │
│   ├─► NO ──► [Outcome: Not qualified/denied/etc.]
│   │          └─ [Required action]
│   │
│   └─► YES ──► Continue to Q2
│       │
│       ├─► Q2: [Second decision point]
│           │
│           ├─► Option A ──► [Specific outcome]
│           │   ├─ Action: [What to do]
│           │   ├─ Form: [Required form]
│           │   ├─ Deadline: [Timeline]
│           │   └─ Effective: [Effective date]
│           │
│           ├─► Option B ──► [Different outcome]
│           │   └─ [Different requirements]
│           │
│           └─► Option C ──► [Another outcome]
\```

---

## Special Circumstances

[Any exceptions or special rules]

---

## Documentation Requirements

| Scenario | Required Documentation |
|----------|------------------------|
| [Case]   | [Documents needed]     |

---

## Processing Steps for HR Specialists

### Step 1: [First step]
[Instructions]

### Step 2: [Second step]
[Instructions]

---

## Common Mistakes to Avoid

1. **[Mistake]**: [Why it's wrong and how to avoid]
2. **[Mistake]**: [Explanation]

---

## Helpful Tips

- [Practical advice]
- [Best practices]

---

## References

- **5 CFR**: [Specific regulation link]
- **OPM Guidance**: [Handbook or BAL link]

---

**Document Control**:
- **Version**: X.Y.Z
- **Authority**: [Citation]
- **Last Review**: [Date]
- **Next Review**: [Date]
```

### Decision Tree Best Practices

1. **Keep it Visual**: Use ASCII tree structure for clarity
2. **Be Comprehensive**: Cover all major scenarios
3. **Cite Authority**: Every outcome needs regulatory basis
4. **Include Timelines**: Deadlines are critical in HR
5. **Add Examples**: Real-world scenarios help understanding
6. **Test with Users**: Have HR specialists walk through it

---

## 🤖 Working with Automation Scripts

### Script Overview

#### `check_opm_currency.py`
**Purpose**: Monitors OPM websites for updates
**Runs**: Daily via GitHub Actions
**Output**: `reports/opm_currency_check.json`

#### `check_module_completeness.py`
**Purpose**: Validates modules have required sections
**Runs**: On every PR
**Output**: `reports/module_completeness.json`

#### `validate_curriculum.py`
**Purpose**: Ensures directory structure is correct
**Runs**: On every PR
**Output**: Pass/Fail exit code

### Running Scripts Locally

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run OPM currency check
python scripts/check_opm_currency.py

# Run module completeness check
python scripts/check_module_completeness.py

# Run curriculum validation
python scripts/validate_curriculum.py
```

### Adding New Automation

**Template for new script**:

```python
#!/usr/bin/env python3
"""
Script Name
Description of what this script does
"""

import os
import sys
import json
from datetime import datetime

def main():
    """Main function"""
    print("=" * 60)
    print("SCRIPT NAME")
    print("=" * 60)

    # Your logic here

    # Save results
    results = {
        "check_time": datetime.now().isoformat(),
        "status": "success",
        "details": {}
    }

    os.makedirs('reports', exist_ok=True)
    with open('reports/script_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("✅ Check complete")
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Add to workflow**:

```yaml
# .github/workflows/custom-check.yml
name: Custom Check

on: [push, pull_request]

jobs:
  custom-check:
    name: Run Custom Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests

      - name: Run custom script
        run: python scripts/your_script.py
```

---

## ✅ Testing and Quality Assurance

### Pre-Commit Checks

Before committing, run:

```bash
# 1. Validate curriculum structure
python scripts/validate_curriculum.py

# 2. Check module completeness
python scripts/check_module_completeness.py

# 3. Test links (if you have tool installed)
markdown-link-check **/*.md

# 4. Spell check
# Use VS Code spell checker or:
aspell check your-file.md
```

### Manual Review Checklist

**Content Accuracy**:
- [ ] All OPM references are current
- [ ] 5 CFR citations are correct
- [ ] Effective dates are accurate
- [ ] Examples are realistic

**Quality**:
- [ ] Plain language used
- [ ] No typos or grammar errors
- [ ] Consistent terminology
- [ ] Proper citations

**Technical**:
- [ ] Markdown renders correctly
- [ ] All links work
- [ ] Images load (if any)
- [ ] File names correct

**Accessibility**:
- [ ] Descriptive link text
- [ ] Proper heading hierarchy
- [ ] Alt text for images
- [ ] Tables have headers

### Peer Review

**Requesting Review**:
1. Create PR with clear description
2. Tag relevant reviewers
3. Respond to feedback promptly
4. Make requested changes
5. Re-request review after changes

**Conducting Review**:
1. Check content accuracy
2. Verify citations and sources
3. Test user experience
4. Look for accessibility issues
5. Provide constructive feedback

---

## 🔀 Git Workflow

### Branch Strategy

```bash
# Create feature branch
git checkout -b feature/module-1.2-benefits-overview

# Create fix branch
git checkout -b fix/broken-link-module-1.1

# Create update branch
git checkout -b update/2025-11-opm-changes
```

### Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <short description>

<longer description if needed>

<footer with references>
```

**Types**:
- `feat`: New training module or major feature
- `fix`: Bug fix, typo, broken link
- `docs`: Documentation changes
- `update`: OPM guidance or regulation updates
- `refactor`: Content reorganization
- `test`: Assessment or quiz updates
- `chore`: Maintenance tasks

**Examples**:

```bash
git commit -m "feat: Add Module 1.2 - Federal Benefits Overview

Complete 8-hour module covering FEHB, FERS, TSP, FLTCIP, and FSAFEDS.
Includes learning activities, case studies, and 30-question assessment.

Refs: #12"
```

```bash
git commit -m "update: FEHB 2026 premium increases

Updated Module 1.3 to reflect 12.3% average premium increase for 2026.
Added PrEP medication coverage requirement.

Source: OPM Press Release October 1, 2025
Refs: #45"
```

```bash
git commit -m "fix: Correct 5 CFR citation in Module 1.4

Changed § 842.304 to § 842.204 (FERS eligibility section).
Verified against current eCFR.

Refs: #67"
```

### Pull Request Process

1. **Create Branch**:
   ```bash
   git checkout -b feature/your-change
   ```

2. **Make Changes**:
   - Follow style guide
   - Test thoroughly
   - Update related docs

3. **Commit**:
   ```bash
   git add .
   git commit -m "type: description"
   ```

4. **Push**:
   ```bash
   git push origin feature/your-change
   ```

5. **Create PR**:
   - Go to GitHub repository
   - Click "New Pull Request"
   - Fill out PR template completely
   - Request reviewers

6. **Address Feedback**:
   - Make requested changes
   - Push additional commits
   - Re-request review

7. **Merge**:
   - After approval, maintainer merges
   - Branch is automatically deleted

### Keeping Fork Updated

```bash
# Fetch upstream changes
git fetch upstream

# Merge into your main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### `quality-check.yml`
**Triggers**: Push, PR, Monthly schedule
**Jobs**:
- Markdown linting
- Link checking
- Spell checking
- OPM regulation currency
- Content quality validation
- Accessibility checks

**Viewing Results**:
1. Go to repository "Actions" tab
2. Select workflow run
3. View job details and logs

#### `opm-update-monitor.yml`
**Triggers**: Daily at 9 AM UTC
**Jobs**:
- Check Federal Register
- Check OPM Benefits Center
- Check 5 CFR changes
- Create issues for updates
- Commit update logs

**Auto-Generated Issues**:
- Labeled `opm-update`, `needs-review`
- Contains detected changes
- Links to official sources

### Workflow Customization

Edit `.github/workflows/*.yml` to:
- Change schedule: `cron: '0 9 * * *'`
- Add new checks
- Modify notifications
- Adjust pass/fail criteria

---

## 📦 Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- **MAJOR** (1.0.0): New training level or complete restructure
- **MINOR** (1.1.0): New modules within a level
- **PATCH** (1.0.1): Bug fixes, minor updates

### Creating a Release

1. **Update CHANGELOG.md**:
   ```markdown
   ## [1.1.0] - 2025-11-15

   ### Added
   - Module 1.2: Federal Benefits Overview
   - Module 1.3: FEHB Basics
   - 3 new case studies for Level 1

   ### Changed
   - Updated FEHB premium information for 2026

   ### Fixed
   - Corrected 5 CFR citation in Module 1.1
   ```

2. **Update version numbers**:
   - README.md
   - CURRICULUM_GUIDE.md
   - Module headers

3. **Commit changes**:
   ```bash
   git add -A
   git commit -m "chore: Prepare v1.1.0 release"
   git push
   ```

4. **Create Git tag**:
   ```bash
   git tag -a v1.1.0 -m "Release version 1.1.0

   - Added Modules 1.2 and 1.3
   - Updated 2026 FEHB information
   - Fixed citations"

   git push origin v1.1.0
   ```

5. **Create GitHub Release**:
   - Go to "Releases" → "Create new release"
   - Select tag: v1.1.0
   - Title: "Version 1.1.0 - Level 1 Expansion"
   - Description: Copy from CHANGELOG
   - Attach any downloadable assets (PDFs, etc.)
   - Click "Publish release"

### Release Checklist

- [ ] All tests passing
- [ ] CHANGELOG updated
- [ ] Version numbers updated
- [ ] Documentation current
- [ ] No broken links
- [ ] Git tag created
- [ ] GitHub release published
- [ ] Announcement made (if major release)

---

## 🔧 Troubleshooting

### Common Issues

#### GitHub Actions Failing

**Problem**: Workflow fails on markdown linting
**Solution**:
```bash
# Install markdownlint-cli locally
npm install -g markdownlint-cli

# Run locally to see errors
markdownlint **/*.md

# Fix issues and re-commit
```

**Problem**: Link checker reports broken links
**Solution**:
1. Identify broken links in workflow log
2. Update links to current URLs
3. Check if OPM reorganized content
4. Update or remove outdated links

#### Script Errors

**Problem**: Python scripts fail locally
**Solution**:
```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt  # If we add this file

# Run with verbose output
python -v scripts/check_opm_currency.py
```

#### Git Issues

**Problem**: Merge conflicts
**Solution**:
```bash
# Update your branch with main
git fetch upstream
git merge upstream/main

# Resolve conflicts in editor
# Then:
git add .
git commit -m "fix: Resolve merge conflicts"
```

**Problem**: Accidentally committed to main
**Solution**:
```bash
# Create branch from current state
git branch feature/your-change

# Reset main to upstream
git checkout main
git reset --hard upstream/main

# Switch to your branch
git checkout feature/your-change
```

### Getting Help

**Development Questions**:
- Create Discussion on GitHub
- Email: patrick.vestal@gmail.com

**OPM Content Questions**:
- Check OPM.gov
- Submit content-update issue
- Consult agency HR policy office

---

## 📚 Additional Resources

### Development Tools
- [Markdown Guide](https://www.markdownguide.org/)
- [GitHub Docs](https://docs.github.com/)
- [Plain Language Guidelines](https://www.plainlanguage.gov/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

### OPM Resources
- [OPM.gov](https://www.opm.gov/)
- [eCFR Title 5](https://www.ecfr.gov/current/title-5)
- [Federal Register](https://www.federalregister.gov/)
- [OPM Policy Data Oversight](https://www.opm.gov/policy-data-oversight/)

### Federal HR Community
- [CHCOC Transmittals](https://www.opm.gov/about-us/our-people-organization/support-functions/human-resources/chcoc/)
- [IPMA-HR](https://www.ipma-hr.org/)
- [SHRM Government Affairs](https://www.shrm.org/advocacy/public-policy-resources)

---

## 🤝 Thank You

Thank you for contributing to federal HR training! Your expertise helps HR professionals serve federal employees better.

**Questions?**
- GitHub Discussions: https://github.com/pvestal/federal-hr-training/discussions
- Email: patrick.vestal@gmail.com

---

**Document Version**: 1.0.0
**Last Updated**: October 28, 2025
**Next Review**: January 2026
