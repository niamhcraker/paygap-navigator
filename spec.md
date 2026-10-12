# PayGap Navigator — Implementation Specification (`spec.md`)

**Stage:** 3 — Specification interview complete; **awaiting owner review and explicit approval before coding**  
**Compiled:** 9 October 2026  
**Application target:** Streamlit Community Cloud; demonstration 26 October 2026; final submission 30 October 2026  
**Authority:** `PayGap_Navigator_CONTEXT` v0.4, `PayGap_Navigator_CALC_SPEC` v0.2, `PayGap_Navigator_UI_SPEC` v0.2, and the **42 explicit decisions** from the Stage 3 interview. The interview decisions clarify implementation details; they do not silently replace the established scope, statutory basis, or calculation rules.

> **Approval gate:** This is a specification, **not application code**. No application code is authorised until the owner reviews and approves this file and `build_plan.md` and explicitly says to begin coding.

## 1. Purpose, user and boundaries

**Primary user:** A remuneration/reward practitioner at a South African public or state-owned company responsible for preparing, understanding, presenting or discussing remuneration disclosures.

**Job story:** When annual remuneration-gap figures are available, a practitioner wants to understand what the ratio means, examine historical movement and explore illustrative changes to remuneration, so that they can communicate the disclosure meaningfully and support informed professional judgement.

**Core journey:** **CALCULATE → UNDERSTAND & TRACK → EXPLORE**, implemented as **three screens only**. The landing/onboarding is part of Screen 1, not a fourth screen. User-facing copy must not say "Version 1".

**Core capabilities:**

1. Accept practitioner-supplied **aggregate** top-5% and bottom-5% total remuneration for the current financial year, plus optional summary remuneration statistics and optional historical years.
2. Compute the vertical remuneration ratio deterministically and explain its meaning in plain language.
3. Display supporting statistics; chart observed historical ratios; report overall historical movement and changes in top/bottom aggregate amounts.
4. Explore bounded hypothetical percentage adjustments to the **confirmed current-year** aggregate amounts.
5. Preserve transparent validation, data-quality and methodological limitations.

**Explicitly excluded from the core build:** Individual payroll records, employee names/IDs, cohort construction or re-ranking, payroll upload, external/sector benchmarking, fairness scores, universal thresholds, normative remuneration recommendations, legal advice, causal claims, runtime LLMs or AI APIs, databases, user accounts and persistence across sessions. Future contextual benchmarking belongs to Version 2. A downloadable consolidated report is a **stretch candidate** (section 13), not a core dependency.

**Statutory basis and caveat:** The supplied CALC_SPEC identifies section 30B's top-5% / bottom-5% **aggregate total-remuneration ratio** in the context of South African public and state-owned company remuneration disclosures, with the relevant requirements effective from 22 May 2026 as recorded in that source. "Total remuneration" is **not basic salary alone**: the source includes salary, benefits, employer benefit-fund contributions, short- and long-term incentives, share options and incentive awards. Do **not** claim the tool reproduces the complete statutory report or resolves unsettled cohort methodology (part-year work, ties, rounding, annualisation or employee population). The user is responsible for supplying appropriately established and consistently defined aggregate figures.

## 2. Minimal project structure and technology

```text
paygap-navigator/
├── app.py                     # Streamlit screens, navigation, widget/session state, rendering
├── calculations.py            # authoritative validation; ratio, trend, scenario, explanation logic
├── tests/
│   └── test_calculations.py   # pytest tests independent of Streamlit
├── requirements.txt           # runtime dependencies only
├── README.md                  # run/deploy instructions, Python version, limitations
├── spec.md                    # approved build specification
└── build_plan.md              # gated slices and test checkpoints
```

The test path is `tests/test_calculations.py`. A separate, small development/testing requirements file **may** be used for `pytest` if simpler than documenting it in the README. Do not make it mandatory for deployment. Plotly is the selected historical-chart library. Pandas is **optional** and should appear only if actually used for temporary chart preparation/display. No separate Python modules for individual screens; separate functions within `app.py` suffice unless a genuine limitation emerges. No multipage Streamlit structure for this version.

**Hosting and release:** Run locally, commit to GitHub, deploy the thin working skeleton to Streamlit Community Cloud **as early as possible, targeting Sunday 11 October 2026**, and verify its URL in a clean browser. Continue in small, tested increments. Keep local execution working as a backup and preserve a known-good Git commit for rollback. Record a consistently supported Python runtime; pin **direct, actually used** library versions **after** a working local/cloud deployment proves compatible. Do not manually pin every transitive dependency without cause. Avoid unnecessary dependency upgrades before Demo Day.

**No runtime AI:** All outputs are produced by inspectable Python arithmetic and deterministic text templates. AI may assist development, debugging and documentation, with its use disclosed in the assignment AI-use log.

## 3. Authoritative data model and units

