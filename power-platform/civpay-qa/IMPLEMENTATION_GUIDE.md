# CIVPAY Q&A — Implementation Guide

A searchable, citation-grounded CIVPAY answer set that runs entirely on the work
network with local Office-365 tools. No Tower/Python runtime dependency: Tower is
used **only** to author the answers (offline); everything the end user touches is
SharePoint + a vanilla-JS web part + one Power Automate flow.

**UNOFFICIAL.** This is a working aid, not an official OPM/DoD publication. Every
answer cites a source of record; verify against that source before acting.

## What's in this folder

| Path | What it is | Where it runs |
|------|------------|---------------|
| `sharepoint/list-schema.json` | Column + view definition for the "CIVPAY Q&A" List | Provisioning reference |
| `data/civpay_qa.csv` | The answers, one row per Q&A, every row citation-carrying | Imported into the List |
| `sharepoint/search-webpart.html` | Vanilla-JS search/filter UI (no dependencies) | Embedded on a SharePoint page |
| `flows/civpay-upkeep-flow.json` | Monthly stale-review guard (emails a digest) | Power Automate |
| `tools/generate_qa_from_probe.py` | Authoring generator (emits the CSV) | **Tower/offline only** |

## One-time setup (≈20 minutes, no admin rights beyond list creation)

### 1. Create the List
On the target SharePoint site: **New → List → Blank list**, name it exactly
**`CIVPAY Q&A`**. Then add the columns from `sharepoint/list-schema.json`:

- Rename the built-in **Title** column's display to **Question** (List settings → Title → Column name).
- Add: **Answer** (Multiple lines of text, plain), **Citation** (Single line, required),
  **System** (Choice: DCPS, DCPDS, FMR Vol 8, 5 CFR, OPM GPPA),
  **Role** (Choice, allow multiple: HR Specialist, Payroll, CSR, Timekeeper, Employee),
  **Keywords** (Single line), **LastReviewed** (Date only, required).

Mark **Citation** and **LastReviewed** as required — the citation-grounded rule is
enforced at the column level so no answer can ship without a source and a review date.

### 2. Import the answers
List → **Integrate → Import from Excel**, or open the CSV in Excel and
**Quick Edit → paste**. Map columns Question→Title, Answer, Citation, System, Role,
Keywords, LastReviewed.

Two content files import into the **same** List:
- `data/civpay_qa.csv` — SOP#1, domestic personnel-action-to-pay (15 answers).
- `data/civpay_qa_overseas.csv` — SOP#2, overseas / special-category: LQA, TQSA,
  post allowance (COLA), post differential, danger pay, foreign-national pay,
  special-category authority, taxability, reconciliation (12 answers).

The `System` filter (DCPS, DCPDS, FMR Vol 8, 5 CFR, OPM GPPA, DSSR, DoDI 1400.25)
and free-text search separate domestic vs overseas — no separate list or web part.

### 3. Add the search web part
Edit a SharePoint page → add an **Embed** web part (modern pages) or a **Script
Editor / Content Editor** web part (classic) → paste the full contents of
`sharepoint/search-webpart.html`. It auto-resolves the site URL from the page and
reads the List over REST with the viewer's own permissions. If your list title
differs, change `LIST_TITLE` at the top of the script.

> Modern pages: if your tenant blocks the **Embed** web part for arbitrary HTML,
> use the **SPFx "Modern Script Editor"** community web part if approved, or host
> the HTML in a Site Assets library and point a **File viewer** at it. The script
> itself needs no changes.

### 4. Install the upkeep flow
Power Automate → **Import** (or rebuild from `flows/civpay-upkeep-flow.json`). Set
the four parameters: `SiteUrl`, `ListTitle` (default `CIVPAY Q&A`),
`ReviewWindowDays` (default 180), `OwnerEmail`. It runs monthly, finds rows whose
`LastReviewed` is past the window, and emails the owner a digest to re-verify. It
is read-only — it never edits answers.

## Updating content (the authoring loop)

Content is **not** hand-edited in SharePoint. To add/revise answers:

1. On Tower, run `tools/generate_qa_from_probe.py` against the seed questions
   (`data/seed-questions.yaml`) — it probes the grounded corpus and emits an
   updated `data/civpay_qa.csv`, every row citation-carrying.
2. Review the CSV. Any row without a Citation is dropped by design.
3. Re-import to the List (step 2), or update changed rows via Quick Edit and bump
   their `LastReviewed`.

This keeps a single source of truth (the generator + corpus) and prevents ungrounded
answers from creeping in through manual edits.

## Design guarantees

- **No ungrounded answers.** Citation is a required column; the generator drops
  rows without one; the web part always renders the Source line.
- **No runtime dependency on Tower.** End users hit only SharePoint + the flow.
  Tower is authoring-time only, offline.
- **Local tools only.** Vanilla JS, no CDN/npm/external calls — safe on the work
  network.
- **Stale content surfaces itself.** The monthly flow flags answers past their
  review window instead of letting citations silently rot after regulation updates.
