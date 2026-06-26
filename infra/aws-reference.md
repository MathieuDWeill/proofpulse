# AWS reference architecture

## MVP deployment

- API: ECS Fargate service behind Application Load Balancer.
- Probe workers: EventBridge scheduled Lambda or ECS scheduled tasks.
- Evidence: S3 bucket with SSE-KMS.
- Metadata: DynamoDB tables.
- Logs: CloudWatch Logs.
- Search: OpenSearch Serverless once event volume justifies it.
- AI: Amazon Bedrock with deterministic fallback.
- Edge: CloudFront + WAF for dashboard/API.

## Estimated pilot spend

- Fargate API + workers: $150–$600/month.
- CloudWatch logs/metrics: $50–$500/month.
- Bedrock analysis: $100–$2,000/month depending on incident volume.
- OpenSearch: $500–$2,000/month if enabled.
- S3/KMS/DynamoDB: $50–$400/month.

## Why credits matter

A realistic infra reliability product needs continuous workloads and retention. A toy deployment cannot prove value to Web3 infrastructure customers.
