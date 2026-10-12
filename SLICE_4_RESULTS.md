# Slice 4 — Deploy first skeleton (12 October 2026)

**Status: COMPLETE — OWNER APPROVED on 12 October 2026.** The public Streamlit Community Cloud skeleton is live and passed the owner’s clean/private-browser checks. The repository and original deployed commit have been inspected through the connected GitHub account. Tests attributed to the owner are distinguished from assistant-run checks.

The owner approved Slice 3 after reporting successful local Mac browser testing on **Python 3.11.2 / Streamlit 1.65.0**, and authorised Slice 4. See `SLICE_3_RESULTS.md` for the owner-observed outcomes.

## Deployment record and verification (12 October 2026)

| Detail | Confirmed value | Evidence |
|---|---|---|
| Live URL | https://paygap-navigator.streamlit.app/ | Owner supplied; clean/private-browser opening passed according to owner |
| GitHub repository | `niamhcraker/paygap-navigator` | Owner supplied; repository directly inspected through GitHub connection |
| Branch | `main` | Owner supplied; GitHub default branch confirmed as `main` |
| Main file | `app.py` | Owner supplied |
| Cloud Python selection | `3.11` | Owner supplied; exact Cloud Python patch not independently recorded |
| Streamlit dependency | `streamlit==1.65.0` | Pinned deployment manifest prepared during Slice 4; Cloud runtime version not separately verified from deployment logs |
| Original deployed/main commit | `6db7fb06fb75445092cbf87d02c4c449c2aac324` | Owner identified as deployed/current at verification; commit independently found in the named GitHub repository |
| User approval | **Slice 4 approved as complete** | Owner explicitly approved in conversation |

The owner's Mac test environment was Python **3.11.2** and Streamlit **1.65.0**. Python **3.11** was selected on Cloud. The exact Cloud Python patch and Streamlit runtime version have not been independently read from Cloud logs.

### Public cloud smoke tests — owner observed in a clean/private browser

| Check | Actual observation | Outcome |
|---|---|---|
| Public access (DEP-01) | URL loaded with no Streamlit authentication | **PASS — owner-verified** |
| Initial access guard (DEP-02 / DEP-09) | No access to results before a successful calculation | **PASS — owner-verified** |
| Start action (DEP-03) | Revealed input fields | **PASS — owner-verified** |
| T001 (DEP-04) | Year 2026; top R10,000,000; bottom R1,000,000 produced **10.0 : 1** | **PASS — owner-verified** |
| Navigation (DEP-05, confirmed result) | Screen 3 and return navigation preserved the confirmed result | **PASS — owner-verified for this journey** |
| T004 (DEP-07) | Zero bottom remuneration blocked | **PASS — owner-verified** |
| T006 (DEP-08) | Blank required amount blocked | **PASS — owner-verified** |

**No deployment or browser failures were reported.** The owner expressly approved Slice 4. Checks not separately described in the Cloud report remain unclaimed: every draft-widget restoration path (remaining DEP-05 detail), fresh Cloud-only draft-edit test without confirmation (DEP-06; passed locally in Slice 3), post-deployment recheck of Mac fallback (DEP-10), and exact Cloud patch/runtime details (part of DEP-11). These are evidence distinctions, not reported defects.

The GitHub commit is verified to exist in this repository; its association with the deployed Cloud build is based on the owner's supplied deployment information, **not** an independent inspection of the Streamlit Cloud deployment dashboard. This documentation-only update will produce a newer `main` commit; that newer documentation commit must not be mistaken for the original deployed application-code baseline.

## Narrow objective

Deploy **only the approved thin three-screen current-year ratio skeleton** to GitHub and Streamlit Community Cloud; verify T001, T004, T006 and navigation at a public URL in a clean browser. Preserve the local fallback and code-only calculation layer. Do not implement any later slice.

## Files changed or created

