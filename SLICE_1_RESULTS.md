# Slice 1 — Environment + numeric-input risk spike (9 October 2026)

**Status: APPROVED COMPLETE by the project owner, 9 October 2026. Core numeric-input feasibility passed in owner-reported local Mac browser checks.**

**Evidence attribution:** Browser observations below were made and reported by the project owner on their Mac; they were **not** executed or independently witnessed in the assistant's container. The assistant's earlier container execution was unable to install Streamlit. Do not conflate the two environments.

This slice is an isolated feasibility experiment, not the PayGap Navigator application. It does not implement the production `app.py`, `calculations.py`, historical analysis, scenario simulator or Cloud deployment. The approved `spec.md` and `build_plan.md` remain unchanged.

## Objective and acceptance criteria

Establish a working local Python/Streamlit runtime and verify with a **real Streamlit browser UI** that `st.number_input` can:

1. Initialise blank as Python `None`, distinct from explicitly entered zero.
2. Accept manually entered `1`, `1.2` and `1.23`.
3. Pass an entered `1.234` to Python with its excessive precision **before** any display normalisation, making a blocking validation error technically possible.
4. Preserve a valid independent draft after hiding and restoring its widget.
5. Confirm basic environment/package feasibility; leave actual hosted deployment to Slice 4.

The frozen application specification additionally requires **invalid over-precise entries to remain in editable draft data and be blocked at confirmation**. Detecting them in this spike does not itself prove that complete production workflow: it must be demonstrated during the validation/interface slices.

## Files created in Slice 1

- `spikes/numeric_input_spike.py` — isolated Streamlit UI experiment with `%.2f` and diagnostic `%.4f` formatting, server-side precision observation and draft-preservation controls.
- `spikes/test_numeric_input.py` — optional `AppTest` backend probes; these do not prove raw browser-entry behaviour.
- `requirements.txt` — provisional Streamlit dependency, **not yet pinned** to a known-good version.
- `.gitignore`, `README.md` and this log — setup guidance and results.
- A local Git repository was initialised in the assistant environment but **no commit made**. Repository/Cloud rollout belongs to later slices.

## A. Project owner's local Mac browser results (reported after the first spike attempt)

| Check | Owner's observed outcome | Assessment |
|---|---|---|
| Local Streamlit starts on Mac | Spike now runs successfully in a Mac browser | **PASS — locally observed by owner** |
| Blank vs explicit zero | Blank remains distinguishable from entered `0` | **PASS — locally observed by owner** |
| Ordinary input precision | `1`, `1.2`, `1.23` accepted | **PASS — locally observed by owner** |
| Critical extra-decimal observation | Typing `1.234` displayed **“OVER-PRECISE VALUE OBSERVED BY PYTHON — can reject”**, **before** the numeric widget visually reverted to `1.23` | **PASS for detection-before-normalisation feasibility**; see caveat below |
| Hide/reveal draft preservation | Entered `1234.56`, unchecked **Show numeric input**, then rechecked; value restored | **PASS — locally observed by owner** |
| Local Python + Streamlit versions | Owner reports **Python 3.11.2** and **Streamlit 1.65.0** for the successful Mac browser checks | **RECORDED — owner-reported** |
| Browser identity/version | Owner reports local Mac browser test; browser and version not supplied | **Not yet documented** |
| Local `AppTest` suite | No Mac `pytest` result reported | **Not independently confirmed; optional complementary probe** |
| Streamlit Community Cloud | No deployment attempted; scheduled for Slice 4 | **Not part of Slice 1 deployed acceptance** |

### Important qualification: `1.234` visually reverted to `1.23`

The decisive positive result is that **Python observed the unrounded `1.234`**. A validation function can therefore identify and block the original over-precise amount rather than silently accepting `1.23`.

However, the widget's subsequent visual reversion is a **real interface risk**, not something to ignore. The spike did **not** establish that an invalid `1.234` remains visibly editable or that the persistent draft retains it after all subsequent reruns/navigation. The production implementation must ensure:

