# Demo Day HTML — browser acceptance and external review gate

**Status: NOT RUN. Do not enable GitHub Pages until these checks have been performed and recorded.**

Branch: `demo-day-html`. Use a local static server from repository root: `python3 -m http.server 8000 --directory docs`, then visit `http://localhost:8000/`. This deliberately exercises the actual static HTML and relative CSV download URL.

Dataset: `docs/sample_remuneration.csv`; synthetic records only. Do not use identifiable staff or sensitive workplace records.

For every row, record **actual result**, **PASS/FAIL**, **confusion/problem**, **fix**, and **retest outcome**.

| ID | Manual test | Expected | Actual | Status | Issue / fix / retest |
|---|---|---|---|---|---|
| WEB-01 | Open local URL in private window | Upload & Validate screen, no data/results yet | Pending | NOT RUN | |
| WEB-02 | Select Download demo dataset | Downloads valid 1,200-row CSV from same origin | Pending | NOT RUN | |
| WEB-03 | Expand required columns | All 11 exact column names visible | Pending | NOT RUN | |
| WEB-04 | Upload demo dataset | Validation passes, FY 2026, 1,200 employees, 60 per 5% cohort | Pending | NOT RUN | |
| WEB-05 | Open Overview | 26.32:1 ratio; distribution and outlier caution; **no** living-wage KPI | Pending | NOT RUN | |
| WEB-06 | Explore Diagnose job and unit tables | Annual remuneration only; no monthly net/benchmark fields | Pending | NOT RUN | |
| WEB-07 | Explore baseline, sliders and reset | Current vs simulated ratio, payroll impact and before/after curve; reset returns baseline | Pending | NOT RUN | |
| WEB-08 | Open Living Wage | Distinct styling; full-time default; n=1,039, below=371, 35.7%, median=R5,620, monthly=R2,121,780, annual=R25,461,360 | Pending | NOT RUN | |
| WEB-09 | Living Wage population toggle | All employment types selects 1,200, shows comparability caution; returning restores 1,039 | Pending | NOT RUN | |
| WEB-10 | Adjust benchmark | Counts, shortfalls, distribution and breakdowns update; Section 30B KPI unchanged | Pending | NOT RUN | |
| WEB-11 | Upload malformed/duplicate/negative CSV | Block with readable errors; no result screens available | Pending | NOT RUN | |
| WEB-12 | Replace upload / reload page | Previous data cleared; CSV not intentionally saved; navigation safely returns to upload | Pending | NOT RUN | |
| WEB-13 | Check privacy and external requests | CSV bytes stay in browser; no outbound CSV request or analytics payload with employee rows; document hosting requests | Pending | NOT RUN | |
| WEB-14 | Projector 1920×1080 and laptop 1366×768, mobile width | Main text, axes, units, controls legible; no clipping/overlap | Pending | NOT RUN | |
| WEB-15 | Tab/keyboard navigation, contrast and zoom | Controls usable, focus visible; charts labelled beyond colour | Pending | NOT RUN | |
| WEB-16 | Two or three observers unfamiliar with app | Observe without step-by-step guidance; document confusion, fix, retest | Pending | NOT RUN | |

**Release gate:** No test should be marked PASS without actual observation. Resolve any blocking issue, rerun affected checks, document tested Git commit, then request approval to enable GitHub Pages. `main` and Streamlit URL remain untouched.
