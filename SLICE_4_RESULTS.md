# Slice 4 — Deploy first skeleton (12 October 2026)

**Status: PARTIALLY COMPLETE — deployment package and local automated checks pass; GitHub publication, Streamlit Community Cloud deployment, and public clean-browser checks remain NOT VERIFIED.**

The owner approved Slice 3 after reporting successful local Mac browser testing on **Python 3.11.2 / Streamlit 1.65.0**, and authorised Slice 4. See `SLICE_3_RESULTS.md` for the owner-observed outcomes.

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
| GitHub publication and remote commit | No connected GitHub account and no authenticated remote available in this environment | **NOT DONE** |
| Streamlit Community Cloud deployment | No authorised authenticated Streamlit Community Cloud workspace accessible to this assistant | **NOT DONE** |
| Public app clean-browser smoke | No actual deployed URL available | **NOT RUN** |

**Failure/blocker:** External publishing requires authentication to the owner's GitHub and Streamlit Community Cloud accounts. This is an **access blocker**, not evidence of failing code or an unsuccessful Cloud deployment. The source has not been presented as hosted.

## Proposed deployment configuration (pending live verification)

- GitHub repository: **PENDING OWNER CONNECTION/PUBLISH**; suggested root contains `app.py`, `calculations.py`, `requirements.txt`, `.gitignore`, `README.md`, and `tests/`.
- Branch: `main` unless owner's existing Git repository requires another.
- Streamlit Cloud main file: `app.py`.
- Python: choose **3.11** in Advanced settings to match owner's working Python 3.11.2 minor release; Cloud patch version **PENDING**.
- Streamlit: **1.65.0**, pinned in the runtime requirements.
- User secrets/API keys: **none required**.
- Public URL: **PENDING**.
- Remote GitHub commit hash: **PENDING**.
- Do not include real company remuneration data in the public repository or demo.

## Next steps to satisfy Slice 4 gate — NOT further development slices

1. Publish the extracted project files to the owner's GitHub repository, preserving the repository-root structure; record the actual commit hash.
2. Deploy from that repository at `https://share.streamlit.io/`, selecting Python **3.11** in Advanced settings, with main file path `app.py`.
3. Observe deployment/build logs; report any dependency/runtime failures verbatim (excluding secrets or sensitive data) before changing architecture or library versions.
4. Open the **actual** public URL in a clean/private browser and perform DEP-01 through DEP-11 from `SLICE_4_CLOUD_CHECKS.md`, including T001/T004/T006, navigation and draft preservation.
5. Independently verify local execution still works as fallback.
6. Record URL, GitHub commit, Cloud Python/Streamlit versions, actual pass/fail outcomes, fixes and retests; request owner's review before Slice 5.

**Scope boundary:** No robust dirty-state workflow, optional current-year context, historical inputs, Plotly chart, scenario simulator, synthetic loader or report feature was added in Slice 4.

**Gate assessment:** **NOT YET COMPLETE**. Local automated checks pass, but the build plan explicitly requires GitHub publication and a successful independently opening public app. Do not mark Slice 4 complete until those have been observed and recorded.

## Local source checkpoint

Prepared source was committed in the assistant's **isolated local Git repository**
for traceability: `357341d34ea279b58865c72a62b9c2393b14cc85`. This is **not** an existing project Mac/GitHub
history, a GitHub push, or the Cloud's deployed commit. The owner's published
GitHub commit will have its own hash and must be recorded separately.

**Resolved documentation-only incident:** A shell quoting mistake occurred while
inserting the local commit hash in this log. It affected only the text of the
log and was corrected before release; no application code or calculations were
changed. The automated tests remained green.