- over-precise source values are caught and confirmation is blocked **before** any normalisation can conceal the error;
- the value held in the authoritative draft remains invalid until the user deliberately corrects it, rather than being silently replaced by the displayed `1.23`;
- the error message and editable input are not misleading after Streamlit reformats the field;
- the prior confirmed data is not overwritten after a precision error.

These are mandatory follow-up checks when actual input validation and draft/session-state workflows are implemented (especially Slices 3, 5 and 6). **Do not silently switch input type or relax Decision 39** if a reliable implementation proves impossible. Escalate any genuine conflict for owner approval.

## B. Earlier assistant container checks (independent environment, retained for traceability)

| Check | Actual outcome | Status |
|---|---|---|
| Python environment | Python **3.13.5** available; virtual environment created | PASS for container Python only; **not** the Mac Python version |
| Streamlit import | `ModuleNotFoundError: No module named 'streamlit'` | NOT AVAILABLE in container |
| Package installation | `pip install` failed because package index was inaccessible / DNS resolution failed; reported `No matching distribution found for streamlit` | BLOCKED by container package access; **not** evidence against Streamlit on Mac |
| Spike syntax | `python -m compileall -q spikes` passed | PASS for syntax only |
| Backend `AppTest` | `1 skipped` because Streamlit was unavailable | SKIPPED, **not passed** |
| Real browser UI | No browser execution in container | NOT TESTED in container; later tested successfully on Mac as above |

## C. Environment and compatibility record

- **Known working local setting:** Project owner's **Mac**, running the provided Streamlit spike successfully in a browser, with Python and Streamlit installed.
- **Mac Python version:** **3.11.2** (owner-reported successful local environment).
- **Mac Streamlit version:** **1.65.0** (owner-reported successful local environment).
- **Browser/version:** Not yet supplied.
- **Assistant container:** Python 3.13.5; Streamlit unavailable because package installation could not reach an index.
- **Dependency file:** Provisional `streamlit` entry only. In line with Decision 40, pin exact direct-dependency versions **after the local and Cloud environments have both been demonstrated to work**.
- **Cloud platform:** Compatibility reviewed at documentation level only; actual Cloud execution and clean-browser smoke test are **Slice 4**, not Slice 1.

The project owner supplied the successful Mac Python/Streamlit version details. The commands to recheck them later are:

```bash
python --version
python -m streamlit version
```

Also record the browser used. These details establish reproducibility; they do not change the frozen input design.

## D. Acceptance assessment and stop point

**The central Slice 1 risk spike has passed on the owner's Mac:** blank is distinct from zero; ordinary cent-level inputs are accepted; over-precision is observable by Python before the widget reformats; a valid draft survives hide/reveal; and Streamlit runs locally.

**Documentation still incomplete:** browser name/version and optional Mac backend `pytest` run were not reported; Python **3.11.2** and Streamlit **1.65.0** are recorded from the owner. The invalid-entry draft-persistence risk described in section A remains an **explicit implementation test**, not evidence of a passed production validation workflow.

**Gate assessment:** The owner explicitly **approved Slice 1 as complete on 9 October 2026**. The narrow numeric-input feasibility gate is satisfied on the owner's direct evidence, and the successful local Python/Streamlit versions are recorded. Do not represent the full Streamlit application, production input validation or Cloud deployment as tested or complete.

**Next gate:** The owner explicitly authorised Slice 2 on 9 October 2026. Slice 1 evidence is frozen; Slice 2 implementation and testing are logged separately.

## Supporting Streamlit documentation (not a substitute for observed behaviour)

- [`st.number_input`](https://docs.streamlit.io/develop/api-reference/widgets/st.number_input) documents `value=None` and presentation formatting, but not every raw browser keystroke path.
- [Widget lifecycle](https://docs.streamlit.io/develop/concepts/architecture/widget-behavior) explains temporary widget cleanup and preservation of separate draft values.
- [Installation](https://docs.streamlit.io/get-started/installation/command-line) and [Community Cloud deployment](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy) provide platform guidance; production compatibility must be verified in Slice 4.
