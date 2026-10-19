/**
 * World: three layers of a world - sea, land, sky - stacked as rounded plates
 * on a plinth, each leaning a little off the one below so the stack is composed
 * at rest. The pointer's height picks a layer; the chosen plate rises clear of
 * the stack, staged outwards for the ones it passes, takes the bright edge and
 * the others dip a little so the answer shows ink. At rest the land's edge is
 * bright, where the eye should start. The slider scales how far it rises.
 */
const {
  Cam, facing, fit, proj, rings, prism, solid, put, tset, tval, tdone,
  tween, disposer, mk, pointer, register,
} = HL;

const SZ = 92, PLATE = 10, ROFF = 12;
const Z0 = [0, PLATE, PLATE * 2];
const OA = [[0, 0], [5, 3], [10, 6]];  /* rest lean of sea, land, sky */
const LIFT = [10, 16, 22];
function mount({ stage, svg, read }, value) {
  const bag = disposer();
  let slide = value;

  const C = Cam(45, 0.5, 1.95);
  fit(C, [[-SZ / 2, -SZ / 2, 0], [SZ / 2 + 10, SZ / 2 + 6, 0], [0, 0, PLATE * 3 + 22]], 200, 166);
  const P = proj(C), front = facing(C);

  const pl = solid(svg);
  const base = rings(-SZ / 2, -SZ / 2, SZ / 2, SZ / 2, ROFF, 2.4);
  put(pl, prism(P, front, base[0], base[1], 0, 3));

  const Ls = [];
  for (let i = 0; i < 3; i++) {
    const s = solid(svg);
    const r = rings(-SZ / 2 + OA[i][0], -SZ / 2 + OA[i][1], SZ / 2 + OA[i][0], SZ / 2 + OA[i][1], ROFF, 2.4);
    Ls.push({ sil: s.sil, cr: s.cr, i, r, tw: tween(0), last: null, drawn: false });
  }

  const hy = [0, 1, 2].map((i) => P(0, 0, Z0[i] + PLATE / 2)[1]);
  const band = (sy) => (sy >= (hy[0] + hy[1]) / 2 ? 0 : sy >= (hy[1] + hy[2]) / 2 ? 1 : 2);
  const B = register(stage, (_dt, now) => {
    let moving = false;
    Ls.forEach((L) => {
      const lift = tval(L.tw, now), z0 = Z0[L.i], z1 = Z0[L.i] + PLATE + lift;
      if (lift !== L.last || !L.drawn) {
        const pr = prism(P, front, L.r[0], L.r[1], z0, z1);
        L.sil.setAttribute("d", pr.sil);
        L.cr.setAttribute("d", pr.crease);
        L.last = lift; L.drawn = true;
      }
      if (!tdone(L.tw, now)) moving = true;
    });
    return moving;
  });
  bag.add(B.unregister);

  let act = -1;
  const NAME = ["sea", "land", "sky"];
  function setActive(a) {
    if (a === act) return;
    const from = a < 0 ? act : a;
    act = a;
    const now = performance.now(), mark = a < 0 ? 1 : a;
    Ls.forEach((L) => {
      const delay = a < 0 ? 0 : Math.abs(L.i - from) * 40;
      const to = a < 0 ? 0 : (L.i === a ? LIFT[L.i] : -3) * (slide / 26);
      tset(L.tw, to, now, delay);
      L.sil.classList.toggle("hi", L.i === mark);
    });
    read.textContent = a < 0 ? "rest" : NAME[a];
    B.wake();
  }
  setActive(-1);

  bag.add(pointer(stage, { move: (p) => setActive(band(p[1])), leave: () => setActive(-1) }));
  bag.add(() => svg.replaceChildren());

  return { set: (v) => { slide = v; }, destroy: bag.dispose };
}

hairline({
  name: "world",
  means: "Three layers of a world: sea, land and sky. The pointer raises the layer under it.",
  rules: [1, 2, 4, 5, 8, 9, 10],
  range: [14, 26, 40],
  tour: [[200, 122], [200, 158], [200, 195], null],
  mount,
});
