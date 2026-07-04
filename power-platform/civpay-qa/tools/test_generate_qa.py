"""Unit test for the authoring generator's pure formatting (no network)."""
from generate_qa_from_probe import to_row, fmt_citation


def test_to_row_builds_citation_and_fields():
    hit = {
        "score": 0.71,
        "payload": {
            "filename": "DCPS_UM_26_1_DCPS_User_Manual_SECTION_D_Employee_DataOnline_Menus_Time_and_Attendance_Timekeeper_p529-531.pdf",
            "text": "After certifying time and attendance as correct, the reviewing certifier's "
                    "SSN, Date, and Time of Certification is recorded in the system. The certifier "
                    "may accept or reject reported time.",
        },
    }
    row = to_row(q="Who certifies T&A?", hit=hit, system="DCPS", roles=["Timekeeper", "Payroll"])
    assert row["Question"] == "Who certifies T&A?"
    assert row["Citation"]                       # non-empty
    assert "Timekeeper" in row["Citation"] or "SECTION D" in row["Citation"]
    assert row["Answer"]                          # distilled from passage
    assert row["System"] == "DCPS"
    assert row["Role"] == "Timekeeper;Payroll"
    assert row["LastReviewed"] == "2026-06-05"


def test_fmt_citation_fmr():
    cite = fmt_citation("FMR_Vol08_08_03.pdf")
    assert cite.startswith("DoD FMR Vol 8 Ch 03")


def test_to_row_requires_no_network():
    # to_row must be pure — passing a minimal hit should not raise.
    row = to_row(q="x", hit={"score": 0, "payload": {"filename": "FMR_Vol08_08_04.pdf", "text": "One sentence. Two sentence."}},
                 system="FMR Vol 8", roles=["Payroll"])
    assert "Mandatory" not in row["Answer"]       # no invented content
    assert row["Citation"].startswith("DoD FMR Vol 8 Ch 04")