Each current/historical record has **exactly the same seven remuneration fields**:

| Field | Meaning | Valid confirmed form |
|---|---|---|
| `year` | Calendar year **in which the financial period ends** | Integer; required |
| `top_5_total` | Aggregate total remuneration, highest-paid 5% | Numeric rand amount; required; >= 0 |
| `bottom_5_total` | Aggregate total remuneration, lowest-paid 5% | Numeric rand amount; required; > 0 |
| `highest_total` | Highest individual total remuneration | Non-negative numeric or `None` |
| `lowest_total` | Lowest individual total remuneration | Non-negative numeric or `None` |
| `average_total` | Average employee total remuneration | Non-negative numeric or `None` |
| `median_total` | Median employee total remuneration | Non-negative numeric or `None` |

**Representation:** One current-year dictionary and a separate list of historical-year dictionaries. The same field names, calculation rules and validation routines apply to both. The current record is separate so Screen 3 cannot accidentally simulate a historical year. `None` represents missing optional values (and blank, unconfirmed required drafts); it must never be silently replaced by zero. Internal monetary values are numeric; the UI displays rand. Pandas may be used *temporarily* but must not be the authoritative data store.

**Financial year convention:** Interface label **"Financial year ending"**; retain internal field `year`. Help text: "Enter the calendar year in which the financial year covered by these remuneration figures ended. For example, a financial year ending in March 2026 should be entered as 2026." This is **not** the publication, AGM or analysis year. No arbitrary recent-year restriction. The code must validate a meaningful, representable integer year; do not treat booleans, fractional years or missing years as valid.

**Currency:** All six remuneration fields for every year must be entered in **full South African rand (ZAR)**, not thousands/millions. Use labels like "Top-5% aggregate remuneration (R)" and show: **"Enter amounts in full rand (ZAR). If your source reports remuneration in thousands or millions of rand, convert the figures to full rand before entering them."** Example: **"R25,000 reported in R'000 = enter 25,000,000."** No automatic unit inference, unit selector or magnitude-based plausibility warnings.

**Manual monetary precision:** Whole rand, one decimal and two decimals are valid; **more than two decimal places is a blocking error**, never silently rounded or truncated. Blank numeric fields initialise as `None`, distinct from zero. Screen 1 uses blank-capable numeric inputs (no free-text currency parser), with an obvious rand indicator. The entered amount must retain its original cent precision through validation and calculations; see the **Streamlit input-precision feasibility gate** in section 14.

**Numeric safety:** All entered monetary values and displayed calculated numeric results must be finite. Reject `NaN`, `+inf`, `-inf`, negative inputs and amounts that cannot be safely represented/processed. Do **not** invent a statutory/business maximum (e.g. R100 billion). Fail safely if an extreme calculation overflows or cannot produce a trustworthy finite result. Retain precision through computation rather than rounding prematurely. Only final presentation is rounded; use suitable tolerance for tests involving non-exact floating-point division.

## 4. Session state, identity, navigation and confirmation

**Single app, conditional rendering:** `app.py` contains rendering functions for Screen 1, Screen 2 and Screen 3. A session-state screen selector determines which is shown. The same three-stage progress/navigation header appears across all screens. Results screens are inaccessible until the first successful calculation. Afterward the user may navigate freely without triggering recalculation.

**Draft vs confirmed:** Keep separately in session state:

- Editable draft current record and editable draft historical list, stored **independently of temporary widget state**.
- Immutable-in-practice *confirmed snapshot* of current and historical records, together with corresponding computed results and confirmed warnings.
- Active screen; onboarding-started flag; stable historical input-block identifiers; scenario slider values; lightweight reset/example-confirmation state where needed.

No database, local file or external storage is deliberately used for entered remuneration data. Streamlit session state is temporary and may be lost on refresh/reconnection/restart. An active session's data is processed by the server, not only on the user's device. Do not claim stronger confidentiality or infrastructure-level deletion than established.

**Input behaviour:** Independently managed input widgets update draft records (Streamlit reruns are acceptable); **they do not trigger confirmed recalculation**. The draft record is the source of truth for editable values. On return to Screen 1, widget state must be reconstructed from draft values if necessary. Incomplete/invalid drafts remain editable. Do **not** use a Streamlit form for the main workflow.

**Stable historical identity:** Each draft historical input block receives an invisible stable ID when created. Streamlit widget keys derive from this ID, never list index. The ID remains **interface metadata**, not an eighth remuneration field; removing one block must not reassign another block's values. Historical list changes affect drafts only until confirmed.

**Calculate button — one explicit commit point:** Clicking **"Calculate my pay gap →"** invokes validation of the entire current/historical draft dataset, followed by calculation. If **all blocking validation passes**, make a **complete new confirmed snapshot** and associated results/warnings, and then navigate to Screen 2. If validation or calculation fails, leave the old confirmed snapshot, its results and the existing scenario untouched. Never partially confirm a dataset. Validating and canonicalising draft values for comparison is not itself a calculation commit.

