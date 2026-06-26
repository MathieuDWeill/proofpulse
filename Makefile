.PHONY: install test api demo bundle verify

install:
	python -m pip install --upgrade pip
	python -m pip install -e ".[dev]"

test:
	PYTHONPATH=apps/api .venv/bin/python -m pytest -q

api:
	PYTHONPATH=apps/api .venv/bin/python -m uvicorn proofpulse_api.main:app --reload --port 8080

demo:
	bash scripts/demo_curl.sh

bundle:
	.venv/bin/python scripts/generate_evidence_bundle.py --target demo-rpc --kind rpc --out examples/generated_bundle.json

verify:
	.venv/bin/python scripts/verify_bundle.py examples/generated_bundle.json
