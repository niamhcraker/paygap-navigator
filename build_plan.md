# PayGap Navigator — Small, Testable Build Plan (`build_plan.md`)

**Stage:** 3 deliverable, for review; **no application code has been authorised**  
**Compiled:** 9 October 2026  
**Companion:** [`spec.md`](spec.md)  
**First deployed skeleton target:** **Sunday 11 October 2026**  
**Demo Day:** **Monday 26 October 2026** | **Final submission:** **Friday 30 October 2026**

> **Gate 0 — Owner approval.** Review both documents, ask for corrections, then explicitly approve `spec.md` **and** this build plan **and** instruct the assistant to start coding. Until that happens: **do not create `app.py`, `calculations.py`, tests or deploy anything.**

## 1. Strategy and rules for every slice

**Build an end-to-end working journey early, then add one separately testable capability at a time.** Keep the app deployable, reversible and demonstrably correct throughout. A slice is complete only when its defined acceptance tests pass; commit the known-good state before moving on. Do not implement future slices early "while we're in the file".

Each coding step must follow the same **gate**:

1. State the narrow objective and the affected file(s).
2. Explain the intended change in plain language.
3. Implement only that slice.
4. Run relevant **automated** tests; perform relevant **manual** UI checks.
5. Verify behaviour locally and, when appropriate, on the Cloud app.
6. Record expected vs actual, failures, fixes and retest in the test log.
7. Save a known-good Git commit; do not proceed if the gate fails.

**Scope protection:** If the timeline slips, omit enhancements or reduce visual polish; **do not weaken validation, disclaimers, privacy boundaries or the three-screen core journey**. The first public build is a **working prototype skeleton**, not a falsely claimed complete app.

## 2. What the first skeleton must do — and nothing more

**Screen 1: Calculate**
- Existing onboarding content with **Start** action that reveals, on Screen 1 itself, the core inputs.
- Ask for **Financial year ending**, top-5% aggregate remuneration (R) and bottom-5% aggregate remuneration (R).
- Required-field and denominator validation; explicit **"Calculate my pay gap →"** confirms a valid dataset.
- No historical-year entries or optional contextual remuneration fields yet.

**Screen 2: Understand & Track**
- Display the **confirmed** ratio, both aggregate amounts and the plain-language interpretation.
- Navigate back to Calculate and forward to Explore.
- No historical chart, contextual statistics or "What changed?" yet.

**Screen 3: Explore**
- Establish the third-screen navigation and display the **confirmed baseline** ratio and remuneration amounts.
- Clearly identify scenario controls as **not implemented yet during development**. This temporary development message must be removed when the full simulator is implemented and must not be misrepresented as working functionality.
- No functioning sliders yet.

**Architecture from day one:** The ratio formula and its authoritative validation live in `calculations.py`, not as temporary math inside `app.py`. `app.py` contains navigation and session state; minimal `tests/test_calculations.py` checks the calculations. `requirements.txt` contains actual runtime packages only.

**Mandatory first-skeleton checks:** T001 (10.0:1), T004 (bottom zero blocked), T006 (missing required value blocked), plus T005 directly against the calculation/validation function (negative value blocked) even if the widget makes that input impossible. Also test empty/zero distinction, back/forward navigation, successful calculation and no results before confirmation.

**Deploy gate:** Skeleton is **not complete** until local execution works; source is committed to GitHub; Streamlit Community Cloud deployment succeeds; the public URL opens in a clean browser; the three-screen journey and minimal validation work **on the deployed version**; and the required automated tests pass. Target: **11 October 2026**. If hosting fails, fix/de-scope the skeleton, **not** by making the app deceptively present static or fake results.

## 3. Incremental build slices

