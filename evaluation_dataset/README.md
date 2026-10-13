# Evaluation Dataset

This folder documents the evaluation dataset used to assess ImageMatch’s AI metadata-extraction pipeline.

The purpose of the dataset is not to train a model. It is a controlled collection of images and expected labels used to evaluate whether the Gemini-powered pipeline produces useful, consistent, and auditable metadata.

## Goals

The dataset should test:

- Category classification accuracy
- Description usefulness and factual grounding
- Handling of clear versus ambiguous images
- Handling of text-heavy images
- Handling of poor-quality images
- AI provider failure logging
- Processing-state updates
- Cost and token logging when available

## Recommended Structure

```text
evaluation_dataset/
├── README.md
├── labels.csv
├── images/
│   ├── product_001.jpg
│   ├── food_001.jpg
│   ├── travel_001.jpg
│   ├── document_001.jpg
│   └── difficult_001.jpg
└── results/
    └── evaluation_results.csv
```

Do not commit private, copyrighted, or personally identifiable images unless you have permission to use them.

## Suggested Dataset Composition

Start with 20 to 40 images. Include multiple examples from each expected category.

| Image type                      | Suggested count | What it evaluates                                      |
| ------------------------------- | --------------: | ------------------------------------------------------ |
| Products                        |            5–10 | Object identification and product category assignment  |
| Food                            |            5–10 | Food recognition and concise description generation    |
| Travel / outdoor scenes         |            5–10 | Scene classification and visual-context description    |
| Documents / text-heavy images   |             3–5 | Limits of visual extraction and text interpretation    |
| Ambiguous or low-quality images |             3–5 | Uncertainty, failure behavior, and safe categorization |

## Label File

Create `labels.csv` using this format:

```csv
image_filename,expected_category,expected_description,quality_notes
product_001.jpg,product,A reusable water bottle on a white background,clear product photo
food_001.jpg,food,A plate of pasta with tomato sauce,clear food image
travel_001.jpg,travel,A mountain landscape under a cloudy sky,wide landscape
document_001.jpg,document,A photographed printed document,text-heavy
difficult_001.jpg,unknown,Image content is unclear,low-light and blurry
```

### Labeling Rules

- `expected_category` should use the same controlled category vocabulary as the application where possible.
- `expected_description` should be short, factual, and based only on visible content.
- `quality_notes` should explain unusual conditions, ambiguity, blur, poor lighting, occlusion, or dense text.
- Use `unknown` when a reliable category cannot reasonably be assigned.
- Do not treat subjective wording differences as failures if the meaning is materially the same.

## Evaluation Procedure

1. Add each evaluation image to the application using the project’s existing ingestion or processing workflow.
2. Confirm the image receives a database record.
3. Run Gemini processing for each image.
4. Retrieve results with:

```text
GET /images/{image_id}
GET /images/{image_id}/calls
```

5. Compare the stored category and description with `labels.csv`.
6. Record results in `results/evaluation_results.csv`.
7. Capture screenshots or JSON output as evidence in `EVIDENCE.md`.

## Results Template

Create `results/evaluation_results.csv`:

```csv
image_filename,image_id,expected_category,predicted_category,category_match,description_review,status,call_status,error_message,reviewer_notes
product_001.jpg,1,product,product,yes,acceptable,completed,success,,Description correctly identifies visible bottle
food_001.jpg,2,food,food,yes,acceptable,completed,success,,Description correctly identifies dish
difficult_001.jpg,3,unknown,unknown,yes,acceptable,completed,success,,Appropriate uncertainty
```

Use these values for `description_review`:

- `acceptable`: Factually useful and sufficiently specific
- `partially_acceptable`: Mostly correct but vague or missing a major visible detail
- `unacceptable`: Hallucinated, materially incorrect, or not useful
- `not_available`: No description was produced because processing failed

## Core Metrics

Calculate these after reviewing the results:

\[
\text{Category accuracy} =
\frac{\text{Number of correct category predictions}}
{\text{Number of completed images with labels}}
\]

\[
\text{Description acceptance rate} =
\frac{\text{Acceptable descriptions}}
{\text{Completed images with descriptions}}
\]

\[
\text{Pipeline completion rate} =
\frac{\text{Images completed successfully}}
{\text{Images submitted for processing}}
\]

\[
\text{Logged failure rate} =
\frac{\text{Images with a logged failed AI call}}
{\text{Images submitted for processing}}
\]

Do not report a metric until the corresponding review data is completed.

## Success Criteria

Suggested initial targets:

| Metric                          |                            Initial target |
| ------------------------------- | ----------------------------------------: |
| Category accuracy               |                              At least 80% |
| Acceptable description rate     |                              At least 80% |
| Audit-log coverage              |               100% of processing attempts |
| Missing-image endpoint behavior |                         100% return `404` |
| Dashboard filter verification   | Status and category filters work manually |

These targets are project goals, not claims of achieved performance. Final values should be filled in after you run the evaluation.

## Limitations

- Category labels can be subjective for multi-object images.
- Gemini availability, quotas, and rate limits may affect completion rate.
- Small evaluation datasets are useful for demonstration but are not statistically representative of all images.
- A human reviewer is required to judge factual usefulness of generated descriptions.
