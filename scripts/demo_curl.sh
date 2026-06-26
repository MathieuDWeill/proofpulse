#!/usr/bin/env bash
set -euo pipefail
BASE=${BASE:-http://localhost:8080}
echo "Health"
curl -s "$BASE/health" | jq

echo "Seed demo"
curl -s -X POST "$BASE/demo/seed" | jq

echo "State"
curl -s "$BASE/demo/state" | jq '.bundles[-1].bundle_hash, .attestations[-1].calldata_preview'
