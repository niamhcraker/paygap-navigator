# Slice 2 — Basic calculation + validation (9 October 2026)

**Status: COMPLETE — approved by the project owner after an additional local Mac test run (9 October 2026).**

## Approved, narrow objective

Implement and independently test the current-year vertical remuneration ratio and basic blocking validation in `calculations.py`. Return a simple, structured outcome for a future Streamlit interface. Do not build Screen 1/2/3, historical calculations, optional statistics, quality warnings, Plotly or scenarios early.

## Files changed

| File | Change |
|---|---|
| `calculations.py` | **New:** current-year core validator and ratio calculation. |
| `tests/test_calculations.py` | **New:** independent `pytest` tests for known answers and basic safety. |
| `SLICE_1_RESULTS.md` | Recorded project owner's approved Slice 1 completion and Mac versions: **Python 3.11.2, Streamlit 1.65.0**. |
| `README.md` | Added instructions to run the Slice 2 tests and identified limits of this slice. |
| `SLICE_2_RESULTS.md` | **New:** this implementation and verification record. |

The approved `spec.md`, `build_plan.md`, existing `requirements.txt` and Slice 1 spike code were **not modified**. No `app.py` exists yet. No Cloud deployment or runtime dependency update was attempted.

## Implementation summary (no application interface yet)

`calculate_current_year(record)` receives a dictionary containing `year`, `top_5_total`, and `bottom_5_total`. The outcome always has `success`, `results`, `errors` and `warnings`.

- Check that financial year is a positive integer, not a boolean; no arbitrary recent-year range is imposed.
- Reject missing, nonnumeric, boolean, negative and non-finite required remuneration inputs. Missing is not silently interpreted as zero.
- Require `bottom_5_total > 0`; allow `top_5_total == 0` per the approved calculation rules.
- Produce `ratio = top_5_total / bottom_5_total`, with simple one-decimal plain-language interpretation.
- Return **no result** when validation fails; errors include machine-friendly `field` / `code` and a user-friendly `message`. Gather multiple basic validation errors together.
- Use Python's standard-library `Decimal` for the division *internally* to avoid converting huge, balanced integers to floats prematurely. Return only a finite, usable numeric ratio; reject overflow and the conversion of a nonzero tiny ratio into false `0.0`. There is no remuneration-business maximum.
- The `warnings` field is present but empty at this slice. Data-quality warnings, optional input checks, manual-precision rejection and advanced formatting are explicitly reserved for their scheduled future slices.
- No Streamlit import, API, database, file persistence, AI inference or network access in `calculations.py`.

## Test execution and results

**Execution environment:** assistant container running **Python 3.13.5**, with **pytest 9.0.2**. This is NOT a test run on the project owner's Mac. Streamlit is not needed for tests of `calculations.py`.

Commands (project directory):

```bash
python -m pytest -q tests/test_calculations.py
python -m compileall -q calculations.py tests/test_calculations.py
```

**Final actual output:** `37 passed in 0.06s` (pytest); Python compile check exited successfully with no errors.

The first test run had `36 passed in 0.10s`. During review, one additional safety edge was identified: a mathematically nonzero, extremely small ratio could underflow to float `0.0`. A guard and regression test were added; final suite reported **37 passed**. **No failed tests** were observed in either run.

### Required known-answer tests (independent calculation-layer call)

| ID | Input | Expected | Actual | Status |
|---|---|---|---|---|
| **T001** | `T=10,000,000`, `B=1,000,000`, `year=2026` | ratio `10.0:1`, meaningful explanation | `success=True`, `ratio=10.0`, interpretation includes `10.0 times` | **PASS** |
| **T004** | `T=20,000,000`, `B=0` | blocked, no result/infinity | `success=False`, `results=None`, `zero_denominator` | **PASS** |
| **T005** | `T=-1`, `B=1,000,000` | blocked even without front-end limits | `success=False`, `results=None`, `negative` | **PASS** |
| **T006** | `T` populated, `B=None` | missing value blocked, no silent zero | `success=False`, `results=None`, `missing` | **PASS** |

Additional `pytest` cases covered missing top/year; invalid years (including booleans/fractions); multiple simultaneous errors; invalid money types (text, boolean, complex, list, dictionary); negative bottom; `NaN` and ±infinity; zero top; cent-valued numerators/denominators; valid huge balanced values (`10**400 / 10**399 = 10.0`); extreme quotient overflow; a nonzero tiny ratio that would underflow in float; and a malformed record.

**Direct smoke-check output:**

```text
T001: success=True; ratio=10.0; error_codes=[]
T004: success=False; ratio=None; error_codes=['zero_denominator']
T005: success=False; ratio=None; error_codes=['negative']
T006: success=False; ratio=None; error_codes=['missing']
```

## Remaining limitations / handoff to the approved next slices

- **This is not yet a runnable application:** no `app.py`, no navigation, no draft/confirmed snapshot and no Streamlit widget validation. These belong to Slices 3–5.
- **Manual >2-decimal precision rejection has not been implemented yet.** It is specified for the later input/validation work, with the unresolved requirement that `1.234` remain invalid across widget reruns and until deliberate correction. Do not mistake the Slice 1 detection spike for an end-to-end pass.
- **No below-one warning or optional-statistic warning yet** (Slice 6). This is intentional incremental scope separation.
- **No historical records, scenario results, adaptive ratio precision or Plotly** (Slices 7–11).
- Plain-language interpretation presently uses the required default one decimal. Bounded adaptive presentation rules remain to be implemented in the UI/formatting slice; tiny/nonzero results must be reviewed for truthful representation then.
- The approved Mac environment is **Python 3.11.2 + Streamlit 1.65.0**. On 9 October 2026 the owner independently reran `tests/test_calculations.py` on that Mac and reported **37 passed**, then explicitly approved Slice 2 as complete. Exact local pytest version and elapsed runtime were not supplied.
- No cloud/browser or usability test is meaningful for this calculation-only module. Slice 4 handles the first hosted end-to-end skeleton.

**Gate:** PASSED. Assistant automated run: **37 passed** under Python 3.13.5. Owner-reported Mac automated run: **37 passed** under Python 3.11.2 / Streamlit 1.65.0. The owner explicitly approved Slice 2 and authorised Slice 3 on 9 October 2026. Preserve the limitations above for later slices; this approval does not claim that those later features already exist.