**Unapplied changes:** Detect by comparing the **canonical substantive data** of draft vs confirmed: all seven fields, numeric normalisation, historical records sorted by year; ignore historical widget IDs and record order. Distinguish `None` from `0`. Add/remove/edit creates a difference; restoring the original data clears it. Navigation does not create a difference. Once a previous successful calculation exists, Screens 2/3 show the exact agreed explanatory warning when drafts differ:

> **You have unapplied changes.** These results are based on your last confirmed data. Return to Calculate and select ‘Calculate my pay gap’ to apply your changes.

Provide a clear action to return to Screen 1. Results continue using **only confirmed data**. A successful recalculation with **identical substantive data** removes any transient validation messages as appropriate but does not unnecessarily reset the scenario.

**Scenario lifecycle:** The selected top/bottom percentage adjustments persist through ordinary navigation and editing of **unconfirmed** drafts. If a successfully confirmed dataset differs substantively from the prior confirmed dataset, reset both controls to 0% and use the new current-year baseline. Failed recalculation does not reset scenarios. Scenario calculations can update live as **scenario sliders** move, but must never modify or recalculate the confirmed baseline from draft data.

**Onboarding:** First arrival on Screen 1 shows prominent introduction and hides the input area. **"Start navigating your pay gap →"** reveals the inputs in the **same screen**, and the started flag stays true during that session. When returning from another screen, prioritise inputs, preserving all drafts; intro may remain available but less prominent. No custom JavaScript scrolling.

**Start new analysis:** A secondary **"Start new analysis"** control requires confirmation:

> **Start a new analysis?** This will clear your entered remuneration data, confirmed results, historical records and scenario adjustments. Your current analysis cannot be recovered.

**Cancel** changes nothing. **Clear and start again** atomically clears **all analysis-related session state**, including draft/confirmed records, entry IDs, calculation/results/warnings, dirty state, widget keys where necessary, scenarios and their results; resets both sliders to 0%; returns to initial Screen 1 onboarding. This resets application state only; do not imply guaranteed deletion from host infrastructure or logs.

## 5. Authoritative validation and messaging

**`calculations.py`** owns validation and warning rules. **`app.py`** displays field-specific, year-specific, practitioner-friendly messages and must not independently reproduce business validation logic. The main validation/calculation workflow returns a small predictable Python outcome (e.g. `success`, `results`, `errors`, `warnings`); exact internal names are implementation details. Multiple errors may be returned together. Expected invalid inputs must not surface as raw exceptions. Small arithmetic helpers can return numbers without wrapping every call.

**Blocking errors (current and, where applicable, each added historical record):**

1. Missing required `year`, `top_5_total` or `bottom_5_total`; blank means missing, not zero.
2. Non-numeric, boolean-as-number, non-finite or unrepresentable monetary values.
3. Negative remuneration in any required or **supplied optional** field.
4. `bottom_5_total == 0` (or otherwise not strictly positive).
5. User-entered monetary precision greater than **two decimal places**, determined **before UI normalisation can conceal it**.
6. Invalid/non-integer financial-year identifier; repeated historical years; historical year equal to or later than current year.
7. Any **added** historical record missing its year, top total or bottom total (do not silently omit it). Each has a **Remove year** control.
8. Inability to produce finite, trustworthy numerical outcomes; technical calculation failure.

Historical data is **optional as a whole**; current-year-only analysis must work. Historical contextual fields stay optional. No arbitrary recency or financial-size rules. If current `year` changes, all historical-year relationships are checked on next Calculate.

**Non-blocking data-quality warnings:**

- For any current or historical year, if `top_5_total < bottom_5_total`, calculate normally (including ratios below 1:1 and top total of zero) but warn that the pattern is unexpected **for equally sized cohorts**, suggesting the figures/reporting basis be checked. This is not a statutory invalidity ruling.
- When supplied values permit comparison: `highest_total >= lowest_total`; supplied `average_total` or `median_total` should be bounded by whichever supplied highest/lowest limits are available. Identify affected year and relationship. Do **not** invent tests between individual statistics and cohort aggregates without population/methodological evidence.

**Message types must remain separate:**

| Type | Blocking? | Where shown |
|---|---|---|
| Validation error | Yes | Screen 1 near affected draft input(s), when validation attempted |
| Confirmed data-quality warning | No | Screen 1 after successful confirmation; Screen 2 for current + all historical years; Screen 3 only current-year warnings relevant to scenario baseline |
| Unapplied-changes notice | No; informational | Screens 2/3 if substantive draft differs from confirmed snapshot |
| Scenario interpretation note | No | Screen 3 only if **hypothetical** `T_scenario < B_scenario` |
| Unexpected technical failure | Operation-specific | Concise recoverable error, never traceback in normal UI |

