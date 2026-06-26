#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, time, uuid
from pathlib import Path


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def sha(data):
    return hashlib.sha256(canonical(data).encode()).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', default='demo-rpc')
    ap.add_argument('--kind', default='rpc')
    ap.add_argument('--out', default='examples/generated_bundle.json')
    args = ap.parse_args()
    body = {
        'schema':'proofpulse.evidence.v1',
        'bundle_id':'bundle_'+uuid.uuid4().hex[:10],
        'created_at':int(time.time()),
        'target':{'id':args.target,'kind':args.kind,'chain':'ethereum-sepolia'},
        'incident':{'severity':'medium','risk_score':61,'summary':'Synthetic demo incident'},
        'checks':[{'latency_ms':420,'status':'degraded','raw_hash':uuid.uuid4().hex}],
    }
    body['bundle_hash']=sha({k:v for k,v in body.items() if k!='bundle_hash'})
    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(body, indent=2), encoding='utf-8')
    print(out)
    print(body['bundle_hash'])

if __name__ == '__main__':
    main()
