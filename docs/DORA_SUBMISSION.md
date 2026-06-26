# DoraHacks submission draft

## BUIDL name

ProofPulse

## Short description

AI-native verifiable reliability layer for Web3 infrastructure.

## Vision

Web3 infrastructure is becoming mission critical, but incident reporting is still based on dashboards, screenshots, and trust. ProofPulse makes infrastructure failures observable, explainable, and provable.

The product monitors RPC endpoints, validators, bridges, RWA oracle pipelines, custody workflows, and other Web3 infrastructure. When it detects risk, it creates an evidence bundle, generates an AI SRE assessment, computes a canonical hash, and prepares an on-chain attestation.

This gives Web3 teams a better way to communicate trust: private evidence stays private, but the proof is tamper-evident.

## Problem solved

- Teams cannot easily prove what happened during an outage.
- AI incident summaries are not tied to evidence.
- Compliance-heavy Web3/RWA workflows need audit trails.
- Status pages are not enough for institutional customers.

## How it works

1. Register an infrastructure target.
2. Run synthetic checks and collect observations.
3. Detect degraded or risky conditions.
4. Generate an AI-style incident report.
5. Create a canonical evidence bundle.
6. Hash the bundle.
7. Prepare an on-chain attestation.

## AWS usage

ProofPulse is designed to use AWS heavily and responsibly: ECS/Fargate, Lambda, EventBridge, CloudWatch, OpenSearch, S3, KMS, DynamoDB, Bedrock, API Gateway, CloudFront, and WAF.

## Demo

The demo shows the full proof loop with a seeded RWA oracle target: checks, incident analysis, evidence hash, and prepared attestation calldata.

## Why now

The next wave of Web3 adoption is institutional, regulated, and infrastructure-heavy. Those users need verifiable operational evidence, not vague uptime claims.
