# Slice 3 — Mac browser acceptance checklist

**Status: NOT YET EXECUTED by the assistant.** Streamlit is unavailable in the
assistant runtime. The project owner needs to run this checklist on the Mac
(Python 3.11.2 / Streamlit 1.65.0) and report observations. Do not mark a
browser check PASS until it has actually been performed.

From the project root, run:

```bash
python -m streamlit run app.py
```

Use **synthetic values only**. For each check, record actual outcome, PASS/FAIL,
issues/fixes and retest result. Do not expose confidential remuneration data.

| ID | Action | Expected result | Actual | Status | Issue/fix/retest |
|---|---|---|---|---|---|
| UI3-01 | Open app in a fresh browser session | CALCULATE onboarding appears; input fields hidden; results navigation disabled | Not observed | NOT RUN | — |
| UI3-02 | Click **Start navigating your pay gap →** | Inputs reveal on same Screen 1; privacy/full-rand/total-remuneration notes visible | Not observed | NOT RUN | — |
| UI3-03 | Inspect initial amount fields | Both amounts blank, not zero | Not observed | NOT RUN | — |
| UI3-04 | Enter year 2026, T=10,000,000, B=1,000,000; click Calculate | Screen 2 shows 10.0:1, correct totals and interpretation (T001) | Not observed | NOT RUN | — |
| UI3-05 | Navigate **Explore** | Screen 3 shows same confirmed ratio and amounts; scenarios expressly unavailable | Not observed | NOT RUN | — |
| UI3-06 | Navigate back to Understand, then Calculate | All entered draft values restored; no second onboarding click | Not observed | NOT RUN | — |
| UI3-07 | Change draft T to 20,000,000; navigate to Screen 2 without Calculate | Screen 2 still shows last confirmed 10.0:1; caption says results use last confirmed data | Not observed | NOT RUN | — |
| UI3-08 | Return to Calculate, set bottom B=0, click Calculate (T004) | Remain on Screen 1 with zero-denominator error; old confirmed result remains after navigation | Not observed | NOT RUN | — |
| UI3-09 | Clear bottom value entirely; click Calculate (T006) | Remain on Screen 1; missing-input message; zero and blank treated differently | Not observed | NOT RUN | — |
| UI3-10 | Enter negative T=-1 and a valid bottom, click Calculate | Blocking message or widget stops negative entry; direct calculation-layer T005 already separately tested | Not observed | NOT RUN | — |
| UI3-11 | With no confirmed data in a fresh browser session, attempt top navigation to Screen 2/3 | Results inaccessible | Not observed | NOT RUN | — |
| UI3-12 | Click Calculate with valid corrected figures after failed attempts | New confirmed result on Screen 2; errors cleared | Not observed | NOT RUN | — |

**Known intentional limitations at this slice:** conditional **unapplied-changes**
warning is added in Slice 5; manual **more-than-two-decimal rejection** and
optional current-year warnings are added in Slice 6. Test those separately at
their own gates; do not mark them as implemented now. No Cloud test is expected
until Slice 4.

**Browser acceptance gate:** PENDING until the recorded manual outcomes meet
UI3-01 through UI3-12. Any discovered failure must be documented and fixed
before claiming Slice 3 complete.
