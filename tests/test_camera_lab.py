"""Camera lab prototypes: pure functions under Node; the page asks before using the camera and says nothing is recorded."""
import json
import os
import shutil
import subprocess

import pytest

from csync.ui import camera_lab

JS = os.path.join(os.path.dirname(camera_lab.__file__), "assets", "camera_lab.js")
needs_node = pytest.mark.skipif(shutil.which("node") is None, reason="node not installed")


def _node(code):
    run = f"const C=require({json.dumps(JS)});process.stdout.write(JSON.stringify(({code})()));"
    return json.loads(subprocess.run(["node", "-e", run], capture_output=True, text=True, check=True, timeout=60).stdout)


@needs_node
def test_pulse_finds_a_72_bpm_rhythm_in_noise_and_refuses_a_short_signal():
    r = _node("()=>{let s=[],x=1;for(let i=0;i<450;i++){x=(x*16807)%2147483647;s.push(120+0.6*Math.sin(2*Math.PI*1.2*i/30)+0.02*i+(x/2147483647)*0.3)}"
              "return [C.bpmFromSignal(s,30),C.bpmFromSignal(s.slice(0,60),30),C.bpmFromSignal(new Array(450).fill(5),30)]}")
    assert abs(r[0]["bpm"] - 72) <= 2 and r[1] is None and r[2] is None


@needs_node
def test_blink_counter_counts_short_closures_only():
    s = _node("()=>{const b=C.blinkCounter(0.21);[.3,.15,.15,.3,.1,.3,...new Array(20).fill(.1),.3].forEach(e=>b.push(e));return b.state()}")
    assert s["blinks"] == 1 and s["long"] == 1   # one-frame dip ignored, 20-frame closure counted apart


def test_page_starts_the_camera_only_on_click_and_pins_the_model_version():
    page = camera_lab.page("blink", {k: k for k in ("start", "stop", "hold", "denied", "nomodel", "clear", "noisy", "wait", "closed", "noface",
                                                     "stopped", "note")}, "blinks/min")
    assert "tasks-vision@1.2.3" in page and "getUserMedia" in page and "onclick" in page
