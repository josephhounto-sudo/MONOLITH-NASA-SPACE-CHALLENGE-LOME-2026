"""Ed25519 envelope for a SIMULATED capsule. A mismatch detects modification."""
from __future__ import annotations

import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives.serialization import Encoding, NoEncryption, PrivateFormat, PublicFormat


def _canonical(capsule: dict) -> bytes:
    return json.dumps(capsule, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _message(digest: str, prev_hash: str | None) -> bytes:
    prev = "" if prev_hash is None else prev_hash
    return f"{digest}.{prev}".encode("utf-8")


def generate_keypair() -> tuple[bytes, bytes]:
    key = Ed25519PrivateKey.generate()
    private = key.private_bytes(Encoding.Raw, PrivateFormat.Raw, NoEncryption())
    public = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return private, public


def sign_capsule(capsule: dict, private_key: bytes, prev_hash: str | None) -> dict:
    """Returns {"payload_sha256": str, "prev_hash": str | None, "signature": str(hex), "public_key": str(hex)}.
    Canonical JSON: sort_keys=True, separators=(",", ":"), ensure_ascii=False. Ed25519 via `cryptography`."""
    digest = hashlib.sha256(_canonical(capsule)).hexdigest()
    key = Ed25519PrivateKey.from_private_bytes(private_key)
    signature = key.sign(_message(digest, prev_hash))
    public = key.public_key().public_bytes(Encoding.Raw, PublicFormat.Raw)
    return {
        "payload_sha256": digest,
        "prev_hash": prev_hash,
        "signature": signature.hex(),
        "public_key": public.hex(),
    }


def verify_capsule(capsule: dict, envelope: dict, expected_prev_hash: str | None) -> tuple[bool, str]:
    """(True, "ok") or (False, reason). Never raises on malformed input; returns (False, "malformed")."""
    try:
        if not isinstance(capsule, dict) or not isinstance(envelope, dict):
            return False, "malformed"
        for field in ("payload_sha256", "prev_hash", "signature", "public_key"):
            if field not in envelope:
                return False, "malformed"
        digest = hashlib.sha256(_canonical(capsule)).hexdigest()
        if envelope["payload_sha256"] != digest:
            return False, "detects modification"
        if envelope["prev_hash"] != expected_prev_hash:
            return False, "chain"
        public = Ed25519PublicKey.from_public_bytes(bytes.fromhex(envelope["public_key"]))
        public.verify(bytes.fromhex(envelope["signature"]), _message(digest, envelope["prev_hash"]))
    except (TypeError, ValueError, KeyError):
        return False, "malformed"
    except InvalidSignature:
        return False, "rejected"
    return True, "ok"
