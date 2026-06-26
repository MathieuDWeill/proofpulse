#!/usr/bin/env python3
from __future__ import annotations
import json, urllib.request

BASE='http://localhost:8080'

def post(path):
    req=urllib.request.Request(BASE+path, method='POST')
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())

def get(path):
    with urllib.request.urlopen(BASE+path, timeout=10) as r:
        return json.loads(r.read())

print('ProofPulse one-command demo')
print('Health:', get('/health'))
data=post('/demo/seed')
print('\nIncident summary:')
print(data['incident']['summary'])
print('\nBundle hash:')
print(data['bundle']['bundle_hash'])
print('\nPrepared attestation:')
print(json.dumps(data['attestation']['calldata_preview'], indent=2))
