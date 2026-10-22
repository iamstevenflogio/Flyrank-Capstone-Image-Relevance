# Evidence Log

This file records implementation and verification evidence for ImageMatch. It is intended to make the project reviewable and reproducible.

**Project:** ImageMatch API  
**Repository:** `https://github.com/iamstevenflogio/Flyrank-Capstone-Image-Relevance`
**Reviewer:** Steven  
**Last updated:** 2026-10-22

## Evidence Rules

For each item:

- Record the date tested
- Record the exact command, URL, or action
- Record the observed result
- Link a screenshot, JSON file, test output, or commit when possible
- Use `PASS`, `FAIL`, or `NOT YET TESTED`
- Do not claim model quality or deployment success without evidence

## Environment

| Item             | Value                                  |
| ---------------- | -------------------------------------- |
| Operating system | `Windows`                              |
| Python version   | `3.12.5`                               |
| FastAPI version  | `0.141.1`                              |
| Database         | `PostgreSQL`                           |
| AI provider      | `Google Gemini`                        |
| Gemini model     | `gemini-3.8-flash`                     |
| Local API URL    | `http://127.0.0.1:8000`                |
| Swagger URL      | `http://127.0.0.1:8000/docs`           |
| Dashboard URL    | `http://127.0.0.1:8000/`               |
| Deployed API URL | `https://imagematch-api.onrender.com/` |

## Implementation Checklist

| Area                          | Evidence required                                       | Status | Evidence / notes                                                                                                                          |
| ----------------------------- | ------------------------------------------------------- | ------ | ----------------------------------------------------------------------------------------------------------------------------------------- | --- |
| FastAPI application starts    | Uvicorn terminal shows startup completed                | PASS   | Verified locally on 2026-10-13                                                                                                            |
| Swagger docs available        | `/docs` opens and lists endpoints                       | PASS   | Verified locally on 2026-10-13                                                                                                            |
| Image listing endpoint        | `GET /images` returns JSON list                         | PASS   | Verified manually in Swagger                                                                                                              |
| Status filter                 | `GET /images?status=completed` returns filtered data    | PASS   | Verified manually in Swagger result                                                                                                       |
| Category filter               | `GET /images?category=<category>` returns filtered data | PASS   | Verified manually in Swagger result                                                                                                       |
| Single-image endpoint         | `GET /images/{image_id}` returns image and metadata     | PASS   | `GET /images/1` returned HTTP 200 with image metadata, caption, category, and confidence. Evidence: `evidence/image-detail-response.json` |     |
| Missing image behavior        | Missing image ID returns `404`                          | PASS   | `GET /images/999999` returned HTTP 404 with `{"detail": "Image not found"}`                                                               |     |
| Audit endpoint exists         | `/images/{image_id}/calls` appears in Swagger           | PASS   | Verified locally on 2026-10-13                                                                                                            |
| Audit endpoint works          | Existing image returns call list                        | PASS   | `GET /images/16/calls` and `GET /images/29/calls` returned HTTP 200 with saved AI-call records                                            |     |
| Audit endpoint missing ID     | Missing image call request returns `404`                | PASS   | `GET /images/999999/calls` returned HTTP 404 with `{"detail": "Image not found"}`                                                         |     |
| AI success logging            | Successful Gemini call stored with status/tokens/cost   | PASS   | evidence/ai-call-success.json                                                                                                             |
| AI failure logging            | Failed Gemini call stores error details                 | PASS   | evidence/ai-call-failure.json                                                                                                             |
| Frontend route                | `/` loads dashboard                                     | PASS   | https://imagematch-api.onrender.com/                                                                                                      |
| Frontend cards                | Dashboard lists images                                  | PASS   | evidence/dashboard-home.png                                                                                                               |
| Dashboard status filter       | UI filter changes displayed images                      | PASS   | evidence/dashboard-filtered.png                                                                                                           |     |
| Automated tests               | `pytest -v` passes                                      | PASS   | 8 tests passed locally on 2026-10-14 using python -m pytest tests -v                                                                      |
| Secrets excluded              | `.env` is in `.gitignore` and not committed             | PASS   | Verified with `git status` and GitHub                                                                                                     |
| README complete               | Setup, architecture, API, and limitations documented    | PASS   | README drafted on 2026-10-13                                                                                                              |
| Evaluation dataset documented | Dataset plan and labels template exist                  | PASS   | `evaluation_dataset/README.md` drafted                                                                                                    |
|                               |

### Existing image

**Date:** `2026-10-22`

**Request:**

GET http://127.0.0.1:8000/images/1

**Expected:**

- HTTP `200`
- A single image object with metadata when available

**Observed:** HTTP `200`. Returned image ID `1` (`bear1.jpg`),
status `completed`, attempts `7`, and error_message `null`.
The metadata included subject `brown bear`, category `animal`,
attributes, caption, confidence `0.98`, and model name.

**Status:** `PASS`
**Evidence link/screenshot:** `evidence/image-detail-response.json`

### AI call audit history

**Date:** `2026-10-22`  
**Request:**

```text
GET http://127.0.0.1:8000/images/<existing_image_id>/calls
```

**Expected:**

- HTTP `200`
- JSON array of zero or more call-log records
- Records may include provider, model name, status, token counts, estimated cost, error message, and timestamp

