/* C-Sync live console: public ISS telemetry (NASA ISSLive feed via push.lightstreamer.com, adapter "ISSLIVE"),
   world clocks (browser Intl), context only. Pure functions are exported for tests (node); the browser part runs only
   when a document exists. Rules (docs/PLAN_V3.md): age of the reading always shown; frozen value flagged; after a signal loss the last value stays
   on screen with the time it was received (Joseph, 20/11: no empty box), never as a fresh value. */
"use strict";

const LIMIT_PPCO2_MMHG = 3.0;          // NASA-STD-3001 Vol 2 V2 6004 (1-hour average), compared to a single live reading: context only
const PSI_TO_MMHG = 51.7149;
const STALE_S = 30;                    // station clock silent for 30 s -> signal lost -> 'Last known' with its time (design parameter, not NASA)
const FROZEN_MIN = 60;                 // same value for 60 min while the signal is up -> flagged (design parameter)
// The feed sends a value only when it changes (MERGE mode), so a quiet CO2 is not a stale CO2. Freshness is judged from
// the station clock item (TIME_000001), which ticks continuously while the ground has signal.

// The feed dictionary labels these PSIA, but the values seen on 20/11/2026 (cabin ~752) are mmHg-sized.
// Decide from the cabin pressure itself: 600-900 = mmHg, 10-17 = psi. Anything else = units unknown.
function unitMode(cabin) {
  if (typeof cabin !== "number" || !isFinite(cabin)) return "unknown";
  if (cabin >= 600 && cabin <= 900) return "mmhg";
  if (cabin >= 10 && cabin <= 17) return "psi";
  return "unknown";
}

function toMmhg(v, mode) {
  if (typeof v !== "number" || !isFinite(v) || mode === "unknown") return null;
  return mode === "psi" ? v * PSI_TO_MMHG : v;
}

// state of one live reading: words, never colour alone
function readingState(value, clockAt, changedAt, now) {
  if (value === null || clockAt === null) return { word: "Connecting", why: "waiting for the first reading from the station", show: false };
  const silent = (now - clockAt) / 1000;
  if (silent > STALE_S) {
    const t = new Date(clockAt).toISOString().slice(11, 16);
    return { word: "Last known", why: "received at " + t + " UTC; station signal lost " + Math.max(1, Math.round(silent / 60)) + " min ago (normal on the station)", show: true };
  }
  const still = (now - changedAt) / 60000;
  if (still >= FROZEN_MIN) return { word: "Check", why: "same value for " + Math.round(still) + " min while the signal is up: sensor or feed may be frozen", show: true };
  return { word: "Live", why: still < 1 ? "changed less than a minute ago" : "stable for " + Math.round(still) + " min, signal up", show: true };
}

function co2Context(mmhg) {
  if (mmhg === null) return "";
  return mmhg > LIMIT_PPCO2_MMHG ? "above the NASA 1-hour limit of 3 mmHg (one reading, context only)"
                                 : "below the NASA 1-hour limit of 3 mmHg (one reading, context only)";
}

function deltaText(mmhg) {
  if (mmhg === null) return "";
  const d = LIMIT_PPCO2_MMHG - mmhg;
  return (d >= 0 ? "\u2193 " : "\u2191 ") + Math.abs(d).toFixed(2) + (d >= 0 ? " under limit" : " over limit");
}

function o2Percent(ppo2, cabin) {
  if (ppo2 === null || cabin === null || cabin <= 0) return null;
  return 100 * ppo2 / cabin;
}

const ZONES = [["Station (UTC)", "UTC"], ["Houston", "America/Chicago"], ["Moscow", "Europe/Moscow"], ["Lomé", "Africa/Lome"]];
function clockText(date, tz) {
  return new Intl.DateTimeFormat("en-GB", { timeZone: tz, hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false }).format(date);
}

if (typeof module !== "undefined") {
  module.exports = { deltaText, unitMode, toMmhg, readingState, co2Context, o2Percent, clockText, ZONES, LIMIT_PPCO2_MMHG, STALE_S, FROZEN_MIN };
}

if (typeof document !== "undefined") {
  const ITEMS = { co2lab: "USLAB000055", co2n3: "NODE3000003", o2lab: "USLAB000053", cabin: "USLAB000058", clock: "TIME_000001" };
  const raw = {}, recv = {}, changed = {};
  const $ = (id) => document.getElementById(id);

  function paint() {
    const now = Date.now();
    ZONES.forEach(([, tz], i) => { const el = $("clk" + i); if (el) el.textContent = clockText(new Date(now), tz); });
    const mode = unitMode(raw.cabin);
    const cabin = toMmhg(raw.cabin, mode);
    const rows = [
      ["co2lab", toMmhg(raw.co2lab, mode), 2],
      ["co2n3", toMmhg(raw.co2n3, mode), 2],
      ["o2", o2Percent(toMmhg(raw.o2lab, mode), cabin), 1],
      ["cabin", cabin, 0],
    ];
    rows.forEach(([key, v, dp]) => {
      const src = key === "o2" ? "o2lab" : key;
      const st = readingState(v, recv.clock ?? null, changed[src] ?? now, now);
      $("v-" + key).textContent = (v === null || !st.show) ? "--" : v.toFixed(dp);
      $("s-" + key).textContent = st.word;
      $("w-" + key).textContent = st.why;
      $("c-" + key).dataset.state = st.word;
    });
    const up = recv.clock !== undefined;   // context stays with the value, live or last known
    $("ctx-co2lab").textContent = up ? co2Context(toMmhg(raw.co2lab, mode)) : "";
    $("d-co2lab").textContent = up ? deltaText(toMmhg(raw.co2lab, mode)) : "";
    $("d-co2n3").textContent = up ? deltaText(toMmhg(raw.co2n3, mode)) : "";
    $("ctx-co2n3").textContent = up ? co2Context(toMmhg(raw.co2n3, mode)) : "";
    $("unit").textContent = (raw.cabin !== undefined && mode === "unknown") ? "Units not recognised: values hidden." : "";
  }

  function start() {
    if (typeof LightstreamerClient === "undefined") { $("feed").textContent = "Live feed unreachable from this browser (network or firewall). The values above stay empty rather than show an old reading."; return; }
    const client = new LightstreamerClient("https://push.lightstreamer.com", "ISSLIVE");
    const sub = new Subscription("MERGE", Object.values(ITEMS), ["Value"]);
    sub.setRequestedSnapshot("yes");
    const byId = Object.fromEntries(Object.entries(ITEMS).map(([k, v]) => [v, k]));
    sub.addListener({ onItemUpdate: (u) => {
      const k = byId[u.getItemName()], v = parseFloat(u.getValue("Value"));
      if (!k || !isFinite(v)) return;
      const t = Date.now();
      if (raw[k] !== v) changed[k] = t;
      raw[k] = v; recv[k] = t;
    } });
    client.addListener({ onStatusChange: (s) => { $("feed").textContent = "Feed: " + s.replace(/:.*$/, "").toLowerCase(); } });
    client.subscribe(sub);
    client.connect();
  }
  paint();
  setInterval(paint, 1000);
  start();
}
