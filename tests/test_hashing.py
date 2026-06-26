from proofpulse_api.core import sha256_hex

def test_hash_is_stable_for_dict_order():
    assert sha256_hex({"a": 1, "b": 2}) == sha256_hex({"b": 2, "a": 1})