| Slice | Implementation focus | Concrete output and completion gate | Tests/checks attached |
|---|---|---|---|
| **0. Specification sign-off** | **No code.** Review frozen `spec.md` and this plan. | Explicit owner approval to proceed. | Confirm scope and first-skeleton gate in writing. |
| **1. Environment + risk spike** | Minimal repository/config; confirm supported Python/Streamlit versions and test blank numeric input and cent-precision feasibility **before** relying on it. | Working local runtime; establish whether the numeric field can reject 3+ decimal entries without silent normalisation. If impossible, **stop and ask before substituting any input method**. | Blank `None` vs 0; inputs 1, 1.2, 1.23, 1.234; check widget preservation; basic Cloud compatibility. |
| **2. Basic calculation + validation** | In `calculations.py`: main structured outcome; required fields; finite/nonnegative checks; `B>0`; ratio + basic interpretation; small pytest suite. | Directly tested ratio function and safe validation interface. No UI business logic duplication. | **T001, T004, T005, T006**; direct non-finite inputs; basic huge finite values. |
| **3. Thin three-screen local journey** | In `app.py`: initial onboarding reveal; Screen 1 core inputs; draft/confirmed snapshot; Calculate button; Screen 2 result; Screen 3 baseline-only placeholder; conditional navigation. | A user can enter valid inputs and reach calculated results on Screen 2, navigate to Screen 3 and back, without opening ChatGPT. Failed input stays on Screen 1; old confirmed data never overwritten. | T001/T004/T006 through UI; first-success gating; draft survives navigation; initial public-prototype privacy/unit notes. |
| **4. Deploy the first skeleton** | GitHub, `requirements.txt`, Streamlit Community Cloud, clean-browser smoke test. | **Initial URL actually works end-to-end** with core ratio. Record commit hash, Python/versions and exact run steps; use the target of **11 October**. | Repeat T001, T004, T006 on public app; verify no access to result screens before first success; local fallback works. |
| **5. Robust session-state workflow** | Stabilise persistent draft records, confirmed snapshot copy, canonical change comparison, unapplied-changes warnings and atomic confirmation. | Edit draft without affecting results; restore draft removes warning; failed validation preserves last confirmed result. | Manual navigation/dirty-state matrix; direct canonical comparisons; reset of widget keys not yet needed. |
| **6. Additional current-year context + quality checks** | Add optional highest, lowest, average, median; blank-as-`None`, per-field validation and limited non-blocking consistency warnings; below-one warnings. | Optional blanks do not block; negative or 3+ decimal manual amounts block; invalid optional relationships warn without blocking; Screen 2 displays supplied context only. | New pytest warning/precision tests; manual current-year warning visibility; `T=0,B>0` valid/warned. |
| **7. Dynamic historical inputs + identity** | Add/Remove year, stable IDs, same seven-field schema, history required/optional rules, uniqueness, strictly earlier-than-current financial year. | Current-year-only works; incomplete added years block; removing one block never shifts another block's values; all changes remain draft until confirmation. | Direct history validation tests; manual add/delete/reorder/restore; duplicate and later-year checks; atomic failure. |
| **8. Historical arithmetic + safe explanation** | Compute observed annual ratios, earliest→current headline percentage/direction, top/bottom changes, zero-start undefined rules, limited deterministic templates and neutral fallback. | T003 outputs and plain-language explanation correct; no invented missing data, causal interpretation or undefined percentage. | **T003**; 0→10, 10→0, 0→0, top-group start 0; missing years; explanation rule/fallback tests. |
| **9. Plotly historical chart** | Purposeful observed-point chart, numeric hover labels/current-year identification, consecutive-year connections only, breaks across gaps; numerical ratio list; graceful chart failure. | Gap-safe chart readable, correct axes, markers and labels. Current year clearly identified without colour alone. | Consecutive and non-consecutive observations; isolated markers; no interpolated values; deliberate rendering-failure manual test while numeric results remain available. |
| **10. Scenario simulator** | Add bottom/top bounded 1%-step sliders, live deterministic calculations from confirmed current year, remuneration differences, ratio change/direction, reset/persistence and disclaimers. | Scenario works end to end; slider navigation persists; changed valid baseline resets both to 0%; failed validation does not; below-one scenario note conditional. | **T002**; zero top baseline; 0% unchanged; fractional-cent internal result/display; undefined ratio %; slider ranges; scenario error recovery. |
| **11. Complete UI + robustness** | Consistent top navigation and practitioner copy; confirmed warning placement; precision formatting; full atomic **Start new analysis**; targeted recoverable errors and all privacy/statutory/simulation notes. | Every Screen 1/2/3 path coherent, accessible and honest; no stale state, unintended reset, raw traceback, invented fairness or legal advice. | Adaptive precision test suite; warning-scoping tests; cancel/reset manual checks; inject calculator/chart/scenario failures; public-data notice and full-ZAR guidance. |
| **12. Full core validation and usability gate** | Run all unit/edge tests, manual protocol locally and in clean public browser, independent hand calculations; **aim to observe 2–3 people other than the developer using the app without step-by-step instruction**. Domain-expert review may supplement but does not replace user observation. | **All must-have functionality fully validated**; record what confused users, what failed, what changed and the retest outcome. Document honestly if fewer than 2–3 observations are possible. Identify a known-good Git commit. | Entire automated suite + all core manual journeys and known-answer cases; clean-browser deployment; repeat after fixes and observation-driven changes. |
| **13. Post-core usability enhancement: synthetic loader** | Only after Slice 12 passes: add an optional secondary **Load synthetic example** using synthetic T003 data, draft-only, stable IDs, confirm-before-overwrite. | Demo data load does not auto-calculate or overwrite confirmed state; cancel and dirty-warning behaviours correct. Can be deferred safely. | T003 after user presses Calculate; replace/cancel tests; confirmed snapshot unchanged before explicit recalculation. |
| **14. Optional report stretch gate** | **Decision checkpoint, not committed core work.** Consider in-memory downloadable report only if there is real time after core, loader (if retained), testing, and demo preparation. | Proceed only with owner approval of format/contents and ability to re-test. Otherwise mark **deferred**; never sacrifice core. | Confirmed-only data, no persistence, existing warnings/disclaimers, no new claims; test optional export if ever built. |
| **15. Demo freeze + handover** | Final cloud/local regression; README, testing evidence, AI-use log, 60–90 sec fallback video, demo rehearsal and submission. **Before final submission, verify/document Streamlit Community Cloud terms/data handling and the hosted prototype's data flow, processing, relevant provider practices and consequences of error for Ethics & Data** (do not delay first skeleton). | Known-good cloud link and Git commit; source and outline by 30 Oct; **working app kept live until 13 November 2026**; project-outline cover page contains the **required signed declaration**. | Clean-browser opening, fallback replay, final regression; record provider source links, verification date and unknowns; check cover declaration and post-submission link availability. |

