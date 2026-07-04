#!/usr/bin/env python3
"""Extend SOP#1 (domestic) and SOP#2 (overseas) CIVPAY Q&A to Top-25 each.

Appends the additional rows to the existing CSVs (idempotent: skips a question
already present). Every added row cites the HIGHEST governing authority for the
rule (OPM/5 CFR/OPM GPPA at Tier 1; DoD FMR Vol 8 / DoDI 1400.25 / DSSR at
Tier 2); DCPS UM and DON/Navy references appear only as 'how it is executed',
never as the authority — a component instruction cannot override a higher
directive (operator precedence rule, 2026-07-04).

UNOFFICIAL working aid; spot-check numeric thresholds and DSSR/CFR sections
against the source of record before official use.
"""
from __future__ import annotations
import csv
from pathlib import Path

REVIEWED = "2026-07-04"
DATA = Path(__file__).resolve().parent.parent / "data"
HEADER = ["Question", "Answer", "Citation", "System", "Role", "Keywords", "LastReviewed"]

# ── SOP#1 domestic additions (16-25) ────────────────────────────────────────
DOMESTIC = [
    ("How is FEHB enrollment and its premium deduction established for pay?",
     "The employee elects FEHB on the SF-2809 (or via Employee Express/self-service); "
     "HR records the enrollment and it flows to DCPS as a health-benefits deduction "
     "code. Premiums are withheld each pay period and, by default, taken pre-tax under "
     "premium conversion unless the employee waives it. The governing authority is "
     "5 CFR Part 892 (premium conversion) and Part 890 (FEHB); DCPS executes the "
     "withholding.",
     "5 CFR Part 890 / Part 892 (FEHB, premium conversion)", "5 CFR", "Payroll;Employee",
     "FEHB;health benefits;premium conversion;SF-2809;deduction"),
    ("How are TSP contributions and the agency match processed?",
     "The employee sets a TSP contribution election; DCPS withholds the employee "
     "amount each pay period and applies the agency automatic 1% plus matching "
     "contributions for FERS employees. Traditional contributions are pre-tax and Roth "
     "are after-tax. The authority is 5 CFR Part 1600 et seq. (FRTIB); DCPS executes "
     "the deduction and reports to the TSP recordkeeper.",
     "5 CFR Part 1600 (TSP); 5 U.S.C. Ch. 84", "5 CFR", "Payroll;Employee",
     "TSP;thrift savings;agency match;FERS;Roth;deduction"),
    ("How is federal and state income tax withholding set for a civilian employee?",
     "Federal income tax withholding is computed by DCPS from the employee's Form W-4 "
     "using the IRS percentage/wage-bracket method; state withholding follows the "
     "applicable state certificate. Supplemental wages (awards, retro) may be withheld "
     "at the supplemental rate. The authority is the Internal Revenue Code and IRS "
     "Pub. 15; DCPS applies it.",
     "26 U.S.C. Subtitle C; IRS Pub. 15 (Circular E)", "FMR Vol 8", "Payroll;Employee",
     "tax withholding;W-4;federal tax;state tax;supplemental wages"),
    ("How are allotments and other voluntary deductions set up?",
     "Voluntary allotments (allotments to financial institutions, charitable "
     "contributions, union dues, etc.) are authorized by the employee and keyed to "
     "DCPS within the categories and limits DoD FMR Vol 8 permits. Discretionary "
     "allotments are limited in number; each is subordinate to mandatory deductions in "
     "the order of precedence.",
     "DoD FMR Vol 8, Ch. 4 (allotments and order of precedence)", "FMR Vol 8", "Payroll;Employee",
     "allotment;voluntary deduction;union dues;charity;limits"),
    ("How are involuntary deductions (garnishments, tax levies, child support) handled and prioritized?",
     "Involuntary deductions — IRS/state tax levies, child support and alimony orders, "
     "commercial garnishments, and salary offsets — are processed by DCPS on receipt of "
     "the legal order and applied in the order of precedence in DoD FMR Vol 8, subject "
     "to the Consumer Credit Protection Act limits on the amount that may be withheld. "
     "Child support and federal debts take priority per the governing statutes.",
     "DoD FMR Vol 8, Ch. 4 / Ch. 8; 15 U.S.C. 1673 (CCPA limits)", "FMR Vol 8", "Payroll",
     "garnishment;tax levy;child support;involuntary deduction;CCPA;offset"),
    ("How is overtime computed and what is the FLSA exempt vs non-exempt distinction?",
     "FLSA non-exempt employees earn overtime at 1.5x the FLSA regular rate for hours "
     "over 40 in a week; FLSA-exempt employees earn Title 5 overtime, which is capped "
     "(the hourly rate is limited by the GS-10 step 1 / GL cap). HR sets the FLSA "
     "status on the position; DCPS computes the pay. The authority is the FLSA and "
     "5 CFR Part 550 Subpart A.",
     "29 U.S.C. 207 (FLSA); 5 CFR Part 550 Subpart A (Title 5 overtime)", "5 CFR", "HR Specialist;Payroll",
     "overtime;FLSA;exempt;non-exempt;Title 5;cap"),
    ("How are night, Sunday, and holiday premiums paid?",
     "General Schedule employees receive night differential of 10% of basic pay for "
     "regularly scheduled night work, Sunday premium of 25% for regularly scheduled "
     "Sunday work, and holiday premium of an additional 100% (double time) for work on "
     "a holiday, under 5 CFR Part 550 Subpart A. DCPS computes each from the certified "
     "time and the position's schedule.",
     "5 CFR Part 550 Subpart A; 5 U.S.C. 5545/5546", "5 CFR", "Payroll;Timekeeper",
     "night differential;Sunday premium;holiday premium;premium pay"),
    ("How is retroactive pay processed after a late personnel action?",
     "When an action reaches DCPS after the pay period covering its effective date, the "
     "DCPS retroactive (retro) process recomputes each affected prior pay period from "
     "the effective date, nets the difference against what was already paid, and issues "
     "the adjustment. The effective date is not changed; the underlying entitlement "
     "governs the recomputation.",
     "DCPS User Manual, Sec. E Batch — Retro Processing; DoD FMR Vol 8, Ch. 3", "DCPS", "Payroll",
     "retroactive pay;retro;late action;recomputation;adjustment"),
    ("How is final pay handled at separation, including unused annual leave?",
     "At separation DCPS pays earned salary through the separation date and a lump-sum "
     "payment for the employee's unused accrued annual leave, projected forward as if "
     "the employee had remained in service. The authority is 5 U.S.C. 5551 and 5 CFR "
     "Part 550 Subpart L; the separation SF-50 triggers the computation.",
     "5 U.S.C. 5551; 5 CFR Part 550 Subpart L (lump-sum annual leave)", "5 CFR", "HR Specialist;Payroll",
     "separation;final pay;lump-sum;annual leave;5551"),
    ("How are aggregate pay limitations (pay caps) applied?",
     "Total compensation is bounded by the biweekly and annual aggregate limitations "
     "in 5 U.S.C. 5307 (generally the rate for Level IV/EX of the Executive Schedule); "
     "premium pay is also subject to the biweekly/annual premium-pay caps in 5 CFR "
     "Part 550. DCPS enforces the caps at computation and defers amounts over the "
     "biweekly cap where the annual method applies.",
     "5 U.S.C. 5307; 5 CFR Part 530 Subpart B / Part 550 (premium caps)", "5 CFR", "HR Specialist;Payroll",
     "pay cap;aggregate limitation;5307;premium cap;EX level"),
]