| File | Action and reason |
|---|---|
| `SLICE_3_RESULTS.md` | Updated with owner-reported local browser acceptance and Slice 3 approval; pre-acceptance results retained for traceability. |
| `requirements.txt` | Restored from the prior Slice 3 ZIP and provisionally pinned direct runtime dependency to `streamlit==1.65.0` (successfully tested on the owner's Mac). Cloud verification remains necessary before finalising environment confirmation. |
| `.gitignore` | Restored from prior ZIP and excluded virtual environments, Python caches, Streamlit secrets, macOS metadata, and `.env` secrets. |
| `README.md` | Added detailed GitHub publishing, Community Cloud creation, Python 3.11 selection, and post-deploy validation instructions. |
| `SLICE_4_CLOUD_CHECKS.md` | New real-browser Cloud acceptance and local fallback checklist, all Cloud outcomes initially NOT RUN. |
| `SLICE_4_RESULTS.md` | This evidence log. |
| `spikes/` | Unchanged files restored from previous Slice 3 release package for complete project history (not part of the main app). |

**Unchanged functional files:** `app.py`, `calculations.py`, `tests/test_calculations.py`.

**Frozen references unchanged:** `/mnt/data/spec.md`, `/mnt/data/build_plan.md`.

## Actual checks run in the assistant environment

| Check | Observed result | Status |
|---|---|---|
| Unit regressions: `python -m pytest -q tests/test_calculations.py` | **37 passed in 0.07s** | **PASS** |
| Python syntax: `python -m compileall -q app.py calculations.py tests/test_calculations.py` | No compile errors; exit code 0 | **PASS** |
| Deployment manifest check | Exactly one direct runtime dependency: `streamlit==1.65.0`; `pytest`, Pandas, Plotly not listed | **PASS** |
| README and Cloud checklist static checks | Local run instruction, T001, and DEP-11 environment checkpoint present | **PASS** |
| Mac local browser tests (previous slice) | Owner reported valid 3-screen journey; T001 10.0:1; draft/confirmed separation; zero/missing blocking | **PASS — owner-reported Slice 3** |
| Streamlit launch in assistant container | Streamlit unavailable in assistant Python 3.13.5 environment; no successful native launch here | **NOT RUN** |
| GitHub publication and original deployed commit | Owner published to `niamhcraker/paygap-navigator`; original deployed commit `6db7fb06fb75445092cbf87d02c4c449c2aac324` confirmed to exist via connected GitHub | **COMPLETE — owner publication / repository inspected** |
| Streamlit Community Cloud deployment | Owner published the three-screen app at https://paygap-navigator.streamlit.app/ | **COMPLETE — owner-reported** |
| Public app clean-browser smoke | Owner ran the specified essential smoke tests using clean/private browser; details above | **PASS — owner-verified** |

**Resolved access blocker:** GitHub and Cloud deployment were completed by the owner. The connected GitHub repository and original deployed commit have now been inspected. The assistant has not separately executed the Cloud smoke tests or inspected the Cloud deployment dashboard.

## Verified deployment configuration

- GitHub repository: `niamhcraker/paygap-navigator`, branch `main`.
- Main application file: `app.py`.
- Original deployed code commit: `6db7fb06fb75445092cbf87d02c4c449c2aac324` (verified GitHub commit, owner-assigned deployed baseline).
- Streamlit Community Cloud Python selection: **3.11**; exact patch unrecorded.
- Direct runtime dependency: `streamlit==1.65.0` in the deployment preparation manifest; running Cloud version not independently logged.
- User secrets/API keys: none required for this skeleton.
- Public URL: **https://paygap-navigator.streamlit.app/**.
- Public app and essential tests: passed in the owner's clean/private-browser check.

## Completion, remaining evidence and scope boundary

1. GitHub publication: **completed by owner**, original deployed commit captured above.
2. Community Cloud deployment: **completed by owner**, live public URL captured above.
3. Clean/private-browser essential acceptance: **passed according to owner**, including access guard, Start, T001, navigation, T004 and T006.
4. Previous local fallback: passed during Slice 3 on Mac; not independently retested after Cloud launch.
5. Optional documentation follow-up: exact Cloud Python patch/Streamlit runtime and any unreported individual DEP-05/06/10 checklist outcomes remain unverified. Do not assert they passed without new evidence.

**Scope boundary:** No robust dirty-state workflow, optional current-year context, historical inputs, Plotly chart, scenario simulator, synthetic loader or report feature was added in Slice 4.

**Gate assessment: COMPLETE — explicitly approved by the owner on 12 October 2026.** Deployment and clean-browser testing satisfied the owner's acceptance of Slice 4. Do not begin Slice 5 until separately authorised.

## Local source checkpoint

Prepared source was committed in the assistant's **isolated local Git repository**
for traceability: `357341d34ea279b58865c72a62b9c2393b14cc85`. This is **not** an existing project Mac/GitHub
history, a GitHub push, or the Cloud's deployed commit. The owner's original deployed GitHub commit has now been recorded and independently located: `6db7fb06fb75445092cbf87d02c4c449c2aac324`.

**Resolved documentation-only incident:** A shell quoting mistake occurred while
inserting the local commit hash in this log. It affected only the text of the
log and was corrected before release; no application code or calculations were
changed. The automated tests remained green.
