# PayGap Navigator — development and deployment guide

The project currently contains the approved **thin three-screen Streamlit
skeleton**. Only the current-year ratio is active; the historical chart,
additional context and scenario simulator are reserved for later build slices.
Use synthetic or publicly available aggregate remuneration figures only.

## Slice 1 — Historical environment/risk spike instructions

The separate `spikes/` experiment tests feasibility of blank numeric inputs
and maximum-two-decimal *rejection*. It is not the main application. The main
application entrypoint is `app.py`.

On a compatible Python environment with working package access:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m streamlit run spikes/numeric_input_spike.py
```

In a second shell with `pytest` installed:

```bash
python -m pip install pytest
python -m pytest -q spikes/test_numeric_input.py
```

**Mandatory manual browser check** (both candidates: `%.2f` and `%.4f`):

1. Confirm initial input is visibly empty and server output is `None`.
2. Enter `0`; ensure it is distinguishable from blank.
3. Enter `1`, `1.2`, `1.23`: confirm widget accepts values without changing them.
4. Enter **`1.234`** and press Tab/Enter. Observe the value in the field **and** the
   `Server widget value` output. A valid experiment must retain the extra
   precision so that it can be rejected; automatically becoming `1.23` is a
   **FAIL**. Browser-side step-validation that merely refuses entry must also
   be noted: whether invalid draft text can be preserved remains a requirement.
5. Hide and re-show the widget. Check the saved draft value is restored.
6. Record actual results, Streamlit version, Python version and browser.

AppTest exercises Streamlit's Python side only. **It cannot verify that raw
browser-typed `1.234` reaches Python without being rounded or rejected.**

Do not substitute a text input or relax the agreed precision rule without the
project owner's approval. See `SLICE_1_RESULTS.md`.

## Slice 2 — Basic calculation and validation

**Slice 2 is a calculation-layer module and tests, not yet a runnable PayGap Navigator UI.**
The first three-screen application belongs to Slice 3, and Cloud deployment to Slice 4.

From the project root, with the Python environment activated:

```bash
python -m pip install pytest     # development/testing only; not a Cloud requirement
python -m pytest -q tests/test_calculations.py
```

The public entrypoint in `calculations.py` is `calculate_current_year(record)`.
It accepts a dictionary containing `year`, `top_5_total` and `bottom_5_total`,
and returns a dictionary containing `success`, `results`, `errors` and `warnings`.
Expected validation failures set `success=False` and `results=None`, with field-
addressable messages in `errors`. The `warnings` list is empty in Slice 2;
optional-context and below-one warnings are added in Slice 6 as planned.

The approved local Slice 1 spike ran on the project owner's **Python 3.11.2 /
Streamlit 1.65.0** Mac environment. Slice 2's 37 calculation tests passed both in the assistant environment
(Python 3.13.5) and in the owner-reported Mac environment (Python 3.11.2);
see `SLICE_2_RESULTS.md` for the exact reporting and approval status.

The manually entered **more-than-two-decimals** rule is a mandatory later
validation gate (Slice 6) tied to preservation of unnormalised widget edits.
It is not yet a completed feature of this Slice 2 calculation-only module.

## Slice 3 — Thin three-screen local journey

From the project root in the **existing Mac environment** that passed the Slice 1
risk spike (Python 3.11.2 / Streamlit 1.65.0):

```bash
python -m streamlit run app.py
```

Use **synthetic or publicly available aggregate remuneration data only**.
The three-screen journey currently covers the **current financial year only**:

1. Click **Start navigating your pay gap →** on the Calculate screen.
2. Enter **Financial year ending**, **Top-5% aggregate remuneration (R)** and
   **Bottom-5% aggregate remuneration (R)** as full-rand figures.
3. Click **Calculate my pay gap →** to validate and confirm; read the ratio and
   interpretation on **Understand & Track**.
4. Open **Explore** to see the confirmed baseline. The scenario controls are
   explicitly a development placeholder in this slice.
5. Navigate back to Calculate. Drafts survive screen changes; the confirmed
   result remains from the last successful calculation.

Run the independent calculation tests:

```bash
python -m pytest -q tests/test_calculations.py
```

**Slice 3 manual acceptance checks** are in `SLICE_3_MANUAL_CHECKS.md`.
Record the *actual* Mac browser outcomes there; browser test results must not
be inferred from successful compilation or passing calculation tests.

**Deliberate limitations:** Historical inputs, optional context, conditional
unapplied-change warnings, explicit rejection of manually entered amounts
containing more than two decimal places, scenarios and adaptive display
precision are not yet implemented. Their build gates remain in the frozen
`build_plan.md`. This development skeleton must not be represented as the
finished decision-support tool.

**Deployment is not part of Slice 3.** GitHub/Streamlit Community Cloud release
and clean-browser hosted checks belong to Slice 4. The runtime dependencies
remain unpinned until a working local and Cloud environment is established.


## Slice 4 — Deploy the approved thin skeleton

**Current status:** Deployment files prepared. GitHub publication, actual
Streamlit Community Cloud deployment and public-browser acceptance require
completion in the owner's accounts. Do not call the deployment complete until
all acceptance checks in `SLICE_4_CLOUD_CHECKS.md` have passed.

### Confirmed local development environment

- **Python:** 3.11.2 on the owner's Mac (Python 3.11 selected in the Cloud UI).
- **Streamlit:** 1.65.0, pinned in `requirements.txt` based on successful local
  Slice 1 and Slice 3 browser tests. Cloud compatibility must still be verified.
- **Runtime dependency:** Streamlit only; `pytest` is a development/test tool,
  not a Cloud requirement. Plotly and Pandas are **not needed yet**.

### Verify locally, using the known-good environment

From the extracted `paygap_navigator` directory:

```bash
python --version
python -m streamlit version
python -m pytest -q tests/test_calculations.py
python -m streamlit run app.py
```

Expected before deployment: Python 3.11.2, Streamlit 1.65.0 and **37 passing
unit tests**; in a clean local browser T001, T004 and T006 must behave as
recorded in the Slice 3 acceptance notes. If the local `pytest` command is
missing, install it for testing (`python -m pip install pytest`); it is not in
`requirements.txt` because the Cloud app doesn't need it to run.

### Publish to GitHub (owner-controlled account)

1. Create a **new, empty repository** on GitHub (for example,
   `paygap-navigator`), preferably public for a straightforward public demo.
   Do not add example confidential remuneration data, passwords, tokens or
   `.streamlit/secrets.toml`.
2. Ensure `app.py`, `calculations.py`, `requirements.txt`, `.gitignore`,
   `README.md` and the `tests/` folder are at the **repository root**. The
   additional slice logs and spike files are optional for deployment.
3. If using Git locally, from the folder containing `app.py`:

```bash
# Only if this folder is not already a Git repository:
git init
# Stage only the intended project files; .gitignore excludes environment and secrets.
git add app.py calculations.py requirements.txt .gitignore README.md tests/   SLICE_1_RESULTS.md SLICE_2_RESULTS.md SLICE_3_RESULTS.md   SLICE_3_MANUAL_CHECKS.md SLICE_4_RESULTS.md SLICE_4_CLOUD_CHECKS.md
# Configure your own author identity if Git prompts for it.
git commit -m "Deploy PayGap Navigator thin skeleton (Slice 4)"
git branch -M main
# Replace YOUR_USERNAME with your GitHub account name:
git remote add origin https://github.com/YOUR_USERNAME/paygap-navigator.git
git push -u origin main
```

If a remote named `origin` already exists, **do not re-add it**; check with
`git remote -v` and use the correct existing repository. Do not force push.
Alternatively, use GitHub's **Add file → Upload files** interface and upload
these project files, maintaining their folders. Do not upload the ZIP itself as
the app entry point: GitHub needs the extracted files.

4. Copy the resulting commit identifier from GitHub (or `git rev-parse HEAD`)
   into `SLICE_4_RESULTS.md`. A local-only Git commit is not a deployment.

### Deploy on Streamlit Community Cloud (owner-controlled account)

1. Open **https://share.streamlit.io/** and sign in with the GitHub account
   with access to that repository.
2. Click **Create app**; select **Yup, I have an app**.
3. Choose the GitHub repository and the `main` branch.
4. Set the **Main file path** to `app.py` (from the repository root).
5. Under **Advanced settings**, choose **Python 3.11**. The Cloud service
   chooses its own patch release, which may not be 3.11.2 exactly.
6. The app has **no API key or required secrets**. Deploy the app.
7. Wait for the actual app to load; if it fails, inspect the Streamlit Cloud
   logs for the first error. Do not assume success from a deployed-status icon
   alone.
8. Copy the **actual** `https://...streamlit.app` URL and run the
   `SLICE_4_CLOUD_CHECKS.md` checklist in a **clean/private browser window**.

### Accept only after checking the deployed app

- Open the public URL without being signed into ChatGPT, and verify that the
  skeleton launches independently (the **Unplugged Test**).
- First load: onboarding only; **Understand & Track** and **Explore** cannot be
  opened before a successful calculation.
- T001: financial year ending **2026**, top **10000000**, bottom **1000000**;
  click Calculate; confirm result **10.0 : 1**.
- Navigate to Explore and back; the confirmed result must persist.
- T004: return to Calculate, set bottom **0**, try again; calculation blocked,
  existing valid result preserved.
- T006: clear bottom and try again; missing-input message; prior confirmed
  result preserved.
- Confirm local fallback still starts via `python -m streamlit run app.py`.

When all checks pass, record the public link, selected Cloud Python version,
observed Streamlit version/health, GitHub commit hash, test outcomes and any
failures/fixes in `SLICE_4_RESULTS.md`. Wait for owner approval before Slice 5.

**Scope remains unchanged:** no historical inputs, additional remuneration
context, dynamic warnings, functioning scenarios, Plotly or downloadable
reports in the first deployed skeleton.

**Note on public input:** This publicly hosted prototype should be tested with
synthetic or publicly disclosed aggregate figures only; it is not a reviewed
production environment for confidential remuneration data.
