# 2-minute demo video script

## Scene 1 — Problem, 15s

“Web3 outages are not only technical failures. They are trust failures. When an RPC, validator, bridge, or RWA oracle breaks, users and auditors need proof: what happened, when, and what evidence supports the response.”

## Scene 2 — Dashboard, 20s

Show the ProofPulse dashboard.

“This is ProofPulse: an AI-native verifiable reliability layer for Web3 infrastructure. We monitor critical endpoints and turn incidents into tamper-evident evidence.”

## Scene 3 — API demo, 35s

Run:

```bash
curl -X POST http://localhost:8080/demo/seed | jq
```

Narration:

“In one flow, ProofPulse registers a target, runs synthetic checks, detects operational risk, and generates an AI-style SRE assessment with severity, likely cause, blast radius, and recommended actions.”

## Scene 4 — Evidence bundle, 30s

Show the generated bundle hash.

“The important part is this bundle hash. The evidence can stay private in S3 or a customer vault, but the canonical SHA-256 hash can be verified forever.”

## Scene 5 — Attestation, 25s

Show prepared calldata.

“Finally, ProofPulse prepares an on-chain attestation. In production this is sent by a wallet or relayer. The result is a verifiable operational proof for customers, auditors, and counterparties.”

## Scene 6 — AWS, 15s

Show architecture diagram or docs.

“AWS credits let us run the real system: ECS, Lambda, CloudWatch, OpenSearch, S3, KMS, DynamoDB, and Bedrock.”

## Closing, 10s

“ProofPulse makes Web3 infrastructure observable, explainable, and provable.”
