// Star Wars style 3D text crawl for the homepage hero.
// Progressive enhancement: the static <h1> stays in the DOM for screen readers
// and search, and is shown instead when WebGL is missing or motion is reduced.
import * as THREE from 'three';

const hero = document.querySelector('.hero');
const canvas = hero?.querySelector('.crawl-canvas');
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Two line breaks of the same text: wide screens, and portrait phones where
// shorter lines let each glyph render larger. A null entry separates the coda.
const LAYOUTS = {
  wide: [
    'Sovereign Source AI is AI whose',
    'complete operational stack can be',
    'owned, inspected, governed,',
    'deployed, modified, moved,',
    'and operated independently',
    'of any single external provider.',
    null,
    'Self-hosting a model is not sovereignty.',
    'Sovereignty is a system property.',
  ],
  narrow: [
    'Sovereign Source AI',
    'is AI whose complete',
    'operational stack',
    'can be owned,',
    'inspected, governed,',
    'deployed, modified,',
    'moved, and operated',
    'independently of any',
    'single external',
    'provider.',
    null,
    'Self-hosting a model',
    'is not sovereignty.',
    'Sovereignty is a',
    'system property.',
  ],
};
const layoutFor = (aspect) => (aspect < 0.85 ? 'narrow' : 'wide');

const CRAWL_COLOR = getComputedStyle(document.documentElement)
  .getPropertyValue('--crawl').trim() || '#ffe81f';
const SPEED = 0.55;       // plane units per second
const PLANE_WIDTH = 9;    // world units
const TILT = -0.95;       // radians the text plane leans back
const FOV = 50;

function webglAvailable() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch { return false; }
}

async function textTexture(layout, maxAnisotropy) {
  const lines = LAYOUTS[layout];
  const font = '"Instrument Sans", "Helvetica Neue", Arial, sans-serif';
  try {
    await Promise.race([
      document.fonts.load(`500 120px "Instrument Sans"`),
      new Promise((r) => setTimeout(r, 1500)),
    ]);
  } catch { /* fall back to system sans */ }

  const W = layout === 'narrow' ? 1280 : 2048;
  const size = 118, lineH = size * 1.32, pad = size;
  const H = Math.ceil(pad * 2 + lineH * lines.length);
  const c = document.createElement('canvas');
  c.width = W; c.height = H;
  const ctx = c.getContext('2d');
  ctx.fillStyle = CRAWL_COLOR;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const codaStart = lines.indexOf(null);
  lines.forEach((line, i) => {
    if (line === null) return;
    const isCoda = i > codaStart;
    ctx.font = `${isCoda ? 400 : 500} ${isCoda ? size * 0.9 : size}px ${font}`;
    ctx.fillText(line, W / 2, pad + lineH * (i + 0.5), W - 80);
  });

  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  tex.anisotropy = maxAnisotropy;
  tex.generateMipmaps = true;
  tex.minFilter = THREE.LinearMipmapLinearFilter;
  return { tex, aspect: H / W };
}

function starfield(count = 1600) {
  const pos = new Float32Array(count * 3);
  for (let i = 0; i < count; i++) {
    // Points on a large shell so stars sit well behind the crawl.
    const u = Math.random() * 2 - 1, t = Math.random() * Math.PI * 2;
    const r = 60 + Math.random() * 40, s = Math.sqrt(1 - u * u);
    pos.set([r * s * Math.cos(t), r * s * Math.sin(t), r * u], i * 3);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
  const m = new THREE.PointsMaterial({
    color: 0xffffff, size: 0.18, sizeAttenuation: true, fog: false,
    transparent: true, opacity: 0.85, depthWrite: false,
  });
  return new THREE.Points(g, m);
}

async function start() {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x000000, 1);
  const maxAniso = renderer.capabilities.getMaxAnisotropy();

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(0x000000, 6, 19); // distant text fades to black; range set in resize()
  const camera = new THREE.PerspectiveCamera(FOV, 1, 0.1, 200);
  scene.add(starfield());

  const group = new THREE.Group();
  group.rotation.x = TILT;
  group.position.y = -1.6;
  scene.add(group);

  // The crawl enters from just below the frame and exits once it has faded out.
  let plane = null, layout = null, startY = 0, endY = 0;

  async function build(next) {
    const { tex, aspect } = await textTexture(next, maxAniso);
    const planeH = PLANE_WIDTH * aspect;
    const mesh = new THREE.Mesh(
      new THREE.PlaneGeometry(PLANE_WIDTH, planeH),
      new THREE.MeshBasicMaterial({ map: tex, transparent: true, depthWrite: false }),
    );
    // Keep progress through the crawl when swapping layouts mid-scroll.
    const progress = plane ? (plane.position.y - startY) / (endY - startY) : 0.12;
    if (plane) {
      group.remove(plane);
      plane.geometry.dispose(); plane.material.map.dispose(); plane.material.dispose();
    }
    startY = -planeH / 2 - 3.2;
    endY = planeH / 2 + 16;
    mesh.position.y = startY + progress * (endY - startY);
    group.add(mesh);
    plane = mesh;
    layout = next;
  }

  function resize() {
    const w = hero.clientWidth, h = hero.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // Back the camera off until the full crawl width fits where the text enters.
    const halfH = Math.tan(THREE.MathUtils.degToRad(FOV / 2));
    const fitZ = (PLANE_WIDTH * 0.62) / (halfH * camera.aspect);
    const z = Math.max(6.5, fitZ);
    camera.position.set(0, 0, z);
    camera.lookAt(0, 0.9 * (z / 6.5), 0);
    scene.fog.near = z + 1;
    scene.fog.far = z + 13;
    camera.updateProjectionMatrix();
    const want = layoutFor(camera.aspect);
    if (plane && want !== layout) build(want);
  }

  // Size the hero for the crawl before measuring it.
  hero.classList.add('crawl-active');
  await build(layoutFor(hero.clientWidth / hero.clientHeight));
  resize();
  window.addEventListener('resize', resize);

  let visible = true, last = performance.now();
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; last = performance.now(); })
    .observe(hero);

  renderer.setAnimationLoop((now) => {
    if (!visible) return;
    const dt = Math.min((now - last) / 1000, 0.1);
    last = now;
    plane.position.y += SPEED * dt;
    if (plane.position.y > endY) plane.position.y = startY;
    renderer.render(scene, camera);
  });
}

if (hero && canvas && !reduceMotion && webglAvailable()) {
  start().catch((err) => {
    console.warn('Crawl disabled:', err);
    hero.classList.remove('crawl-active');
  });
}
