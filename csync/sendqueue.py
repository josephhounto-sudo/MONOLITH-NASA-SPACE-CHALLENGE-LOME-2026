"""Store-and-forward send queue: offline-first, exactly-once delivery via message_id, original timestamps kept."""
from __future__ import annotations
import hashlib, json
from datetime import timedelta

def message_id(payload: dict) -> str:
    """Anti-duplicate key: stable hash of the payload."""
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()[:16]

def deliver(messages, link_down, link_up, ground_delay_min=20, duplicates=(), reverse_queued=True):
    """Simulate a link cut. messages: [{message_id, created}]. Returns (arrivals, ground_view)."""
    sent = [{**m, "sent": link_up if link_down <= m["created"] < link_up else m["created"]} for m in messages]
    stream = sent + [dict(sent[i], sent=sent[i]["sent"] + timedelta(minutes=5)) for i in duplicates]
    queued = [s for s in stream if s["sent"] == link_up]
    other = [s for s in stream if s["sent"] != link_up]
    if reverse_queued:
        queued.reverse()
    arrivals = [{**s, "received": s["sent"] + timedelta(minutes=ground_delay_min)} for s in other + queued]
    return arrivals, ground_view(arrivals)

def ground_view(arrivals):
    """Ground side: drop duplicates by message_id, order by creation time, never rewrite timestamps."""
    seen, kept = set(), []
    for a in arrivals:
        if a["message_id"] not in seen:
            seen.add(a["message_id"]); kept.append(a)
    return sorted(kept, key=lambda x: x["created"])