### Why slice order matters

- **Slices 1–4 prove the Unplugged Test and deploy early.** They are deliberately smaller than the finished app.
- **Slices 5–7 solve the hardest state-management problems before complicated charts/scenarios depend on them.**
- **Slices 8–10 build one independently testable analytical capability at a time** (historical arithmetic, visualisation, then scenario).
- **Slices 11–12 prioritise clear explanations, safety, validation, user testing and recoverability over decorative polish.**
- **Slice 13 is useful but optional on schedule; Slice 14 is explicitly stretch-only.**

## 4. Known-answer test mapping and pass criteria

| Case | What must be verified in `calculations.py` | First required by |
|---|---|---|
| **T001 — Simple ratio** | `10,000,000 / 1,000,000 = 10.0:1`; correct interpretation and safe display. | Slice 2, repeated on UI/cloud in 3–4 |
| **T004 — Zero denominator** | `B=0` returns **blocking error**, **no result**, no `inf`/`NaN`. | Slice 2, repeated cloud in 4 |
| **T005 — Negative amount** | `T=−1` returns **blocking error**, even when bypassing Streamlit controls. | Slice 2; check direct function at skeleton gate |
| **T006 — Missing required field** | `B=None` returns missing-field blocking error, never silently 0. | Slice 2, repeated cloud in 4 |
| **T003 — Historical trend** | 2024=25.0, 2025=22.0, 2026=18.0; earliest→current `−28%`, direction **narrowed**. | Slice 8; chart representation Slice 9 |
| **T002 — Scenario uplift** | T=20m, B=1m, bottom +20%, top 0%; B scenario=1.2m, ratio=16.666…, bottom difference R200k, ratio change ≈−16.67% internally; suitable displayed rounding. | Slice 10 |

