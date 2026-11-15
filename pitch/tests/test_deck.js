// FICHIER: pitch/tests/test_deck.js · 14/11/2026 09:00 Lomé · commit dc61786 · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
// Usage : npm install jsdom (ou NODE_PATH=<dossier>/node_modules) puis node pitch/tests/test_deck.js <fichier.html> <sortie_texte.txt>
const fs=require('fs');const {JSDOM}=require('jsdom');
const src=fs.readFileSync(process.argv[2],'utf8');let f=0;const ok=(c,m)=>{console.log((c?'PASS ':'FAIL ')+m);if(!c)f++;};
ok(!/(src|href)\s*=\s*["']?(https?:)?\/\//i.test(src),'aucune ressource externe');
const dom=new JSDOM(src,{runScripts:'dangerously',pretendToBeVisual:true});const d=dom.window.document;
const s=[...d.querySelectorAll('.slide')];ok(s.length===7,'7 diapositives');
let all='';const CAP=+process.env.WORDCAP||25;
s.forEach((el,k)=>{const t=[...el.querySelectorAll('[data-count]')].map(e=>e.textContent).join(' ');
 const n=(t.match(/[A-Za-z0-9][A-Za-z0-9.\-~%']*/g)||[]).length; ok(n<=CAP,`diapo ${k+1} : ${n} mots ≤ ${CAP}`); all+=el.textContent+'\n';});
['s3','s4','s5'].forEach(id=>ok(d.querySelectorAll('#'+id+' .capture .sb').length===d.querySelectorAll('#'+id+' .capture').length,`${id} : bandeau SYNTHETIC DATA sur chaque cadre de capture`));
const press=k=>d.dispatchEvent(new dom.window.KeyboardEvent('keydown',{key:k}));
press('ArrowRight');ok(s[1].classList.contains('active'),'→ passe à la diapo 2');press('End');ok(s[6].classList.contains('active'),'Fin → diapo 7');press('ArrowLeft');ok(s[5].classList.contains('active'),'← revient à la diapo 6');press('Home');ok(s[0].classList.contains('active'),'Début → diapo 1');
for(const bad of ['EWMA','23 tests','13/13','17 %','2.7','2,7','validated by NASA','uses our method'])ok(!all.includes(bad),`absent : « ${bad} »`);
if(/final/.test(process.argv[2])){for(const bad of ['[CAPTURE','LOGO_À_FOURNIR','À CONFIRMER','à insérer','English figure','37 h','37 hours'])ok(!src.replace(/data:[^"]{100,}/g,'').includes(bad),`version finale : absent « ${bad} »`);}
fs.writeFileSync(process.argv[3],all);console.log(f?'ÉCHECS '+f:'TOUS LES TESTS PASSENT');process.exit(f?1:0);
