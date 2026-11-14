from datetime import datetime, timedelta
from csync.sendqueue import deliver, message_id

def test_exactly_once_in_order_timestamps_kept():
    t0 = datetime(2031, 3, 9, 12, 0)
    msgs = [{"created": t0 + timedelta(minutes=30 * k), "body": k} for k in range(14)]
    msgs = [{**x, "message_id": message_id(x)} for x in msgs]
    arrivals, ground = deliver(msgs, t0 + timedelta(hours=1), t0 + timedelta(hours=7), duplicates=(2, 5, 9))
    assert len(arrivals) == len(msgs) + 3
    assert [g["message_id"] for g in ground] == [m["message_id"] for m in msgs]
    assert all(g["created"] == m["created"] for g, m in zip(ground, msgs))
    assert min(a["received"] for a in arrivals) >= t0 + timedelta(minutes=20)
