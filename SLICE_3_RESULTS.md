# Slice 3 — Thin three-screen local journey (9 October 2026)

**Status: COMPLETE — owner-approved after successful local Mac browser verification (reported 12 October 2026).**
The project owner authorised this slice after independently rerunning Slice 2 on
macOS (**Python 3.11.2 / Streamlit 1.65.0; 37 passed**) and approving Slice 2.
Cloud deployment is exclusively Slice 4; it was **not** attempted here.

## Narrow objective

Connect the approved Slice 2 current-year calculation to a very small standalone
Streamlit interface: onboarding and 3 required current-year fields on Calculate,
confirmed ratio and aggregates on Understand & Track, baseline-only placeholder
on Explore, and gated three-screen navigation. Keep draft data separate from
confirmed results. Do not implement future feature slices early.

## Files created or modified

| File | Action |
|---|---|
| `SLICE_2_RESULTS.md` | Updated to record owner's successful local Mac test (`37 passed`) and explicit Slice 2 approval. |
| `app.py` | **Created.** Single-script conditional 3-screen interface; initial onboarding reveal; current-year core fields; explicit confirmation calling `calculate_current_year()`; separate draft and confirmed state; minimal guided navigation; baseline-only Explore placeholder; public-prototype privacy and full-ZAR notes. |
| `README.md` | Updated local run instructions and accurately distinguished scope and test environment. |
| `SLICE_3_MANUAL_CHECKS.md` | **Created.** Structured, repeatable Mac browser checklist with expected results and initially unfilled actual results. |
| `SLICE_3_RESULTS.md` | **Created.** This report. |

The approved `spec.md` and `build_plan.md`, `calculations.py`,
`tests/test_calculations.py`, and `requirements.txt` remain **unchanged**.
No historical inputs, context stats, scenario controls, Plotly, report export,
synthetic loader, Cloud/GitHub deployment, new modules or database were added.

## Implementation details

- Uses `st.session_state` for `pn_started`, `pn_screen`, a seven-field
  `pn_draft_current` record (four optional fields remain `None`), and a separate
  copy of the last valid `pn_confirmed_current` plus `pn_confirmed_result`.
  Draft and confirmed history lists exist but remain empty and uneditable.
- Widget callbacks copy current-year input into draft state before widgets are
  removed; returning to Screen 1 reconstructs widget keys from the draft.
- The Calculate button runs `calculate_current_year(deepcopy(draft))`. On success,
  it separately snapshots the confirmed record and result and shows Screen 2.
  On validation failure, it leaves the previously confirmed data intact,
  remains on Screen 1 and shows field-addressed error messages. An unexpected
  calculation exception shows a generic message rather than a traceback.
- Navigation to Screens 2 and 3 is disabled before first success. After
  success, top-stage navigation and specific back/forward controls are present.
  Navigating alone does not call the calculator or modify the confirmed result.
- Screen 2 shows the default one-decimal ratio, confirmed aggregates and the
  basic interpretation. Screen 3 displays **only** the confirmed baseline and
  explicitly states that the simulator is not implemented yet.
- Results screens contain a permanent note that the visible figures reflect
  **last confirmed data**. The conditional unapplied-changes warning and
  canonical data comparison are intentionally deferred to Slice 5.
- Screen 1 shows the required financial-year-end help text, full-rand guidance,
  total-remuneration explanation and public-hosted-prototype confidentiality
  warning. No payroll/individual records are requested.

## Checks actually run in assistant environment

| Check | Expected | Actual | Status |
|---|---|---|---|
| `python -m pytest -q tests/test_calculations.py` | Slice 2 regressions stay green | `37 passed in 0.06s` | **PASS** |
| `python -m compileall -q app.py calculations.py tests/test_calculations.py` | No syntax errors | Success (exit 0) | **PASS** |
| Static Python AST check | Three screen render functions; `calculate_current_year()` imported and used; no Plotly dependency yet | All assertions passed | **PASS** |
| Simulated state-flow smoke with a minimal fake Streamlit object | First-success gate, T001 10.0:1 confirmation, navigation, independent snapshots, T004 and T006 failure preservation | All assertions passed | **PASS — simulated only** |
| Native Streamlit app launch | App starts on Mac and browser renders | Not available in assistant environment (`streamlit` is not installed) | **NOT RUN** |
| Mac real-browser manual checks `UI3-01` to `UI3-12` | Onboarding, blank fields, T001/T004/T006, navigation, draft preservation, failed-confirmation integrity | No Mac result submitted for this slice | **NOT RUN** |
| Cloud-hosted smoke test | Public URL works | Slice 4 only | **NOT DUE** |

