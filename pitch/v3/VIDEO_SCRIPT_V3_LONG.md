# Vidéo C-Sync : version complète (1 min 38 montée), format « revue de conception »

**Pourquoi cette version :** la limite de 30 s concernait la soumission, qui est close. Cette vidéo est pour le responsable local et pour toute personne qui veut comprendre le produit en une séance. Elle suit l'ordre d'une revue d'ingénieur : besoin → preuve → démonstration → limites. La version 30 s (`VIDEO_SCRIPT_V3.md`) reste valable comme bande-annonce.

**Essence (19 mots) :** Quand l'aide est à vingt minutes, C-Sync compare chaque astronaute à lui-même et laisse une personne décider.

**La citation comme argument, pas comme décor.** La légende dit qu'un panneau à l'entrée de la NASA affirme que le bourdon ne peut pas voler. C'est une légende (nous le disons). Le fait réel : un calcul de 1934 supposait une aile fixe ; l'erreur était dans le modèle, pas dans l'insecte. Dickinson, Lehmann & Sane (*Science* 284, 1999) ont mesuré le battement réel. C-Sync fait la même remarque sur les équipages : une moyenne est un modèle fixe. Le plan 1 pose la légende, le plan 2 la retourne, le plan 8 la referme sur la phrase à répéter.
*À vérifier avant tournage : la date et l'auteur du calcul de 1934 (NON VÉRIFIÉ ici ; ne pas le citer à voix haute tant qu'on n'a pas le texte).*

| # | Temps | Image | Voix (= sous-titres anglais) | Statut de la donnée |
|---|---|---|---|---|
| 1 | 0–15 s | Flow : bourdon en vol, macro, ralenti | A legend says a sign at NASA’s entrance reads: the bumblebee cannot fly. It is only a legend. | Image générée par IA |
| 2 | 15–30 s | App : écran d’arrivée (trois lignes) | The calculation was wrong, not the bee. It assumed fixed wings. An average astronaut is the same mistake. | Vrai (Dickinson et al., 1999) |
| 3 | 30–48 s | App : Habitat, rejeu des missions | Daily averages hid hours that mattered. In real cabin data from fourteen ISS missions, eight had hours above 3 millimetres of mercury that the daily average concealed. | RÉEL (`research/retro/RESULTS.md` : 370 h sur 8 missions sur 14, seuil 3 mmHg de notre analyse, capteur de cabine, pas l'air respiré) |
| 4 | 48–66 s | App : console en direct, âge de la mesure | This is the live station. Every value shows its age. NASA data here is context, never a decision. | Réel, en direct ; âge affiché |
| 5 | 66–95 s | App : histoire, jour 7 puis jour 9, liaison coupée | Meet Kora, simulated. C-Sync compares her to her own normal. On day nine, the link to Earth drops. | SIMULÉ |
| 6 | 95–113 s | App : guide d’urgence, Pip | Help is twenty minutes away. The steps are already on board, and Pip walks the crew through them. | Étapes sourcées NASA ; 20 min = paramètre de démo |
| 7 | 113–140 s | App : Technologies | Every piece can be touched, and each says: tested, in development, or still a promise. | SIMULÉ ; prototype clignement « en développement » |
| 8 | 140–160 s | Flow : la Terre depuis l’orbite, puis logo C-Sync + MONOLITH | Not validated on real crews. Measure the astronaut, not the average. | Carton : « AI-generated shots: 1, 8 · AI voice » |

**Montage réel (20/11, 13:35) :** voix ElevenLabs (Roger) de 92,4 s sur le texte ci-dessous, 1,5 s de musique avant, logo et carton final à la fin : 97,7 s, −16 LUFS. Deux fichiers : voix anglaise + sous-titres anglais, voix anglaise + sous-titres français. Les durées par plan sont calées sur les pauses mesurées dans la voix (ffmpeg silencedetect), pas sur une estimation.
Texte exact de la voix : « A legend says a sign at NASA's entrance reads: the bumblebee cannot fly. It is only a legend. The calculation was wrong, not the bee. It assumed fixed wings. An average astronaut is the same mistake. Daily averages hid hours that mattered. In real cabin data from fourteen space station missions, eight had hours above three millimetres of mercury that the daily average concealed. The hour shows what the day hides. This is the live station. Every value shows its age. NASA data here is context, never a decision. Choose a role: crew member or commander. Same data, same words, a different first question. Meet Kora. She is simulated, and every screen says so. C-Sync compares her to her own normal, so a slow drift shows before any single number looks wrong. On day nine, the link to Earth drops. Help is twenty minutes away. The steps are already on board, and Pip walks the crew through them. A person decides. C-Sync keeps the steps ready. Every piece can be touched, and each one says: tested, in development, or still a promise. One prototype reads blinking from the visitor's own camera. It is marked in development, with the reason: not validated. Nothing is recorded. This is a demonstration on synthetic data and public NASA data. Not validated on real crews. Measure the astronaut, not the average. »
**Défaut connu :** le plan « live station » a été filmé depuis un serveur qui ne joint pas le flux de la station : les cartes affichent « Connecting ». À remplacer par une capture de 8 s de la console en direct faite depuis un navigateur ordinaire.

## Prompts de production
**Flow (Veo), plan 1, 8 s :** « Extreme macro of a single bumblebee hovering in front of a dark background, wings beating, visible wing rotation, slow motion, warm amber rim light, shallow depth of field, cinematic, no text, no people. »
**Flow (Veo), plan 8, 6 s :** « Slow push-in on Earth’s night side from low orbit, thin blue atmosphere line, city lights, faint orange sunrise on the limb, no spacecraft logos, no text, no people. »
**Musique :** la piste synthétisée (72 BPM) tient 30 s ; pour 2 min 40, la boucler en plans de 8 mesures avec un crescendo léger du plan 5 au plan 7, ou la régénérer dans Flow Music (« minimal cinematic pulse, 72 BPM, no vocals, 2 min 40, resolves at 2:20 »). Niveau : −19 LUFS, voix nettement au-dessus.
**ElevenLabs :** voix anglaise calme (Roger, stabilité ≈ 0,55, similarité ≈ 0,75, style 0), un bloc par plan, pause de 0,4 s entre plans.

## Règles
- Aucune personne identifiable, aucun logo NASA. Le logo d’équipe MONOLITH a été généré par IA avant l’événement : le dire dans le carton final et dans `AI_USAGE.md`.
- Le CO2 en direct change à chaque prise : ne jamais le citer à voix haute.
- Mots interdits dans les sous-titres : cause, diagnostic, prouve, garantie, maladie.
- Toute affirmation chiffrée à voix haute renvoie à un fichier du dépôt (ici : 8 missions sur 14, 370 h au-dessus de 3 mmHg → `research/retro/RESULTS.md` ; 3 mmHg est le seuil de notre analyse, pas la limite NASA, qui est 2,5 mmHg selon OCHMO-TB-004).

## Contrôles (aucun ne dépend de nous)
- Lecture à froid du texte par une autre IA, puis 7 inconnues : elles regardent une fois, racontent en 3 phrases. Cible : 5 sur 7 disent « il compare l’astronaute à lui-même » et « une personne décide ». Noter la première hésitation, mots exacts.
- Le responsable local confirme la durée acceptable (≈ 2 min 40).
- Sous-titres lisibles sur téléphone ; loudness mesuré ; durée mesurée (ffprobe).