All six need independent pytest coverage and, where implemented in the UI, at least one manual end-to-end check. For T002, ensure internal percentage precision is not confused with one-decimal default UI formatting. Additional tests are not replacements for T001–T006.

### Additional test matrix

| Area | Representative edge case | Expected behaviour |
|---|---|---|
| Input precision | `1250000.456` manually entered | Blocking precision error; original draft retained; prior confirmed data intact |
| Optional context | Highest R500k, average R700k | Non-blocking specific warning; ratio remains usable |
| Ratio below 1 | Current top R800k, bottom R1m | Ratio 0.8:1 remains valid with clearly labelled data-quality warning |
| Undefined ratio % | Ratios `0.0→10.0`, `10.0→0.0`, `0.0→0.0` | Directions widened/narrowed/unchanged; % undefined/−100%/undefined |
| Draft comparison | Edit a figure then restore it | Warning appears, then disappears; confirmed calculation never changes |
| Historical identity | Add 2023/2024/2025 then remove 2024 | Values for 2023 and 2025 remain attached correctly |
| Missing history years | Observed 2022, 2025, 2026 | Markers for all; line only 2025→2026; no 2023/2024 values inferred |
| Scenario persistence | Change slider, navigate away/back | Same scenario maintained until confirmed dataset substantively changes |
| Scenario unusual result | Hypothetical top < hypothetical bottom | Numerical output shown, separate **conditional** scenario note; baseline warning not fabricated |
| Scenario fractional cent | R1,000.01 with +1% | Internal `R1,010.0101` equivalent used in math; displayed `R1,010.01` |
| Adaptive precision | `20.01:1→20.02:1` | Two decimals in comparison and **widened**, not equal rounded labels |
| Numerical extremes | Very large valid values; `NaN`/infinity; output overflow | Valid finite result or safe failure; no imposed arbitrary rand ceiling |
| Reset | Click Start new analysis then Cancel vs Confirm | Cancel changes nothing; Confirm clears **all** analysis state and restores onboarding |
| Visualisation failure | Force chart rendering error in development | Valid numeric results remain visible; concise chart failure note |
| Unhandled operation failure | Force scenario/calculation error in development | No false new result, confirmed baseline preserved, recoverable explanation |
| Privacy/units | New user sees input controls | Public-prototype and full-rand-unit notices visible and understandable |

## 5. Manual end-to-end testing protocol

Use one running document/log (e.g., `PayGap_Navigator_TEST_LOG.md` if this file already exists or is created during implementation). For each interaction, capture:

| Field | What to record |
|---|---|
| Test ID and build | e.g. `UI-07`, Git commit/Cloud build |
| Setup | Existing draft/confirmed state, data, active screen |
| Action | Exactly which user interaction occurred |
| Expected | Predetermined behaviour from `spec.md` |
| Actual | What the user actually saw |
| Pass/fail | Clear result |
| Issue + fix | Description and code/design change, if any |
| Retest | Date/build and whether the corrected behaviour now passes |

**Minimum manual journey to rehearse:** Open the clean-browser URL → read the confidentiality/full-rand notes → click Start → enter valid T001 fields → Calculate → interpret Screen 2 → visit Screen 3 → return to Screen 1 → edit bottom amount without confirmation → observe old results + warning → restore original and check warning clears → add history with missing field and confirm it blocks → complete/remove history → observe Plotly if available → adjust/reset scenarios → test Cancel and Confirm for Start new analysis → verify fresh onboarding and absence of stale values.

Repeat representative **failure** paths. Check on **local and deployed Cloud** after material changes. Perform independent spreadsheet/manual cross-checks (especially T001/T002/T003). **Aim to observe 2–3 people who are not the developer using the application without step-by-step instruction**; record what confused them, what failed, subsequent changes and the retest result for each issue. A domain-expert review may supplement, not replace, this observation; document any shortfall honestly. Do not claim "fully tested" merely because the server starts without exceptions. Log the failures as evidence of critical oversight.

## 6. Schedule, checkpoints and cutoff rules

