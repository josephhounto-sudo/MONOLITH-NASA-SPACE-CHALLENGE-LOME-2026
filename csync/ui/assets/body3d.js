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
// callout anchors (body space) and label side, like an anatomical chart: a leader line from the zone to its label
const CALLOUTS = { "region-head": [0, 2.62, 0.2, "L"], "region-chest": [0.15, 1.95, 0.3, "R"], "region-arm": [-0.57, 1.6, 0.05, "L"],
                   "region-hand": [0.62, 0.96, 0.1, "R"], "region-abdomen": [0, 1.15, 0.3, "L"], "region-legs": [0.18, 0.45, 0.12, "R"] };
const FOCUS = { "region-head": 2.55, "region-chest": 1.9, "region-abdomen": 1.2, "region-arm": 1.6, "region-hand": 1.0,
                "region-legs": 0.45, "region-body": 1.35, "region-habitat": 0.6 };

// Embedded model (V3): "Cesium Man", Khronos glTF Sample Assets, CC BY 4.0 (c) Cesium 2017, loaded from a pinned CDN copy.
// The mesh is one piece, so zones are drawn by position bands (normalised by the figure height H), measured on its A-pose.
// Same thresholds in JS (picking, tests) and in the shader (highlight); its texture and logo are never used.
const ZONE_IDS = ["region-head", "region-chest", "region-abdomen", "region-arm", "region-hand", "region-legs"];
function zoneOf(ax, y) {   // ax = |x| / H, y = height / H
  if (ax >= 0.312) return "region-hand";
  if (ax >= 0.093 && y > 0.53) return "region-arm";
  if (y > 0.777) return "region-head";
  if (y > 0.584) return "region-chest";
  if (y > 0.418) return "region-abdomen";
  return "region-legs";
}
const CALLOUTS_MODEL = { "region-head": [0, 0.88, "L"], "region-chest": [0.05, 0.68, "R"], "region-arm": [-0.2, 0.66, "L"],
                         "region-hand": [0.355, 0.55, "R"], "region-abdomen": [0, 0.50, "L"], "region-legs": [0.07, 0.22, "R"] };

function partsFor(region) { return PARTS[region] || []; }

if (typeof module !== "undefined") module.exports = { zoneOf, ZONE_IDS, CALLOUTS_MODEL, zoneLook, partsFor, PARTS, PROFILES, FOCUS, CALLOUTS, LOOK, SELECTED_GLOW };

