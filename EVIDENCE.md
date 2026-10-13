# Evidence Log

This file records implementation and verification evidence for ImageMatch. It is intended to make the project reviewable and reproducible.

**Project:** ImageMatch API  
**Repository:** Add GitHub repository URL here  
**Reviewer:** Steven  
**Last updated:** 2026-10-13

## Evidence Rules

For each item:

- Record the date tested
- Record the exact command, URL, or action
- Record the observed result
- Link a screenshot, JSON file, test output, or commit when possible
- Use `PASS`, `FAIL`, or `NOT YET TESTED`
- Do not claim model quality or deployment success without evidence

## Environment

| Item             | Value                        |
| ---------------- | ---------------------------- |
| Operating system | Windows                      |
| Python version   | `TBD`                        |
| FastAPI version  | `TBD`                        |
| Database         | `TBD`                        |
| AI provider      | Google Gemini                |
| Gemini model     | `TBD: add exact model name`  |
| Local API URL    | `http://127.0.0.1:8000`      |
| Swagger URL      | `http://127.0.0.1:8000/docs` |
| Dashboard URL    | `http://127.0.0.1:8000/`     |

## Implementation Checklist

| Area                          | Evidence required                                       | Status           | Evidence / notes                       |
| ----------------------------- | ------------------------------------------------------- | ---------------- | -------------------------------------- |
| FastAPI application starts    | Uvicorn terminal shows startup completed                | PASS             | Verified locally on 2026-10-13         |
| Swagger docs available        | `/docs` opens and lists endpoints                       | PASS             | Verified locally on 2026-10-13         |
| Image listing endpoint        | `GET /images` returns JSON list                         | PASS             | Verified manually in Swagger           |
| Status filter                 | `GET /images?status=completed` returns filtered data    | `NOT YET TESTED` | Add URL/result                         |
| Category filter               | `GET /images?category=<category>` returns filtered data | `NOT YET TESTED` | Add URL/result                         |
| Single-image endpoint         | `GET /images/{image_id}` returns image and metadata     | `NOT YET TESTED` | Add image ID and result                |
| Missing image behavior        | Missing image ID returns `404`                          | `NOT YET TESTED` | Example: `/images/999999`              |
| Audit endpoint exists         | `/images/{image_id}/calls` appears in Swagger           | PASS             | Verified locally on 2026-10-13         |
| Audit endpoint works          | Existing image returns call list                        | `NOT YET TESTED` | Add image ID and response summary      |
| Audit endpoint missing ID     | Missing image call request returns `404`                | `NOT YET TESTED` | Example: `/images/999999/calls`        |
| AI success logging            | Successful Gemini call stored with status/tokens/cost   | `NOT YET TESTED` | Add screenshot or JSON                 |
| AI failure logging            | Failed Gemini call stores error details                 | `NOT YET TESTED` | Add screenshot or JSON                 |
| Frontend route                | `/` loads dashboard                                     | `NOT YET TESTED` | Add screenshot                         |
| Frontend cards                | Dashboard lists images                                  | `NOT YET TESTED` | Add screenshot                         |
| Dashboard status filter       | UI filter changes displayed images                      | `NOT YET TESTED` | Add screenshot/notes                   |
| Dashboard category filter     | UI filter changes displayed images                      | `NOT YET TESTED` | Add screenshot/notes                   |
| Automated tests               | `pytest -v` passes                                      | `NOT YET TESTED` | Add terminal output                    |
| Secrets excluded              | `.env` is in `.gitignore` and not committed             | `NOT YET TESTED` | Verify with `git status` and GitHub    |
| README complete               | Setup, architecture, API, and limitations documented    | PASS             | README drafted on 2026-10-13           |
| Evaluation dataset documented | Dataset plan and labels template exist                  | PASS             | `evaluation_dataset/README.md` drafted |
| Deployment                    | Public URL works                                        | `NOT YET TESTED` | Add URL when deployed                  |

## Manual API Verification

### Image list

**Date:** `TBD`  
**Request:**

```text
GET http://127.0.0.1:8000/images
```

**Expected:**

- HTTP `200`
- JSON array
- Each image includes core fields and optional `metadata_record`

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`  
**Evidence link/screenshot:** `TBD`

### Existing image

**Date:** `TBD`  
**Request:**

```text
GET http://127.0.0.1:8000/images/<existing_image_id>
```

**Expected:**

- HTTP `200`
- Image data plus Gemini metadata when available

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`  
**Evidence link/screenshot:** `TBD`