# ── SOP#2 overseas additions (13-25) ────────────────────────────────────────
OVERSEAS = [
    ("What is the Education Allowance for dependents overseas?",
     "The Education Allowance helps cover the cost of adequate elementary and secondary "
     "schooling for dependents at a foreign post where free public schooling comparable "
     "to the U.S. is not available. Rates are set per post by the DSSR; it is a "
     "cost-reimbursement allowance, not salary.",
     "DSSR Section 270 (Education Allowance)", "DSSR", "HR Specialist;Employee",
     "overseas;education allowance;dependents;school;DSSR 270"),
    ("What is the Separate Maintenance Allowance (SMA)?",
     "SMA helps offset the added expense when an employee must maintain family members "
     "at a location other than the foreign post — involuntarily (e.g., dangerous or "
     "unhealthful post) or voluntarily. It is authorized and rated under the DSSR.",
     "DSSR Section 260 (Separate Maintenance Allowance)", "DSSR", "HR Specialist;Employee",
     "overseas;SMA;separate maintenance;family;DSSR 260"),
    ("What is the Foreign Transfer Allowance (FTA)?",
     "FTA reimburses certain extraordinary, necessary costs of transferring TO a foreign "
     "post — pre-departure subsistence, lease-penalty, wardrobe, and miscellaneous "
     "expenses — under the DSSR. It is distinct from TQSA (which covers temporary "
     "quarters AT the post).",
     "DSSR Section 240 (Foreign Transfer Allowance)", "DSSR", "HR Specialist;Employee",
     "overseas;FTA;foreign transfer allowance;relocation;DSSR 240"),
    ("Who is eligible for Home Leave from an overseas assignment?",
     "Home leave is leave earned for service abroad, to be used in the United States, "
     "under 5 U.S.C. 6305 and 5 CFR Part 630 Subpart F. It accrues based on completed "
     "months of qualifying overseas service and is separate from annual leave.",
     "5 U.S.C. 6305; 5 CFR Part 630 Subpart F (home leave)", "5 CFR", "HR Specialist;Employee",
     "overseas;home leave;6305;overseas service;leave"),
    ("What is Rest and Recuperation (R&R) travel?",
     "R&R provides government-funded travel from a designated hardship post to a relief "
     "location during a tour, to relieve the effects of difficult conditions. "
     "Eligibility and destinations are set by the agency under DoD/DSSR overseas policy "
     "for qualifying posts.",
     "DSSR / DoDI 1400.25 overseas policy (R&R at designated posts)", "DoDI 1400.25", "HR Specialist;Employee",
     "overseas;R&R;rest and recuperation;hardship post;travel"),
    ("What is an Advance of Pay for an overseas assignment?",
     "An eligible employee assigned abroad may receive an advance of up to three months' "
     "net salary to meet extraordinary costs incident to the assignment, recovered "
     "through payroll deduction over a set period. It is authorized under the DSSR.",
     "DSSR Section 850 (Advance of Pay)", "DSSR", "Payroll;Employee",
     "overseas;advance of pay;three months salary;recovery;DSSR 850"),
    ("What is the Consumables Allowance?",
     "At posts where suitable consumable goods (food, household supplies) are not "
     "reliably available locally, the Consumables Allowance helps cover the cost of "
     "shipping/purchasing them, under the DSSR for designated posts.",
     "DSSR (consumables at designated posts)", "DSSR", "HR Specialist;Employee",
     "overseas;consumables allowance;goods;designated post"),
    ("How do post differential and danger pay combine, and are there caps?",
     "Post (hardship) differential and danger pay are each a percentage of basic pay "
     "and may apply at the same post; they are computed separately and both are taxable. "
     "Each is capped at the DSSR-set maximum percentage for the post, and total premium "
     "compensation remains subject to the aggregate pay limitation (5 U.S.C. 5307).",
     "DSSR Sections 500 and 650; 5 U.S.C. 5307 (aggregate limitation)", "DSSR", "Payroll",
     "overseas;post differential;danger pay;stacking;cap;taxable"),
    ("How is currency fluctuation handled in LQA and allowance payments?",
     "LQA and other quarters allowances are paid in U.S. dollars using a currency "
     "conversion rate carried on the DCPS entitlement record; as exchange rates change, "
     "the payable amount is adjusted and the allowance is reconciled against actual "
     "expenses. DCPS stores the conversion rate per entitlement period.",
     "DCPS User Manual, Sec. D Ch. 5 (currency conversion rate); DSSR Section 130", "DCPS", "Payroll",
     "overseas;currency fluctuation;conversion rate;LQA;reconciliation"),
    ("How are overseas evacuation payments handled?",
     "On an ordered or authorized departure (evacuation) from a foreign post, evacuees "
     "may receive subsistence and travel payments and continued salary/allowances for a "
     "period, under the DSSR evacuation provisions administered through DoD payroll.",
     "DSSR Section 600 (Payments During Evacuation)", "DSSR", "Payroll;Employee",
     "overseas;evacuation;ordered departure;subsistence;DSSR 600"),
    ("Do within-grade increases and GS pay-setting work differently overseas?",
     "No — GS basic-pay setting, promotion rules, and within-grade increase waiting "
     "periods follow the same Title 5 / 5 CFR rules regardless of duty location. What "
     "differs overseas is the ADDED allowances and differentials (LQA, COLA, "
     "differential, danger pay), not the underlying rate of basic pay.",
     "5 CFR Part 531 (GS pay / WGI) — applies regardless of location", "5 CFR", "HR Specialist;Payroll",
     "overseas;WGI;pay setting;GS;same rules;allowances separate"),
    ("What is the Extraordinary Quarters Allowance (EQA)?",
     "EQA covers unusually high, temporary quarters costs an employee must incur at a "
     "post beyond what LQA provides in specific circumstances, under the DSSR quarters "
     "provisions for designated situations.",
     "DSSR Section 130 (quarters allowances — extraordinary)", "DSSR", "HR Specialist;Payroll",
     "overseas;EQA;extraordinary quarters;LQA;DSSR 130"),
    ("Can recruitment or retention incentives be used for hard-to-fill overseas positions?",
     "Yes — recruitment, relocation, and retention incentives under 5 CFR Part 575 may "
     "be used for positions likely to be difficult to fill, including overseas, subject "
     "to the same approval and service-agreement rules as domestic incentives. These "
     "are Title 5 incentives, separate from DSSR allowances.",
     "5 CFR Part 575 (recruitment/relocation/retention incentives)", "5 CFR", "HR Specialist",
     "overseas;recruitment incentive;retention;3Rs;5 CFR 575;hard to fill"),
]


def _append(csv_path: Path, rows: list) -> int:
    existing = set()
    if csv_path.exists():
        with csv_path.open() as f:
            for r in csv.DictReader(f):
                existing.add(r["Question"].strip())
    added = 0
    with csv_path.open("a", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        for q, a, cite, system, role, kw in rows:
            if q.strip() in existing:
                continue
            assert cite.strip(), f"row missing citation: {q}"
            w.writerow([q, a, cite, system, role, kw, REVIEWED])
            added += 1
    return added


def main() -> int:
    d = _append(DATA / "civpay_qa.csv", DOMESTIC)
    o = _append(DATA / "civpay_qa_overseas.csv", OVERSEAS)
    print(f"appended domestic=+{d} overseas=+{o}")
    for name in ("civpay_qa.csv", "civpay_qa_overseas.csv"):
        n = sum(1 for _ in csv.DictReader((DATA / name).open()))
        print(f"  {name}: {n} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
