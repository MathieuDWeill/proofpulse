# Architecture

```txt
Customer targets
  | RPC / validator / bridge / oracle / custody endpoint
  v
Probe workers on AWS ECS/Fargate or Lambda
  | metrics + observations
  v
EventBridge -> API service
  | stores metadata
  v
DynamoDB + CloudWatch + OpenSearch
  | raw bundle storage
  v
S3 encrypted with KMS
  | AI analysis
  v
Amazon Bedrock incident agent
  | canonical JSON + SHA-256
  v
ProofPulse attestation relayer
  | proof hash
  v
On-chain anchor contract
```

## AWS services

- **ECS/Fargate:** API and probe workers.
- **Lambda:** lightweight scheduled checks and webhook handlers.
- **EventBridge:** schedules and incident pipeline orchestration.
- **CloudWatch:** logs, metrics, alarms.
- **OpenSearch:** incident/log search.
- **S3:** encrypted evidence bundles.
- **DynamoDB:** targets, checks, incidents, attestations.
- **KMS:** tenant encryption and signing boundaries.
- **Bedrock:** AI SRE analysis.
- **API Gateway / CloudFront / WAF:** secure public access.

## Data privacy

Only the hash is anchored on-chain. Raw logs, customer data, and documents remain encrypted in the customer's tenant storage.
