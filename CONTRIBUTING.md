# Contributing to Federal HR Training Program

Thank you for your interest in improving federal HR training materials! This project relies on contributions from federal HR professionals to maintain accuracy and relevance.

## 🎯 How to Contribute

### Types of Contributions Welcome

1. **Content Updates**
   - OPM policy changes
   - 5 CFR regulation amendments
   - FEHB/FERS updates
   - New hiring authorities
   - Best practice updates

2. **Bug Fixes**
   - Broken links
   - Incorrect information
   - Typos and grammatical errors
   - Formatting issues

3. **Enhancements**
   - New case studies
   - Interactive decision trees
   - Additional resources
   - Practice exercises
   - Assessment questions

4. **Feedback**
   - Training effectiveness
   - Clarity improvements
   - Accessibility suggestions
   - Real-world applicability

---

## 📝 Contribution Process

### Step 1: Check Existing Issues
Before starting work, check if an [issue already exists](https://github.com/pvestal/federal-hr-training/issues) for your contribution.

### Step 2: Create or Comment on Issue
- **New contribution**: Create a new issue using the appropriate template
- **Existing issue**: Comment that you'd like to work on it
- Wait for assignment or approval from maintainers

### Step 3: Fork and Branch
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR-USERNAME/federal-hr-training.git
cd federal-hr-training

# Create a branch for your work
git checkout -b feature/your-contribution-name
# or
git checkout -b fix/bug-description
```

### Step 4: Make Your Changes
- Follow the [style guide](#style-guide) below
- Ensure accuracy with official sources
- Test any links or interactive elements
- Update related documentation

### Step 5: Commit Your Changes
```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "type: brief description

Detailed explanation of changes made.

Refs: #issue-number"
```

**Commit Message Format:**
- `docs:` Documentation changes
- `feat:` New training module or feature
- `fix:` Bug fixes
- `update:` Content updates (OPM guidance, regulations)
- `style:` Formatting, typos
- `refactor:` Content reorganization
- `test:` Assessment/quiz updates

### Step 6: Push and Create Pull Request
```bash
# Push to your fork
git push origin feature/your-contribution-name

# Create Pull Request on GitHub
# Use the PR template provided
```

### Step 7: Respond to Review
- Address reviewer feedback
- Make requested changes
- Update your PR as needed

---

## 📚 Style Guide

### Content Writing Standards

#### 1. Plain Language
- Write in clear, simple language
- Avoid jargon where possible; define when necessary
- Use active voice
- Keep sentences concise (20 words or fewer when possible)

**Good**: "Submit your retirement application 90 days before your retirement date."
**Bad**: "The retirement application should be submitted no less than 90 days prior to the anticipated retirement date."

#### 2. Accuracy Requirements
- All content must cite official sources (OPM, 5 CFR, Federal Register)
- Verify information is current (2025-2026)
- Include effective dates for regulations
- Note when guidance is subject to change

#### 3. Structure
- Use clear hierarchical headings (H1 → H2 → H3)
- Include learning objectives for each module
- Provide assessments or knowledge checks
- List required resources

#### 4. Formatting

**Headers:**
```markdown
# Module Title (H1)
## Section Title (H2)
### Subsection Title (H3)
```

**Lists:**
- Use bullets for unordered items
- Use numbers for sequential steps
- Maintain consistent indentation

**Links:**
```markdown
[Descriptive Link Text](https://www.opm.gov/exact-url/)
```

**Emphasis:**
- **Bold** for key terms on first use
- *Italics* for emphasis
- `Code formatting` for system names (DCPDS, FEHB)

**Tables:**
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data     | Data     | Data     |
```

#### 5. Citations
Always cite official sources:

```markdown
According to 5 CFR § 630.201, annual leave accrues as follows...

Reference: [5 CFR § 630.201](https://www.ecfr.gov/current/title-5/chapter-I/subchapter-B/part-630/subpart-B/section-630.201)
```

### File Naming Conventions

**Training Modules:**
- `01-basic-hr/modules/module-1.1-intro-to-federal-hr.md`
- `02-intermediate-hr/modules/module-2.3-classification.md`

**Case Studies:**
- `case-studies/retirement-planning-complex-scenario.md`
- `case-studies/rif-competitive-area-analysis.md`

**Decision Trees:**
- `decision-trees/fehb-qualifying-life-event.md`
- `decision-trees/leave-approval-decision.md`

**Resources:**
- `reference-materials/opm-guidance-summary-2025.md`
- `reference-materials/5cfr-part-630-leave-quick-reference.md`

### Directory Structure
```
federal-hr-training/
├── 01-basic-hr/
│   ├── modules/
│   ├── assessments/
│   └── resources/
├── 02-intermediate-hr/
│   ├── modules/
│   ├── assessments/
│   └── resources/
├── case-studies/
├── decision-trees/
├── opm-updates/
└── reference-materials/
```

---

## 🔍 Review Process

### What Reviewers Check

1. **Accuracy**
   - Content matches official OPM guidance
   - Regulations cited correctly
   - Effective dates included

2. **Currency**
   - Information is current (2025-2026)
   - Recent regulatory changes incorporated
   - Outdated content flagged

3. **Quality**
   - Writing is clear and professional
   - Learning objectives are measurable
   - Assessments align with objectives
   - Resources are accessible

4. **Technical**
   - Markdown formatted correctly
   - Links work properly
   - No broken references
   - Files named appropriately

### Review Timeline
- **Initial review**: Within 7 days
- **Follow-up**: Within 3 days of changes
- **Approval**: When all checks pass

---

## ✅ Quality Standards

### Content Must:
- [ ] Be based on official federal sources (OPM, 5 CFR, OMB)
- [ ] Include effective dates for regulations
- [ ] Use plain language (8th-10th grade reading level)
- [ ] Cite all sources properly
- [ ] Be free of personally identifiable information (PII)
- [ ] Be appropriate for public domain use
- [ ] Align with Section 508 accessibility standards
- [ ] Include learning objectives (for training modules)
- [ ] Provide assessment criteria (for training modules)

### Technical Requirements:
- [ ] Markdown linting passes
- [ ] All links tested and working
- [ ] Spelling checked
- [ ] Proper file naming convention
- [ ] Committed to correct directory

---

## 🚫 What NOT to Contribute

- **Classified or sensitive information**
- **Agency-specific proprietary processes** (unless cleared for public release)
- **Personally identifiable information (PII)**
- **Political opinions or bias**
- **Unofficial interpretations** of regulations
- **Copyrighted materials** without permission
- **Personal contact information**

---

## 🤝 Code of Conduct

### Expected Behavior
- Be respectful and professional
- Focus on constructive feedback
- Assume good intentions
- Collaborate openly
- Credit others' contributions

### Unacceptable Behavior
- Harassment or discrimination
- Personal attacks
- Trolling or inflammatory comments
- Sharing private information
- Other conduct inappropriate for a professional setting

### Reporting Issues
Contact the project maintainer at [patrick.vestal@outlook.com](mailto:patrick.vestal@outlook.com) to report conduct concerns.

---

## 📧 Questions or Help

- **General questions**: Open a [Discussion](https://github.com/pvestal/federal-hr-training/discussions)
- **Bug reports**: Create a [Bug Report Issue](https://github.com/pvestal/federal-hr-training/issues/new?template=bug_report.yml)
- **Content updates**: Create a [Content Update Issue](https://github.com/pvestal/federal-hr-training/issues/new?template=content-update.yml)
- **Feedback**: Create a [Feedback Issue](https://github.com/pvestal/federal-hr-training/issues/new?template=feedback.yml)
- **Direct contact**: patrick.vestal@outlook.com

---

## 📜 License

By contributing to this project, you agree that your contributions will be released under the project's license (public domain for federal government training materials).

---

## 🙏 Recognition

Contributors will be recognized in:
- `CONTRIBUTORS.md` file
- Release notes for significant contributions
- Annual acknowledgments

Thank you for helping improve federal HR training!

---

**Last Updated**: October 28, 2025
**Version**: 1.0.0
