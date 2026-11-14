# FICHIER: STORYBOARD_v4.md
Date/heure : sam. 14/11/2026 08:50 Lomé (UTC) · Commit de référence : dc61786 · Version v4.1 (corrigée contre le zip rev4)
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Remplace : STORYBOARD_VIDEO_30S v3 du 13/11.
Programme appliqué : `docs/PROGRAMME_OFFICIEL.md` (lu). Pour le minutage détaillé et le texte : `pitch/deck/SCRIPT_FR.md` (oral) et `pitch/video/SHOTLIST_30S.md` (vidéo), qui priment sur ce fichier.

## Ce qui change par rapport à la v3
| # | v3 | v4 | Pourquoi |
|---|---|---|---|
| 1 | Pitch de 3 min, deux réponses préparées | Pitch de 5:00, sans questions | Programme officiel |
| 2 | « Jamais de maquette » | **OUVERT.** Ligne source v3 : « Écrans = captures du vrai logiciel gelé… Jamais de maquette. » Le bloc v1 (règle 5) autorise des wireframes étiquetés tant que le logiciel n'existe pas. Hypothèse : version finale = captures réelles seulement, sauf la silhouette étiquetée « À CONFIRMER M1 — non codée » dans les diapositives | Contradiction entre documents, à trancher par M1 |
| 3 | Ordre : urgence, puis dérive, puis reprise | Accroche = scénario de la vidéo, puis ordre chronologique : Dérive (j6–9) → Urgence (j9) → Reprise (j10) | Accroche fidèle à la vidéo, et histoire qui se suit |
| 4 | Capsule « jour 10 » | Capsule **jour 7** (seed 42, **drift_amp 2.5** : Attention DEGRADED, Body WATCH, procédure PROC-FATIGUE-01 IMPORTANT ; vérifié par exécution de `scripts/run_story.py`), sur une dérive des jours 6–9 | MAJ phase 1, point 5 |
| 5 | « a crewmate collapses » | « a crewmate reports sharp chest pain » : événement déclaré par l'astronaute | Scénario de la vidéo (NON VÉRIFIÉ, Q2) |
| 6 | Codes SC-02/12/10, phrase négative du plan 4 v3 (mot interdit), « Human decision required » | Actes 1/2/3, formulations positives, « Human decision: pending » | Règles des mots et des codes |

## Règles de production (inchangées sauf mention)
- Aucune voix humaine dans la vidéo.
- Sous-titres anglais incrustés.
- Bandeau SYNTHETIC DATA sur chaque capture. Filigrane « AI-generated » sur tout élément généré par IA.
- Aucun visage, nom ou numéro. Pas de logo NASA. Logo MONOLITH = `LOGO_ACTUEL`, non modifié.
- Musique libre de droits, licence notée.
- Chaque capture vient de `pitch/deck/captures_map.md` (C1–C6).

---
## VERSION A — Pitch oral de 5:00 (diapositives en anglais, oral en français)
| Diapo | Début → fin (cumulé) | Durée | À l'écran | Ce qui est dit (FR, résumé ; texte complet dans `SLIDES_EN_v1.md`) | Capture |
|---|---|---|---|---|---|
| 1 | 0:00 → 0:25 | 0:25 | Titre + phrase d'accroche | Le scénario de la vidéo : douleur thoracique à mi-chemin de Mars, la Terre à 20 minutes | Aucune (visuel Terre → Mars) |
| 2 | 0:25 → 1:05 | 0:40 | Le problème | Délai jusqu'à 20 min, coupures de plusieurs semaines, l'équipage seul ; les astronautes ne sont pas médecins | Aucune (schéma) |
| 3 | 1:05 → 1:55 | 0:50 | Acte 1 · Dérive | Chaque astronaute comparé à ses 5 premiers jours ; jour 7 : Attention DEGRADED ; ce qui a changé, quand, à quel point on est sûr ; décision humaine | C1 (vue 5 dimensions) + C2 (capsule jour 7) |
| 4 | 1:55 → 2:55 | 1:00 | Acte 2 · Urgence | Jour 9, douleur thoracique déclarée → procédure CRITICAL ; mesures guidées une par une, avec « comment la prendre » ; compte rendu livré une seule fois | C3 (procédure guidée) + C4 (file d'envoi 20:00) ; silhouette fixe étiquetée |
| 5 | 2:55 → 3:45 | 0:50 | Acte 3 · Reprise, **démo en direct** (Q5) | Jour 10 : donnée vieille de 14 min, limite 10 min ; override consigné, reprise refusée | C5 en repli si la démo échoue |
| 6 | 3:45 → 4:25 | 0:40 | Preuves et méthode | 0,7 % des équipages sains simulés (300) ; 95 % des dérives progressives, limite 59 % sur saut brutal (oral) ; télémétrie ISS réelle pour le contrôle qualité ; phrase autorisée sur Artemis II | C6 (figure EDA en anglais) |
| 7 | 4:25 → 5:00 | 0:35 | Limites et suite + phrase finale | Ce qui n'est pas mesuré ; prochaines étapes ; « Hors ligne. Explicable. L'humain décide. » | Aucune |
| | **Total** | **5:00** | | | |

Démo en direct (diapo 5) :
- Ordinateur hors ligne, application déjà ouverte au jour 10.
- Budget 0:50.
- Si rien ne s'affiche après 10 s, on passe à la capture C5 sans commentaire.

---
## VERSION B — Vidéo de 30,0 s (anglais, sous-titres, sans voix)
| Plan | Début → fin | Durée | Image | Sous-titre (EN) | Capture |
|---|---|---|---|---|---|
| 1 | 0,0 → 4,0 | 4,0 | Fond noir, trait de lumière Terre → Mars, compteur jusqu'à 20:00 | Halfway to Mars, a crew member reports sharp chest pain. Earth is up to twenty minutes away. | Aucune (SVG) |
| 2 | 4,0 → 8,0 | 4,0 | Cinq pastilles dispersées (Body, Attention, Morale, Mission, Habitat) qui se rejoignent | Five streams of data. No single picture. | Aucune (SVG) |
| 3 | 8,0 → 14,0 | 6,0 | Capsule jour 7, zoom lent sur la ligne Attention | C-Sync compares each astronaut with their own first days. Day seven: attention degraded. | C2 |
| 4 | 14,0 → 20,5 | 6,5 | Procédure guidée : une étape de mesure, puis le compte rendu en file d'envoi, compte à rebours 20:00 | Day nine: guided measurements, one at a time. The report reaches the ground once. | C3 → C4 |
| 5 | 20,5 → 26,0 | 5,5 | Appui sur « Request resume » puis « Commander override » : REFUSE_RESUME, une ligne de journal par override ; 2 s de silence sur le refus | Day ten: the data is fourteen minutes old. Resume refused, even with an override. | C5 |
| 6 | 26,0 → 30,0 | 4,0 | Icône de liaison qui s'éteint, l'écran continue ; logo | Offline. Explainable. The human decides. C-Sync. — en petit : Synthetic data · AI use declared | Aucune |
| | **Total** | **30,0 s** | | | |

Sous-titres : 14 à 17 mots maximum par plan. Plans 1 et 4 au plafond, à vérifier en lecture réelle. Si c'est trop dense, retirer « Earth is up to 20 minutes away » du plan 1 : le compteur 20:00 le montre déjà.

## Repli (dimanche avant 12:00)
Si les captures C2–C5 ne sont pas prêtes, il n'y a pas de vidéo : on présente le PDF des 7 diapositives (Version A), avec les emplacements de captures **retirés**. Jamais de capture inventée ni de wireframe non étiqueté.