**Testing limitation:** Assistant environment is Python 3.13.5, without
Streamlit. A package-index lookup failed because network DNS resolution was
unavailable. The passed mock test is **not a substitute** for real widget or
browser verification, which must be conducted by the project owner locally.

## Version-control checkpoint and incident

A first attempt to commit failed with Git's `Author identity unknown` error
because the assistant container has no configured commit author. No code was
lost. The checkpoint was successfully created using a **one-command,
repository-local Git author override** identifying the build assistant (not
impersonating the project owner), without changing global Git settings.
Checkpoint commit: **`eb90eb3`**. This is a local container repository commit,
**not** a GitHub push and **not** evidence of a deployed or browser-tested app.
The checkpoint is provisional until the manual acceptance gate passes.

## Original mandatory manual gate (historical; now owner-approved)

See `SLICE_3_MANUAL_CHECKS.md`. On the Mac with working Streamlit:

```bash
python -m streamlit run app.py
```

Key expected outcomes: blank is not zero; valid T001 navigates to Screen 2;
T004/T006 remain on Screen 1 with clear messages; first-success gating; full
three-screen navigation; editing draft without confirmation never changes
previously confirmed figures; the draft restores when returning to Screen 1.
Record actual outcomes, failures, fixes and retests before marking the slice
fully complete. If any Mac browser check fails, correct and rerun before
proceeding to Slice 4.

## Intentional open limitations (not Slice 3 regressions)

- The confirmed-vs-draft *conditional* unapplied-changes warning and fully
  robust state lifecycle are implemented in **Slice 5**, not here.
- The authoritative more-than-two-decimal manual-input precision rejection,
  optional remuneration fields and data-quality warnings are in **Slice 6**.
  The Slice 1 experiment verified detection is feasible on the Mac; it did
  **not** make the Slice 3 UI a complete precision-validating app. Do not use
  this skeleton with confidential or decision-critical organisational data.
- Historical inputs/analysis, Plotly and functioning scenarios remain later
  slices (7–10), with additional quality/formatting work in Slice 11.
- No deployment or public browser URL exists yet. That is the Slice 4 gate.

**Original pre-approval gate (superseded by the owner acceptance update below):** The Slice 3 implementation and available automated/simulated
checks have passed, but the full **local UI acceptance gate remains pending**
actual Mac browser results. **STOP before Slice 4** and request the owner's
review and manual test observations; do not infer successful browser testing.


## Slice 3 completion update — owner-reported Mac browser verification (12 October 2026)

The project owner independently ran the Slice 3 application in the known local
**Python 3.11.2 / Streamlit 1.65.0** Mac environment and reported that the
three-screen browser journey works as intended. Specifically, the owner verified:

| Browser check reported | Actual outcome (owner report) | Status |
|---|---|---|
| Start action reveals inputs | Inputs revealed correctly | PASS — owner-observed |
| T001 current-year inputs | Result displayed **10.0 : 1** | PASS — owner-observed |
| Move between Screens 1/2/3 | Confirmed result remained available and unchanged | PASS — owner-observed |
| Edit drafts without recalculating | Previously confirmed result did not change | PASS — owner-observed |
| Bottom-5% zero and blank required inputs | Both blocked; previous valid result preserved | PASS — owner-observed |

The owner confirmed that local browser acceptance was satisfactory and explicitly
**approved Slice 3 as complete** on 12 October 2026, authorising Slice 4.
This replaces the earlier "pending" acceptance state above. The original
pre-acceptance test log is retained as historical evidence. The assistant did
not personally execute the Mac browser tests; the stated actual outcomes are
owner-reported. No claim is made that the Cloud app has been deployed or tested.
