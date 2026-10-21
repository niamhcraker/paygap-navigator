# Demo Day HTML — browser acceptance and external review gate

**Status: PARTIALLY VERIFIED — owner confirmed function in Chrome and identified two remaining chart-layout issues at the prior commit. These plus an expanded upload introduction have been implemented; new visual retest PENDING. GitHub Pages must remain disabled.**

Branch: `demo-day-html`. Use a local static server from repository root: `python3 -m http.server 8000 --directory docs`, then visit `http://localhost:8000/`. This deliberately exercises the actual static HTML and relative CSV download URL.

Dataset: `docs/sample_remuneration.csv`; synthetic records only. Do not use identifiable staff or sensitive workplace records.

For every row, record **actual result**, **PASS/FAIL**, **confusion/problem**, **fix**, and **retest outcome**.

| ID | Manual test | Expected | Actual | Status | Issue / fix / retest |
|---|---|---|---|---|---|
| WEB-01 | Open local URL in private window | Upload & Validate screen, no data/results yet | Pending | NOT RUN | |
| WEB-02 | Select Download demo dataset | Downloads valid 1,200-row CSV from same origin | Owner used the downloaded demo CSV successfully for upload | PASS — owner-reported | Post-polish download link unchanged |
| WEB-03 | Expand required columns | All 11 exact column names visible | Pending | NOT RUN | |
| WEB-04 | Upload demo dataset | Validation passes, FY 2026, 1,200 employees, 60 per 5% cohort | Owner confirms Upload & Validate works with supplied dataset | PASS — owner-reported | |
| WEB-05 | Open Overview | 26.32:1 ratio; distribution and outlier caution; **no** living-wage KPI | Owner confirms calculations and visuals render; ratio 26.32:1 | PASS — owner-reported for reported elements | All other detailed accessibility conditions not separately verified |
| WEB-06 | Explore Diagnose job and unit tables | Annual remuneration only; no monthly net/benchmark fields | Owner confirms Diagnose tables/charts and calculations render | PASS — owner-reported for functions | Polish finding: job-level median chart too small; compact SVG implemented, VISUAL RETEST PENDING |
| WEB-07 | Explore baseline, sliders and reset | Current vs simulated ratio, payroll impact and before/after curve; reset returns baseline | Owner: baseline 26.32:1; +20% bottom and −10% top ≈22.91:1; payroll −R3.44m; reset correct | PASS — owner-reported | Slider neutral position was ambiguous; labelled 0% baseline marker added, VISUAL RETEST PENDING |
| WEB-08 | Open Living Wage | Distinct styling; full-time default; n=1,039, below=371, 35.7%, median=R5,620, monthly=R2,121,780, annual=R25,461,360 | Owner confirms all stated figures and default | PASS — owner-reported for functions | Separation too subtle; scoped muted-plum theme added. Shortened Median shortfall and responsive five-card layout; VISUAL RETEST PENDING |
| WEB-09 | Living Wage population toggle | All employment types selects 1,200, shows comparability caution; returning restores 1,039 | Owner confirms all types n=1,200 and comparability caution; full-time default n=1,039 | PASS — owner-reported for reported switching | |
| WEB-10 | Adjust benchmark | Counts, shortfalls, distribution and breakdowns update; Section 30B KPI unchanged | Owner confirms benchmark adjustment updates only Living Wage; Overview ratio remains 26.32:1 | PASS — owner-reported | |
| WEB-11 | Upload malformed/duplicate/negative CSV | Block with readable errors; no result screens available | Pending | NOT RUN | |
| WEB-12 | Replace upload / reload page | Previous data cleared; CSV not intentionally saved; navigation safely returns to upload | Pending | NOT RUN | |
| WEB-13 | Check privacy and external requests | CSV bytes stay in browser; no outbound CSV request or analytics payload with employee rows; document hosting requests | Pending | NOT RUN | |
| WEB-14 | Projector 1920×1080 and laptop 1366×768, mobile width | Main text, axes, units, controls legible; no clipping/overlap | Pending | NOT RUN | |
| WEB-15 | Tab/keyboard navigation, contrast and zoom | Controls usable, focus visible; charts labelled beyond colour | Pending | NOT RUN | |
| WEB-16 | Two or three observers unfamiliar with app | Observe without step-by-step guidance; document confusion, fix, retest | Pending | NOT RUN | |