**Observed:** HTTP `200`. Returned an empty JSON array (`[]`)
for existing image ID `1` (`bear1.jpg`). This confirms the endpoint
returns a call list for an existing image, but does not verify
retrieval of populated call-log records.

**Status:** `PASS`
**Evidence link/screenshot:** `evidence/image-id-test.png`

### Missing image audit history

**Date:** `2026-10-22`  
**Request:**

```text
GET `http://127.0.0.1:8000/images/999999/calls`
```

**Expected:**

```json
{
  "detail": "Image not found"
}
```

**Observed:** HTTP `404`. Returned `{"detail": "Image not found"}`.
**Status:** `PASS`

## AI Processing Evidence

### Successful processing example

Successful AI-call evidence is saved in
[evidence/ai-call-success.json](evidence/ai-call-success.json).

See the JSON file for the recorded call details.

### Failed processing example

Failed AI-call evidence is saved in
[evidence/ai-call-failure.json](evidence/ai-call-failure.json).

See the JSON file for the recorded failure details.

## Frontend Evidence

### Dashboard load

**Date:** `2026-10-13`

**URL:** `http://127.0.0.1:8000/`

**Observed:** Dashboard loaded successfully and displayed image cards.

**Status:** `PASS`
**Screenshot path:** `evidence/dashboard-home.png`

### Filter test

**Screenshot:** `evidence/dashboard-filtered.png`

## Evaluation Dataset Results

**Date:** `2026-10-22`
**Scope:** Limited animal-image pilot covering image IDs 16–34.

**Command used:**

python -m scripts.process_pending_images --batch-size 19

| Metric                           | Result         | Verification status                                  |
| -------------------------------- | -------------- | ---------------------------------------------------- |
| Images submitted                 | 19             | Confirmed from terminal output                       |
| Images completed                 | 16             | Confirmed from terminal output                       |
| Images failed                    | 3              | Confirmed from terminal output                       |
| Pipeline completion rate         | 84.21% (16/19) | Measured                                             |
| Terminal processing failure rate | 15.79% (3/19)  | Measured                                             |
| Category accuracy                | Not measured   | Requires review of stored predictions against images |
| Description acceptance rate      | Not measured   | Requires manual review of stored captions            |
| Logged failure rate              | 15.79% (3/19)  | verified                                             |

### Database audit verification

**Date:** `2026-10-22`
**Scope:** Image IDs 16–34

**Observed:**

- 19/19 evaluated images returned one saved AI-call record.
- 16 completed images returned a success record.
- 3 failed images (IDs 29, 31, 34) returned a failed record.
- Logged failure rate: 15.79% (3/19 images).
- Image-level final-outcome log coverage: 100% (19/19 images).

**Status:** `PASS`
**Evidence:** `evaluation_dataset/results/evaluation_results.csv`
and `evaluation_dataset/results/calls-<image_id>.json`

**Limitation:** This verifies saved final outcomes for all evaluated
images, not coverage of individual provider retries.

## Commands Used

```powershell
# Start local development server
uvicorn app.main:app --reload

# Run automated tests when added
pytest -v

# Review uncommitted changes
git status

# Commit documentation
git add README.md EVIDENCE.md evaluation_dataset
git commit -m "docs: add project README evaluation plan and evidence log"
git push
```

## Screenshots and Artifacts

Store evidence under an `evidence/` folder if you want it version-controlled:

```text
evidence/
├── swagger-endpoints.png
├── dashboard-home.png
├── dashboard-filtered.png
├── image-detail-response.json
├── ai-call-success.json
├── ai-call-failure.json
└── pytest-output.txt
```

| Artifact                 | Purpose                             | Added? |
| ------------------------ | ----------------------------------- | ------ |
| `swagger-endpoints.png`  | Shows API endpoints in Swagger      | `YES`  |
| `dashboard-home.png`     | Shows dashboard loading image cards | `YES`  |
| `dashboard-filtered.png` | Shows a working filter              | `YES`  |
| `ai-call-success.json`   | Shows successful AI audit record    | `YES`  |
| `ai-call-failure.json`   | Shows failed AI audit record        | `YES`  |
| `pytest-output.txt`      | Shows passing test suite            | `YES`  |

## Deployment Evidence

**Date:** `2026-10-22`
**Public URL:** https://imagematch-api.onrender.com/
**Hosting:** Render Free
**Database:** Neon PostgreSQL

**Observed:** The deployed dashboard and Swagger documentation loaded successfully.
The `/images`, `/images/16/calls`, and `/images/29/calls` endpoints returned HTTP 200
with the expected records. Missing-image requests to `/images/999999` and
`/images/999999/calls` returned HTTP 404 with `{"detail": "Image not found"}`.

**Status:** `PASS`
**Screenshot:** `evidence/deployment-dashboard.png`

## Remaining Work

- [x] Verify dashboard at `/`
- [x] Test status and category filtering through both API and UI
- [x] Add and run automated tests — 8 tests passed
- [x] Add screenshots or JSON evidence
- [x] Confirm `.env` is excluded from Git
- [x] Run an initial animal-image processing pilot — 16/19 completed
- [ ] Review stored predictions and captions to measure category accuracy and description acceptance
- [x] Verify database audit records for the evaluated images
- [deferred to avoid additional API usage] Expand evaluation to mixed categories — deferred to avoid additional API usage
- [x] Deploy application
