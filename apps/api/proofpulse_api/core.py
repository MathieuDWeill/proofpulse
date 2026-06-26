from __future__ import annotations

import hashlib
import json
import random
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from .models import (
    AttestationPrepareRequest,
    CheckRequest,
    CheckResult,
    EvidenceBundle,
    EvidenceBundleRequest,
    IncidentAnalysis,
    IncidentAnalyzeRequest,
    PreparedAttestation,
    Severity,
    Target,
    TargetCreate,
)


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)


def sha256_hex(data: Any) -> str:
    if not isinstance(data, str):
        data = canonical_json(data)
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class InMemoryStore:
    def __init__(self) -> None:
        self.targets: Dict[str, Target] = {}
        self.checks: Dict[str, CheckResult] = {}
        self.incidents: Dict[str, IncidentAnalysis] = {}
        self.bundles: Dict[str, EvidenceBundle] = {}
        self.attestations: Dict[str, PreparedAttestation] = {}
        self.latest_seed: Any = None

    def create_target(self, payload: TargetCreate) -> Target:
        target = Target(id=f"target_{uuid.uuid4().hex[:10]}", created_at=now_utc(), **payload.model_dump())
        self.targets[target.id] = target
        return target

    def run_check(self, payload: CheckRequest) -> CheckResult:
        target = self.targets[payload.target_id]
        base_latency = {
            "rpc": 120,
            "validator": 240,
            "bridge": 380,
            "rwa_oracle": 180,
            "custody": 210,
            "dex": 160,
        }.get(target.kind.value, 200)
        jitter = random.randint(-40, 260)
        latency = max(20, base_latency + jitter)
        stale_blocks = random.choice([0, 0, 0, 1, 2, 5])
        error_rate = random.choice([0.0, 0.0, 0.01, 0.03, 0.08])
        status = "ok"
        if latency > 420 or stale_blocks >= 5 or error_rate >= 0.08:
            status = "degraded"
        if latency > 560 or error_rate >= 0.12:
            status = "incident"
        observations = {
            "target_name": target.name,
            "target_kind": target.kind.value,
            "chain": target.chain,
            "probe_mode": payload.mode,
            "latency_ms": latency,
            "stale_blocks": stale_blocks,
            "error_rate": error_rate,
            "finality_lag_seconds": random.choice([0, 1, 2, 5, 13, 21]),
            "sample_request_id": uuid.uuid4().hex,
        }
        result = CheckResult(
            id=f"check_{uuid.uuid4().hex[:10]}",
            target_id=target.id,
            timestamp=now_utc(),
            status=status,
            latency_ms=latency,
            observations=observations,
            raw_hash=sha256_hex(observations),
        )
        self.checks[result.id] = result
        return result

    def analyze_incident(self, payload: IncidentAnalyzeRequest) -> IncidentAnalysis:
        target = self.targets[payload.target_id]
        selected = [self.checks[cid] for cid in payload.check_ids if cid in self.checks]
        if not selected:
            selected = [c for c in self.checks.values() if c.target_id == payload.target_id][-3:]
        max_latency = max([c.latency_ms for c in selected], default=0)
        degraded = sum(1 for c in selected if c.status != "ok")
        risk = min(100, 25 + degraded * 20 + int(max_latency / 20))
        if risk >= 85:
            severity = Severity.critical
        elif risk >= 70:
            severity = Severity.high
        elif risk >= 45:
            severity = Severity.medium
        else:
            severity = Severity.low
        summary = (
            f"{target.name} shows {severity.value} operational risk. "
            f"Observed max latency is {max_latency}ms across {len(selected)} checks, "
            f"with {degraded} degraded observations."
        )
        likely_cause = {
            "rpc": "RPC saturation, upstream node lag, or regional network contention.",
            "validator": "Validator heartbeat instability, peer connectivity issue, or signing infrastructure delay.",
            "bridge": "Indexer lag, message relayer backlog, or source/destination chain finality mismatch.",
            "rwa_oracle": "Stale source feed, document pipeline delay, or oracle publisher failure.",
            "custody": "Policy engine delay, transaction queue congestion, or KMS signing bottleneck.",
            "dex": "Matching engine latency, liquidity route failure, or websocket feed degradation.",
        }.get(target.kind.value, "Infrastructure degradation requiring operator review.")
        incident = IncidentAnalysis(
            id=f"incident_{uuid.uuid4().hex[:10]}",
            target_id=target.id,
            severity=severity,
            risk_score=risk,
            summary=summary,
            likely_cause=likely_cause,
            blast_radius="Users may experience delayed confirmations, stale balances, failed quotes, or reduced trust in operational reporting.",
            recommended_actions=[
                "Fail over traffic to a healthy region or provider.",
                "Capture CloudWatch/OpenSearch logs for the affected window.",
                "Publish a customer-facing proof bundle hash after operator review.",
                "Schedule a post-incident control review for RWA/compliance workflows.",
            ],
            evidence_refs=[c.id for c in selected],
            model_disclaimer="Prototype deterministic triage. Production version should use Bedrock with guardrails and human approval for regulated decisions.",
        )
        self.incidents[incident.id] = incident
        return incident

    def create_bundle(self, payload: EvidenceBundleRequest) -> EvidenceBundle:
        target = self.targets[payload.target_id]
        incident = self.incidents[payload.incident_id]
        checks = [self.checks[cid] for cid in incident.evidence_refs if cid in self.checks]
        bundle_payload = {
            "target": target.model_dump(mode="json"),
            "incident": incident.model_dump(mode="json"),
            "checks": [c.model_dump(mode="json") for c in checks] if payload.include_raw_observations else [{"id": c.id, "raw_hash": c.raw_hash} for c in checks],
        }
        bundle = EvidenceBundle(
            bundle_id=f"bundle_{uuid.uuid4().hex[:10]}",
            created_at=now_utc(),
            target=bundle_payload["target"],
            incident=bundle_payload["incident"],
            checks=bundle_payload["checks"],
            bundle_hash=sha256_hex(bundle_payload),
        )
        self.bundles[bundle.bundle_id] = bundle
        return bundle

    def prepare_attestation(self, payload: AttestationPrepareRequest) -> PreparedAttestation:
        bundle = self.bundles[payload.bundle_id]
        contract = payload.contract_address or "0xProofPulseDemo000000000000000000000000000000"
        attestation = PreparedAttestation(
            attestation_id=f"att_{uuid.uuid4().hex[:10]}",
            chain=payload.chain,
            contract_address=contract,
            method="anchorEvidence(bytes32 bundleHash,string bundleURI,string targetId,uint8 severity)",
            calldata_preview={
                "bundleHash": "0x" + bundle.bundle_hash,
                "bundleURI": f"s3://proofpulse-evidence/{bundle.bundle_id}.json",
                "targetId": bundle.target["id"],
                "severity": bundle.incident["severity"],
            },
            bundle_hash=bundle.bundle_hash,
            note="Prepared only. Wire this into a wallet or relayer for the final demo.",
        )
        self.attestations[attestation.attestation_id] = attestation
        return attestation
