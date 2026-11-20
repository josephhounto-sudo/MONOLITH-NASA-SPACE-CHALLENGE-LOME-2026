/* C-Sync live console: public ISS telemetry (NASA ISSLive feed via push.lightstreamer.com, adapter "ISSLIVE"),
   world clocks (browser Intl), context only. Pure functions are exported for tests (node); the browser part runs only
   when a document exists. Rules (docs/PLAN_V3.md): age of the reading always shown; frozen value flagged; no reading = Unknown. */
"use strict";

const LIMIT_PPCO2_MMHG = 3.0;          // NASA-STD-3001 Vol 2 V2 6004 (1-hour average), compared to a single live reading: context only
const PSI_TO_MMHG = 51.7149;
const STALE_S = 120;                   // no update for 2 min -> Unknown (design parameter, not NASA)
const FROZEN_MIN = 15;                 // same value for 15 min -> flagged as possibly frozen (design parameter)

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
function readingState(value, receivedAt, changedAt, now) {
  if (value === null || receivedAt === null) return { word: "Unknown", why: "no live reading" };
  const age = (now - receivedAt) / 1000;
  if (age > STALE_S) return { word: "Unknown", why: "no update for " + Math.round(age / 60) + " min (signal loss is normal on the station)" };
  const still = (now - changedAt) / 60000;
  if (still >= FROZEN_MIN) return { word: "Check", why: "same value for " + Math.round(still) + " min: sensor or feed may be frozen" };
  return { word: "Live", why: "received " + Math.round(age) + " s ago" };
}

function co2Context(mmhg) {
  if (mmhg === null) return "";
  return mmhg > LIMIT_PPCO2_MMHG ? "above the NASA 1-hour limit of 3 mmHg (one reading, context only)"
                                 : "below the NASA 1-hour limit of 3 mmHg (one reading, context only)";
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
  module.exports = { unitMode, toMmhg, readingState, co2Context, o2Percent, clockText, ZONES, LIMIT_PPCO2_MMHG, STALE_S, FROZEN_MIN };
}

if (typeof document !== "undefined") {
  const ITEMS = { co2lab: "USLAB000055", co2n3: "NODE3000003", o2lab: "USLAB000053", cabin: "USLAB000058", temp: "USLAB000059" };
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
      const st = readingState(v, recv[src] ?? null, changed[src] ?? now, now);
      $("v-" + key).textContent = v === null ? "--" : v.toFixed(dp);
      $("s-" + key).textContent = st.word;
      $("w-" + key).textContent = st.why;
      $("c-" + key).dataset.state = st.word;
    });
    $("ctx-co2lab").textContent = co2Context(toMmhg(raw.co2lab, mode));
    $("ctx-co2n3").textContent = co2Context(toMmhg(raw.co2n3, mode));
    $("unit").textContent = (raw.cabin !== undefined && mode === "unknown") ? "Units not recognised: values hidden." : "";
  }

  function start() {
    if (typeof LightstreamerClient === "undefined") { $("feed").textContent = "Live feed unreachable from this browser: showing Unknown, never an old value."; return; }
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
