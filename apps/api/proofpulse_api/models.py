from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, HttpUrl, ConfigDict

class TargetKind(str, Enum):
    rpc = "rpc"
    validator = "validator"
    bridge = "bridge"
    rwa_oracle = "rwa_oracle"
    custody = "custody"
    dex = "dex"

class Severity(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"

class TargetCreate(BaseModel):
    name: str = Field(..., examples=["Stellar RPC EU-1"])
    kind: TargetKind
    endpoint: str = Field(..., examples=["https://rpc.example.org"])
    owner: str = Field("demo-team")
    chain: str = Field("generic")
    tags: List[str] = Field(default_factory=list)

class Target(TargetCreate):
    id: str
    created_at: datetime

class CheckRequest(BaseModel):
    target_id: str
    mode: str = Field("synthetic", description="synthetic, passive, replay, or auditor")

class CheckResult(BaseModel):
    id: str
    target_id: str
    timestamp: datetime
    status: str
    latency_ms: int
    observations: Dict[str, Any]
    raw_hash: str

class IncidentAnalyzeRequest(BaseModel):
    target_id: str
    check_ids: List[str] = Field(default_factory=list)
    operator_note: Optional[str] = None

class IncidentAnalysis(BaseModel):
    id: str
    target_id: str
    severity: Severity
    risk_score: int = Field(..., ge=0, le=100)
    summary: str
    likely_cause: str
    blast_radius: str
    recommended_actions: List[str]
    evidence_refs: List[str]
    model_disclaimer: str

class EvidenceBundleRequest(BaseModel):
    target_id: str
    incident_id: str
    include_raw_observations: bool = True

class EvidenceBundle(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    schema_name: str = Field("proofpulse.evidence.v1", alias="schema")
    bundle_id: str
    created_at: datetime
    target: Dict[str, Any]
    incident: Dict[str, Any]
    checks: List[Dict[str, Any]]
    bundle_hash: str
    canonicalization: str = "json.dumps(sort_keys=True,separators=(',',':'))"

class AttestationPrepareRequest(BaseModel):
    bundle_id: str
    chain: str = "ethereum-sepolia"
    contract_address: Optional[str] = None

class PreparedAttestation(BaseModel):
    attestation_id: str
    chain: str
    contract_address: str
    method: str
    calldata_preview: Dict[str, Any]
    bundle_hash: str
    status: str = "prepared_not_broadcast"
    note: str

class DemoState(BaseModel):
    targets: List[Target]
    checks: List[CheckResult]
    incidents: List[IncidentAnalysis]
    bundles: List[EvidenceBundle]
    attestations: List[PreparedAttestation]
