#!/usr/bin/env python3
"""SOP#2 content-authoring: overseas / special-category CIVPAY Q&A (2026-07-04).

Emits data/civpay_qa_overseas.csv, imported into the SAME "CIVPAY Q&A" List as
SOP#1 (no parallel system — reuses the List, search web part, and upkeep flow).

Grounding: answers are grounded in the on-disk DCPS UM overseas sources
(SECTION D Ch.5 Pay — Overseas Allowances screen P1128; SECTION C Ch.1 COLA
table; SECTION D Ch.4 Foreign-National gross pay; DCPS Interface Spec SECTION T
LQA employee data file) plus the governing allowance regulations (DSSR sections,
DoD FMR Vol 8 Ch.10, DoDI 1400.25, 26 U.S.C. 912). DSSR web retrieval from
allowances.state.gov returned only the site shell (2026-07-04); DSSR section
citations are from the established regulation structure — spot-check against the
DSSR source before official use (UNOFFICIAL working aid).
"""
from __future__ import annotations
import csv
from pathlib import Path

REVIEWED = "2026-07-04"
OUT = Path(__file__).resolve().parent.parent / "data" / "civpay_qa_overseas.csv"

# (Question, Answer, Citation, System, Role, Keywords)
ROWS = [
    (
        "Who is eligible for Living Quarters Allowance (LQA) overseas?",
        "LQA is available to eligible U.S.-hire civilian employees recruited in the "
        "United States and assigned to a foreign post where government housing is not "
        "provided. It is not paid to locally-hired employees or where quarters are "
        "furnished. Eligibility and rates are set by the DSSR and administered per the "
        "DoD overseas policy; DCPS carries the LQA entitlement (code YE) once HR "
        "establishes it.",
        "DSSR Section 130 (LQA); DoDI 1400.25 (overseas); DCPS UM Sec D Ch.5 (entitlement YE)",
        "DSSR", "HR Specialist;Payroll",
        "overseas;LQA;living quarters allowance;eligibility;US hire",
    ),
    (
        "What does LQA cover and how is the maximum set?",
        "LQA reimburses rent (quarters) and utilities up to a maximum set by the DSSR "
        "for the post and the employee's family size/grade. In DCPS the entitlement "
        "record carries a quarters daily rate and a utilities daily rate; the LQA "
        "screen displays the DSSR 'table maximum' and the payable annual amount used "
        "to compute the allowance each pay period. Amounts are entered with a Q "
        "(quarters) or U (utilities) indicator and a currency conversion rate.",
        "DSSR Section 130; DCPS UM Sec D Ch.5 Pay — Overseas Allowances (screen P1128, p1210-1222)",
        "DCPS", "Payroll",
        "overseas;LQA;quarters;utilities;DSSR maximum;currency conversion",
    ),
    (
        "What is TQSA and how long can it be paid?",
        "Temporary Quarters Subsistence Allowance (TQSA) covers temporary lodging and "
        "meals when an employee first arrives at a post (before occupying permanent "
        "quarters) or is departing. In DCPS it is entitlement code YJ with an "
        "arrival/departure indicator. TQSA may be paid up to 150 days for an arrival "
        "and up to 30 days for a departure.",
        "DSSR Section 120 (TQSA); DCPS UM Sec D Ch.5 (entitlement YJ, 150/30-day limits)",
        "DSSR", "HR Specialist;Payroll",
        "overseas;TQSA;temporary quarters;arrival;departure;150 days;30 days",
    ),
    (
        "What is the Post Allowance (overseas COLA) and what is it based on?",
        "The Post (Cost-of-Living) Allowance compensates employees at foreign posts "
        "where the cost of goods and services substantially exceeds the Washington, "
        "D.C. base. It is based on the post's cost-of-living index relative to D.C. and "
        "the employee's spendable income and family size. DCPS applies it from the COLA "
        "central table; it is a recurring allowance, not a reimbursement.",
        "DSSR Section 220 (Post Allowance); DCPS UM Sec C Ch.1 COLA table (p179-181)",
        "DSSR", "Payroll;Employee",
        "overseas;post allowance;COLA;cost of living;index",
    ),
    (
        "What is Post (Hardship) Differential and is it taxable?",
        "Post Hardship Differential is additional compensation, expressed as a "
        "percentage of basic pay, for service at posts with extraordinarily difficult "
        "living conditions, excessive physical hardship, or notably unhealthful "
        "conditions. Unlike LQA/TQSA/post allowance, it is taxable wages subject to "
        "withholding.",
        "DSSR Section 500 (Post Differential); 26 U.S.C. 912 (allowance exclusions — differential not excluded)",
        "DSSR", "Payroll;Employee",
        "overseas;post differential;hardship;taxable;percentage of basic pay",
    ),
    (
        "What is Danger Pay?",
        "Danger Pay is additional compensation, a percentage of basic pay, for service "
        "at posts where civil insurrection, civil war, terrorism, or wartime conditions "
        "threaten physical harm or imminent danger. Like post differential it is "
        "taxable. It is authorized post-by-post by the Department of State.",
        "DSSR Section 650 (Danger Pay)",
        "DSSR", "Payroll;Employee",
        "overseas;danger pay;imminent danger;taxable;percentage of basic pay",
    ),
    (
        "How are overseas allowances recorded and paid in DCPS?",
        "HR/pay establishes the allowance entitlement in DCPS on the Overseas "
        "Allowances screen (P1128): entitlement code YE for LQA or YJ for TQSA, the "
        "entitlement from/to dates, amount with a quarters/utilities (Q/U) indicator, "
        "and a currency conversion rate. Normal biweekly payments (payment type B) are "
        "generated by the pay process; advances use type A/V, and reconciliations use "
        "type R. The DSSR maximum on the second screen bounds the payable amount.",
        "DCPS UM Sec D Ch.5 Pay — Overseas Allowances (screen P1128, p1210-1222)",
        "DCPS", "Payroll",
        "overseas;DCPS;P1128;entitlement code;payment type;advance;reconciliation",
    ),
    (
        "How is a foreign national (local national) employee's gross pay handled?",
        "Foreign national / local national employees are paid under host-country "
        "prevailing wage plans and local compensation systems, not the GS schedule, and "
        "their gross pay is computed in DCPS under the foreign-national pay rules rather "
        "than the domestic basic-pay tables. Entitlements follow the applicable "
        "country/labor agreement and DoD overseas policy.",
        "DCPS UM Sec D Ch.4 Gross Pay — Foreign National; DoDI 1400.25 (overseas/local-national)",
        "DoDI 1400.25", "HR Specialist;Payroll",
        "overseas;foreign national;local national;prevailing wage;gross pay",
    ),
    (
        "What governs special-category and overseas pay administration?",
        "Special-category civilian pay (including overseas allowances and differentials) "
        "is administered under DoD FMR Vol 8 Ch.10, which implements the DSSR and other "
        "authorities for DoD payroll. Overseas employment eligibility, allowances, and "
        "conditions of employment are governed by the DoDI 1400.25 overseas volumes. "
        "Both cross-reference the domestic personnel-action-to-pay flow (see SOP#1).",
        "DoD FMR Vol 8 Ch.10 (special category); DoDI 1400.25 (overseas volumes)",
        "FMR Vol 8", "HR Specialist;Payroll",
        "overseas;special category;FMR Vol 8 Ch 10;DoDI 1400.25;authority",
    ),
    (
        "Which overseas allowances are taxable and which are not?",
        "LQA, TQSA, and the Post (COLA) allowance are generally excluded from taxable "
        "gross income under 26 U.S.C. 912 — they are cost-reimbursement/quarters "
        "allowances, not wages. Post (hardship) differential and danger pay ARE taxable "
        "wages subject to federal withholding. DCPS applies the correct tax treatment "
        "based on the entitlement/pay-detail code.",
        "26 U.S.C. 912 (exclusion of certain cost-of-living and quarters allowances); DSSR",
        "DSSR", "Payroll;Employee",
        "overseas;taxable;LQA;COLA;differential;danger pay;IRC 912",
    ),
    (
        "How is LQA reconciled and what happens if it was overpaid?",
        "LQA is paid on an estimated basis and reconciled against the employee's actual "
        "rent and utility expenses for the entitlement year. In DCPS a reconciliation is "
        "entered as payment type R; if reconciliation shows the employee received more "
        "than actual allowable expenses, the excess is an overpayment that becomes a "
        "debt collected under the debt rules (see SOP#1 debts).",
        "DCPS UM Sec D Ch.5 (reconciliation payment type R); DSSR Section 130; DoD FMR Vol 8 Ch.9 (debt)",
        "DCPS", "Payroll",
        "overseas;LQA;reconciliation;overpayment;debt;actual expenses",
    ),
    (
        "How does overseas allowance/entitlement data get from HR to DCPS?",
        "As with domestic actions, effected personnel/entitlement data flows from DCPDS "
        "to DCPS over the personnel interface (see SOP#1 handoff). Active LQA employee "
        "data is carried on the DCPS interface in the LQA employee data file, so the "
        "allowance entitlement is established from the HR system of record rather than "
        "keyed independently in pay.",
        "DCPS Interface Spec Sec T (Active LQA Employees data file); DCPS UM Sec D Ch.5",
        "DCPS", "HR Specialist;Payroll",
        "overseas;DCPDS to DCPS;interface;LQA data file;handoff",
    ),
]

HEADER = ["Question", "Answer", "Citation", "System", "Role", "Keywords", "LastReviewed"]

def main() -> int:
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        for q, a, cite, system, role, kw in ROWS:
            w.writerow([q, a, cite, system, role, kw, REVIEWED])
    missing = [r[0] for r in ROWS if not r[2].strip()]
    assert not missing, f"rows missing citation: {missing}"
    print(f"wrote {len(ROWS)} overseas rows -> {OUT}; every row carries a citation")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
