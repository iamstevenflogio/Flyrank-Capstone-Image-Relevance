# AI Image Understanding and Content Matching Engine

This Capstone is an AI-assisted image metadata pipeline and dashboard. It stores uploaded image records, uses Gemini to extract structured metadata, records every AI-provider attempt, and exposes the results through a FastAPI API and simple browser dashboard.

## Problem

Image libraries become difficult to search and audit when metadata is incomplete, inconsistent, or manually entered.

The project addresses that problem by:

- Processing images with Gemini to generate structured metadata
- Saving metadata alongside the original image record
- Tracking processing state such as `pending`, `processing`, `completed`, and `failed`
- Recording each Gemini/API attempt, including failures, token usage, timestamps, and estimated cost
- Providing a dashboard to browse, filter, and inspect images and their processing history

## Features

- FastAPI backend with automatically generated Swagger documentation
- SQLAlchemy database models for images, extracted metadata, and AI-call audit records
- Gemini-powered image metadata extraction
- Image listing with optional status and category filters
- Per-image metadata endpoint
- Per-image Gemini audit-history endpoint
- Dashboard served directly by FastAPI
- Error visibility for failed AI requests, including quota or provider failures
- API response schemas using Pydantic

## Architecture

```mermaid
flowchart TD
    User[User / Reviewer]
    Dashboard[Dashboard<br/>static/index.html]
    Docs[Swagger API Docs<br/>/docs]

    User --> Dashboard
    User --> Docs

    Dashboard -->|GET /images| API
    Dashboard -->|GET /images/{id}/calls| API
    Docs --> API

    API[FastAPI Application<br/>app/main.py]
    API --> Service[Image Processing / Gemini Service]
    API --> DB[(Database)]

    Service -->|Image + prompt| Gemini[Google Gemini API]
    Gemini -->|Structured metadata or error| Service

    Service -->|Create/update image metadata| DB
    Service -->|Log status, tokens, cost, errors| DB

    DB --> Images[images]
    DB --> Metadata[image_metadata]
    DB --> Calls[ai_call_logs]
```

The API documentation is generated from the FastAPI route definitions and Pydantic models, and is available at `/docs`. FastAPI provides Swagger UI by default at that path. [web:617]

## Data Flow

1. An image record is created in the database.
2. The processing pipeline sends the image and extraction instructions to Gemini.
3. Gemini returns structured metadata or an error.
4. The application saves metadata to the database and updates the image processing status.
5. The application creates an AI call-log record for every attempt.
6. The dashboard retrieves image data from `GET /images`.
7. The dashboard retrieves each image’s audit history from `GET /images/{image_id}/calls`.

## API Endpoints

| Method | Endpoint                      | Purpose                                     |
| ------ | ----------------------------- | ------------------------------------------- |
| `GET`  | `/`                           | Serves the ImageMatch dashboard             |
| `GET`  | `/docs`                       | Interactive Swagger API documentation       |
| `GET`  | `/images`                     | Lists images and AI metadata                |
| `GET`  | `/images?status=completed`    | Filters images by processing status         |
| `GET`  | `/images?category=<category>` | Filters images by Gemini category           |
| `GET`  | `/images/{image_id}`          | Returns one image and its metadata          |
| `GET`  | `/images/{image_id}/calls`    | Returns AI-call audit records for one image |

### Example requests

```text
GET /images
GET /images?status=completed
GET /images?category=product
GET /images/4
GET /images/4/calls
```

## Database Model

| Table / Model   | Purpose                                                                                     |
| --------------- | ------------------------------------------------------------------------------------------- |
| `Image`         | Stores the source image record, filename, type, size, status, and timestamps                |
| `ImageMetadata` | Stores metadata extracted by Gemini, such as category and description                       |
| `AICallLog`     | Stores provider/model details, outcome, token usage, estimated cost, errors, and timestamps |

The audit-log table is important because an AI pipeline should expose failures and estimated usage rather than silently discarding unsuccessful provider calls.

## Local Setup

### Prerequisites

- Python 3.10 or later
- A Google Gemini API key
- A local database configured for the project

### Install dependencies

```powershell
pip install -r requirements.txt
```

### Configure environment variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_key_here
DATABASE_URL=your_database_connection_string
```

Do not commit `.env` or API keys to GitHub.

### Run the application

```powershell
uvicorn app.main:app --reload
```

Open:

```text
Dashboard: http://127.0.0.1:8000/
Swagger docs: http://127.0.0.1:8000/docs
```

## Dashboard

The dashboard is served from `static/index.html` by FastAPI. It provides:

- Image cards
- Processing-status filter
- Gemini category filter
- Image metadata display
- Gemini audit-history display
- Provider error-message visibility
- Token and estimated-cost visibility where available

Because the dashboard is served by the same FastAPI application as the API, it uses the same origin and does not require CORS configuration.

## Evaluation Dataset

The evaluation dataset is documented in [`evaluation_dataset/README.md`](evaluation_dataset/README.md).

The dataset should contain representative images across categories and difficulty levels, plus an expected metadata label file. It is used to assess extraction quality, failure behavior, and consistency.

## Evidence

Implementation evidence, manual verification results, API screenshots, and test results are tracked in [`EVIDENCE.md`](EVIDENCE.md).

## Known Limitations

- AI output quality depends on the source image quality and Gemini availability.
- A provider quota or overload response can prevent processing.
- Estimated token cost is an estimate and may not exactly match provider billing.
- The dashboard is intentionally lightweight and does not yet include authentication, uploads, pagination controls, or advanced search.
- Evaluation labels require human review because some categories or descriptions can be subjective.

## Future Improvements

- Add an image-upload endpoint and upload form
- Add pagination and sorting controls
- Add automated API tests with `pytest`
- Add a retry policy for temporary Gemini failures
- Add authentication and role-based access control
- Deploy the dashboard and API publicly
- Add dataset-level accuracy metrics and evaluation reports
- Add image previews or object storage integration
