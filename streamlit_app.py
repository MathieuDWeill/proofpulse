import hashlib
import json
import random
import uuid
from datetime import datetime, timezone

import streamlit as st


st.set_page_config(
    page_title="ProofPulse",
    page_icon="🫀",
    layout="wide",
)

def now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def canonical_hash(payload: dict) -> str:
    clean = dict(payload)
    clean.pop("bundle_hash", None)
    raw = json.dumps(clean, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()

def make_check(target_id: str, target_name: str, status: str, latency: int, error_rate: float, stale_blocks: int):
    observations = {
        "target_name": target_name,
        "target_kind": "rwa_oracle",
        "chain": "ethereum-sepolia",
        "probe_mode": "synthetic_streamlit_demo",
        "latency_ms": latency,
        "stale_blocks": stale_blocks,
        "error_rate": error_rate,
        "finality_lag_seconds": random.randint(1, 18),
        "sample_request_id": uuid.uuid4().hex,
    }
    return {
        "id": "check_" + uuid.uuid4().hex[:10],
        "target_id": target_id,
        "timestamp": now_iso(),
        "status": status,
        "latency_ms": latency,
        "observations": observations,
        "raw_hash": hashlib.sha256(json.dumps(observations, sort_keys=True).encode()).hexdigest(),
    }

def generate_demo():
    target_id = "target_" + uuid.uuid4().hex[:10]
    target = {
        "id": target_id,
        "name": "EU RPC + RWA Oracle Cluster",
        "kind": "rwa_oracle",
        "endpoint": "https://demo-rwa-oracle.proofpulse.local",
        "owner": "aws-activate-demo-team",
        "chain": "ethereum-sepolia",
        "tags": ["rwa", "oracle", "compliance", "aws"],
        "created_at": now_iso(),
    }

    checks = [
        make_check(target_id, target["name"], "ok", 241, 0.02, 0),
        make_check(target_id, target["name"], "degraded", 412, 0.08, 2),
        make_check(target_id, target["name"], "degraded", 537, 0.11, 3),
        make_check(target_id, target["name"], "degraded", 468, 0.09, 1),
    ]

    degraded = sum(1 for c in checks if c["status"] != "ok")
    max_latency = max(c["latency_ms"] for c in checks)
    risk_score = min(100, 45 + degraded * 18 + int(max_latency / 20))
    severity = "critical" if risk_score >= 90 else "high"

    incident = {
        "id": "incident_" + uuid.uuid4().hex[:10],
        "target_id": target_id,
        "severity": severity,
        "risk_score": risk_score,
        "summary": f"{target['name']} shows {severity} operational risk. Observed max latency is {max_latency}ms across {len(checks)} checks, with {degraded} degraded observations.",
        "likely_cause": "Stale source feed, document pipeline delay, or oracle publisher failure.",
        "blast_radius": "Users may experience delayed confirmations, stale balances, failed quotes, or reduced trust in operational reporting.",
        "recommended_actions": [
            "Fail over traffic to a healthy region or provider.",
            "Capture CloudWatch/OpenSearch logs for the affected window.",
            "Publish a customer-facing proof bundle hash after operator review.",
            "Schedule a post-incident control review for RWA/compliance workflows.",
        ],
        "evidence_refs": [c["id"] for c in checks],
        "model_disclaimer": "Prototype deterministic triage. Production version should use Bedrock with guardrails and human approval for regulated decisions.",
    }

    bundle = {
        "schema": "proofpulse.evidence.v1",
        "bundle_id": "bundle_" + uuid.uuid4().hex[:10],
        "created_at": now_iso(),
        "target": target,
        "incident": incident,
        "checks": checks,
        "canonicalization": "json.dumps(sort_keys=True,separators=(',',':'))",
    }
    bundle["bundle_hash"] = canonical_hash(bundle)

    attestation = {
        "attestation_id": "att_" + uuid.uuid4().hex[:10],
        "chain": "ethereum-sepolia",
        "contract_address": "0xProofPulseDemo000000000000000000000000000000",
        "method": "anchorEvidence(bytes32 bundleHash,string bundleURI,string targetId,uint8 severity)",
        "calldata_preview": {
            "bundleHash": "0x" + bundle["bundle_hash"],
            "bundleURI": f"s3://proofpulse-evidence/{bundle['bundle_id']}.json",
            "targetId": target_id,
            "severity": severity,
        },
        "bundle_hash": bundle["bundle_hash"],
        "status": "prepared_not_broadcast",
        "note": "Prepared only. Wire this into a wallet or relayer for the final demo.",
    }

    return {
        "target": target,
        "checks": checks,
        "incident": incident,
        "bundle": bundle,
        "attestation": attestation,
    }


st.markdown("""
<style>
.stApp { background: #070b12; color: #f8fafc; }
.block-container { padding-top: 2rem; max-width: 1280px; }
.hero {
    border: 1px solid #263044;
    border-radius: 24px;
    padding: 28px;
    background: linear-gradient(180deg, #111827, #0b1020);
    box-shadow: 0 20px 80px rgba(0,0,0,.35);
}
.badge {
    display: inline-block;
    padding: 6px 10px;
    margin: 4px 6px 4px 0;
    border: 1px solid #334155;
    border-radius: 999px;
    background: #172033;
    color: #d7e3ff;
    font-size: 13px;
}
.critical {
    background: linear-gradient(135deg, #ef4444, #f97316);
    border: none;
    color: white;
    font-weight: 800;
}
.hashbox {
    word-break: break-all;
    background: #030712;
    border: 1px solid #263044;
    border-radius: 14px;
    padding: 14px;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    color: #8ee6c3;
}
.big {
    font-size: 64px;
    font-weight: 900;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([1.2, 0.8], gap="large")

with left:
    st.markdown("""
    <div class="hero">
      <span class="badge">AWS Activate</span>
      <span class="badge">Infrastructure / Middleware</span>
      <span class="badge">AI Agents</span>
      <span class="badge">Web3 Reliability</span>
      <h1>ProofPulse</h1>
      <h3>Datadog + AI SRE + on-chain proof for Web3 infrastructure.</h3>
      <p>
      When an RPC, validator, bridge, oracle, or RWA pipeline fails, ProofPulse
      creates a verifiable evidence bundle — not just another alert.
      </p>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="hero">
      <h3>Submission-ready demo</h3>
      <p>Generate an incident, compute a deterministic bundle hash, and prepare an on-chain attestation.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🚨 Generate Demo Incident", type="primary", use_container_width=True):
        st.session_state.demo = generate_demo()

if "demo" not in st.session_state:
    st.session_state.demo = generate_demo()

demo = st.session_state.demo
incident = demo["incident"]
bundle = demo["bundle"]
attestation = demo["attestation"]
target = demo["target"]

st.divider()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Target", target["name"])
c2.metric("Severity", incident["severity"].upper())
c3.metric("Risk score", incident["risk_score"])
c4.metric("Checks", len(demo["checks"]))

st.markdown(f"""
<span class="badge critical">{incident["severity"].upper()}</span>
<span class="badge">Ethereum Sepolia</span>
<span class="badge">RWA Oracle</span>
<span class="badge">Prepared attestation</span>
""", unsafe_allow_html=True)

st.subheader("AI SRE incident analysis")
st.write(incident["summary"])
st.write("**Likely cause:** " + incident["likely_cause"])
st.write("**Blast radius:** " + incident["blast_radius"])

st.write("**Recommended actions**")
for action in incident["recommended_actions"]:
    st.write("• " + action)

st.subheader("Evidence bundle hash")
st.markdown(f'<div class="hashbox">{bundle["bundle_hash"]}</div>', unsafe_allow_html=True)

st.subheader("Prepared on-chain attestation")
st.markdown(f'<div class="hashbox">{attestation["method"]}<br><br>{json.dumps(attestation["calldata_preview"], indent=2)}</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Evidence bundle JSON", "AWS architecture", "Judge FAQ"])

with tab1:
    st.json(bundle)

with tab2:
    st.markdown("""
    **Why AWS Activate credits matter**

    - Continuous probes on EC2 or Lambda
    - S3 evidence bundle storage
    - CloudWatch and OpenSearch ingestion
    - Bedrock AI SRE analysis
    - Multi-region Web3 infrastructure monitoring
    - Testnet/mainnet relayer and observability costs
    """)

with tab3:
    st.markdown("""
    **Is it on-chain?**  
    The demo prepares the attestation call. Production connects this to a wallet or relayer.

    **What is AI here?**  
    The prototype uses deterministic triage; production uses Bedrock with guardrails.

    **Why not just Datadog?**  
    Datadog observes. ProofPulse makes incidents verifiable through evidence bundles and hashes.

    **What is real vs simulated?**  
    The demo uses synthetic checks. The architecture is designed for real RPC, validator, oracle, and RWA probes.
    """)

st.caption("ProofPulse — auditable, not just observable.")
