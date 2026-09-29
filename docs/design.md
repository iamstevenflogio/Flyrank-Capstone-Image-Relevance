# AI Image Understanding & Content Matching Engine

## Problem

Blog posts need relevant images, but filename and keyword matching can select visually or semantically wrong images. This service classifies an image library, embeds image descriptions and posts, ranks candidates, and safely refuses a recommendation when confidence is insufficient.

## Goal

For a post about red fox behavior, the system should rank a red fox image first, rank wolf and dog images lower, and reject a wolf candidate with an understandable reason.

## Limitations

This project will not build a public-facing frontend, a large-scale image hosting platform, or real-time image processing during normal API requests.

# Initial Scope

- 40-50 licensed-free images
- At least 4 categories, beginning with animal images
- Initial subjects: red fox, wolf, dog, bear, deer
- At least 10 hand-labeled blog-post-to-correct-image evaluation cases

# Image metadata schema

{
"subject": "red fox",
"category": "animal",
"attributes": ["orange fur", "wild", "forest"],
"caption": "A red fox standing in a forest",
"confidence": 0.94
}

Rules:

- `subject`, `category`, and `caption` are required strings.
- `attributes` is a list of strings.
- `confidence` must be between 0 and 1.
- Invalid AI output is rejected and retried as flagged.
- Results below a chosen confidence threshold are flagged for review.

## Matching approach

1. Generate an embedding from each validated image caption.
2. Generate an embedding from each blog post's title and body.
3. Rank images using cosine similarity
4. Pass ranked candidates to a mismatch guard before returning a recommendation.

# Mismatch guard

The guard rejects a candidate if:

- Image metadata confidence is below the minimum threshold
- Semantic similarity is below the tuned threshold.
- The post expects a specific subject and the candidate subject conflicts.
- The candidate category conflicts with the post's inferred category.

Example:
Post: "The behavior of red foxes"
Candidate: "A gray wolf in the forest"
Decision: REJECTED
Reason: "Subject mismatch: post expects a red fox; image is classified as wolf."

## Initial data model

- images
- image_metadata
- image_embeddings
- posts
- post_embeddings
- match_suggestions
- reviews
- ai_call_costs
- background_jobs

## Initial API

- POST /images
- POST /posts
- POST /jobs/process-images
- GET /jobs/{job_id}
- GET /posts/{post_id}/images
- POST /suggestions/{suggestion_id}/review
- GET /suggestions/{suggestion_id}

## Layer sketch

HTTP routes -> service layer -> repositories -> PostgreSQL
|
-> AI clients -> vision and embedding providers
|
-> mismatch guarrd

## Success criteria

- Every image has schema-valid metadata or is flagged
- A fox post ranks a fox image first
- A forced wolf candidate is rejected with a clear reason.
- A no-match post post returns "no confident match."
- Top-1 precision is measured on at least 10 labeled examples.
