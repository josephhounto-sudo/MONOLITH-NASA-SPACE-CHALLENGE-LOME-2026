// Camera lab (V3 prototypes camera_pulse and eye_blink). Runs only in the visitor's browser, after a click; no frame is stored
// or sent. Pure functions first (tested under Node), browser code after.

// Pulse from the mean green value of the skin box: remove the slow trend, then find the strongest rhythm between 42 and 180
// beats per minute (0.7-3 Hz) with a direct Fourier scan. Returns null when the signal is too short or flat.
function bpmFromSignal(samples, fps) {
  if (!Array.isArray(samples) || !(fps > 0)) return null;
  const n = samples.length;
  if (n < fps * 6) return null;                               // under 6 seconds there are too few beats to count
  const w = Math.max(1, Math.round(fps));                     // 1-second moving mean = the slow trend (light, movement)
  const x = samples.map((v, i) => {
    let s = 0, c = 0;
    for (let j = Math.max(0, i - w); j <= Math.min(n - 1, i + w); j++) { s += samples[j]; c++; }
    return v - s / c;
  });
  const sd = Math.sqrt(x.reduce((a, v) => a + v * v, 0) / n);
  if (!(sd > 1e-6)) return null;
  let best = null, bestP = 0, total = 0;
  for (let bpm = 42; bpm <= 180; bpm += 1) {
    const f = bpm / 60;
    let re = 0, im = 0;
    for (let i = 0; i < n; i++) { const a = 2 * Math.PI * f * i / fps; re += x[i] * Math.cos(a); im += x[i] * Math.sin(a); }
    const p = re * re + im * im;
    total += p;
    if (p > bestP) { bestP = p; best = bpm; }
  }
  return { bpm: best, share: total > 0 ? bestP / total : 0 };   // share: how much the peak stands out (quality hint)
}

// Eye opening (eye aspect ratio, Soukupova & Cech 2016) from 6 points [outer, top1, top2, inner, bottom2, bottom1].
function ear(p) {
  const d = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);
  const h = d(p[0], p[3]);
  return h > 0 ? (d(p[1], p[5]) + d(p[2], p[4])) / (2 * h) : null;
}
// MediaPipe face mesh indices for the two eyes, in the order ear() expects
const LEFT_EYE = [33, 160, 158, 133, 153, 144], RIGHT_EYE = [362, 385, 387, 263, 373, 380];

// Counts a blink when the opening stays below the threshold for 2 to 12 frames (longer = eyes closed, counted apart).
function blinkCounter(threshold) {
  const s = { blinks: 0, closedFrames: 0, frames: 0, run: 0, long: 0 };
  return {
    push(e) {
      if (e === null || e === undefined) return s;
      s.frames++;
      if (e < threshold) { s.run++; s.closedFrames++; }
      else { if (s.run >= 2 && s.run <= 12) s.blinks++; else if (s.run > 12) s.long++; s.run = 0; }
      return s;
    },
    state: () => ({ ...s, closedShare: s.frames ? s.closedFrames / s.frames : 0 }),
  };
}

if (typeof module !== "undefined") module.exports = { bpmFromSignal, ear, blinkCounter, LEFT_EYE, RIGHT_EYE };

if (typeof document !== "undefined" && window.CS_CAM) {
  const cfg = window.CS_CAM, T = cfg.words;
  const $ = (id) => document.getElementById(id);
  let stream = null, running = false;
  $("go").onclick = async () => {
    if (running) { stop(); return; }
    try {
      stream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480, facingMode: "user" }, audio: false });
    } catch (e) { $("msg").textContent = T.denied; return; }
    const v = $("vid"); v.srcObject = stream; await v.play();
    running = true; $("go").textContent = T.stop; $("msg").textContent = T.hold;
    const c = document.createElement("canvas"), g = c.getContext("2d", { willReadFrequently: true });
    const green = [], t0 = performance.now();
    let face = null;
    if (cfg.mode === "blink") {
      try {
        const vis = await import(cfg.tasks);
        const files = await vis.FilesetResolver.forVisionTasks(cfg.wasm);
        face = await vis.FaceLandmarker.createFromOptions(files, { baseOptions: { modelAssetPath: cfg.model }, runningMode: "VIDEO", numFaces: 1 });
      } catch (e) { $("msg").textContent = T.nomodel; }
    }
    const counter = blinkCounter(0.21);
    const tick = () => {
      if (!running) return;
      const sec = (performance.now() - t0) / 1000;
      if (cfg.mode === "pulse") {
        c.width = 64; c.height = 64;
        const w = v.videoWidth, h = v.videoHeight;
        g.drawImage(v, w * 0.4, h * 0.22, w * 0.2, h * 0.12, 0, 0, 64, 64);   // forehead box drawn on the video
        const d = g.getImageData(0, 0, 64, 64).data; let s = 0;
        for (let i = 1; i < d.length; i += 4) s += d[i];
        green.push(s / (d.length / 4));
        const fps = green.length / Math.max(sec, 0.1);
        const r = sec > 8 ? bpmFromSignal(green.slice(-Math.round(fps * 15)), fps) : null;
        $("val").textContent = r ? r.bpm : "…";
        $("q").textContent = r ? (r.share > 0.08 ? T.clear : T.noisy) : T.wait;
      } else if (face) {
        const res = face.detectForVideo(v, performance.now());
        const lm = res.faceLandmarks && res.faceLandmarks[0];
        if (lm) {
          const e = (ear(LEFT_EYE.map((i) => lm[i])) + ear(RIGHT_EYE.map((i) => lm[i]))) / 2;
          const s = counter.push(e), st = counter.state();
          $("val").textContent = Math.round(st.blinks / Math.max(sec / 60, 1 / 60));
          $("q").textContent = T.closed.replace("{p}", Math.round(100 * st.closedShare));
        } else { $("q").textContent = T.noface; }
      }
      requestAnimationFrame(tick);
    };
    tick();
  };
  function stop() {
    running = false; if (stream) stream.getTracks().forEach((t) => t.stop());
    $("vid").srcObject = null; $("go").textContent = T.start; $("msg").textContent = T.stopped;
  }
}
