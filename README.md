# AdForge AI

AdForge AI is a full-stack, serverless, multimodal ad-generation platform that transforms a product image into a complete marketing asset using computer vision and generative AI.

## Tech Stack
- React (Frontend)
- AWS Lambda + API Gateway
- AWS Step Functions
- Amazon Rekognition
- Amazon Bedrock
- Amazon Polly
- Amazon S3

## Status
🚧 In active development

## Project Structure

### API Layer (`backend/api/`)

| File | Description |
|------|-------------|
| `start_job/handler.py` | Receives a base64-encoded product image, uploads it to S3, and triggers the Step Functions pipeline. Returns a `jobId` for tracking. |
| `get_status/handler.py` | Polls job completion by checking for a `manifest.json` in the output bucket. Returns `IN_PROGRESS` or `COMPLETED` with asset data. |

### Pipeline Steps (`backend/pipeline/`)

| File | Description |
|------|-------------|
| `vision/rekognition.py` | Analyzes the product image using Amazon Rekognition to extract labels/features. (stub) |
| `reasoning/bedrock_text.py` | Generates ad copy using Amazon Bedrock based on extracted labels. (stub) |
| `audio/polly.py` | Converts generated text to speech using Amazon Polly. (stub) |
| `visual/bedrock_image.py` | Generates visual ad assets using Amazon Bedrock image models. (stub) |
| `assemble/assemble_assets.py` | Combines all generated assets into a final manifest. (stub) |

### Orchestration (`backend/orchestration/`)

| File | Description |
|------|-------------|
| `adforge_pipeline.asl.json` | AWS Step Functions state machine definition that orchestrates the pipeline flow: Vision → Reasoning → Done. |

### Infrastructure Docs (`backend/infra/`)

| File | Description |
|------|-------------|
| `iam.md` | IAM roles and policies documentation |
| `s3.md` | S3 bucket configuration documentation |
| `architecture.md` | Architecture overview |

### Frontend (`frontend/`)

React-based UI for uploading product images and viewing generated ads.

## Progress

- [x] Set up project structure
- [x] Created API handlers (start_job, get_status)
- [x] Configured dynamic STATE_MACHINE_ARN using AWS account ID
- [x] Created stub pipeline handlers
- [x] Defined Step Functions state machine
- [ ] Implement Rekognition integration
- [ ] Implement Bedrock text generation
- [ ] Implement Polly audio generation
- [ ] Implement Bedrock image generation
- [ ] Implement asset assembly
- [ ] Complete frontend integration