## Owner's 21 October 2026 Chrome acceptance and targeted polish

The owner tested the local Chrome build with the supplied downloadable demo CSV and reported these successful functional checks: upload/validation; Overview and Diagnose rendering; baseline 26.32:1; +20% bottom guaranteed pay / −10% top variable pay ≈22.91:1 and −R3.44m annual remuneration change; slider reset; Living Wage full-time (n=1,039; below 371; 35.7%; median monthly shortfall R5,620; monthly total R2,121,780; annualised R25,461,360); all-employment-types 1,200 and caution; benchmark isolation from Section 30B.

The owner reported five presentation findings only. Changes committed on the existing `demo-day-html` branch:

| Finding | Implemented presentation-only fix | Actual post-fix observation | Retest status |
|---|---|---|---|
| Diagnose bar chart undersized | Compact aspect ratio with greater vertical spacing for the job-level median chart only | Direct JS check confirms compact SVG uses 650-unit width; real browser sizing not yet observed | PENDING owner Chrome retest |
| Explore top-tail 0% looks offset | Visible **0% · baseline** marker positioned at 50/70 = 71.43% of slider span, without changing slider range or values | Markup verified; visual alignment not observed | PENDING owner Chrome retest |
| Living Wage lacks distinct palette | Scoped muted plum for heading, benchmark control, KPIs, chart bars and tables; distinct active navigation state | Rendered code/markup verified; on-screen contrast not observed | PENDING owner Chrome retest |
| Living Wage KPI wraps/misaligned; fifth card alone | Changed heading to **Median shortfall**, subtext to **Per month among employees below benchmark**; responsive 5/3/2/1 column strategy | Source verified; layout at projected/browser breakpoints not observed | PENDING owner Chrome retest |
| Upload text implies Mac-only | Changed to **choose a file from your device** | Source wording verified | PENDING owner screen retest |

**Regression evidence:** 32 direct checks executed against the production JavaScript in `docs/index.html` and the committed 1,200-row CSV — **32 passed, 0 failed**. No numerical logic was changed. The runnable Node `node --test tests/test_prototype.mjs` command was not independently run in the owner's local checkout in this turn.

**Still not verified:** WEB-01/03/11–16 in detail, independent observers, and all five post-fix visual checks. Passing production JS/static checks does not establish browser acceptance or projector legibility.

## 21 October 2026 — second visual retest and new presentation fixes

**Owner-observed Chrome result for prior commit `893db1d8706ce42eeec76aac445cf96ab22a11b9`:** calculation logic remained correct. The job-level median chart still underused its card despite previous compact-height changes, and the shared pay-position curve's rotated **Annual total remuneration (ZAR)** title overlapped currency tick labels in both Overview and Explore. These are visual observations from the owner, not assistant browser verification.

**Fixes in `docs/index.html` (presentation only):**

- Job-level chart: increased usable plot share via a compact width of 560 SVG units and a smaller left gutter; thicker 32-unit bars and larger value/row labels; retained row spacing. The business-unit chart stays on the original 900-unit layout and 23-unit bars.
- Shared `payCurve()`: moved the plot origin from x=78 to x=185, tick labels to x=l−14, and the rotated axis title to x=28; this affects both Overview and Explore without shrinking labels.
- Upload: replaced the short introduction with **PayGap Navigator — From disclosure to understanding and action**, added a compact four-stage overview and a decision-support boundary statement; kept upload and demo dataset download together immediately below.

**Automated evidence:** 34 direct assertions against production JavaScript extracted from the branch HTML and the supplied CSV **passed, 0 failed**. This includes existing baseline, simulation, Living Wage reference figures, CSV validation, rendering of all four screens and specific SVG/landing markup. The previously existing calculation routines and simulator are unchanged. These structural checks do **not** establish visual non-overlap in Chrome.

**New post-fix Chrome visual acceptance remains PENDING** for: the job-level chart's real available plot weight versus the composition panel; tick/title separation on both pay-position curves; upload-page readability and immediate visibility of both primary actions on laptop/projector/mobile. Retest these before release. GitHub Pages remains disabled.

**Release gate:** No test should be marked PASS without actual observation. Resolve any blocking issue, rerun affected checks, document tested Git commit, then request approval to enable GitHub Pages. `main` and Streamlit URL remain untouched.
