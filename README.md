# ProofPulse

**AI-native verifiable reliability layer for Web3 infrastructure.**

ProofPulse monitors validators, RPC endpoints, bridges, RWA data pipelines, custodial workflows, and trading infrastructure. It turns operational incidents into tamper-evident evidence bundles, generates an AI reliability/risk assessment, and anchors the bundle hash on-chain.

The goal is simple: **make Web3 infrastructure observable, auditable, and credit-worthy enough to run on serious cloud infrastructure.**

## Why this wins the AWS Activate track

AWS Activate rewards teams that can use real cloud credits meaningfully. ProofPulse is designed to be AWS-intensive from day one:

- **Infrastructure / Middleware:** validator and RPC observability, latency checks, proof bundles, attestation ledger.
- **AI Agents:** incident triage, root-cause summaries, risk scoring, recommended remediations.
- **RWA / Compliance tooling:** evidence trails for tokenized assets, attestations, and audit exports.
- **High-compute potential:** CloudWatch ingestion, OpenSearch, Bedrock, Lambda, ECS/Fargate, DynamoDB, S3, KMS, EventBridge, VPC networking.

The product is not “another Web3 app.” It is the missing trust layer between cloud infrastructure, on-chain systems, and compliance teams.

## Demo story

A Web3 project adds its RPC endpoint, validator, bridge indexer, or RWA oracle to ProofPulse. ProofPulse:

1. Runs live health checks and synthetic transactions.
2. Detects anomalies such as latency spikes, missed validator heartbeats, stale oracle feeds, or inconsistent bridge messages.
3. Creates an evidence bundle containing timestamps, endpoint snapshots, metrics, and raw observations.
4. Uses an AI agent to summarize severity, likely cause, blast radius, and recommended fix.
5. Hashes the evidence bundle.
6. Anchors the hash on-chain or prepares an attestation transaction.
7. Exports an audit-ready report for customers, investors, or compliance reviewers.

## Repository structure

```txt
apps/api/                  FastAPI backend prototype
apps/web/                  Static dashboard demo
contracts/                 Solidity proof-anchor contract + interface notes
docs/                      Pitch, AWS Activate answers, roadmap, demo script
infra/                     AWS architecture, Terraform skeleton, deployment guide
scripts/                   Demo seed, evidence generation, hash verification
examples/                  Evidence bundles and sample reports
tests/                     API and hashing tests
.github/workflows/         CI
```

## Quick start

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn proofpulse_api.main:app --reload --port 8080
```

Open:

- API docs: `http://localhost:8080/docs`
- Dashboard: `apps/web/index.html`

Generate a sample evidence bundle:

```bash
python scripts/generate_evidence_bundle.py --target demo-rpc --kind rpc --out examples/generated_bundle.json
python scripts/verify_bundle.py examples/generated_bundle.json
```

## Core endpoints

- `GET /health`
- `POST /targets`
- `POST /checks/run`
- `POST /incidents/analyze`
- `POST /evidence/bundle`
- `POST /attestations/prepare`
- `GET /demo/state`

## Submission-ready one-liner

**ProofPulse is an AI SRE and compliance proof layer for Web3 infrastructure: it monitors critical endpoints, generates incident evidence bundles, scores operational risk with an AI agent, and anchors tamper-evident proofs on-chain.**

## What to build next

The current repo is intentionally demo-first. Codex should prioritize:

1. Real RPC/validator probes.
2. Real AWS deployment on ECS/Fargate or Lambda.
3. Bedrock integration for AI analysis.
4. Real on-chain deployment on the target chain.
5. A 2-minute demo video using the script in `docs/DEMO_SCRIPT.md`.
