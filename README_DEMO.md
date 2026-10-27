# PayGap Navigator — HTML Demo Day build

**Work in progress on `demo-day-html`. GitHub Pages is intentionally not published until local verification and browser acceptance pass.**

## Run locally

No backend or package installation is needed for the application. From the repository root:

```bash
python3 -m http.server 8000 --directory docs
```

Open http://localhost:8000/, click **Download demo dataset**, and upload it back into the app. The provided sample is synthetic.

## Test production code

With Node 22 or a compatible modern release:

```bash
node --test tests/test_prototype.mjs
```

The tests extract and execute the browser application's own `parseCSV`, `validate`, `analyse`, `living`, and `scenario` functions from `docs/index.html`, using `docs/sample_remuneration.csv` as a reference input. Complete the independent hands-on protocol in `tests/DEMO_ACCEPTANCE.md` before publication.

## CSV structure

Exactly these 11 headings, one reporting year, full ZAR amounts:

`Employee_ID,Financial_Year,Job_Level,Business_Unit,Employment_Type,Annual_Guaranteed_Pay_ZAR,Employer_Benefits_ZAR,STI_ZAR,LTI_Share_Awards_ZAR,Annual_Total_Remuneration_ZAR,Monthly_Net_Earnings_ZAR`

Upload one organisation's appropriately de-identified CSV. `Employee_ID` must be a unique pseudonymous technical identifier; do not include names, identity numbers, banking details or actual confidential payroll information. The component totals must reconcile to annual total remuneration within the displayed tolerance. This does not import arbitrary HR-system exports.

## Calculation interpretation

**Section 30B-relevant lens:** The vertical ratio uses the aggregate annual total remuneration of the top 5% divided by that of the bottom 5% of employees. The prototype ranks observations by annual total remuneration and rounds cohort sizes to whole employees; this is documented as a prototype convention rather than independent legal guidance. Descriptive statistics, percentile positions, grouped breakdowns and outlier flags are not fairness determinations. A lower simulated ratio is not automatically fairer. Simulation applies adjustments to *original* tail members, reranks afterwards, and shows mathematical annual remuneration impact; not a policy recommendation.

**Living Wage:** A separate analysis uses monthly net earnings, not the statutory Section 30B remuneration measure. The default population is Permanent full-time. The 2026 Living Wage South Africa Network reference is **R20,000 net/month** for a 40-hour work week; it is voluntary and not the statutory minimum wage. Source: [Living Wage South Africa Network](https://www.linkedin.com/company/living-wage-south-africa-network); corroborated by [June 2026 reporting](https://www.businesslink.co.za/the-latest-living-wage-figure-announced-and-why-sa-should-embrace-it/business/). Including all employment types adds part-time employees and learners without hours adjustment, so its comparisons require caution. The illustrative annualisation of monthly net shortfall is **not** a gross-payroll-cost estimate.

## Privacy and data flow

This version is self-contained, with local JavaScript CSV parsing in the user's browser tab; no back-end upload handler, app database, tracking code or external JavaScript library is included. The app does not intentionally persist CSV contents or transmit them to a remote API. Static HTML/CSV files are served by the hosting provider; its ordinary request logs, privacy practices and browser behaviour must be reviewed before representing the service as appropriate for sensitive organisational data. De-identification must be assessed carefully because combinations of job level/unit/rare values can still be identifying. Only synthetic or appropriately de-identified, authorised data is suitable for this demo.

## Deployment strategy

Existing `main` branch and [Streamlit demo](https://paygap-navigator.streamlit.app/) remain unchanged. Once **all local and manual acceptance checks are complete**, enable GitHub Pages from the **`demo-day-html`** branch's **`/docs`** folder; do not merge. Anticipated Pages URL: https://niamhcraker.github.io/paygap-navigator/ (not active until separately verified). Record published SHA and test in clean browser. Application must remain available through 13 November 2026 for assignment review.

## Post-Demo Day refinement

Following Demo Day feedback, Explore now makes **cohort turnover after re-ranking** explicit. Scenario adjustments still apply to the original baseline tail cohorts, after which the full workforce is re-ranked. The simulated bottom 5% may therefore contain different employees from the baseline bottom 5%.

The application also reports an **internal remuneration Gini coefficient** calculated from the full uploaded annual total-remuneration distribution. It is a complementary descriptive inequality measure, not a fairness judgement and not a substitute for the Section 30B-relevant top/bottom 5% ratio.

Ratios are displayed to two decimal places as a presentation convention. Calculations retain full internal precision; the app does not represent two-decimal display precision as a statutory Section 30B requirement.

