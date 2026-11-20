/* C-Sync body in 3D: a mannequin built in code from spheres and capsules (no downloaded model, so no model licence),
   rendered with three.js 0.187.0 (MIT). The look of each zone comes from its status in pitch/silhouette/fiches.json:
   measured = solid smoky cream, unknown = faded glass (never shown as normal), context = floor only.
   The selected zone glows orange. Drag to turn; a slow turn stops at the first touch and is off when the system asks
   for reduced motion. Pure functions are exported for node tests; the browser part runs only when a document exists. */
"use strict";

const LOOK = {
  measured: { color: 0xE9D7C6, opacity: 1.0, emissive: 0x000000 },
  unknown: { color: 0x8A7C72, opacity: 0.32, emissive: 0x000000 },
  context: { color: 0x6E625A, opacity: 0.5, emissive: 0x000000 },
};
const SELECTED_GLOW = 0xFF8A4C;

function zoneLook(status, selected) {
  const base = LOOK[status] || LOOK.unknown;          // an unexpected status is never drawn as measured
  return selected ? { color: base.color, opacity: Math.max(base.opacity, 0.85), emissive: SELECTED_GLOW } : { ...base };
}

// region id -> parts: [kind, x, y, z, a, b, rotZ, sx, sy, sz]. kinds: sphere (a = radius), capsule (a = radius, b = length),
// torso / pelvis (lathe profiles). Proportions follow a plain 7.5-head figure; it is a neutral shape, not a person.
const PARTS = {
  "region-head": [["sphere", 0, 2.62, 0, 0.26, 0, 0, 0.92, 1.08, 1.0]],
  "region-chest": [["torso", 0, 1.58, 0], ["sphere", -0.46, 2.12, 0, 0.13], ["sphere", 0.46, 2.12, 0, 0.13]],
  "region-abdomen": [["pelvis", 0, 1.02, 0]],
  "region-arm": [["capsule", -0.53, 1.82, 0, 0.095, 0.42, 0.10], ["capsule", 0.53, 1.82, 0, 0.095, 0.42, -0.10],
                 ["capsule", -0.60, 1.30, 0.04, 0.08, 0.40, 0.04], ["capsule", 0.60, 1.30, 0.04, 0.08, 0.40, -0.04],
                 ["sphere", -0.575, 1.56, 0.02, 0.092], ["sphere", 0.575, 1.56, 0.02, 0.092]],
  "region-hand": [["sphere", -0.62, 0.96, 0.06, 0.085, 0, 0, 0.8, 1.35, 0.55], ["sphere", 0.62, 0.96, 0.06, 0.085, 0, 0, 0.8, 1.35, 0.55]],
  "region-legs": [["capsule", -0.17, 0.66, 0, 0.13, 0.48, 0.02], ["capsule", 0.17, 0.66, 0, 0.13, 0.48, -0.02],
                  ["capsule", -0.18, 0.18, 0, 0.10, 0.42, 0], ["capsule", 0.18, 0.18, 0, 0.10, 0.42, 0],
                  ["sphere", -0.175, 0.41, 0.01, 0.112], ["sphere", 0.175, 0.41, 0.01, 0.112],
                  ["sphere", -0.18, -0.12, 0.08, 0.10, 0, 0, 0.9, 0.5, 1.7], ["sphere", 0.18, -0.12, 0.08, 0.10, 0, 0, 0.9, 0.5, 1.7]],
};
// lathe profiles [radius, height] from bottom to top
const PROFILES = {
  torso: [[0.001, 0], [0.30, 0.02], [0.29, 0.18], [0.31, 0.34], [0.38, 0.50], [0.42, 0.62], [0.40, 0.70], [0.20, 0.76], [0.001, 0.77]],
  pelvis: [[0.001, 0], [0.28, 0.02], [0.33, 0.14], [0.32, 0.30], [0.29, 0.40], [0.001, 0.42]],
};
const FOCUS = { "region-head": 2.55, "region-chest": 1.9, "region-abdomen": 1.2, "region-arm": 1.6, "region-hand": 1.0,
                "region-legs": 0.45, "region-body": 1.35, "region-habitat": 0.6 };

function partsFor(region) { return PARTS[region] || []; }

if (typeof module !== "undefined") module.exports = { zoneLook, partsFor, PARTS, PROFILES, FOCUS, LOOK, SELECTED_GLOW };