Warnings found in **unconfirmed drafts** must never be presented on results screens as though they qualified confirmed data. Reconfirmation replaces old confirmed warnings with newly applicable ones. Keep scenario-specific warnings visually/verbally distinct from baseline data-quality warnings.

**Examples:** Zero bottom: "The bottom-5% total remuneration must be greater than zero to calculate a ratio." Incomplete historical data: "Incomplete historical data for 2024. Enter the missing required value or remove this reporting year before calculating." Year conflict: "Historical reporting years must be earlier than your selected current reporting year (2025). Change the year or remove this entry before calculating." Precision error identifies year and exact field. Never show `NaN`, `inf`, raw Python tracebacks or a fabricated replacement answer.

## 6. Deterministic calculation rules

Let `T_y` be the **aggregate** highest-paid 5% total remuneration in financial year `y`, and `B_y` the aggregate lowest-paid 5% total remuneration, with `B_y > 0`.

**Vertical ratio:** `R_y = T_y / B_y`, displayed as `X : 1`. Explain: "The top 5% highest-paid employees collectively received X times the total remuneration received by the bottom 5% lowest-paid employees." Do not portray the ratio as a fairness or legality verdict.

**Historical comparisons:** Include only user-supplied current/historical financial-year records. Sort chronologically for presentation. When there is >=1 valid historical year, the **headline comparison** is between the **earliest available historical year** and the **current financial year**, not necessarily the latest consecutive pair. Label **"Overall change from [earliest year] to [current year]"**. No year-comparison selector in core build. Intermediate observed fluctuations appear in the chart; no inferred intermediate values or claims of a consistent annual rate.

For a quantity `Q`: `percentage_change(Q) = ((Q_later - Q_earlier) / Q_earlier) × 100` when `Q_earlier != 0`. Apply to ratio, top-group and bottom-group remuneration. Direction is determined **separately using unrounded values**: later > earlier = widened/increased; later < earlier = narrowed/decreased; equality = unchanged. If start is zero, percentage change = **undefined**, displayed as **"Not calculable (zero starting value)"**, while direction and absolute changes remain valid. Thus `0→10` is widened with undefined percentage; `10→0` is narrowed at −100%; `0→0` is unchanged with undefined percentage. Since confirmed `B>0`, a valid bottom-group historical percentage always has a nonzero starting denominator. Do not display infinity or zero in place of undefined.

**"What changed?"** Compare `T` and `B` **over the same earliest-to-current interval**. Report actual amounts and percent changes where defined. Use a **limited, tested decision tree** of safe arithmetic interpretations from UI_SPEC (e.g., bottom rising proportionately faster, top falling/bottom rising). Where rules are not safely applicable, use a **neutral factual fallback**: earlier/later ratios, widened/narrowed/unchanged, and absolute top and bottom changes (percentage only if defined). For `T: R0→R0`, `B: R1m→R1.5m`, explain unchanged `0.0:1` and the absolute values, not a fictional proportional comparison. No causal, fairness, policy-effect or prescriptive language; no runtime LLM.

**Scenario inputs (confirmed current year only):**

| Slider | Minimum | Maximum | Step | Default |
|---|---:|---:|---:|---:|
| Bottom-5% aggregate remuneration change | −20% | +50% | 1 percentage point | 0% |
| Top-5% aggregate remuneration change | −20% | +20% | 1 percentage point | 0% |

These bounds are **interface/usability parameters**, **not legal/professional thresholds or recommended actions**. Formulae, interpreting percentages as fractions:

- `T_scenario = T_confirmed × (1 + p_top)`
- `B_scenario = B_confirmed × (1 + p_bottom)`
- `R_scenario = T_scenario / B_scenario`
- `ratio_percentage_change = ((R_scenario − R_confirmed) / R_confirmed) × 100` **only if** `R_confirmed != 0`
- `top_difference = T_scenario − T_confirmed`
- `bottom_difference = B_scenario − B_confirmed`

Retain full internal numeric precision, **including fractions of cents generated by calculation**; round monetary values/differences **only when displaying** (maximum two decimal places). Values from the bounded slider ranges must still satisfy valid numerical-output requirements. For a zero top-group baseline, changing its slider cannot change `T_scenario` from zero; the ratio may remain zero and the ratio percentage change stays undefined. Scenario displays current vs scenario amounts and ratios side-by-side, a neutral direction label (GAP NARROWS / GAP WIDENS / GAP UNCHANGED), percentage change where defined, monetary differences and deterministic explanation. **Reset scenario** sets both sliders to 0%.

**Required Screen 3 notices:**

> **About this scenario**  
> This simulation applies percentage changes to the supplied top-5% and bottom-5% aggregate remuneration figures. It does not recalculate which employees would belong to these groups after the hypothetical changes. The scenario result is therefore illustrative and should not be treated as a verified future statutory disclosure.

