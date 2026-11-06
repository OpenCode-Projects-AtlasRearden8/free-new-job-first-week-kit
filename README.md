# First-Week-of-Work Freebie Kit

Printable and fillable one-pagers for your first week at a new job. Plain English, warm, ADHD-friendly — short steps, zero "should." Made by **Asdale Dynamics, LLC**.

Local-first by design: no accounts, no forms that phone home, no data collection. Everything downloads, opens in a browser, prints on letter or A4 paper, and stays on your side of the desk.

## What's inside

| # | Printable | What it does |
|---|---|---|
| 1 | **The First Week, Handled** | Day-by-day checklist (before day 1 → day 5), ★ marks true must-dos |
| 2 | **Papers: Keep or Shred** | Sort every week-one paper in 10 minutes + a shredding session and folder system |
| 3 | **W-4 & Direct Deposit Sanity Checklist** | Fill the two forms where your money goes all year, right the first time |
| 4 | **Benefits Deadline Mini-Tracker** | One page, one HR email, every enrollment deadline caged and dated |
| 5 | **Badge Photo Tips** | The 60-second recipe for an ID photo you won't resent for years |
| 6 | **First 90 Days: Reflections** | Three five-minute check-ins (day 30/60/90) — land, traction, steer |

Two ways to read everything:

- **Markdown guides** in [`guides/`](guides/) — the deep-dive versions with extra context
- **PDF-ready HTML** in [`print/`](print/) — self-contained, open in any browser, hit *Print / Save as PDF*

## How to use

- **Print:** open [`print/index.html`](print/index.html), click a card, hit the *Print / Save as PDF* button (or Ctrl/Cmd+P). Print blank and handwrite, or
- **Fill on screen first:** the same pages are fillable — click the checkboxes and type into the dotted lines in your browser, *then* print. Filled marks and text come along on paper.
- **Suggested order:** first-week checklist now; papers/w4/direct-deposit during week one; benefits tracker the moment HR mentions enrollment; badge photo when photo day is announced; 90-day reflections printed ahead of day 30.

Each HTML file is fully self-contained (no external fonts, scripts beyond a local print button, or CDNs), so it works offline and prints identically on letter or A4.

## Verify it all works

Requires Python 3.8+, no dependencies:

```sh
python3 verify.py
```

This checks: every expected file exists, all HTML parses and has proper structure (lang, DOCTYPE, encoding, self-containedness), guides and printables stay in sync by count, the LICENSE copyright line is exact, and no file contains accidental secrets or API keys.

## File map

```
print/index.html                     → print index (start here)
print/01…06-*.html                   → six fillable print sheets
guides/01…06-*.md                    → companion markdown guides
LICENSE                              → MIT, © 2026 Asdale Dynamics, LLC
verify.py                            → local verification script
```

## License & credits

All content © 2026 Asdale Dynamics, LLC, MIT-licensed — see [LICENSE](LICENSE). Free to print, share, and adapt; attribution appreciated but not required.

These are life-admin tools, not legal, tax, or financial advice. Part of the world of [Dylan Asdale](https://dylanasdale.github.io) — author of *The Massive AI Manual*, explaining AI "like a friend would."

Distinct sibling kits: `free-resume-pack` (job hunting) and `workplace-benefits-decoded-guide` (benefit concepts). This one is for the week you actually show up.
