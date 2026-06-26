# Paste this into Codex

You are working on the ProofPulse repo. Goal: make this AWS Activate / DoraHacks submission production-demo ready.

Priorities:

1. Run the project locally and fix any broken imports/tests.
2. Add a real RPC probe implementation using JSON-RPC methods such as `eth_blockNumber`, with timeout, latency, status, and response hash.
3. Add optional Bedrock integration behind an environment variable. Keep deterministic fallback if AWS credentials are missing.
4. Add S3 evidence bundle storage abstraction with local filesystem fallback.
5. Add a real EVM deployment script for `contracts/ProofPulseAnchor.sol` using Foundry or Hardhat, whichever is quickest.
6. Add a CLI command:
   `proofpulse demo --endpoint <url> --chain ethereum-sepolia --anchor false`
   that runs target creation, checks, incident analysis, bundle creation, and attestation preparation.
7. Improve the static dashboard so it fetches `/demo/state` from the API and renders real data.
8. Keep README and docs updated.
9. Do not over-engineer auth unless the demo requires it.
10. Make sure `pytest` passes.

Winning criteria:

- The demo must be understandable in 2 minutes.
- Every generated evidence bundle must have a reproducible hash.
- Private data must not be put on-chain.
- The AWS credit justification must remain obvious.
