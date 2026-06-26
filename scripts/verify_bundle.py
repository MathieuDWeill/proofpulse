#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sys
from pathlib import Path

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"))

def main(path):
    data=json.loads(Path(path).read_text())
    claimed=data.get('bundle_hash')
    body={k:v for k,v in data.items() if k!='bundle_hash'}
    actual=hashlib.sha256(canonical(body).encode()).hexdigest()
    print('claimed:', claimed)
    print('actual :', actual)
    if claimed != actual:
        raise SystemExit('invalid bundle hash')
    print('OK')

if __name__ == '__main__':
    main(sys.argv[1])