if (typeof document !== "undefined" && window.CS_BODY) {
  (async () => {
    const cfg = window.CS_BODY;
    const host = document.getElementById("stage");
    let THREE;
    try {
      THREE = await import(cfg.three);
      const probe = document.createElement("canvas");
      if (!(probe.getContext("webgl2") || probe.getContext("webgl"))) throw new Error("no webgl");
    } catch (e) {
      host.innerHTML = cfg.fallback;                      // the flat map, never a blank frame
      return;
    }
    const W = host.clientWidth, H = host.clientHeight;
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(2, window.devicePixelRatio || 1));
    renderer.setSize(W, H);
    host.appendChild(renderer.domElement);
    const scene = new THREE.Scene();
    const cam = new THREE.PerspectiveCamera(32, W / H, 0.1, 50);
    cam.position.set(0, 1.6, 7.2);
    cam.lookAt(0, 1.45, 0);
    scene.add(new THREE.HemisphereLight(0xFFF2DA, 0x2E2621, 1.1));
    const key = new THREE.DirectionalLight(0xFFFBF5, 2.2); key.position.set(2.5, 4, 4); scene.add(key);
    const rim = new THREE.DirectionalLight(0xFF9A5C, 2.4); rim.position.set(-3, 2, -3); scene.add(rim);

    const body = new THREE.Group();
    body.position.y = 0.14;
    scene.add(body);
    const pickable = [];
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.11, 0.2, 24),
      new THREE.MeshPhysicalMaterial({ color: 0xC9B4A2, roughness: 0.45 }));
    neck.position.set(0, 2.36, 0); body.add(neck);
    // soft contact shadow drawn on a canvas (no texture file)
    const sc = document.createElement("canvas"); sc.width = sc.height = 128;
    const g2 = sc.getContext("2d"); const gr = g2.createRadialGradient(64, 64, 4, 64, 64, 62);
    gr.addColorStop(0, "rgba(0,0,0,.55)"); gr.addColorStop(1, "rgba(0,0,0,0)"); g2.fillStyle = gr; g2.fillRect(0, 0, 128, 128);
    const shadow = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.0), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.012; scene.add(shadow);
    for (const [region, status] of Object.entries(cfg.status)) {
      const look = zoneLook(status, region === cfg.selected);
      for (const [kind, x, y, z, r, len, rot, sx, sy, sz] of partsFor(region)) {
        const geo = kind === "sphere" ? new THREE.SphereGeometry(r, 40, 28)
          : kind === "capsule" ? new THREE.CapsuleGeometry(r, len, 10, 28)
          : new THREE.LatheGeometry(PROFILES[kind].map(([px, py]) => new THREE.Vector2(px, py)), 48);
        const mat = new THREE.MeshPhysicalMaterial({ color: look.color, roughness: 0.32, clearcoat: 0.8, clearcoatRoughness: 0.25,
          transparent: look.opacity < 1, opacity: look.opacity, emissive: look.emissive, emissiveIntensity: look.emissive ? 0.9 : 0 });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(x, y, z); m.rotation.z = rot || 0;
        if (sx) m.scale.set(sx, sy, sz);
        m.userData.region = region;
        pickable.push(m);
        body.add(m);
      }
    }
    // floor: the whole-body ring (measured) and the habitat disc (context only)
    const ringOn = cfg.status["region-body"] === "measured";
    const ring = new THREE.Mesh(new THREE.TorusGeometry(0.9, 0.025, 12, 96),
      new THREE.MeshBasicMaterial({ color: cfg.selected === "region-body" ? SELECTED_GLOW : 0xE9A27A, transparent: true, opacity: ringOn ? 0.9 : 0.3 }));
    ring.rotation.x = Math.PI / 2; ring.position.y = 0.02; scene.add(ring);
    const disc = new THREE.Mesh(new THREE.CircleGeometry(1.7, 64), new THREE.MeshBasicMaterial({
      color: cfg.selected === "region-habitat" ? SELECTED_GLOW : 0xD79A76, transparent: true, opacity: cfg.selected === "region-habitat" ? 0.35 : 0.14 }));
    disc.rotation.x = -Math.PI / 2; disc.position.y = 0.0; scene.add(disc);

    const still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let spin = !still, drag = null, angle = -0.35;
    renderer.domElement.style.touchAction = "pan-y";
    renderer.domElement.addEventListener("pointerdown", (e) => { drag = e.clientX; spin = false; });
    window.addEventListener("pointerup", () => { drag = null; });
    window.addEventListener("pointermove", (e) => { if (drag !== null) { angle += (e.clientX - drag) * 0.01; drag = e.clientX; } });
    const tip = document.getElementById("tip");
    const ray = new THREE.Raycaster(), ptr = new THREE.Vector2();
    renderer.domElement.addEventListener("pointermove", (e) => {
      const r = renderer.domElement.getBoundingClientRect();
      ptr.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
      ray.setFromCamera(ptr, cam);
      const hit = ray.intersectObjects(pickable)[0];
      if (hit && tip) {
        const rid = hit.object.userData.region;
        tip.textContent = (cfg.labels[rid] || rid) + " — " + (cfg.words[cfg.status[rid]] || "");
        tip.style.left = (e.clientX - r.left + 14) + "px"; tip.style.top = (e.clientY - r.top + 10) + "px"; tip.style.opacity = 1;
      } else if (tip) { tip.style.opacity = 0; }
    });
    const focusY = FOCUS[cfg.selected] ?? 1.45;
    let lookY = 1.45, camY = 1.6, dist = 7.2;
    const near = cfg.selected && cfg.selected !== "region-body" && cfg.selected !== "region-habitat";
    (function loop() {
      if (spin) angle += 0.004;
      body.rotation.y = angle;
      lookY += (focusY - lookY) * 0.06; camY += (focusY + 0.15 - camY) * 0.06; dist += ((near ? 5.6 : 7.2) - dist) * 0.06;
      cam.position.set(0, camY, dist); cam.lookAt(0, lookY, 0);
      renderer.render(scene, cam);
      requestAnimationFrame(loop);
    })();
  })();
}