| Target | Gate |
|---|---|
| **9 Oct (specification completion)** | Owner has `spec.md` + `build_plan.md` for review; no code before explicit approval. |
| **By Sunday 11 Oct** | Smallest working ratio skeleton deployed; T001/T004/T005/T006 pass; clean-browser cloud URL; local fallback. |
| **Monday 12 Oct (Build Clinic)** | Bring working link and specific issues from initial deployment (if any). |
| **By Monday 19 Oct** | Aim for complete core calculations, histories, Plotly chart, scenario and at least an initial external usability test; retain room for bug fixes. |
| **By Friday 23 Oct (feature freeze)** | Core validation and regressions complete, known-good commit secured; fallback recording made. Avoid new features. Synthetic loader only if safely added/tested. Report stretch likely deferred unless already proven. |
| **Monday 26 Oct** | Live 5-minute Demo Day pitch; 60–90-second fallback recording ready; test URL and laptop in advance. |
| **Friday 30 Oct, 23:55** | Deliver working tool/source, max-5-body-page outline (plus allowable cover/references/AI-use appendix) and fallback recording; **verify provider terms/data flow for Ethics & Data**, and include the **required signed declaration on the cover page**. App must remain live **until 13 November 2026**. |

**If delayed:**

1. Fix critical math, validation, cloud deployment, session-state or misleading-message issues **before** adding features.
2. Keep three core screens, even if visual polish must be reduced.
3. Defer downloadable report first; defer synthetic loader next if needed.
4. Do **not** cut testing, public-data warning, scenario limitation, truthful handling of missing years or zero denominators.
5. Preserve a tested live build and demo recording over last-minute embellishments.

## 7. Open technical risks — validation gates, not unanswered design questions

| Risk | Earliest gate | Plan if it fails |
|---|---|---|
| Streamlit numeric widget silently rounds 3+ entered decimals or lacks reliable blank `None` | **Slice 1** | Stop, report actual limitation and propose minimum equivalent control; **ask owner before changing numeric-input decision**. |
| Streamlit hidden widget state loses values or stable IDs mismatch | Slices 3, 5, 7 | Fix draft source-of-truth and stable-key handling; do not ship history before passing manual tests. |
| Python floating-point precision, overflow, signed zero, tiny changes | Slices 2, 8, 10–11 | Check finite outcomes; targeted precision/format rules; add regression tests, no business cap. |
| Chart accidentally connects unobserved years or invents points | Slice 9 | Rework into consecutive-run traces; retain numerical observations as a fallback. |
| Data-quality warnings confused with invalid input or unconfirmed drafts | Slices 6–11 | Keep distinct message categories and confirmed-only warning storage; retest UI. |
| Scenario accidentally uses historical or draft data | Slice 10 | Enforce confirmed-current-year source; baseline and reset tests. |
| Hosting/availability/connection on Demo Day | Slices 4 and 15 | Local backup, known-good Git commit, deployed smoke tests and mandatory screen recording. |
| Public-prototype remuneration confidentiality | From first UI skeleton | Display explicit synthetic/public-only warning, no sensitive demo data or unnecessary logs, no false POPIA/security assurances. |
| Methodological ambiguity of cohorts/cross-year comparability | All slices | User supplies aggregate figures, no cohort construction; use descriptive and explicitly bounded interpretation only. |

## 8. Stop point and sign-off

**Stage 3 is complete.** The build specification has enough precision to start a safe minimum skeleton, subject to owner approval. The technical feasibility of cent-level numeric input validation is an **early test gate**, not a new scope decision to make without evidence.

**Owner review checklist:**

- [ ] `spec.md` accurately reflects the established Context, Calculation and UI specifications and interview Decisions 1–42.
- [ ] The first deployed skeleton is small enough and testable.
- [ ] The build slices keep validation and recorded failures central.
- [ ] Post-core synthetic loader and optional report are correctly deprioritised.
- [ ] The technical risk/approval gates are acceptable.
- [ ] Explicit approval to begin coding has been given **after** this review.

**STOP. Do not generate or modify application code until explicit approval.**
