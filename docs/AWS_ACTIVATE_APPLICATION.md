# AWS Activate application draft

## Project name

ProofPulse

## One-line description

ProofPulse is an AI-native verifiable reliability layer for Web3 infrastructure that monitors critical endpoints, generates incident evidence bundles, scores operational risk, and anchors tamper-evident proofs on-chain.

## Category

Infrastructure / Middleware, AI Agents, RWA compliance tooling.

## Problem

Web3 teams increasingly run critical infrastructure on cloud platforms: validators, RPC endpoints, bridge relayers, oracle pipelines, custody workflows, trading systems, and RWA data feeds. When something fails, the operational trail is fragmented across dashboards, logs, chats, and status pages.

That creates a trust gap. Users, institutions, auditors, and counterparties need to know what happened, when it happened, what evidence was used, and whether the record was tampered with after the fact.

## Solution

ProofPulse turns Web3 operational events into verifiable evidence.

The platform continuously checks infrastructure health, detects anomalies, creates an evidence bundle, runs an AI agent to summarize severity and remediation, computes a canonical hash, and anchors that hash on-chain. The evidence itself remains private in secure storage, while the proof can be independently verified.

## Why AWS

ProofPulse is cloud-native and infrastructure-heavy. AWS credits would be used to build the production-grade backbone:

- ECS/Fargate or Lambda for probes and API services.
- EventBridge for scheduled checks and incident pipelines.
- CloudWatch for metrics and alarms.
- OpenSearch for log/event search.
- S3 for encrypted evidence bundle storage.
- DynamoDB for multi-tenant metadata and audit indices.
- KMS for tenant-specific encryption and signing workflows.
- Bedrock for AI incident analysis and remediation generation.
- API Gateway / CloudFront / WAF for secure customer access.
- VPC, NAT, and private subnets for production isolation.

## Why this needs credits

The project is not just a frontend. It requires realistic, always-on infrastructure to prove value: recurring probes, logs, AI analysis, secure storage, chain relayers, and multi-region availability checks. AWS credits would let us run credible pilots with Web3 teams without cutting corners on security or observability.

## Target users

- RPC providers and validator operators.
- Bridge and oracle teams.
- RWA tokenization platforms.
- Custody and compliance teams.
- DeFi protocols that need better incident reporting.
- Web3 startups preparing for institutional customers.

## MVP status

The repository includes:

- FastAPI backend prototype.
- Evidence bundle generation and verification.
- AI-style incident analyzer scaffold.
- Dashboard mock.
- Solidity anchor contract.
- AWS architecture plan.
- Demo script and roadmap.

## 90-day plan

1. Deploy API and probe workers on AWS.
2. Add real RPC/validator/bridge probes.
3. Store encrypted bundles in S3 and metadata in DynamoDB.
4. Integrate Bedrock for incident summarization with guardrails.
5. Deploy anchor contract and relayer.
6. Run pilots with 3 Web3 infrastructure teams.

## Expected AWS monthly usage

Early pilot: $500–$1,500/month.

Scale test: $3,000–$8,000/month depending on probe frequency, log volume, Bedrock usage, OpenSearch retention, and multi-region deployment.

## Why now

As Web3 moves toward institutional adoption, operational trust becomes a buying criterion. RWA platforms, exchanges, bridge operators, and validators need evidence-grade reliability reporting, not just dashboards.

ProofPulse makes cloud infrastructure auditable by default.
