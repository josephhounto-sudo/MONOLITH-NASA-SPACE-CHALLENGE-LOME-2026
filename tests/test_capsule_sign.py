"""SIMULATED capsule. A changed byte is detected. The wording never claims more than that."""
import hashlib
import json

from csync.crypto.capsule_sign import generate_keypair, sign_capsule, verify_capsule

CAPSULE = {"crew": "SIMULATED", "day": 7, "note": "watch"}


def _canonical(capsule):
    return json.dumps(capsule, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def test_signed_capsule_verifies():
    private, public = generate_keypair()
    envelope = sign_capsule(CAPSULE, private, None)
    assert verify_capsule(CAPSULE, envelope, None) == (True, "ok")
    assert envelope["public_key"] == public.hex()
    assert envelope["prev_hash"] is None


def test_one_changed_byte_is_detected():
    private, _public = generate_keypair()
    envelope = sign_capsule(CAPSULE, private, "prev")
    changed = dict(CAPSULE, note="watxh")
    assert _canonical(changed) != _canonical(CAPSULE)
    assert verify_capsule(changed, envelope, "prev") == (False, "detects modification")


def test_wrong_key_is_rejected():
    private, _public = generate_keypair()
    _other_private, other_public = generate_keypair()
    envelope = sign_capsule(CAPSULE, private, None)
    envelope["public_key"] = other_public.hex()
    ok, _reason = verify_capsule(CAPSULE, envelope, None)
    assert ok is False


def test_broken_chain_is_rejected():
    private, _public = generate_keypair()
    envelope = sign_capsule(CAPSULE, private, "hash-a")
    ok, _reason = verify_capsule(CAPSULE, envelope, "hash-b")
    assert ok is False


def test_truncated_envelope_is_malformed():
    private, _public = generate_keypair()
    envelope = sign_capsule(CAPSULE, private, None)
    del envelope["signature"]
    assert verify_capsule(CAPSULE, envelope, None) == (False, "malformed")
    assert verify_capsule(CAPSULE, {}, None) == (False, "malformed")
    assert verify_capsule("not-a-capsule", envelope, None) == (False, "malformed")


def test_fingerprint_is_deterministic():
    private, _public = generate_keypair()
    first = sign_capsule(CAPSULE, private, "prev")
    second = sign_capsule(CAPSULE, private, "prev")
    assert first["payload_sha256"] == second["payload_sha256"]
    assert first["signature"] == second["signature"]
    assert first["payload_sha256"] == hashlib.sha256(_canonical(CAPSULE)).hexdigest()
