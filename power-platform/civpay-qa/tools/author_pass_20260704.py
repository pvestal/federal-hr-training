#!/usr/bin/env python3
"""One-off content-authoring pass for civpay_qa.csv (2026-07-04).

The scaffold's 15 answers were raw probe fragments and several citations were
mis-grabbed (NOAC -> a holiday table; SF-52 -> a privacy assessment). This
rewrites each answer as a readable, accurate, citation-grounded answer and
re-points each citation to its actual source of record.

Grounding discipline: answers state well-established federal civilian-pay
process and cite the GOVERNING authority (OPM GPPA, 5 CFR, DoD FMR Vol 8, DCPS
UM). Where a specific numeric/threshold is stated it is the regulation's own
value. Anything the operator wants verified against a page-exact probe is noted
in the row's Keywords with 'verify:'.
"""
from __future__ import annotations
import csv
from pathlib import Path

REVIEWED = "2026-07-04"
OUT = Path(__file__).resolve().parent.parent / "data" / "civpay_qa.csv"

# (Question, Answer, Citation, System, Role, Keywords)
ROWS = [
    (
        "What information must the SF-52/RPA include to start a personnel action?",
        "The SF-52 (paper) or its electronic Request for Personnel Action (RPA) in "
        "DCPDS starts the action. It must identify the employee, the requested "
        "action by Nature of Action Code (NOAC) and legal authority, the requested "
        "effective date, and the position/pay data being changed (pay plan, series, "
        "grade, step, duty station). The request is routed for review and approval "
        "before it is effected as an SF-50.",
        "OPM Guide to Processing Personnel Actions (GPPA), Ch. 4",
        "DCPDS", "HR Specialist",
        "SF-52;RPA;request personnel action;effective date;NOAC",
    ),
    (
        "What is a Nature of Action Code (NOAC) and how do I pick the right one?",
        "A NOAC is the three-digit code that identifies the specific type of "
        "personnel action (for example 100 Career Appointment, 702 Promotion, 893 "
        "Within-Grade Increase). You select it from the OPM GPPA action tables, which "
        "pair each code with its legal authority and required remarks. The NOAC drives "
        "how DCPDS effects the SF-50 and what data flows to pay.",
        "OPM Guide to Processing Personnel Actions (GPPA), Ch. 6-8 (action tables)",
        "OPM GPPA", "HR Specialist",
        "NOAC;nature of action;SF-50;action code;GPPA tables",
    ),
    (
        "Which fields on a personnel action actually drive pay (pay plan, grade, step, effective date, locality)?",
        "The pay-driving fields carried on the SF-50 and passed to DCPS are pay plan, "
        "occupational series, grade, step, the pay-basis and work schedule, the duty "
        "station (which sets the locality pay area), the retirement plan, and the "
        "effective date. A change to any of these on an effected action recomputes "
        "the employee's rate of basic pay and adjusted (locality) pay.",
        "DoD FMR Vol 8, Ch. 3 (basic and locality pay); DCPS User Manual, Master Employee Record fields",
        "FMR Vol 8", "HR Specialist;Payroll",
        "pay plan;grade;step;locality;duty station;effective date;pay-driving fields",
    ),
    (
        "Where are retirement, FEHB, and TSP election fields recorded for pay?",
        "Retirement plan, FEHB enrollment code, and TSP elections are recorded in "
        "DCPDS (from the SF-50 and the employee's benefit elections) and passed to "
        "DCPS, where they become deduction codes on the Master Employee Record. DCPS "
        "then withholds the corresponding retirement, health, and TSP amounts each "
        "pay period.",
        "DoD FMR Vol 8, Ch. 4 (deductions); DCPS User Manual, Employee Data — deductions",
        "FMR Vol 8", "Payroll",
        "retirement;FEHB;TSP;deductions;benefit codes;MER",
    ),
    (
        "How does a personnel action get from DCPDS (HR) to DCPS (pay)?",
        "Once HR effects the action as an SF-50 in DCPDS, the scheduled DCPDS-to-DCPS "
        "personnel interface transmits the effected data to DCPS, which applies it to "
        "the employee's Master Employee Record (MER). HR does not key pay data into "
        "DCPS directly for standard actions — the interface is the handoff line "
        "between the HR system of record and the pay system of record.",
        "DCPS User Manual, Personnel Interface (DCPDS-DCPS handoff)",
        "DCPS", "HR Specialist;Payroll",
        "DCPDS to DCPS;personnel interface;SF-50;MER;handoff",
    ),
    (
        "Who owns the action at each step — HR or Payroll?",
        "HR owns the action from the SF-52/RPA through review, approval, and effecting "
        "the SF-50 in DCPDS. Ownership passes to Payroll when the effected action "
        "reaches DCPS through the personnel interface and updates the MER; from that "
        "point Payroll owns pay computation, certification, and any exception or "
        "correction. The interface is the ownership boundary.",
        "OPM GPPA, Ch. 4 (HR effecting); DoD FMR Vol 8, Ch. 3 (payroll computation)",
        "OPM GPPA", "HR Specialist;Payroll",
        "ownership;HR vs payroll;handoff;responsibility",
    ),
    (
        "When does a personnel action update the DCPS master record and take effect in pay?",
        "DCPS applies the action to the MER when it receives the action over the "
        "personnel interface. Pay reflects the change in the pay period that covers "
        "the SF-50 effective date; if the action reaches DCPS after that pay period "
        "has processed, DCPS computes retroactive pay back to the effective date "
        "rather than changing the effective date.",
        "DCPS User Manual, Master Employee Record update; DoD FMR Vol 8, Ch. 3 (effective dates)",
        "DCPS", "Payroll",
        "effective date;retroactive;master record update;pay period",
    ),
    (
        "How is gross pay calculated after a pay-affecting personnel action?",
        "DCPS computes gross pay from the updated MER: rate of basic pay applied to "
        "the hours/pay basis, plus locality pay and any authorized premiums "
        "(overtime, night, environmental, etc.). Mandatory and voluntary deductions "
        "are then withheld in the required order of precedence to reach net pay.",
        "DoD FMR Vol 8, Ch. 3 (pay computation) and Ch. 4 (deductions)",
        "FMR Vol 8", "Payroll",
        "gross pay;basic pay;locality;premiums;net pay;computation",
    ),
    (
        "In what order are mandatory deductions taken from civilian pay?",
        "When available pay cannot cover all deductions, DCPS applies them in the "
        "order of precedence set by DoD FMR Vol 8, Ch. 4 — retirement first, then "
        "OASDI (Social Security) and Medicare, federal income tax, FEHB, and the "
        "remaining categories in the listed sequence. Lower-precedence deductions are "
        "reduced or not taken when pay is insufficient.",
        "DoD FMR Vol 8, Ch. 4 (order of precedence)",
        "FMR Vol 8", "Payroll",
        "order of precedence;deductions;retirement;OASDI;Medicare;FEHB",
    ),
    (
        "How is pay set on a promotion (two-step / maximum payable rate)?",
        "On a GS promotion, basic pay is set using the two-step rule: the employee's "
        "existing GS rate is increased by two within-grade steps, then set to the "
        "lowest step of the higher grade that at least equals that amount. Where a "
        "higher prior rate applies, the maximum payable rate rule may set a higher "
        "step. Locality/adjusted pay is then applied at the new grade and step.",
        "DoD FMR Vol 8, Ch. 3; 5 CFR 531.214 (promotion pay-setting)",
        "5 CFR", "HR Specialist;Payroll",
        "promotion;two-step rule;maximum payable rate;pay setting",
    ),
    (
        "When does a within-grade increase take effect and how is the waiting period counted?",
        "A within-grade increase (WGI) takes effect on the first day of the first pay "
        "period after the employee completes the required waiting period at an "
        "acceptable level of competence: 52 calendar weeks for steps 2-4, 104 weeks "
        "for steps 5-7, and 156 weeks for steps 8-10. Certain nonpay status and "
        "breaks in service extend the waiting period.",
        "5 CFR 531 Subpart D (531.405 effective date; 531.406 waiting periods)",
        "5 CFR", "HR Specialist;Payroll",
        "within-grade increase;WGI;waiting period;52 104 156 weeks;effective date",
    ),
    (
        "How does an HR specialist confirm an action effected — DCPDS, HR Link, or MyBiz?",
        "HR confirms the effected SF-50 in DCPDS (the system of record) and in HR Link "
        "reporting, which reads DCPDS. MyBiz is employee self-service only — the "
        "employee can view their own effected SF-50 and data there, but it is not the "
        "HR verification tool. Confirm the SF-50 posted in DCPDS before treating the "
        "action as complete.",
        "DCPDS / HR Link user documentation; MyBiz self-service scope",
        "DCPDS", "HR Specialist",
        "confirm effected;DCPDS;HR Link;MyBiz;SF-50 verification",
    ),
    (
        "Who certifies time and attendance and what does DCPS record on certification?",
        "The timekeeper records reported time; a designated certifier reviews and "
        "certifies it as correct. DCPS records the certified hours by type (regular, "
        "leave, overtime, premium) against the MER and uses them to compute pay for "
        "the pay period. Uncertified or corrected time is handled through the T&A "
        "correction process before pay is finalized.",
        "DCPS User Manual, Time and Attendance — timekeeper/certifier",
        "DCPS", "Timekeeper;Payroll",
        "time and attendance;certification;timekeeper;certifier;hours",
    ),
    (
        "Pay is wrong after a personnel action — how is it corrected (manual pay adjustment)?",
        "When DCPS cannot automatically compute the correction (for example an "
        "unusual retroactive change or an amount the automated process does not "
        "handle), Payroll uses the manual Pay Adjustment process to enter the "
        "correcting amount. The adjustment posts to the MER and appears on the pay "
        "adjustment reports; the underlying personnel data should also be corrected so "
        "future pay computes correctly.",
        "DCPS User Manual, Pay — Automated/Manual Pay Adjustments",
        "DCPS", "Payroll",
        "pay correction;manual pay adjustment;retroactive;pay error",
    ),
    (
        "How are civilian pay underpayments and debts handled?",
        "Underpayments are paid to the employee for the amount owed. Overpayments "
        "create a debt that is collected under due-process rules — the employee is "
        "notified and given the chance to review, request waiver, or arrange "
        "repayment before collection, with statutory limits on how much may be "
        "withheld per pay period. DCPS records and schedules the collection.",
        "DoD FMR Vol 8, Ch. 9 (over/underpayments and debt collection)",
        "FMR Vol 8", "Payroll",
        "underpayment;overpayment;debt;waiver;collection;due process",
    ),
]

HEADER = ["Question", "Answer", "Citation", "System", "Role", "Keywords", "LastReviewed"]

def main() -> int:
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        w.writerow(HEADER)
        for q, a, cite, system, role, kw in ROWS:
            w.writerow([q, a, cite, system, role, kw, REVIEWED])
    print(f"wrote {len(ROWS)} curated rows -> {OUT}")
    # integrity guard: no row without a citation
    missing = [r[0] for r in ROWS if not r[2].strip()]
    assert not missing, f"rows missing citation: {missing}"
    print("integrity: every row carries a citation")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
