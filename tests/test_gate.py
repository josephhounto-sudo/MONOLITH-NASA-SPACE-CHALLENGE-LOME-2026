"""Resume-gate acceptance cases G1-G10 (TESTS_ET_CONTROLES). Any implementation must pass these."""
from datetime import datetime, timedelta
from csync.gate import resume_gate

REQ = datetime(2031, 3, 10, 9, 0)
PROC = {"prerequisites": [{"indicator_id": "PH01", "max_age_min": 10, "sources": ["GUIDED"]},
                          {"indicator_id": "CO01", "max_age_min": 10, "sources": ["GUIDED"]}],
        "override_policy": {"override_never_resumes_alone": True}}
def m(ind, minutes_ago, quality="OK", source="GUIDED"):
    return {"indicator_id": ind, "timestamp": REQ - timedelta(minutes=minutes_ago), "quality": quality, "source": source}
FRESH = [m("PH01", 3), m("CO01", 5)]

def dec(*a, **k): return resume_gate(*a, **k)[0]

def test_g1_all_valid():            assert dec(REQ, FRESH, PROC) == "RESUME_AUTHORIZED"
def test_g2_missing():              assert dec(REQ, FRESH[:1], PROC) == "REFUSE_RESUME"
def test_g3_stale_story_act3():     assert dec(REQ, [m("PH01", 14), FRESH[1]], PROC) == "REFUSE_RESUME"
def test_g4_artifact():             assert dec(REQ, [m("PH01", 3, quality="ARTIFACT"), FRESH[1]], PROC) == "REFUSE_RESUME"
def test_g5_no_policy():            assert dec(REQ, FRESH, dict(PROC, override_policy=None)) == "REFUSE_RESUME"
def test_g6_override_never_alone():
    d, reasons = resume_gate(REQ, [m("PH01", 14), FRESH[1]], PROC, override={"by": "Commander"})
    assert d == "REFUSE_RESUME" and any(r.startswith("G6") for r in reasons)
def test_g7_no_prerequisite():      assert dec(REQ, FRESH, dict(PROC, prerequisites=[])) == "REFUSE_RESUME"
def test_g7_explicit_none():        assert dec(REQ, [], dict(PROC, prerequisites=[], no_physical_prereq=True)) == "RESUME_AUTHORIZED"
def test_g8_future_timestamp():     assert dec(REQ, [m("PH01", -2), FRESH[1]], PROC) == "REFUSE_RESUME"
def test_g9_not_suspended():        assert dec(REQ, FRESH, PROC, session_state="RUNNING") == "REFUSE_RESUME"
def test_g10_concurrent():          assert dec(REQ, FRESH, PROC, pending_lock=True) == "REFUSE_RESUME"
def test_edge_exactly_10_min():     assert dec(REQ, [m("PH01", 10), FRESH[1]], PROC) == "RESUME_AUTHORIZED"
def test_edge_wrist_not_enough():   assert dec(REQ, [m("PH01", 3, source="WRIST"), FRESH[1]], PROC) == "REFUSE_RESUME"