if (typeof document !== "undefined" && window.CS_BODY) {
  (async () => {
    const cfg = window.CS_BODY;
    const host = document.getElementById("stage");
    let THREE;
    try {
      THREE = await import("three");   // resolved by the page's import map (pinned version)
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
    // soft contact shadow drawn on a canvas (no texture file)
    const sc = document.createElement("canvas"); sc.width = sc.height = 128;
    const g2 = sc.getContext("2d"); const gr = g2.createRadialGradient(64, 64, 4, 64, 64, 62);
    gr.addColorStop(0, "rgba(0,0,0,.55)"); gr.addColorStop(1, "rgba(0,0,0,0)"); g2.fillStyle = gr; g2.fillRect(0, 0, 128, 128);
    const shadow = new THREE.Mesh(new THREE.PlaneGeometry(1.6, 1.0), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sc), transparent: true, depthWrite: false }));
    shadow.rotation.x = -Math.PI / 2; shadow.position.y = 0.012; scene.add(shadow);
    const HM = 2.75;   // figure height in scene units
    let model = null;
    if (cfg.model) {
      try {
        const { GLTFLoader } = await import("three/addons/loaders/GLTFLoader.js");
        const gltf = await new GLTFLoader().loadAsync(cfg.model);
        model = gltf.scene;
        const b0 = new THREE.Box3().setFromObject(model);
        model.scale.setScalar(HM / b0.getSize(new THREE.Vector3()).y);
        const b1 = new THREE.Box3().setFromObject(model), c1 = b1.getCenter(new THREE.Vector3());
        model.position.set(-c1.x, -b1.min.y, -c1.z);
        const sel = ZONE_IDS.indexOf(cfg.selected);
        const off = ZONE_IDS.map((z) => (cfg.status[z] === "measured" ? 0 : 1));
        const uni = { uH: { value: HM }, uSel: { value: sel }, uOff: { value: off }, uBodyInv: { value: new THREE.Matrix4() } };
        model.traverse((o) => {
          if (!o.isMesh) return;
          const mat = new THREE.MeshPhysicalMaterial({ color: 0xE9D7C6, roughness: 0.34, clearcoat: 0.75, clearcoatRoughness: 0.3, transparent: true });
          mat.onBeforeCompile = (sh) => {
            Object.assign(sh.uniforms, uni);
            sh.vertexShader = "uniform mat4 uBodyInv;\nvarying vec3 vLoc;\n" + sh.vertexShader.replace("#include <skinning_vertex>",
              "#include <skinning_vertex>\n vLoc = (uBodyInv * modelMatrix * vec4(transformed, 1.0)).xyz;");
            sh.fragmentShader = "uniform float uH; uniform float uSel; uniform float uOff[6];\nvarying vec3 vLoc;\n" +
              "float zoneOf(float ax, float y){ if (ax >= 0.312) return 4.0; if (ax >= 0.093 && y > 0.53) return 3.0;" +
              " if (y > 0.777) return 0.0; if (y > 0.584) return 1.0; if (y > 0.418) return 2.0; return 5.0; }\n" +
              sh.fragmentShader.replace("#include <color_fragment>", "#include <color_fragment>\n float zz = zoneOf(abs(vLoc.x) / uH, vLoc.y / uH);" +
                "\n if (vLoc.y / uH > 0.765) discard;" +   // the model's head is a flat logo disc: replaced by a sphere below
                "\n if (uOff[int(zz)] > 0.5) { diffuseColor.rgb *= 0.55; diffuseColor.a *= 0.38; }" +
                "\n if (abs(zz - uSel) < 0.5) diffuseColor.rgb = mix(diffuseColor.rgb, vec3(1.0, 0.45, 0.2), 0.85);")
              .replace("#include <emissivemap_fragment>", "#include <emissivemap_fragment>\n if (abs(zz - uSel) < 0.5) totalEmissiveRadiance += vec3(1.0, 0.42, 0.16) * 0.7;");
          };
          o.material = mat;
          o.userData.model = true;
          pickable.push(o);
        });
        body.add(model);
        body.userData.uni = uni;
        const hl = zoneLook(cfg.status["region-head"], cfg.selected === "region-head");
        const head = new THREE.Mesh(new THREE.SphereGeometry(0.1 * HM, 48, 32), new THREE.MeshPhysicalMaterial({ color: hl.color,
          roughness: 0.34, clearcoat: 0.75, emissive: hl.emissive, emissiveIntensity: hl.emissive ? 0.9 : 0 }));
        head.scale.set(0.9, 1.08, 0.95); head.position.set(0, 0.862 * HM, 0.01); head.userData.region = "region-head";
        pickable.push(head); body.add(head);
      } catch (e) { model = null; }   // the code-built mannequin below takes over, never a blank frame
    }
    if (!model) {
    const neck = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.11, 0.2, 24),
        new THREE.MeshPhysicalMaterial({ color: 0xC9B4A2, roughness: 0.45 }));
      neck.position.set(0, 2.36, 0); body.add(neck);
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
        let rid = hit.object.userData.region;
        if (hit.object.userData.model) {
          const p = body.worldToLocal(hit.point.clone());
          rid = zoneOf(Math.abs(p.x) / HM, p.y / HM);
        }
        tip.textContent = (cfg.labels[rid] || rid) + " — " + (cfg.words[cfg.status[rid]] || "");
        tip.style.left = (e.clientX - r.left + 14) + "px"; tip.style.top = (e.clientY - r.top + 10) + "px"; tip.style.opacity = 1;
      } else if (tip) { tip.style.opacity = 0; }
    });
    // callouts: projected each frame; the selected zone's label is highlighted
    const overlay = document.getElementById("callouts");
    const anchors = model ? Object.fromEntries(Object.entries(CALLOUTS_MODEL).map(([k, [x, y, sd]]) => [k, [x * HM, y * HM, 0.1, sd]])) : CALLOUTS;
    const calls = Object.entries(anchors).map(([rid, [x, y, z, side]]) => {
      const el = document.createElement("div");
      el.className = "co" + (rid === cfg.selected ? " sel" : "") + (cfg.status[rid] === "measured" ? "" : " off");
      el.innerHTML = "<b>" + (cfg.labels[rid] || rid) + "</b><span>" + ((cfg.methods && cfg.methods[rid]) || (cfg.status[rid] === "measured" ? cfg.measuredWord : cfg.offWord)) + "</span>";
      overlay.appendChild(el);
      const line = document.createElementNS("http://www.w3.org/2000/svg", "path");
      line.setAttribute("class", "ld" + (rid === cfg.selected ? " sel" : ""));
      document.getElementById("leaders").appendChild(line);
      return { rid, v: new THREE.Vector3(x, y, z), side, el, line };
    });
    // sensor points: a small light where each measured zone is read (no loop, no pulse: static marks)
    for (const rid of cfg.sensors || []) {
      const a = anchors[rid]; if (!a || cfg.status[rid] !== "measured") continue;
      const dot = new THREE.Mesh(new THREE.SphereGeometry(0.045, 20, 14), new THREE.MeshBasicMaterial({ color: rid === cfg.selected ? SELECTED_GLOW : 0xFFE3C8 }));
      dot.position.set(a[0], a[1], rid === "region-head" ? 0.33 : (a[2] || 0) + 0.12); body.add(dot);
      const halo = new THREE.Mesh(new THREE.RingGeometry(0.06, 0.085, 32), new THREE.MeshBasicMaterial({ color: 0xFF8A4C, transparent: true, opacity: 0.8, side: THREE.DoubleSide }));
      halo.position.copy(dot.position); body.add(halo);
    }
    function placeCallouts() {
      const Wd = renderer.domElement.clientWidth, Hd = renderer.domElement.clientHeight;
      calls.forEach((c, i) => {
        const p = body.localToWorld(c.v.clone()); p.project(cam);
        const px = (p.x * 0.5 + 0.5) * Wd, py = (-p.y * 0.5 + 0.5) * Hd;
        const lx = c.side === "L" ? 14 : Wd - 14 - c.el.offsetWidth;
        const ly = Math.max(6, Math.min(Hd - 40, py - 16));
        c.el.style.left = lx + "px"; c.el.style.top = ly + "px";
        const ex = c.side === "L" ? lx + c.el.offsetWidth : lx;
        c.line.setAttribute("d", `M${ex},${ly + 16} L${(ex + px) / 2},${ly + 16} L${px},${py}`);
      });
    }
    const focusY = 1.25 + 0.25 * ((FOCUS[cfg.selected] ?? 1.45) - 1.45);
    let lookY = 1.45, camY = 1.6, dist = 7.2;
    const near = cfg.selected && cfg.selected !== "region-body" && cfg.selected !== "region-habitat";
    (function loop() {
      if (spin) angle += 0.004;
      body.rotation.y = angle;
      if (body.userData.uni) { body.updateMatrixWorld(); body.userData.uni.uBodyInv.value.copy(body.matrixWorld).invert(); }
      lookY += (focusY - lookY) * 0.06; camY += (focusY + 0.15 - camY) * 0.06; dist += ((near ? 6.6 : 7.4) - dist) * 0.06;
      cam.position.set(0, camY, dist); cam.lookAt(0, lookY, 0);
      renderer.render(scene, cam);
      placeCallouts();
      requestAnimationFrame(loop);
    })();
  })();
}
