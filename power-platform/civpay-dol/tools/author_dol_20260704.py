#!/usr/bin/env python3
"""Author the consolidated CIVPAY Division-of-Labor map -> data/civpay_dol.csv.

Maps the DoD/DON civilian personnel-action-to-pay lifecycle: each step's
responsible role, the system it happens in, the GOVERNING AUTHORITY (Tier 1-2:
OPM/5 CFR/OPM GPPA, DoD FMR Vol 8, DoDI 1400.25, DSSR) and the LOCAL
PROCEDURE/SYSTEM that executes it (Tier 3-4: DCPDS UM, DCPS UM/Interface Spec,
DON/OCHR procedures). Precedence rule (operator, 2026-07-04): a component/system
reference is NEVER the governing authority — the rule always traces to the
highest directive.

Grounded in: DON Civilian HR Roles and Responsibilities; DON OCHR RPA Handling
Procedures; DCPDS UM; DCPS UM (incl. audit/reconciliation reports P6634 Pre-Pay
Audit, P6698 Gross Pay Reconciliation, P6628 Pay Certification); DoD FMR Vol 8;
OPM GPPA; DSSR; DoDI 1400.25. UNOFFICIAL working aid.
"""
from __future__ import annotations
import csv
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "data" / "civpay_dol.csv"

OPM_GPPA = "https://www.opm.gov/policy-data-oversight/data-analysis-documentation/personnel-documentation/"
ECFR5 = "https://www.ecfr.gov/current/title-5"
FMR8 = "https://comptroller.defense.gov/FMR/vol8_chapters.aspx"
DSSR = "https://aoprals.state.gov/content.asp?content_id=231&menu_id=81"
DODI1400 = "https://www.esd.whs.mil/DD/DoD-Issuances/1400/"

HEADER = ["Title", "Phase", "ResponsibleRole", "System", "GoverningAuthority",
          "LocalProcedure", "AuthorityTier", "ReferenceLink", "Notes"]

