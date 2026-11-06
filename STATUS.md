# STATUS.md

Last updated: 2026-11-06

## What was built

**First-Week-of-Work Freebie Kit** — a printable and fillable pack of life-admin one-pagers for a person starting a new job. Six topics, each shipped two ways: a deep-dive markdown guide (`guides/`) and a self-contained, PDF-ready, fillable HTML sheet (`print/`). Distinct from the sibling kits `free-resume-pack` (job hunting) and `workplace-benefits-decoded-guide` (benefit concepts).

Printables:

1. **First Week Checklist** (`01`) — day-by-day (before day 1 → day 5), ★ marks true must-dos, "only three things" fallback
2. **Papers: Keep or Shred** (`02`) — keep/shred table, 10-minute shredding session, filing-system picker
3. **W-4 & Direct Deposit Sanity Checklist** (`03`) — form-by-form sanity checks, common mistakes, first-paycheck day check
4. **Benefits Deadline Mini-Tracker** (`04`) — one HR email to get dates in writing + full deadline table + finish line
5. **Badge Photo Tips** (`05`) — 60-second photo recipe, on-site vs. self-submitted branches
6. **First 90 Days Reflections** (`06`) — day-30/60/90 check-in prompts on one page, quiet-first path when something's off

Supporting files:

- `print/index.html` — linked card index with print instructions
- `README.md` — what it is, how to use, file map; credits Asdale Dynamics, LLC
- `LICENSE` — MIT, copyright line exactly `Copyright (c) 2026 Asdale Dynamics, LLC`
- `verify.py` — local verification script

Properties honored: fully local (no external requests, works offline, no data collection anywhere), letter/A4 print CSS, fillable on-screen before printing, ADHD-friendly tone, plain commit, no secrets or personal data.

## How to run / use

- Open `print/index.html` in any browser → pick a sheet → fill checkboxes/text lines → hit **Print / Save as PDF** (or Ctrl/Cmd+P). Or print blank and handwrite.
- Read the surrounding markdown guides in `guides/` for the deeper walk-throughs.
- No dependencies, no build, no server, no network needed.

## Verification

Run `python3 verify.py` (Python 3.8+, zero dependencies). **Result: OK — all checks pass.**

It confirms:

- All 16 expected files exist (6 guides, 6 printables, index, README, LICENSE, verify.py)
- Every HTML file: balanced tags (HTMLParser structural probe), DOCTYPE, `lang="en"`, UTF-8 charset, `<title>`, no external `src/href` references (self-containedness), fillable fields present on all six print sheets
- Guides and printables stay in sync (6 each)
- LICENSE contains the exact string `Copyright (c) 2026 Asdale Dynamics, LLC` and is MIT
- README and every print sheet credit Asdale Dynamics, LLC
- No obvious API keys, tokens, SSN-format strings, or bare personal emails in any file

Note: the first verifier run reported seven "unterminated <title>" failures — a bug in the probe itself (it never cleared its in-title flag), not in the HTML. Fixed in `verify.py`; clean second run.

## Known gaps

- Print pagination is tuned for letter/A4 margins via `@page`, but browsers differ in checkbox rendering; not pixel-identical across all browsers/printers.
- Filable values typed in the browser persist only until you navigate/close the page; forms don't auto-save (deliberate — no data stays anywhere). The print button is the export path.
- The W-4 guidance is intentionally direction-level ("use the IRS estimator / ask a pro" for status edge cases) — never tax advice.
- Benefit plan types only; employer-specific plan names, costs, and rules must come from each employer's documents.
- No dark-mode styling (docs end up on paper); not responsive beyond a readable mobile width.
- verify.py's email/SSN pattern checks are heuristic — reviewed by hand too, not a guarantee.
