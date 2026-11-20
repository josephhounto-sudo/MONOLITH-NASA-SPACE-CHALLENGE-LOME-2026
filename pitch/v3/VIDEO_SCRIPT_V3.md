# Vidéo C-Sync : 30 secondes, plan à plan et prompts de production

**Pourquoi 30 s :** le guide officiel de soumission de Space Apps limite la démo vidéo à 30 secondes (ou 7 diapositives, titre compris). Une voix dans une autre langue que l'anglais doit avoir des sous-titres anglais. La vidéo pour le responsable local respecte la même limite, pour pouvoir servir telle quelle.

**Essence (story-writer, 19 mots) :** Quand l'aide est à vingt minutes, C-Sync compare chaque astronaute à lui-même et laisse une personne décider.
**Fil :** le bourdon (l'erreur de qui n'a pas mesuré) → preuve sur données NASA réelles → Kora (simulée) → les étapes à bord → les pièces qu'on touche → la phrase à répéter.
**Animatique v0 :** `C-Sync_animatique_30s_v0.mp4`, monté à partir de vrais enregistrements de l'app. Il fixe le rythme et les sous-titres ; les plans 1 et 7 sont des cartons à remplacer.

| # | Temps | Image | Sous-titre anglais (= voix) | Statut de la donnée |
|---|---|---|---|---|
| 1 | 0–4,5 s | **Flow** : bourdon en vol, macro, ralenti | A famous quote says NASA’s entrance reads: the bumblebee cannot fly. | Image générée par IA (mention dans le carton final) |
| 2 | 4,5–8,5 s | App : écran d'arrivée, les trois lignes | It’s a legend. The bee flies. Nobody had measured how it really moves. | Vrai (Dickinson et al., Science 1999) |
| 3 | 8,5–13 s | App : Habitat, rejeu des missions | On 14 real ISS missions, daily averages hid 370 hours above NASA’s CO2 limit. | RÉEL (`research/retro/RESULTS.md`) |
| 4 | 13–17,5 s | App : histoire, jour 9, liaison coupée | C-Sync compares each astronaut to their own usual. Kora is simulated. | SIMULÉ |
| 5 | 17,5–22,5 s | App : guide d'urgence, étapes | When help is twenty minutes away, the steps are already on board. | Étapes sourcées NASA ; 20 min = paramètre de démo |
| 6 | 22,5–27 s | App : Technologies, curseur de la messagerie | Every piece can be touched, and says if it is tested or still a promise. | SIMULÉ (liaison) |
| 7 | 27–30 s | **Flow** : la Terre depuis l'orbite, puis carton | Measure the astronaut, not the average. | Carton : « C-Sync · Team MONOLITH, Lomé · AI-generated shots: 1, 7 » |

## Prompts de production
**Flow (Veo), plan 1, 4,5 s, 16:9 :** « Extreme macro of a single bumblebee hovering in front of a dark background, wings beating, visible wing rotation, slow motion 120 fps look, warm amber rim light, shallow depth of field, cinematic, no text, no people. »
**Flow (Veo), plan 7, 3 s, 16:9 :** « Slow push-in on Earth’s night side from low orbit, thin blue atmosphere line, city lights, a faint orange sunrise on the limb, cinematic, no spacecraft logos, no text, no people. »
**Flow Music, 30 s :** « Minimal cinematic pulse, 72 BPM, soft analog synth pad, a low heartbeat-like kick from second 8, builds gently, resolves on one warm chord at second 27, no vocals. » Mixer la musique nettement sous la voix (environ −18 LUFS).
**ElevenLabs, voix :** une voix anglaise calme et posée, pas une voix de bande-annonce ; stabilité ≈ 0,55, similarité ≈ 0,75, style 0. Texte : les 7 sous-titres ci-dessus, dans l'ordre, une pause de 0,3 s entre deux plans. Durée cible ≤ 26 s, pour finir sur la musique seule. Si la voix est synthétique, écrire « AI voice » dans le carton final.

## Règles
- Aucune personne identifiable (décision de Joseph), aucun logo de la NASA.
- Le CO2 en direct change à chaque prise : ne jamais le citer à voix haute.
- Mots interdits : cause, diagnostic, prouve, garantie, maladie.

## Contrôles avant d'envoyer (aucun ne dépend de nous)
- Durée ≤ 30,0 s (ffprobe) ; sous-titres anglais lisibles sur téléphone.
- Test de reformulation : 7 personnes qui ne connaissent pas le projet regardent la vidéo une fois et la racontent en 3 phrases. Cible : 5 sur 7 disent « il compare l'astronaute à lui-même » et « une personne décide ». Noter la première hésitation, mots exacts.