> This scenario shows the mathematical effect of hypothetical remuneration changes. It does not determine whether the scenario is fair, appropriate, affordable or legally required.

**Conditional scenario note only when `T_scenario < B_scenario`:**

> **Scenario interpretation note**  
> This scenario produces a top-5% aggregate remuneration amount below the bottom-5% amount. This is unexpected for equally sized highest-paid and lowest-paid groups. Because the simulator does not re-rank employees, this result should be interpreted only as an illustrative mathematical outcome.

A below-one scenario is **not blocked**. The conditional note disappears when the scenario no longer meets the condition; it is **not** a finding about confirmed input quality.

## 7. Presentation and numerical formatting

- Inputs show rand units; outputs use readable separators, e.g. `R20,000,000` or `R1,250,000.75`. Suppress unnecessary `.00`. Fractions of a cent never display.
- Ratio headline normally **one decimal place**, `18.4 : 1`; percentage normally **one decimal place**.
- **Adaptive precision for comparisons:** Determine change from **unrounded** data. If two distinct ratios have the same one-decimal display, show two decimals; if still identical, up to **three decimals maximum**. If still visually indistinguishable, explicitly note that a genuine difference exists below displayed ratio precision, retaining the correct direction. Do not round direction decisions.
- If a genuinely nonzero percentage change would show as `0.0%`, use two decimal places; if still too small, display **"Change is less than 0.01%"**, accompanied by the correct neutral direction. Never display misleading `+0.0%` or `−0.0%`. Exactly equal underlying values remain unchanged. Do not invent categories like "slightly".
- When displaying a ratio comparison, apply consistent extra precision to both values in that comparison. Monetary scenario values may be shown to cents even where internal arithmetic includes fractions of a cent.
- Adaptive precision is a **presentation rule**, never a change to underlying ratio/trend/scenario calculations. Test ordinary rounding boundaries and extremely small differences.

## 8. Required screen behaviour and copy

### Screen 1 — Orient + Calculate

