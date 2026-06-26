# Evidence anchor interface

Production versions can target EVM, Stellar Soroban, Casper, or any chain supported by the hackathon.

Minimal method:

```solidity
anchorEvidence(bytes32 bundleHash, string bundleURI, string targetId, uint8 severity)
```

Security notes:

- Never put private customer logs on-chain.
- Put only the canonical bundle hash and pointer.
- Use KMS or wallet-controlled signing.
- Use per-tenant encryption for evidence bundles stored in S3.
