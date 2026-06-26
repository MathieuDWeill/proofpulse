from fastapi.testclient import TestClient
from proofpulse_api.main import app

client = TestClient(app)

def test_dashboard_static():
    r = client.get('/')
    assert r.status_code == 200
    assert "text/html" in r.headers.get("content-type", "")
    assert "ProofPulse Dashboard" in r.text

def test_demo_seed_flow():
    r = client.post('/demo/seed')
    assert r.status_code == 200
    data = r.json()
    assert data['bundle']['bundle_hash']
    assert data['attestation']['status'] == 'prepared_not_broadcast'

def test_demo_latest():
    # Before seed, get /demo/latest could be null or return last state from previous tests.
    # Let's post to seed first to guarantee a state.
    r_seed = client.post('/demo/seed')
    assert r_seed.status_code == 200
    seed_data = r_seed.json()
    
    r_latest = client.get('/demo/latest')
    assert r_latest.status_code == 200
    latest_data = r_latest.json()
    
    assert latest_data is not None
    assert latest_data['bundle']['bundle_hash'] == seed_data['bundle']['bundle_hash']

