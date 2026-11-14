// FICHIER: pitch/tests/test_silhouette.js · 14/11/2026 09:00 Lomé · commit dc61786 · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
// Usage : npm install jsdom (ou NODE_PATH=<dossier>/node_modules) puis node pitch/tests/test_silhouette.js <fichier.html> <sortie_texte.txt>
// Test jsdom de pitch/silhouette/silhouette_demo.html
const fs = require('fs');
const { JSDOM } = require('jsdom');
const file = process.argv[2];
const src = fs.readFileSync(file, 'utf8');
let fails = 0;
const ok = (c, m) => { console.log((c ? 'PASS ' : 'FAIL ') + m); if (!c) fails++; };

ok(!/(src|href)\s*=\s*["']?(https?:)?\/\//i.test(src), 'aucune ressource externe (src/href http)');
ok(!/@import|url\(\s*["']?https?:/i.test(src), 'aucun @import ni url() externe');

const dom = new JSDOM(src, { runScripts: 'dangerously' });
const d = dom.window.document;
ok(d.getElementById('synthetic-banner')?.textContent.includes('SYNTHETIC DATA'), 'bandeau SYNTHETIC DATA présent');
ok(d.getElementById('mock-label')?.textContent.includes('À CONFIRMER M1'), 'étiquette « À CONFIRMER M1 — non codée » présente');
const ids = ['region-head','region-chest','region-arm','region-hand','region-abdomen','region-legs','region-body','region-habitat'];
for (const id of ids) {
  const g = d.getElementById(id);
  ok(g && g.getAttribute('role') === 'button' && g.getAttribute('tabindex') === '0' && g.getAttribute('aria-label'), `${id} : role=button, tabindex=0, aria-label`);
  g.dispatchEvent(new dom.window.MouseEvent('click', { bubbles: true }));
  const f = d.getElementById('fiche');
  const hs = [...f.querySelectorAll('h3')].map(h => h.textContent);
  ok(f.dataset.region === id, `${id} : clic → fiche affichée`);
  ok(['How to measure','Why it matters','When to alert','What we do not do'].every(h => hs.includes(h)), `${id} : 4 rubriques présentes`);
  const SOURCED=['region-head','region-chest','region-arm'];  // « Why » filled from pages read on 14/11 (docs/HELP_CARD_SOURCES.md)
  if(SOURCED.includes(id)) ok(/nasa\.gov\/reference\//.test(f.textContent), `${id} : « Why » avec source NASA lue`);
  else ok(f.textContent.includes('No NASA in-flight reference'), `${id} : « Why » sans source → No NASA in-flight reference`);
  ok(g.classList.contains('selected'), `${id} : région marquée sélectionnée`);
}
// clavier sur la région SVG
d.getElementById('region-chest').dispatchEvent(new dom.window.KeyboardEvent('keydown', { key: 'Enter', bubbles: true }));
ok(d.getElementById('fiche').dataset.region === 'region-chest', 'touche Entrée sur une région → fiche');
// liste de repli
const btns = [...d.querySelectorAll('#fallback-list button')];
ok(btns.length === 8, 'liste de repli : 8 boutons');
btns[3].click();
ok(d.getElementById('fiche').dataset.region === btns[3].dataset.region && btns[3].getAttribute('aria-pressed') === 'true', 'liste de repli : clic → fiche + aria-pressed');
fs.writeFileSync(process.argv[3], [...ids.map(id => { d.getElementById(id).dispatchEvent(new dom.window.MouseEvent('click', {bubbles:true})); return d.getElementById('fiche').textContent; }), d.body.textContent].join('\n'));
console.log(fails ? `ÉCHECS : ${fails}` : 'TOUS LES TESTS PASSENT');
process.exit(fails ? 1 : 0);
