# Demo Day HTML build — implementation and verification log

**Date:** 20 October 2026  
**Branch:** `demo-day-html`  
**Status:** Production logic and static render checks passed; **browser acceptance pending; GitHub Pages NOT enabled**. This is not yet an externally released build.

## Scope implemented

- Original self-contained HTML/JavaScript preserved as the basis of the new `docs/index.html`.
- Fourth navigation item **Living Wage**, separate from annual total remuneration analysis.
- Living Wage filters default to **Permanent full-time**; an **All employment types** option shows an explicit comparability caution.
- Living Wage displays selected population, below-benchmark count/share, median monthly shortfall among below-benchmark employees, total monthly and annualised shortfalls, monthly net earnings distribution, and job-level/business-unit breakdowns.
- 2026 Living Wage South Africa Network R20,000 net/month source and 40-hour comparability context shown.
- Living Wage references removed from Overview KPI row, Diagnose tables and Explore simulator, which remain about Section 30B-relevant annual total remuneration.
- Download demo dataset action and an accessible list of required CSV columns provided on the upload screen.
- Original 1,200-row synthetic CSV supplied as `docs/sample_remuneration.csv`; **no stand-in sample substituted**.
- Privacy, descriptive fairness/outlier cautions and deployment/hosted data-flow limitations documented.
- Pure Node automated test suite and manual browser acceptance checklist added.

## Test evidence performed

**29 direct production-JavaScript calculations/structure assertions: 29 PASS, 0 FAIL.** These were run against the actual `docs/index.html` production functions fetched from the branch and the supplied 1,200-row CSV. They tested parser syntax, schema/rows, numerical validation failures, ratio, Living Wage counts/shortfalls, zero-gap behaviour, scenario baseline/changed result and key structural isolation.

**Additional direct rendering smoke:** **4/4 views rendered** via production JS functions (Overview, Diagnose, Explore, Living Wage). Full-time and all-employment-types Living Wage content rendered; all-types caution confirmed. This is **not** a replacement for an interactive browser acceptance check.

### Supplied CSV reference checks (production calculation functions)

| Value | Expected | Observed | Outcome |
|---|---|---|---|
| Input records | 1,200 | 1,200 | PASS |
| 5% cohort members, each tail | 60 | 60 | PASS |
| Annual remuneration vertical ratio | ~26.32:1 | 26.318409809088365:1 | PASS |
| Living Wage full-time population | 1,039 | 1,039 | PASS |
| Below R20,000 net/month | 371 | 371 | PASS |
| Below as share | 35.7% | 35.7074109721% | PASS |
| Median monthly shortfall | R5,620 | R5,620 | PASS |
| Total monthly shortfall | R2,121,780 | R2,121,780 | PASS |
| Annualised shortfall | R25,461,360 | R25,461,360 | PASS |

**Runnable automated test file:** `tests/test_prototype.mjs`, which extracts production JS from the actual HTML (not duplicate formulas). The Node test command `node --test tests/test_prototype.mjs` has **NOT** yet been independently run with local repository files; its result should not be conflated with the 29 direct tests.

## Outstanding acceptance

- The actual local browser interaction tests `tests/DEMO_ACCEPTANCE.md` are **NOT RUN**. No successful browser click, upload/download, slider, keyboard, cross-browser, or projector observation is claimed.
- Usability observation with **2–3 independent testers** is **NOT RUN**.
- Provider/data-flow practices beyond source inspection remain to be documented/confirmed before final submission.
- Statutory/cohort methodology requires practitioner review; whole-person 5% rounding is documented as a prototype convention, not asserted as regulatory guidance.
- App is not yet appropriate for actual confidential remuneration files. De-identified employee information may still be sensitive.

## Deployment safeguard and source integrity

- Existing `main` and https://paygap-navigator.streamlit.app/ remain unchanged.
- New HTML files exist only on `demo-day-html`; GitHub Pages **has NOT been enabled**.
- Follow the release gate in `tests/DEMO_ACCEPTANCE.md`; no Pages publishing until actual local browser checks pass, critical findings are fixed and retested, and the user authorises release.

## 27 October 2026 — post-Demo Day feedback and refinement

Demo Day feedback identified three useful refinement areas:

1. **Cohort-boundary behaviour in the simulator.** A question from Tristan highlighted that, when the original bottom 5% receives an uplift, treated employees can move above the post-simulation bottom-5% threshold and previously untreated employees can enter the newly re-ranked bottom cohort. The production simulator was already re-ranking the full workforce correctly, but this turnover was not visible to the user.
   - The Explore screen now states this explicitly beneath the bottom-tail control.
   - It also reports cohort turnover after re-ranking.
   - On the supplied 1,200-row synthetic dataset with a +30% bottom-tail guaranteed-pay uplift, 20 of the original 60 bottom-5% employees remain in the simulated bottom 5%; 40 move out and 40 previously outside the cohort enter it. The simulated ratio is approximately 22.78495:1.

2. **Whole-distribution inequality measure.** Anton suggested considering an internal Gini coefficient. A deterministic Gini calculation has been added as a complementary descriptive measure, not as a fairness score.
   - Supplied dataset baseline internal remuneration Gini: 0.4790855.
   - +30% bottom-tail uplift simulated Gini: 0.4753589.
   - The app explicitly notes that the Gini uses the full annual total-remuneration distribution and may move differently from the tail-focused top/bottom 5% ratio.

3. **Displayed ratio precision.** The app continues to display ratios to two decimal places, but now labels this as a prototype presentation choice and states that calculations retain full internal precision. The display rule is not represented as a Section 30B legal requirement.

Anton also commented during Demo Day that the tool has real practical relevance to addressing inequality in South Africa. This is recorded as expert/lecturer feedback on the problem's practical relevance, while further practitioner testing remains necessary before making claims about real-world effectiveness.

Regression tests were extended to cover the Gini calculation, +30% cohort turnover, simulated ratio and the new explanatory UI text.

### Lorenz-curve refinement

Following Anton's suggestion to consider an internal Gini coefficient, the Understand screen now includes an **Internal remuneration inequality** panel with:
- the internal remuneration Gini calculated from the full uploaded annual total-remuneration distribution;
- a Lorenz curve generated from the same production values;
- a perfect-equality reference line;
- an explicit note that the Gini complements, rather than replaces, the Section 30B top/bottom 5% ratio and is not a fairness threshold.

To avoid adding dashboard clutter, the previous large statistical-outlier panel was removed. The Tukey 1.5 × IQR result is retained as a compact exploratory note beneath the remuneration distribution. This preserves the diagnostic information while giving greater visual prominence to the whole-distribution inequality measure suggested during Demo Day.

Automated structural checks were extended to confirm the Lorenz-curve production function, inequality panel labels, perfect-equality reference and continued presence of the compact outlier note.

