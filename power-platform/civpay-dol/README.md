# CIVPAY Division of Labor

A consolidated who-does-what map for the DoD/DON civilian **personnel-action-to-pay**
lifecycle, with its own searchable SharePoint List. Companion to the CIVPAY Q&A
package (`../civpay-qa/`) — the Q&A answers *how*; this map answers *who, in which
system, under whose authority*.

**UNOFFICIAL working aid.** Verify against the cited source of record before acting.

## Authority precedence (the load-bearing rule)

A lower tier **implements but never overrides** a higher one:

| Tier | Level | Sources |
|------|-------|---------|
| **T1** | Federal (OPM) | 5 U.S.C., 5 CFR, OPM GPPA |
| **T2** | DoD / overseas | DoD FMR Vol 8, DoDI 1400.25, DSSR |
| **T3** | Systems | DCPDS UM, DCPS UM / Interface Spec |
| **T4** | Component (DON) | DON/OCHR instructions, DON Civilian HR Roles & Responsibilities |

Every row separates the **Governing Authority** (the rule's source, T1–T2) from the
**Local Procedure / System** (how DON/DCPDS/DCPS executes it, T3–T4). A DON
instruction or a DCPS manual is cited as *execution*, never as the authority.

## Files

| Path | What |
|------|------|
| `sharepoint/list-schema.json` | List columns + views (By Phase / By Role / By Authority Tier) |
| `data/civpay_dol.csv` | 19 lifecycle steps: role, system, governing authority, local procedure, reference link |
| `sharepoint/dol-search-webpart.html` | Vanilla-JS searchable view; reference links clickable |

## Provisioning

1. Create a List named **`CIVPAY Division of Labor`** with the columns in
   `list-schema.json` (Phase, ResponsibleRole, System, GoverningAuthority,
   LocalProcedure, AuthorityTier, ReferenceLink [Hyperlink], Notes).
2. Import `data/civpay_dol.csv`.
3. Embed `sharepoint/dol-search-webpart.html` on a page (Embed / Script Editor).
4. Use the **By Authority Tier** view to see, at a glance, which steps trace to
   OPM vs DoD/DSSR vs the systems vs DON.

## Grounding

DON Civilian HR Roles & Responsibilities; DON OCHR RPA Handling Procedures;
DCPDS UM; DCPS UM (incl. reports **P6634** Pre-Pay Audit, **P6698** Gross Pay
Reconciliation, Sec F Ch 5 Pay Certification); DoD FMR Vol 8; OPM GPPA; DSSR;
DoDI 1400.25. Reference links point to the public governing authority where one
exists; internal DCPS/DCPDS reports are cited by manual section + report ID.
