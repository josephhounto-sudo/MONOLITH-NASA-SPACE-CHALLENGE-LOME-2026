# Gemini G4 — cohérence diapos / script / README — STATUT : revue par Claude, NON validée par un humain
Date/heure : sam. 14/11/2026 ~15:00 UTC.
**Verdict de Claude :** cette fois les étiquettes (D/S/R) sont valides et le périmètre est respecté. Sur 26 constats :
- **Réels, corrigés** : « La Terre est à vingt minutes » vs « jusqu'à » (script diapo 1) ; README « 400 + 600 essais » périmé (pilote 3 : 300/150/150) ; chiffres 0,7 % / 95,3 % / 59,3 % absents du README ; « UI screens in progress » vs maquette statique ; « radiation dose » ambigu (cabine réelle vs dose équipage) ; absolus « opens instantly », « no … ever collected », « never hides missing data », « decision always stays human ».
- **Bruit, non retenus** : jour 7 vs plage 6–9 (ce n'est pas une contradiction) ; Refused / Refusée / REFUSE_RESUME (même état, langues/code différents) ; durée de coupure 6 h (détail de démo) ; liste des 4 mesures (absente du README, sans enjeu).
- **Conservés tels quels (couverts par des tests)** : « jamais présentée comme normale » (résumé de reprise, tests G1–G10), « exactly once » (`test_sendqueue.py`).
Texte ci-dessous = sortie brute de Gemini, non modifiée.

---
### 1. Écarts entre DECK, SCRIPT et README

| Sujet | DECK / SCRIPT / README (étiquettes) | Valeurs ou formulations qui divergent |
| --- | --- | --- |
| Taille de l'échantillon simulé | DECK (`D006`), SCRIPT (`S027`) vs README (`R032`) | `300 simulated healthy crews` (`D006`) et `trois cents équipages simulés` (`S027`) vs `400 control runs and 600 drift runs` (`R032`). |
| Période de l'Acte 1 (Dérive) | DECK (`D003`), SCRIPT (`S015`) vs README (`R011`) | `day 7` (`D003`) et `jour sept` (`S015`) vs plage `6-9` (`R011`). |
| Dimensions et états (Acte 1) | DECK (`D003`) vs SCRIPT (`S015`) vs README (`R011`, `R023`) | `Attention Degraded` uniquement (`D003`) vs `Attention` en `dégradée` et `Corps` en `surveillance` (`S015`) vs `dimensions go WATCH then DEGRADED` (`R011`) et états en majuscules `NORMAL, WATCH, DEGRADED, UNKNOWN` (`R023`). |
| Durée de coupure (Acte 2) | DECK (`D004`), SCRIPT (`S018`) vs README (`R012`) | `link down then restored` (`D004`) et `liaison est coupée ; dès qu'elle revient` (`S018`) vs durée chiffrée `down for 6 h` (`R012`). |
| Signalement de la douleur (Acte 2) | DECK (`D004`), SCRIPT (`S018`) vs README (`R012`) | `Sharp chest pain reported` (`D004`) et `L'astronaute signale` (`S018`) vs `A crewmate ticks chest pain` (`R012`). |
| Délai Terre-Mars | SCRIPT (`S009`) vs DECK (`D002`), SCRIPT (`S012`), README (`R004`, `R021`) | Formulé comme fixe (`La Terre est à vingt minutes`, `S009` ; `20 minutes away`, `R004` ; `+20 min`, `R021`) vs plafond (`Up to ~20 minutes`, `D002` ; `jusqu'à vingt minutes`, `S012`). |
| Dose de rayonnement | DECK (`D007`), SCRIPT (`S030`) vs README (`R027`) | `Not measured yet: ... radiation dose` (`D007`, `S030`) vs `radiation` listé comme donnée réelle ISS utilisée (`R027`). |
| État de refus de reprise (Acte 3) | DECK (`D005`) vs SCRIPT (`S023`) vs README (`R013`) | `Resume: refused` (`D005`) vs `Refusée` (`S023`) vs code `REFUSE_RESUME` (`R013`). |

---

### 2. Affirmations absolues

| Étiquette | Phrase | Présente aussi dans un autre texte ? | Version plus prudente |
| --- | --- | --- | --- |
| `D005` | `Stale data is never shown as normal` | Oui : `S023` (`jamais présentée comme normale`), `R023` (`never shown as NORMAL`) | `Stale data is flagged as expired and excluded from normal status.` |
| `S012` | `ne laisse jamais une donnée absente passer pour une bonne nouvelle` | Oui : `R005` (`never hides missing data`), `R023` (`never shown as NORMAL`) | `signale explicitement toute donnée absente avec l'état UNKNOWN.` |
| `S015` | `Pendant ces cinq jours, rien n'est jugé` | Oui : `R010` (`never "normal"`) | `Pendant ces cinq jours, aucune alerte de dérive n'est évaluée.` |
| `S018` | `Une règle d'événement ouvre aussitôt une procédure critique` | Oui : `R012` (`opens instantly`) | `Une règle d'événement déclenche directement une procédure critique.` |
| `S018` | `C-Sync ne propose aucun médicament et n'interprète pas le symptôme` | Oui : `R006` (`proposes no treatment or drug`) | `C-Sync est conçu sans recommandation médicamenteuse ni diagnostic.` |
| `S018` | `dès qu'elle revient, le rapport arrive au sol une seule fois` | Oui : `D004` (`delivered once`), `R012` (`arrives exactly once`) | `au rétablissement de la liaison, la file déduplique l'envoi par identifiant.` |
| `S023` | `Un forçage ne suffit jamais, seul, à reprendre` | Oui : `R013` (`even with a Commander override`) | `Dans les règles implémentées, un forçage commandant ne suffit pas sans mesure récente.` |
| `S030` | `ils sont affichés inconnus, jamais normaux` | Oui : `R023` (`never shown as NORMAL`) | `ils sont affichés avec l'état UNKNOWN tant qu'aucun capteur n'est relié.` |
| `S030` | `rien de ce que nous montrons ne pose d'étiquette sur une personne` | Non | `l'interface affiche uniquement des écarts statistiques sans qualification médicale.` |
| `R005` | `The decision always stays human` | Oui : `D001`, `S015`, `S030` | `The final operational decision remains assigned to a human operator.` |
| `R029` | `no team or personal data is ever collected` | Non | `no team or personal data is included in this synthetic dataset.` |

---

### 3. Affirmations chiffrées ou factuelles sans appui dans le README

| Étiquette | Affirmation (présente dans DECK ou SCRIPT, absente du README) |
| --- | --- |
| `D006`, `S027` | Taux de fausses alertes de `0.7 %` (`zéro virgule sept pour cent`) mesuré sur `300` équipages témoins simulés (le README mentionne `400 control runs` en `R032`, sans le taux de `0,7 %`). |
| `S027` | Taux de détection de `95 %` (`quatre-vingt-quinze pour cent`) sur les dérives progressives simulées. |
| `S027` | Taux de détection de `59 %` (`cinquante-neuf pour cent`) sur un saut brutal simulé. |
| `S015` | Règle des `deux jours de suite` hors référence et suivi des `erreurs d'attention` (le README en `R011` cite uniquement le sommeil sous `6 h`, le temps de réaction et la somnolence). |
| `S018` | Liste des quatre mesures de l'Acte 2 (`fréquence cardiaque, tension, température, glycémie`) et mention `La glycémie est marquée sans référence NASA en vol`. |
| `D004`, `S018` | Mention d'une maquette statique / carte du corps à cliquer non codée (le README en `R058` indique seulement `UI screens ... in progress`). |
| `D007`, `S030` | Mention spécifique que les os (`bones`) et l'immunité (`immunity`) ne sont pas encore mesurés. |

Textes comparés : DECK (`D001`–`D007`), SCRIPT (`S001`–`S045`), README (`R001`–`R060`) ; non comparés : `docs/PROGRAMME_OFFICIEL.md`, `AI_USAGE.md`, `SOURCES.md`, `HYPOTHESES.md`, `METHODES_NASA_DOSSIER.md` et le code source du dépôt.