Show name **PAYGAP NAVIGATOR**, tagline **"From disclosure to understanding and action"**, introduction **"Understand your vertical pay gap"**, a short explanation of the statutory aggregate comparison and the limitation of fairness judgements, and the three-stage journey. Initially hide inputs behind **"Start navigating your pay gap →"**; after first start, prioritise inputs on future returns. Show **"Financial year ending"**, required `T` and `B` amounts, total-remuneration (not basic salary) note, full-rand conversion note, and optional expandable/context section with highest, lowest, average, median. Optional historical blocks have stable IDs, year and identical monetary fields, **Add another year**/**Remove year** actions. Show distinct input-validation and data-quality messages; Calculate navigates to Screen 2 only on success. No extra page or legal-compliance form. Keep "Start new analysis" and, after core is validated, optional synthetic loader secondary.

**Public prototype privacy notice near inputs:**

> **Before entering remuneration data**  
> This is a publicly hosted prototype. Please use synthetic or publicly available aggregate remuneration figures only. Do not enter confidential organisational information.  
> PayGap Navigator does not include a database or application feature designed to permanently store your remuneration inputs. However, information entered into the application is processed through the hosting environment while you use the tool.

Separate note: the app uses aggregate figures and **does not require individual payroll/employee data**. No mandatory acknowledgement checkbox or unsupported assertion that the public host has been audited for POPIA compliance.

### Screen 2 — Understand & Track

Display prominent **confirmed** current ratio, plain-language interpretation, confirmed top/bottom amounts and only supplied contextual stats (or neutral "Not provided"). Explain the descriptive nature of the ratio and absence of a universal fairness threshold. If no historical year: **do not show empty trend chart or "What changed?"**, optionally invite users to add historical years. If at least one: show Plotly trend and annual ratio labels; headline overall earliest-to-current change with safe direction; top/bottom changes and deterministic "What changed?" explanation. Keep a secondary **"← Edit remuneration data"** and primary **"Explore scenarios →"** action. Show relevant current/historical **confirmed** data-quality warnings and unapplied-changes message if applicable.

### Screen 3 — Explore

Display confirmed current-year baseline amounts and ratio, two bounded percentage sliders, dynamically calculated scenario amounts/differences, side-by-side baseline/scenario ratios, neutral direction, percentage change or zero-start message, short deterministic scenario interpretation and all agreed scenario disclaimers. Show only **confirmed current-year** data-quality warnings relevant to the baseline, plus any *conditional* hypothetical scenario note. Provide **"Reset scenario"** and **"← Back to Understand & Track"**; sliders persist during navigation/draft edits but reset when substantively different data are confirmed. Show unapplied-changes message if applicable. Never claim the hypothetical outcome is the organisation's verified future disclosure.

### Visual design baseline

Readable headings and labels, unobtrusive information notes, sufficient whitespace, large primary ratio, clear next action, no reliance on colour alone, practitioner-friendly language, no unsupported traffic-light/fairness scoring, no unnecessary dashboard widgets. The app must remain usable without instructions external to the application.

## 9. Plotly historical visualisation

- Use **Plotly** for the one purposeful historical line/marker chart (not a general dashboard framework). Chronological x-axis is **financial year ending**, y-axis is vertical remuneration ratio; clear title, accessible hover showing exact **year and ratio**; highlight current reporting year using a **label/marker distinction not solely colour**.
- Plot **only actual supplied observations**. Connect **only consecutive years**. If one or more intervening reporting years are absent, **break the line**. Implementation may segment consecutive observations into separate traces (or use gaps) but must not create synthetic observations or interpolate ratios.
- Non-consecutive observations may display markers with no connecting line; within longer data, connect each consecutive run separately.
- Beneath/beside the chart, always show annual ratios numerically. Display an optional note when years are missing: **"No data was supplied for some intervening reporting years. The chart shows only observed values."**
- The overall earliest/current change and direction are separate from the chart; their calculation is unaffected by line gaps.
- If chart rendering fails after calculations succeed, continue showing **valid annual ratios and trend statistics** and show: "The historical chart could not be displayed, but the calculated historical results remain available below."

## 10. Safe failures and observability

**Ordinary validation failures:** Return structured blocking messages without confirming or overwriting valid prior results. 

**Unexpected calculation failure:** Keep prior confirmed snapshot intact, present no **new** calculated result, and show:

> **Unable to complete the calculation**  
> Something unexpected prevented this calculation. Your previously confirmed results have not been changed. Please try again.

**Unexpected scenario failure:** Preserve confirmed baseline and existing valid information; do **not** display a failed scenario output as successful. Provide a clear message and allow reset/retry.

**Unexpected Plotly failure:** Localise failure to chart only if numeric results are valid (section 9).

Technical exception details may be consulted in development/server logs; raw tracebacks are not part of the normal user-facing UI. Avoid deliberately logging input remuneration amounts. Use targeted error handling rather than disguising every programming failure with a generic success-looking fallback.

## 11. Verification and acceptance tests

**Automated:** `pytest` tests directly call `calculations.py`, independent of Streamlit. Verify ratio, validation, warnings, trends, undefined percentages, deterministic texts, formatting helpers and scenario maths. **Manual:** documented end-to-end interface tests, local and on deployed URL where relevant. Manual log must record **expected**, **actual**, **pass/fail**, **issue**, **fix**, **retest**; include clean-browser checks and safe-failure attempts. No automated Streamlit UI suite by default; reconsider only for demonstrated recurring risk. Cross-check selected calculations by hand or independent spreadsheet. **Usability-testing target:** aim to observe **2–3 people who are not the developer** using the application **without step-by-step instruction**. Record what confused them, what failed, what changed in response and the outcome of the retest. A domain-expert review can supplement this observation but **must not replace it**. If the target cannot be reached, document the limitation honestly.

### Existing CALC_SPEC known-answer cases (unchanged)

| ID | Inputs | Required outcome | Primary build gate |
|---|---|---|---|
| **T001** | `T=10,000,000; B=1,000,000` | `10.0 : 1` | Core ratio / first deployed skeleton |
| **T002** | `T=20,000,000; B=1,000,000; top +0%; bottom +20%` | `B_s=1,200,000; R_s≈16.666666…` displayed `16.7:1`; bottom difference `R200,000`; ratio change ≈`−16.67%` internally (adaptive UI rounding) | Scenario slice |
| **T003** | `2024: 25m/1m; 2025: 22m/1m; 2026: 18m/1m` | Annual ratios `25.0,22.0,18.0`; overall narrowed `−28%` (2024→2026) | Trends and Plotly |
| **T004** | `T=20,000,000; B=0` | No ratio, clear blocking error, no infinity/NaN | Core validation / first skeleton |
| **T005** | `T=−1; B=1,000,000` | Blocked with validation error | Core validation / first skeleton, including direct helper tests |
| **T006** | `T` entered; `B=None` | Blocked with missing-input message | Core validation / first skeleton |

**Additional required test categories:**

- Current-year-only succeeds; added but incomplete historical record blocks; duplicates and years >= current block; changing current year revalidates history; removing year doesn't scramble remaining fields.
- `None` ≠ zero, zero `T` allowed with quality warning, contextual missing values omitted rather than invented, supplied optional negatives block; individual summary-statistic consistency warnings are non-blocking.
- Zero-start ratio and top-group historical percentage changes; direction retained for `0→positive`, `positive→0`, `0→0`; no false `NaN`/`inf`.
- Scenario 0% = baseline; state persists during navigation/draft edits; resets only after a different **valid confirmed snapshot**; T002; scenario `T=0`; conditional scenario `<1` interpretation warning appears/disappears.
- Adaptive precision: a true ratio difference hidden at 1 decimal is revealed at 2/3 or disclosed textually; percentage below 0.01% uses text + direction; equality reports unchanged; no signed zero display.
- Currency: whole/one/two decimal entry accepted; 3+ decimal entry rejected **before loss of precision**, confirmed state preserved; scenario fractional cents retained internally and displayed to cents.
- Finite and extreme values: very large valid `T/B` with ordinary ratio; `NaN`, ±infinity and non-finite calculated result safely rejected; no arbitrary business cap.
- Plotly: all years chronological, non-consecutive observations unconnected, numerical labels present; fail chart deliberately during testing and ensure numeric outputs survive.
- Manual navigation/state: start reveals form once; unconfirmed edit warning, restore clears warning; confirmed warnings scoped correctly; draft persists when widgets hidden; reset Cancel preserves all; reset Confirm clears all keys/results/IDs and returns to onboarding; no stale values.
- Security/usability: rand-unit and public-prototype privacy notes are visible before entry; synthetic data only at demo; all critical functions work from deployed URL in a clean browser; handled errors show no tracebacks.

The initial deployed skeleton must **already pass T001, T004, T006 and T005 where negative values can reach the calculation layer**. The underlying validation function must also be tested directly against negative values irrespective of front-end controls.

## 12. Reproducible deployment, ethics and handover

- First functional skeleton must run **locally**, be committed to GitHub, **deploy to Streamlit Community Cloud**, open at its own clean-browser URL, and perform the basic data→validated calculation→result journey; no chat interface is needed (**Unplugged Test**).
- Record supported Python runtime and exact successfully tested direct dependency versions after first known-good deployment; document one-command local launch and `pytest` instructions in README. Deployment should not require pytest unless it is a runtime dependency (it should not be).
- A known-good Git commit should be retained before later changes, especially before Demo Day; test local and cloud after meaningful updates.
- Aggregate-level input only; no storage by design; no user account; publicly hosted **prototype** is not approved for confidential organisational data. Real/identifiable employee data is prohibited for demonstration; use synthetic figures. Do not send user remuneration data to an LLM/API. No assertions of audited POPIA compliance or guaranteed infrastructure-level deletion.
- **Before final submission (not a prerequisite for the first deployed skeleton):** verify and document relevant **Streamlit Community Cloud provider terms and data-handling practices** for the Assignment 2 **Ethics & Data** section. Describe what data passes through the hosted prototype, where/how it is processed according to verified provider information, relevant provider practices or terms (including any supported statements about logging, retention or access), and the potential consequences of incorrect application outputs. Record source links and verification date; clearly identify any information that could not be verified rather than asserting it.
- Prepare assignment evidence: version history, test/failure/retest log, manually verified arithmetic, **2–3 unguided usability-observation records as the target** (or documented shortfall), any supplemental domain-expert feedback, limitation notes and transparent AI-use log. Before Demo Day produce the mandatory **60–90-second fallback screen recording** and rehearse the 5-minute presentation; keep local fallback available. Submission includes the source, working link/run steps, outline and recording according to the assignment handout.
- **Final administrative requirements:** Keep the working application **live until 13 November 2026**. The final project-outline **cover page must include the assignment's required signed declaration**, verbatim: “This tool is my own work. I have declared all AI platforms used, I understand and take responsibility for everything submitted, and I have not misrepresented the capabilities of what I built.”

## 13. Deferred enhancements, not core dependencies

**Priority 1 after core passes: Synthetic-example loader (approved post-core usability enhancement).** Screen 1 may show a secondary **"Load synthetic example"** / **"Try PayGap Navigator with example data"** action. Use clearly labelled synthetic **T003** records: 2024 `25m/1m`, 2025 `22m/1m`, 2026 `18m/1m`; optional contextual statistics only if separately validated. Loader writes **draft only**, uses stable historical IDs, does **not** auto-confirm/calculate, and asks permission before replacing nonempty drafts. Cancel changes nothing. Existing confirmed data remain unchanged until explicit valid recalculation; dirty-warning logic remains active. No permanent storage. Add only after core journey is working and tested; defer if threatened.

**Priority 2: Consolidated downloadable report (high-value stretch candidate, not yet authorised for implementation).** If core screens, validation, deployment and demonstration prep are secure, *consider* an in-session report comprising confirmed reporting year/ratio/aggregates and interpretation, optional stats, observed Plotly trend/annual ratios, overall change and "What changed?", currently selected scenario when applicable, relevant **confirmed** warnings, and all agreed disclaimers. Generate only from **confirmed records**, not draft data; do not persist or add fairness/causal interpretations/recommendations. Choose format, layout and generation mechanism **later only if** this feature clears a separate scope/time/quality gate. Otherwise explicitly defer; no impact on core dates.

Future product opportunities such as sector benchmarks, company size/revenue comparators, intervention markers, external datasets and persistent organisational accounts remain outside Version 1.

## 14. Implementation assumptions and explicit risk gates

The following are **technical details to test**, not invitations to silently change agreed decisions:

1. **Streamlit cent precision and blank fields — highest feasibility risk.** Confirm that the chosen Streamlit `number_input` configuration supports `None` and preserves enough of a manually entered number to **reject three or more decimal places before auto-formatting/rounding conceals them**. If it cannot do both reliably, stop that slice and propose the smallest alternative for owner approval; do not secretly relax the two-decimal rejection rule or switch to currency free-text parsing.
2. **Widget lifecycle and atomic snapshots.** Confirm temporary Streamlit widget keys can be destroyed/recreated without losing drafts, stable IDs preserve historical values, and reset deletes stale widget-backed state. Test deep/separate copies so editing the draft never mutates confirmed data by reference.
3. **Numerical safety.** Python numeric limits/representation and extremely small/large valid ratios can cause overflow or apparent equality. Check finite inputs/outputs, preserve cents, adopt consistent rounding presentation, and surface under-resolution changes neutrally rather than inventing equality. Do not add an arbitrary remuneration ceiling.
4. **Plotly gaps.** Ensure missing-year line breaks without inserting invented ratio observations; avoid costly materialisation of every missing calendar year over a huge range. Use consecutive-run traces or an equivalent truthful technique; test two non-consecutive years.
5. **History comparability.** `year` stores only financial year-end calendar year, **not exact start/end dates**. The app cannot verify whether financial periods, coverage or definitions are comparable; explanatory claims should be qualified accordingly.
6. **Domain uncertainty.** Existing statutory sources do not resolve equal cohort sizes, part-year inclusion, ties or 5% rounding. User supplies aggregates; app does not certify statutory eligibility or compliance. A ratio below 1 is warned about, not banned.
7. **Platform/privacy.** Streamlit Community Cloud is a publicly accessible prototype and may process session information on its infrastructure. No database does not imply complete secrecy, zero logs, recoverability or permanent deletion. Use synthetic/public data only.
8. **Live demonstration and hosting risk.** Cloud cold starts/connectivity may fail; verify from clean browser, retain known-good rollback, local execution and mandatory recorded fallback. Do not delay validation to make visuals/report more elaborate.
9. **Document precedence.** In the app UI, the interview's clarified **"Financial year ending"** label supersedes the more ambiguous earlier "Reporting year" label while retaining internal `year`. The interview's Plotly choice supersedes the earlier tentative native-chart suggestion. No other existing statutory or mathematical rule is changed.

## 15. Interview decision traceability (1–42)

| Decisions | Frozen implementation choice |
|---|---|
| **1–2** | Minimal modules; uniform seven-field dictionaries; current separated from historical; optional `None`, Pandas temporary only |
| **3–4** | Draft/confirmed snapshots; explicit Calculate commit; free navigation after first success; unapplied-change notice |
| **5–8** | Added historical records complete-or-remove; zero-start percentage undefined but direction valid; prior-year uniqueness/order; low-top aggregate warnings |
| **9–10** | Three conditionally rendered functions in one `app.py`; session-only data; no persistent storage |
| **11–12** | Earliest-to-current headline trends; scenario persists in navigation but resets after changed valid confirmation |
| **13–14** | Blank-capable numeric rand inputs; bounded percentage sliders |
| **15–17** | Plotly observed-year chart; broken lines over missing years; stable invisible historical widget IDs |
| **18–19** | Early GitHub/Cloud deployment; thin first skeleton with core ratio and initial tests |
| **20–21** | Authoritative validation in `calculations.py`; up-to-two-decimal manual input; no premature rounding |
| **22–24** | Canonical substantive dirty comparison; contextual consistency warnings; confirmed warnings propagated by screen |
| **25–26** | Widgets write persistent drafts; first Start reveals inputs on Screen 1 and persists |
| **27–28** | Deterministic, limited historical explanation/fallback; pytest plus documented manual UI tests |
| **29–30** | Scenarios do not re-rank cohorts; conditional scenario-specific below-one note |
| **31–32** | Bounded adaptive display precision; targeted safe failures without misleading results |
| **33–34** | Confirmation-protected complete analysis reset; fractional-cent scenario arithmetic kept internally |
| **35–36** | Public-prototype confidentiality notice; post-core synthetic T003 loader |
| **37–39** | Financial year-end year as integer; full ZAR input; manual >2 decimals blocked without rounding |
| **40–42** | Test-proven dependency pinning; no arbitrary amount cap but finite safety; small structured validation/calculation outcome |

**Next gate:** Review this `spec.md` and companion `build_plan.md`. If approved, explicitly instruct the assistant to begin implementation **one testable slice at a time**. Until then, **STOP — no application code**.
