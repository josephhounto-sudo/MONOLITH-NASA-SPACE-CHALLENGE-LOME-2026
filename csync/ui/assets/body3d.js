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

// region id -> parts: [kind, x, y, z, radius, length, rotZ]
const PARTS = {
  "region-head": [["sphere", 0, 2.62, 0, 0.30]],
  "region-chest": [["capsule", 0, 1.86, 0, 0.40, 0.42, 0], ["sphere", -0.47, 2.17, 0, 0.15], ["sphere", 0.47, 2.17, 0, 0.15]],
  "region-abdomen": [["capsule", 0, 1.28, 0, 0.35, 0.26, 0]],
  "region-arm": [["capsule", -0.56, 1.72, 0, 0.12, 0.70, 0.12], ["capsule", 0.56, 1.72, 0, 0.12, 0.70, -0.12]],
  "region-hand": [["sphere", -0.63, 1.13, 0, 0.12], ["sphere", 0.63, 1.13, 0, 0.12]],
  "region-legs": [["capsule", -0.19, 0.50, 0, 0.15, 0.80, 0.02], ["capsule", 0.19, 0.50, 0, 0.15, 0.80, -0.02]],
};

function partsFor(region) { return PARTS[region] || []; }

if (typeof module !== "undefined") module.exports = { zoneLook, partsFor, PARTS, LOOK, SELECTED_GLOW };

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
    scene.add(body);
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.11, 0.13, 0.22, 24),
      new THREE.MeshPhysicalMaterial({ color: 0x9C8373, roughness: 0.5 }));
    neck.position.set(0, 2.28, 0); body.add(neck);
    for (const [region, status] of Object.entries(cfg.status)) {
      const look = zoneLook(status, region === cfg.selected);
      for (const [kind, x, y, z, r, len, rot] of partsFor(region)) {
        const geo = kind === "sphere" ? new THREE.SphereGeometry(r, 40, 28) : new THREE.CapsuleGeometry(r, len, 10, 28);
        const mat = new THREE.MeshPhysicalMaterial({ color: look.color, roughness: 0.32, clearcoat: 0.8, clearcoatRoughness: 0.25,
          transparent: look.opacity < 1, opacity: look.opacity, emissive: look.emissive, emissiveIntensity: look.emissive ? 0.9 : 0 });
        const m = new THREE.Mesh(geo, mat);
        m.position.set(x, y, z); m.rotation.z = rot || 0;
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
    (function loop() {
      if (spin) angle += 0.004;
      body.rotation.y = angle;
      renderer.render(scene, cam);
      requestAnimationFrame(loop);
    })();
  })();
}