# (Task, Phase, Roles, System, GoverningAuthority(T1-2), LocalProcedure(T3-4), Tier, Link, Notes)
ROWS = [
    ("Initiate the personnel action (SF-52 / RPA)", "Initiation",
     "Manager/Supervisor;HR Specialist", "DCPDS",
     "OPM GPPA (what an action requires)",
     "DON OCHR RPA Handling Procedures; DCPDS RPA entry",
     "T4 Component (DON)", OPM_GPPA,
     "Supervisor requests; HR reviews. DON procedure governs routing, not the rule."),
    ("Classify the action and assign the NOAC / legal authority", "Initiation",
     "HR Specialist", "DCPDS",
     "OPM GPPA action tables (NOAC + authority)",
     "DCPDS UM (RPA processing)",
     "T1 Federal (OPM)", OPM_GPPA,
     "NOAC and authority are OPM-defined; DCPDS is the entry system."),
    ("Approve and effect the SF-50", "Effecting (HR)",
     "HR Specialist", "DCPDS",
     "OPM GPPA; 5 CFR (pay-setting rules)",
     "DCPDS UM; DON OCHR effecting procedures",
     "T1 Federal (OPM)", ECFR5,
     "HR owns through effecting the SF-50."),
    ("Record benefits elections (retirement, FEHB, TSP)", "Effecting (HR)",
     "HR Specialist;Employee", "DCPDS",
     "5 U.S.C. Ch. 83/84; 5 CFR 890/892; 5 CFR 1600",
     "DCPDS / employee self-service; flows to DCPS deduction codes",
     "T1 Federal (OPM)", ECFR5,
     "Elections are statutory/CFR; systems record them."),
    ("Transmit effected personnel data DCPDS -> DCPS", "HR→Pay Interface",
     "System (automated)", "DCPS",
     "DoD FMR Vol 8 (payroll data source of record)",
     "DCPS Interface Spec (Personnel Interface); nightly file",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "The interface is the HR->Pay ownership boundary."),
    ("Record time and attendance", "Timekeeping",
     "Timekeeper", "DCPS",
     "5 CFR Part 550 / Part 610 (hours of work, premium pay)",
     "DCPS UM Sec D (T&A entry)",
     "T1 Federal (OPM)", ECFR5,
     "Timekeeper records reported time."),
    ("Certify time and attendance", "Timekeeping",
     "Certifying Officer;Manager/Supervisor", "DCPS",
     "DoD FMR Vol 8, Ch. 2 (T&A certification)",
     "DCPS UM Sec D (certification)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "Certifier attests to correctness before pay computes."),
    ("Compute gross pay, locality, and premiums", "Pay Computation",
     "System (automated);Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 3; 5 CFR Part 550",
     "DCPS UM Sec D Ch. 5 (Pay)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "DCPS computes from the updated Master Employee Record."),
    ("Apply deductions in order of precedence and pay caps", "Pay Computation",
     "System (automated);Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 4 (order of precedence); 5 U.S.C. 5307 (caps)",
     "DCPS UM Sec D (deductions)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "Precedence and caps are FMR/statute; DCPS enforces."),
    ("Run the pre-pay audit before certification", "Reconciliation/Audit",
     "Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 5 (pay certification controls)",
     "DCPS UM Sec F Ch. 5 Report P6634 (Pre-Pay Audit — Gross to Deductions)",
     "T3 System (DCPDS/DCPS)", FMR8,
     "Report P6634 flags pre-pay exceptions for CSR review."),
    ("Certify the payroll for payment", "Certification",
     "Certifying Officer", "DCPS",
     "31 U.S.C. 3528 (certifying officer liability); DoD FMR Vol 8, Ch. 5",
     "DCPS UM Sec F Ch. 5 (Pay Certification)",
     "T1 Federal (OPM)", FMR8,
     "Certifying officer is personally accountable for the certification."),
    ("Disburse net pay to the employee", "Disbursing",
     "DFAS Disbursing", "Disbursing",
     "DoD FMR Vol 8, Ch. 5 (disbursing); 31 U.S.C. (disbursing authority)",
     "DCPS -> disbursing / Treasury",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "Net pay and allotments paid via Treasury/EFT."),
    ("Reconcile gross pay and labor to accounting", "Reconciliation/Audit",
     "Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 7 (accounting/labor/gross)",
     "DCPS UM Sec F Ch. 7 Report P6698 (Gross Pay Reconciliation)",
     "T3 System (DCPDS/DCPS)", FMR8,
     "Report P6698 reconciles gross pay to the accounting/labor system."),
    ("Correct pay via manual pay adjustment", "Corrections/Debt",
     "Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 3 (corrections)",
     "DCPS UM Sec D Ch. 5 (Automated/Manual Pay Adjustments)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "Used when DCPS cannot auto-compute the correction."),
    ("Establish and collect a pay debt (overpayment)", "Corrections/Debt",
     "Payroll (CSR)", "DCPS",
     "DoD FMR Vol 8, Ch. 9 (over/underpayments and debt)",
     "DCPS UM (debt module)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", FMR8,
     "Due-process notice, waiver rights, and withholding limits apply."),
    ("Confirm the action effected (SF-50 posted)", "Verification",
     "HR Specialist;Employee", "DCPDS",
     "OPM GPPA (SF-50 is the record of the action)",
     "DCPDS / HR Link (HR); MyBiz (employee self-service view only)",
     "T3 System (DCPDS/DCPS)", OPM_GPPA,
     "MyBiz is view-only; HR verifies in DCPDS/HR Link."),
    ("Establish overseas allowance entitlement (LQA/TQSA/COLA)", "Overseas",
     "HR Specialist;Payroll (CSR)", "DCPS",
     "DSSR (allowance rules); DoDI 1400.25 (overseas eligibility)",
     "DCPS UM Sec D Ch. 5 screen P1128 (Overseas Allowances)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", DSSR,
     "DSSR sets the rules/max; DCPS records and pays."),
    ("Reconcile LQA annually against actual expenses", "Overseas",
     "Payroll (CSR)", "DCPS",
     "DSSR Section 130 (LQA); DoD FMR Vol 8, Ch. 9 (resulting debt)",
     "DCPS UM Sec D Ch. 5 (reconciliation payment type R)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", DSSR,
     "Overpaid LQA becomes a collectible debt."),
    ("Administer foreign-national (local-national) pay", "Overseas",
     "HR Specialist;Payroll (CSR)", "DCPS",
     "DoDI 1400.25 (overseas/local-national); host-country/SOFA",
     "DCPS UM Sec D Ch. 4 (Foreign-National Gross Pay)",
     "T2 DoD/Overseas (FMR/DoDI/DSSR)", DODI1400,
     "LN pay follows prevailing-wage plans, not the GS schedule."),
]


def main() -> int:
    for r in ROWS:
        assert r[4].strip(), f"row missing governing authority: {r[0]}"
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        for (title, phase, roles, system, gov, local, tier, link, notes) in ROWS:
            w.writerow([title, phase, roles, system, gov, local, tier, link, notes])
    print(f"wrote {len(ROWS)} division-of-labor rows -> {OUT}")
    print("every row carries a Tier 1-2 GoverningAuthority")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
