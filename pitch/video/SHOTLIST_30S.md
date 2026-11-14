# FICHIER: pitch/video/SHOTLIST_30S.md
Date/heure : sam. 14/11/2026 08:35 Lomé (UTC) · Commit de référence : dc61786 · Version v1
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Livrable facultatif (Q6) : produit seulement si le temps le permet ; le PDF des 7 diapositives reste le livrable principal.

## Règles
- 6 plans, 30,0 s au total. Texte à l'écran en anglais ; sous-titres incrustés, identiques à la voix off.
- **Voix off : voix de synthèse uniquement.** Le bloc interdit toute voix humaine. Filigrane « AI-generated » à l'écran pendant la voix, et usage déclaré dans `AI_USAGE.md`.
- **Pas de silhouette** dans la vidéo.
- Bandeau « SYNTHETIC DATA — demo story, not a real astronaut » sur chaque capture. Aucun nom, visage ou numéro. Pas de logo NASA.
- Musique libre de droits, licence notée (`TODO_M1`).
- Captures : celles de `pitch/deck/captures_map.md` (même réglage : seed 42, drift_amp 2.5).

## Plans
| Plan | Début → fin (cumulé) | Durée | Image | Texte à l'écran / sous-titre = voix off (EN) | Mots |
|---|---|---|---|---|---|
| 1 | 0,0 → 4,0 | 4,0 s | Fond noir, trait Terre → Mars (SVG de la diapo 1), compteur jusqu'à 20:00 | Halfway to Mars, a crew member reports sharp chest pain. Earth is up to twenty minutes away. | 17 |
| 2 | 4,0 → 8,0 | 4,0 s | Cinq pastilles dispersées : Body, Attention, Morale, Mission, Habitat | Five streams of data. No single picture. | 7 |
| 3 | 8,0 → 14,0 | 6,0 s | Capture C1, puis zoom sur C2 (jour 7) | C-Sync compares each astronaut with their own first days. Day seven: attention degraded. | 13 |
| 4 | 14,0 → 20,5 | 6,5 s | Capture C3, puis C4 (« Delivered to ground (once) ») | Day nine: guided measurements, one at a time. The report reaches the ground once. | 14 |
| 5 | 20,5 → 26,0 | 5,5 s | Capture C5 : REFUSE_RESUME + ligne de journal de l'override | Day ten: the data is fourteen minutes old. Resume refused, even with an override. | 14 |
| 6 | 26,0 → 30,0 | 4,0 s | Icône de liaison qui s'éteint ; nom C-Sync ; cadre `LOGO_À_FOURNIR` | Offline. Explainable. The human decides. — en petit : Synthetic data · AI use declared | 5 |
| | **Total** | **30,0 s** | | | **70** |

Débit : 70 mots en 30 s, soit 140 mots/min, ce qui est rapide pour une voix de synthèse. Si la voix dépasse son plan, retirer « of data » (plan 2) et « one at a time » (plan 4), soit −6 mots.

## Contrôles faits sur ce fichier
- Aucun mot de la liste interdite (`csync/language.py`), vérifié par `banned_hits`.
- Aucun pourcentage, aucun détecteur non codé, aucun décompte de tests.
- « Heart rate » n'est pas nommé au plan 5, pour tenir dans le temps. La capture C5 affiche « PH01 is stale (14 min > 10 min) ».