### Missing image

**Date:** `TBD`  
**Request:**

```text
GET http://127.0.0.1:8000/images/999999
```

**Expected:**

```json
{
  "detail": "Image not found"
}
```

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`

### AI call audit history

**Date:** `TBD`  
**Request:**

```text
GET http://127.0.0.1:8000/images/<existing_image_id>/calls
```

**Expected:**

- HTTP `200`
- JSON array of zero or more call-log records
- Records may include provider, model name, status, token counts, estimated cost, error message, and timestamp

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`  
**Evidence link/screenshot:** `TBD`

### Missing image audit history

**Date:** `TBD`  
**Request:**

```text
GET http://127.0.0.1:8000/images/999999/calls
```

**Expected:**

```json
{
  "detail": "Image not found"
}
```

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`

## AI Processing Evidence

### Successful processing example

| Field                   | Value |
| ----------------------- | ----- |
| Date                    | `TBD` |
| Image filename          | `TBD` |
| Image ID                | `TBD` |
| Gemini model            | `TBD` |
| Resulting category      | `TBD` |
| Resulting description   | `TBD` |
| Image processing status | `TBD` |
| AI call status          | `TBD` |
| Input tokens            | `TBD` |
| Output tokens           | `TBD` |
| Estimated cost          | `TBD` |
| Screenshot/JSON path    | `TBD` |

### Failed processing example

| Field                      | Value                                             |
| -------------------------- | ------------------------------------------------- |
| Date                       | `TBD`                                             |
| Image filename             | `TBD`                                             |
| Image ID                   | `TBD`                                             |
| Gemini model               | `TBD`                                             |
| Image processing status    | `TBD`                                             |
| AI call status             | `TBD`                                             |
| Error message              | `TBD`                                             |
| Expected behavior verified | `TBD: error is logged and visible through /calls` |
| Screenshot/JSON path       | `TBD`                                             |

## Frontend Evidence

### Dashboard load

**Date:** `TBD`  
**URL:**

```text
http://127.0.0.1:8000/
```

**Expected:**

- Dashboard title is visible
- Image cards load from the API
- Status and category filters are present
- Each card displays metadata and Gemini audit history

**Observed:** `TBD`  
**Status:** `NOT YET TESTED`  
**Screenshot path:** `TBD`

### Filter test

| Test            | Input                | Expected result                 | Observed result | Status           |
| --------------- | -------------------- | ------------------------------- | --------------- | ---------------- |
| Status filter   | `completed`          | Only completed images shown     | `TBD`           | `NOT YET TESTED` |
| Category filter | `TBD`                | Only matching category shown    | `TBD`           | `NOT YET TESTED` |
| Empty result    | Nonexistent category | “No images match those filters” | `TBD`           | `NOT YET TESTED` |

## Evaluation Dataset Results

| Metric                      | Formula / definition                             | Current result | Status           |
| --------------------------- | ------------------------------------------------ | -------------: | ---------------- |
| Dataset size                | Number of images evaluated                       |          `TBD` | `NOT YET TESTED` |
| Category accuracy           | Correct categories / labeled completed images    |          `TBD` | `NOT YET TESTED` |
| Description acceptance rate | Acceptable descriptions / completed descriptions |          `TBD` | `NOT YET TESTED` |
| Pipeline completion rate    | Completed images / submitted images              |          `TBD` | `NOT YET TESTED` |
| Logged failure rate         | Images with failed AI call / submitted images    |          `TBD` | `NOT YET TESTED` |
| Audit-log coverage          | Processing attempts with logs / total attempts   |          `TBD` | `NOT YET TESTED` |

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
| `swagger-endpoints.png`  | Shows API endpoints in Swagger      | `NO`   |
| `dashboard-home.png`     | Shows dashboard loading image cards | `NO`   |
| `dashboard-filtered.png` | Shows a working filter              | `NO`   |
| `ai-call-success.json`   | Shows successful AI audit record    | `NO`   |
| `ai-call-failure.json`   | Shows failed AI audit record        | `NO`   |
| `pytest-output.txt`      | Shows passing test suite            | `NO`   |

## Remaining Work

- [ ] Verify dashboard at `/`
- [ ] Test status and category filtering through both API and UI
- [ ] Add and run automated tests
- [ ] Build and evaluate a representative image dataset
- [ ] Add screenshots or JSON evidence
- [ ] Confirm `.env` is excluded from Git
- [ ] Deploy application
- [ ] Add public deployment URL here
