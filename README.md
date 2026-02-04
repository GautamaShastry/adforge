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
| `vision/rekognition.py` | ✅ Analyzes the product image using Amazon Rekognition to extract labels with 80%+ confidence. |
| `reasoning/bedrock_text.py` | ✅ Generates a 60-second ad script and scene description using Claude 3.5 Sonnet on Amazon Bedrock. |
| `audio/polly.py` | ✅ Converts the ad script to speech using Amazon Polly (neural engine, Matthew voice), saves MP3 to S3. |
| `visual/bedrock_image.py` | ✅ Generates lifestyle product imagery using Amazon Titan Image Generator v1 (512x512), saves PNG to S3. |
| `assemble/assemble_assets.py` | ✅ Bundles script, audio, and image into a manifest.json and uploads to S3. |

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
- [x] Defined Step Functions state machine
- [x] Implement Rekognition integration (extracts labels with 80%+ confidence)
- [x] Implement Bedrock text generation (Claude 3.5 Sonnet for ad scripts)
- [x] Implement Polly audio generation (neural voice, saves to S3)
- [x] Implement Bedrock image generation (Titan Image Generator v1, 512x512)
- [x] Implement asset assembly (creates manifest.json with all asset references)
- [ ] Complete frontend integration
