# Slice 4 — Cloud deployment acceptance checklist

**Status: NOT YET RUN.** Use synthetic figures only. Do not mark any check as
passed based on a successful local browser session or a screenshot of the
Streamlit deployment UI. The owner (or an authorised connected deployment tool)
will record observations from the real public app in a clean browser.

**App URL:** PENDING

**GitHub repo + branch:** PENDING

**Deployed Git commit hash:** PENDING

**Cloud Python version:** Select 3.11; actual patch/build PENDING

**Cloud Streamlit version:** Intended 1.65.0 (`requirements.txt`); PENDING confirmation

| ID | Action | Expected | Actual observed | Status | Issue / fix / retest |
|---|---|---|---|---|---|
| DEP-01 | Open public `streamlit.app` URL in clean/private browser | App opens independently of AI chat | Not yet observed | NOT RUN | — |
| DEP-02 | First load with no confirmed data | Calculate onboarding, no exposed results; Screen 2/3 navigation disabled | Not yet observed | NOT RUN | — |
| DEP-03 | Click Start | Same-screen inputs revealed; privacy/full-ZAR information available | Not yet observed | NOT RUN | — |
| DEP-04 | Enter `2026`, top `10000000`, bottom `1000000`, click Calculate (T001) | Screen 2 shows **10.0 : 1** and correct confirmed values | Not yet observed | NOT RUN | — |
| DEP-05 | Navigate Explore → Understand → Calculate | Baseline/confirmed result persists; draft inputs restored | Not yet observed | NOT RUN | — |
| DEP-06 | Edit draft top without calculating; navigate to results | Previous confirmed ratio is unchanged | Not yet observed | NOT RUN | — |
| DEP-07 | Set bottom `0`; click Calculate (T004) | Blocking error, no inf/NaN, previously confirmed result preserved | Not yet observed | NOT RUN | — |
| DEP-08 | Clear bottom; click Calculate (T006) | Missing-input error (different from zero), previous confirmed result preserved | Not yet observed | NOT RUN | — |
| DEP-09 | In a fresh session attempt results navigation | Screens 2 and 3 inaccessible without first confirmed result | Not yet observed | NOT RUN | — |
| DEP-10 | Execute local fallback `python -m streamlit run app.py` | Local app still launches; independent tests pass | Previously owner verified Slice 3 locally, not reconfirmed for Slice 4 | NOT RUN | — |
| DEP-11 | Record exact deployed commit and environment | GitHub commit, Python minor/patch if visible, and Streamlit version documented | Not yet observed | NOT RUN | — |

**Independent calculation-layer regression:** run
`python -m pytest -q tests/test_calculations.py` locally. T005 (negative
remuneration) is checked directly at this layer even if browser inputs prevent
negative values.

**Gate:** All DEP checks and local regression pass; URL opens publicly;
source is actually in GitHub. Record issues and retests before approval.
