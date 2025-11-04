# OPM Updates Archive

This directory contains automated monitoring reports from the OPM Update Monitor workflow.

## Purpose

The OPM Update Monitor workflow runs daily to check for updates to:

- **Federal Register**: HR-related rules and notices
- **OPM Benefits Administration**: Changes to benefits guidance
- **OPM Policy & Oversight**: Policy documents and regulatory updates
- **5 CFR**: Title 5 Code of Federal Regulations changes

When updates are detected, the workflow:

1. Generates a comprehensive update report
2. Creates a GitHub issue for review
3. Creates a pull request with the update log
4. Stores the report in this directory

## Directory Structure

```
opm-updates/
├── README.md (this file)
├── 2025/
│   ├── update-2025-01-15.md
│   ├── update-2025-02-03.md
│   └── ...
├── 2026/
│   └── ...
```

Updates are organized by year and dated with the detection date (not the publication date).

## How to Use These Reports

When you receive a notification about an OPM update:

1. **Read the update report** in this directory
2. **Review the related GitHub issue** for discussion and tracking
3. **Identify affected training modules** based on the changes
4. **Update training content** to reflect current guidance
5. **Close the issue** once updates are complete

## Workflow Details

- **Schedule**: Daily at 9 AM UTC (4 AM EST)
- **Workflow File**: `.github/workflows/opm-update-monitor.yml`
- **Scripts**:
  - `scripts/monitor_federal_register.py`
  - `scripts/monitor_opm_benefits.py`
  - `scripts/monitor_opm_policy.py`
  - `scripts/monitor_5cfr.py`
  - `scripts/generate_opm_update_report.py`

## Manual Monitoring

You can also manually check for updates by running the workflow:

1. Go to the Actions tab in GitHub
2. Select "OPM Update Monitor"
3. Click "Run workflow"

Or run the scripts locally:

```bash
cd scripts
python3 monitor_federal_register.py
python3 monitor_opm_benefits.py
python3 monitor_opm_policy.py
python3 monitor_5cfr.py
python3 generate_opm_update_report.py
```

## Important Notes

- Reports are **automated** and may contain false positives
- Always verify changes with official OPM sources
- Some changes may not require training updates
- Critical regulatory changes should be prioritized

## Related Documentation

- [User Guide](../USER_GUIDE.md)
- [Developer Guide](../DEVELOPER_GUIDE.md)
- [Curriculum Guide](../CURRICULUM_GUIDE.md)
