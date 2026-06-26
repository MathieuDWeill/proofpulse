from __future__ import annotations

import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .core import InMemoryStore
from .models import (
    AttestationPrepareRequest,
    CheckRequest,
    DemoState,
    EvidenceBundleRequest,
    IncidentAnalyzeRequest,
    TargetCreate,
)

app = FastAPI(
    title="ProofPulse API",
    version="0.2.0",
    description="AI-native verifiable reliability layer for Web3 infrastructure.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

STATIC_DIR = Path(__file__).parent / "static"
# Ensure the directory exists
STATIC_DIR.mkdir(parents=True, exist_ok=True)

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

store = InMemoryStore()

@app.get("/health")
def health():
    return {"status": "ok", "service": "proofpulse-api", "version": "0.2.0"}

@app.post("/targets")
def create_target(payload: TargetCreate):
    return store.create_target(payload)

@app.get("/targets")
def list_targets():
    return list(store.targets.values())

@app.post("/checks/run")
def run_check(payload: CheckRequest):
    if payload.target_id not in store.targets:
        raise HTTPException(status_code=404, detail="target not found")
    return store.run_check(payload)

@app.post("/incidents/analyze")
def analyze_incident(payload: IncidentAnalyzeRequest):
    if payload.target_id not in store.targets:
        raise HTTPException(status_code=404, detail="target not found")
    return store.analyze_incident(payload)

@app.post("/evidence/bundle")
def create_evidence_bundle(payload: EvidenceBundleRequest):
    if payload.target_id not in store.targets:
        raise HTTPException(status_code=404, detail="target not found")
    if payload.incident_id not in store.incidents:
        raise HTTPException(status_code=404, detail="incident not found")
    return store.create_bundle(payload)

@app.post("/attestations/prepare")
def prepare_attestation(payload: AttestationPrepareRequest):
    if payload.bundle_id not in store.bundles:
        raise HTTPException(status_code=404, detail="bundle not found")
    return store.prepare_attestation(payload)

@app.post("/demo/seed")
def seed_demo():
    target = store.create_target(TargetCreate(
        name="EU RPC + RWA Oracle Cluster",
        kind="rwa_oracle",
        endpoint="https://demo-rwa-oracle.proofpulse.local",
        owner="aws-activate-demo-team",
        chain="ethereum-sepolia",
        tags=["rwa", "oracle", "compliance", "aws"],
    ))
    checks = [store.run_check(CheckRequest(target_id=target.id, mode="synthetic")) for _ in range(4)]
    incident = store.analyze_incident(IncidentAnalyzeRequest(target_id=target.id, check_ids=[c.id for c in checks]))
    bundle = store.create_bundle(EvidenceBundleRequest(target_id=target.id, incident_id=incident.id))
    att = store.prepare_attestation(AttestationPrepareRequest(bundle_id=bundle.bundle_id, chain="ethereum-sepolia"))
    
    state = {"target": target, "checks": checks, "incident": incident, "bundle": bundle, "attestation": att}
    store.latest_seed = state
    return state

@app.get("/demo/latest")
def get_latest_demo():
    return store.latest_seed

@app.get("/demo/state", response_model=DemoState)
def demo_state():
    return DemoState(
        targets=list(store.targets.values()),
        checks=list(store.checks.values()),
        incidents=list(store.incidents.values()),
        bundles=list(store.bundles.values()),
        attestations=list(store.attestations.values()),
    )

@app.get("/", response_class=FileResponse)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")

