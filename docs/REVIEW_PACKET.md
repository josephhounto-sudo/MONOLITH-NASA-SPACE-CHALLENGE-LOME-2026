# Dossier de relecture — règles C-Sync (M2, pour M4 puis un spécialiste)

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ. Données de démo = SYNTHÉTIQUES. Aucun seuil ici n'est un seuil clinique.

Fichiers relus pour ce dossier (15/11/2026, dans le dépôt, pas de mémoire) : `csync/rules.py`, `csync/gate.py`, `csync/capsule.py`, `data/procedures/PROC-FATIGUE-01.json`, `data/procedures/PROC-EMERGENCY-01.json`, `pitch/silhouette/fiches.json`, `docs/OPEN_DECISIONS.md`, `docs/METHODES_NASA_DOSSIER.md` §7, `research/pilot/pilot.py` (planchers). `docs/PITCH_FIGE_ET_REPONSES.md` n'est pas dans le dépôt à cette date.

`relu par M4 :` ________________________________ (nom, date). L'expert répond après cette signature.

---

## 1. Dérive (règle v3)

### Ce que le code fait

Chaque jour, pour huit indicateurs, le code calcule un écart signé : `d = sens × (valeur du jour − moyenne personnelle) / écart-type utilisé`. Le sens est +1 si une hausse est défavorable, −1 si une baisse l'est (`csync/rules.py`, `DIRECTION`). Un indicateur est marqué seulement si `d` atteint le seuil sur assez de jours d'affilée, et seulement après la fin de la référence. Un jour sans valeur remet le compteur à zéro.

Trois dimensions sont notées : Corps (`PH01` fréquence cardiaque de repos, `PH09` sommeil déclaré), Attention (`CO01` temps de réaction, `CO02` lapses), Moral (`PS01` somnolence, `PS02` stress, `PS03` humeur, `PS04` charge). Une dimension est `WATCH` avec 1 indicateur marqué, `DEGRADED` avec 2 ou plus. S'il manque la valeur du jour d'un indicateur de la dimension, l'état est `UNKNOWN`, sauf si deux indicateurs sont déjà marqués : dans ce cas l'état reste `DEGRADED` (l'ordre du test est dégradé, puis manquant, puis surveillance, puis normal — `evaluate`, une seule ligne d'affectation). `UNKNOWN` n'est pas compté comme normal et n'ouvre pas de procédure. Deux dimensions en `WATCH` ou `DEGRADED` le même jour ouvrent `PROC-FATIGUE-01`. La criticité d'un épisode déjà ouvert ne redescend pas (`IMPORTANT` si un jour a été `DEGRADED`, sinon `ROUTINE`).

Pendant les jours de référence, les trois dimensions sont `UNKNOWN` : aucune comparaison. Mission et Habitat ne sont pas dans ce décompte (`csync/capsule.py`, `CONTEXT_DIMENSIONS`) : la capsule les affiche `UNKNOWN`, jamais `NORMAL`.

La fréquence cardiaque du jour est la moyenne des points poignet de 06:00 à 07:00 s'il y a au moins 3 points de qualité `OK`. Sinon la valeur manque. En mode rapide du générateur, une ligne `WRIST-DAILY` fournit déjà cette moyenne.

### Chaque paramètre

| Paramètre | Valeur dans `Params()` | D'où elle vient |
|---|---|---|
| `baseline_days` | 5 | Choix de conception. `docs/OPEN_DECISIONS.md` n°3 : 5 jours proposés ; le même tableau dit qu'une référence de 7 jours n'améliorait pas le taux de fausses procédures sur le pilote d'alors (12 %). Pas une source NASA. |
| `d_threshold` | 1,5 | Choix de conception, décision M1 du 14/11 (« le plus juste scientifiquement »), écrite dans `docs/METHODES_NASA_DOSSIER.md` §7.10. Sur les scénarios synthétiques du pilote 3 (graines 1000–7149) : 0,7 % d'équipages témoins avec une procédure, 95,3 % des dérives progressives 1,5 ET, 59,3 % des sauts 2 ET. Le seuil a été choisi sur les mêmes familles de scénarios que cette mesure. Ce n'est pas un seuil clinique. |
| `consecutive_days` | 2 | Choix de conception (en-tête de `csync/rules.py`, « PARAMETRES v3, P-06 »). Pas de source externe dans le dépôt pour le nombre 2. |
| `sd_floor_rel` | 0,05 | Choix de conception : plancher à 5 % de la valeur absolue de la moyenne de référence (`csync/rules.py` ; le même 0,05 est dans `research/pilot/pilot.py`). Pas de source externe. |
| `sd_floor_abs` | PS01 1,0 ; PS02 1,0 ; PS03 0,5 ; PS04 1,0 ; CO02 1,0 ; PH09 0,5 ; PH01 3,0 | Choix de conception. Dictionnaire identique à `ABS_FLOOR` dans `research/pilot/pilot.py`. `CO01` n'a pas de plancher absolu : seul le plancher relatif s'applique. Unités : celles des indicateurs (bpm, heures, ms, comptes, échelles). Pas de source externe pour ces nombres. |
| Écart-type | écart-type corrigé (`ddof=1`), valeurs manquantes ignorées | Choix de conception dans `evaluate`. Si l'écart-type est nul ou manquant, le plancher le remplace. |
| Sens | PH09 −1, PH01 +1, CO01 +1, CO02 +1, PS01 +1, PS02 +1, PS04 +1, PS03 −1 | Choix de conception. L'en-tête dit que le sens de PS03 est une proposition (P-07). `docs/OPEN_DECISIONS.md` n°5 : « humeur ↓ défavorable » comme défaut proposé, case décision M1 vide. |
| `max_age_min` | 10 | Présent dans `Params` mais **non lu** par `evaluate`. Il sert la porte de reprise (page 3). |
| `ground_delay_min` | 20 | Présent dans `Params` mais **non lu** par `evaluate`. `docs/OPEN_DECISIONS.md` : valeur de démonstration. Le même fichier dit que le délai vers Mars va jusqu'à ~22 min, avec la source NTRS citée ailleurs dans le dépôt (`20220013418`). Ce 20 n'est pas ce délai. |

La procédure ouverte par la dérive est fixée dans le code : toujours `PROC-FATIGUE-01`. Son texte dit de revoir les signaux avec l'officier médical de bord, de noter le sommeil et de refaire le test de réaction de 3 minutes (`data/procedures/PROC-FATIGUE-01.json`). Les phrases « why » de cette procédure citent la page NASA HRP sur le sommeil et les horaires irréguliers (URL dans le fichier). Ce ne sont pas des seuils.

### Ce qui est inconnu

- Aucun de ces nombres n'a été fixé à partir d'une série d'astronautes. Le dépôt le dit : tout le pilote 3 est synthétique, un seul générateur de bruit (`docs/METHODES_NASA_DOSSIER.md` §7.8).
- On ne sait pas si 5 jours suffisent pour un écart-type stable, ni si le plancher absolu (surtout `PH01` = 3 bpm, `PS03` = 0,5 point) est large ou étroit pour un vrai relevé.
- Le code ne sait pas si la personne est déjà fatiguée pendant les jours 1 à 5. Si la référence est décalée, `d` rapetisse. Ce biais n'est pas corrigé dans la règle livrée.
- Tension (`PH10`) et température (`PH11`) sont mesurées dans l'urgence guidée et absentes de la dérive. `docs/OPEN_DECISIONS.md` n°5 laisse la case M1 vide.
- Une valeur manquante et un seul indicateur marqué donnent `UNKNOWN`, pas `WATCH`. `docs/M2_CONSIGNES.md` point D dit que c'est voulu. Un spécialiste ne s'est pas prononcé.
- `CO01` peut avoir un écart-type de référence très petit ; le plancher relatif (5 % de la moyenne, soit de l'ordre de 13 ms si la moyenne est près de 265) est alors le seul garde-fou. L'effet sur de vraies séries n'est pas mesuré ici.

### Cinq questions pour un spécialiste de médecine spatiale

1. Pour le sommeil déclaré, le temps de réaction et la fréquence cardiaque de repos, une référence personnelle de 5 jours suffit-elle à distinguer la variation habituelle d'un changement qui devrait changer le plan de travail ?
2. « Deux jours de suite à au moins 1,5 écart-type personnel, du mauvais côté » est-il un déclencheur opérationnel acceptable pour un contrôle sans interprétation médicale, ou la persistance devrait-elle être un autre nombre de jours ?
3. L'humeur (échelle 1–5 dans ce prototype) est traitée comme défavorable quand elle baisse. Est-ce le sens qu'un médecin de bord utiliserait, et doit-elle partager la même règle que la somnolence ?
4. La tension et la température restent hors de la comparaison quotidienne (affichées seulement dans la procédure guidée). Faut-il les laisser dehors ?
5. S'il manque un indicateur aujourd'hui, toute la dimension passe à `UNKNOWN`, même si un autre indicateur de cette dimension est marqué (sauf si deux sont déjà marqués). Est-ce le comportement voulu le jour d'un relevé incomplet ?

---

## 2. Urgence guidée

### Ce que le code fait

Dès qu'une ligne a l'indicateur `SY01`, `event_rule` ouvre `PROC-EMERGENCY-01` avec la criticité `CRITICAL`. Il n'y a pas de seuil sur la valeur. Le texte du symptôme est `value_text` (dans l'histoire synthétique : `chest_pain;zone=thorax`). La capsule d'urgence (`build_emergency_capsule`) recopie les mesures guidées telles quelles et écrit qu'aucun seuil n'est appliqué. La glycémie (`PH12`) reçoit l'étiquette « no NASA in-flight reference ». `human_decision` reste `pending`.

La fiche poitrine (`pitch/silhouette/fiches.json`, `region-chest`) décrit la même chose : la fréquence cardiaque suit la dérive ; un symptôme déclaré ouvre la procédure critique tout de suite. La fiche dit aussi que la sélection de zone est codée dans l'application. Ce dossier ne revérifie pas l'écran (`csync/ui/` est hors de cette tâche).

### Chaque paramètre

Il n'y a pas de seuil numérique dans `event_rule`. Les paramètres sont ceux de la procédure et de l'histoire.

| Élément | Valeur | D'où elle vient |
|---|---|---|
| Déclencheur | présence de `SY01`, quelle que soit la valeur | Choix de conception (`csync/rules.py`, `event_rule`). |
| Procédure | `PROC-EMERGENCY-01` | Identifiant fixé dans le code et dans `data/procedures/PROC-EMERGENCY-01.json`. |
| Criticité | `CRITICAL` | Fixée dans `event_rule`. La fiche poitrine renvoie à `contracts/decision.schema.json` pour le lien « CRITICAL = flight surgeon ». Ce dossier ne modifie pas `contracts/` ; il ne recopie pas le schéma. |
| Mesures guidées | `PH01` bpm, `PH10` mmHg (SYS et DIA), `PH11` °C, `PH12` mg/dL | Liste dans `PROC-EMERGENCY-01.json`, étapes 3. `PH11` et `PH12` ont `nasa_reference: false` dans ce fichier. |
| Phrases « why » de PH01 et PH10 | pages NASA HRP adaptations cardiovasculaires | URL dans la procédure : `https://www.nasa.gov/reference/risk-of-cardiovascular-adaptations/`. Le fichier dit que les pages ont été ouvertes le 14/11/2026. Ce dossier ne les a pas rouvertes. |
| Phrase fixe | « Follow the onboard medical checklist and the crew medical officer. » | `fixed_sentence` de la procédure, et `fixed_medical_sentence` dans `csync/config/strings_en.json`. |
| Reprise après cette procédure | `PH01` et `CO01`, 10 min, source `GUIDED` | `prerequisites` de `PROC-EMERGENCY-01.json`. Détail page 3. `CO01` n'est pas dans la liste des mesures guidées de l'étape 3 ; il est seulement un prérequis de reprise. |
| `override_policy` | `override_never_resumes_alone: true` | Champ de la procédure. Le code de la porte ne lit pas ce booléen : il refuse seulement si la clé `override_policy` est absente (`csync/gate.py`). |

`docs/OPEN_DECISIONS.md` n°8 : la tension est une mesure par valeur, avec `value_text` SYS/DIA. C'est déjà le cas dans le générateur et dans la capsule. Case décision M1 vide.

### Ce qui est inconnu

- Le code ne classe pas le symptôme. Il ne sait pas si « n'importe quel symptôme coché » est trop large (un symptôme léger ouvre la même procédure critique).
- Aucune limite numérique n'accompagne les mesures guidées. On ne sait pas, dans ce dépôt, quelles limites un médecin de bord utiliserait, et le prototype refuse d'en inventer.
- La température et la glycémie sont enregistrées avec la mention d'absence de référence NASA en vol. On ne sait pas si elles doivent rester dans le flux guidé.
- Le prérequis de reprise demande un temps de réaction guidé, alors que l'étape 3 de la procédure ne liste pas ce test. Écart entre les deux listes du même fichier JSON.
- La validation humaine M4 de la procédure est encore « À FAIRE » dans l'en-tête du JSON (relecture assistant du 14/11, pas une signature M4).

### Cinq questions pour un spécialiste de médecine spatiale

1. Faut-il ouvrir la même procédure critique pour tout symptôme coché, ou seulement pour une liste courte de symptômes déclarés par l'équipage ?
2. Le premier bloc guidé (fréquence cardiaque, tension SYS et DIA, température, glycémie) est-il le bon bloc mesurable en vol, et quelle mesure manque encore alors qu'elle est faisable à bord ?
3. Le prototype affiche les nombres guidés sans les comparer à une limite. Faut-il le laisser ainsi, la limite restant dans la check-list humaine ?
4. La zone du corps est un texte libre fourni par l'équipage. Une liste fermée de zones est-elle préférable pour le compte rendu ?
5. Pour autoriser ensuite la reprise du travail, le fichier exige une fréquence cardiaque et un temps de réaction de moins de 10 minutes, pas la tension ni la température. Le temps de réaction a-t-il sa place dans ce prérequis ?

---

## 3. Porte de reprise

### Ce que le code fait

`resume_gate` répond `RESUME_AUTHORIZED` ou `REFUSE_RESUME`, avec une liste de raisons codées G1 à G10. Elle échoue fermée. Un forçage du commandant, s'il est passé et que la porte refuse déjà, ajoute la raison G6. Il ne change pas la décision. S'il est passé alors que tout le reste est bon, la fonction ne le mentionne pas : elle renvoie quand même G1.

Ordre des refus, tel que le code les teste :

1. G10 — une autre demande est déjà en cours (`pending_lock`).
2. G9 — la session n'est pas `SUSPENDED`.
3. G5 — `override_policy` est absent (`None`). Une politique vide mais présente (`{}`) ne déclenche pas G5.
4. G7 — la liste de prérequis est vide et `no_physical_prereq` n'est pas vrai.
5. Pour chaque prérequis : G2 si aucune mesure de cet indicateur ne vient d'une source autorisée ; G8 si l'horodatage est après `now` ; G4 si la qualité n'est pas exactement `OK` ; G3 si l'âge dépasse la limite.
6. G1 — sinon.

L'âge est `(heure de la demande − heure de la mesure)` en minutes. La comparaison « dans le futur » utilise `now`, qui vaut l'heure de la demande si l'appelant ne passe pas autre chose. La limite par prérequis est `max_age_min` du prérequis, sinon l'argument `max_age_min` de la fonction (défaut 10).

`PROC-EMERGENCY-01` a deux prérequis, 10 minutes, source `GUIDED` seulement : `PH01` et `CO01`. Une mesure de dérive quotidienne (autre source) ne compte pas.

`PROC-FATIGUE-01` a `prerequisites: []` et `no_physical_prereq: false`. La porte répond donc G7 pour cette procédure : refus, parce qu'elle ne déclare aucun contrôle. Ce n'est pas un oubli silencieux : la raison est explicite. On ne sait pas si c'était le but (une procédure de fatigue sans porte) ou une liste restée vide.

La capsule de reprise met la décision dans `action.gate_decision`, laisse `human_decision` à `pending`, et ajoute toujours la phrase G6 à l'explication affichée, même quand le forçage n'a pas été demandé (`build_resume_capsule` concatène la phrase G6 après les raisons). Le texte affiché en cas de refus demande de nouvelles mesures guidées. `ui_hint` : reprise autorisée → `NOMINAL` (parce que l'action devient `CONTINUE`) ; refus → `FOCUS`. `docs/OPEN_DECISIONS.md` marque ce mapping comme provisoire.

### Chaque paramètre

| Paramètre | Valeur | D'où elle vient |
|---|---|---|
| Limite d'âge | 10 minutes | Choix de conception. Défaut de `resume_gate` et de `Params.max_age_min`. Recopié dans les deux prérequis de `PROC-EMERGENCY-01.json`. Pas de source NASA dans le dépôt pour « 10 minutes ». |
| Sources acceptées | `GUIDED` pour l'urgence | Liste du JSON. Le défaut du code, si la clé `sources` manque, est aussi `["GUIDED"]`. |
| Qualité acceptée | chaîne exacte `OK` | Choix de conception dans `csync/gate.py`. `MISSING` et `ARTIFACT` refusent (G4). |
| Session exigée | `SUSPENDED` | Choix de conception (G9). |
| Forçage | consigné, jamais suffisant seul | Choix de conception (`csync/gate.py`, commentaire et G6). Le booléen `override_never_resumes_alone` du JSON n'est pas lu par la fonction. |
| Politique absente | refus G5 | Choix de conception : échec fermé si la clé manque. |

### Ce qui est inconnu

- 10 minutes est un choix d'ingénierie. On ne sait pas si c'est court pour un test de réaction de 3 minutes (le test dure 3 minutes dans la procédure de fatigue ; un relevé « de moins de 10 minutes » laisse peu de marge après le test).
- Si `now` est plus tard que l'heure de la demande, une mesure située entre les deux n'est pas « dans le futur » et son âge par rapport à la demande est négatif : elle n'est pas refusée pour péremption. Le cas n'est pas tranché par un spécialiste.
- G7 sur `PROC-FATIGUE-01` : on ne sait pas si la reprise après une procédure de fatigue doit être sans contrôle matériel, ou si la liste vide est inachevée.
- La capsule ajoute la phrase de forçage à chaque explication de reprise. Un lecteur peut croire qu'un forçage a eu lieu alors que l'appelant n'en a pas passé.
- Aucune relecture M4 signée. L'en-tête des deux procédures dit encore « VALIDATION HUMAINE M4 : À FAIRE ».

### Cinq questions pour un spécialiste de médecine spatiale

1. Dix minutes de fraîcheur pour la fréquence cardiaque et pour le temps de réaction, avant de reprendre une tâche, est-ce une limite opérationnelle raisonnable ?
2. Une mesure horodatée dans le futur doit-elle toujours bloquer la reprise, y compris quand les horloges de bord ne concordent pas ?
3. Un forçage du commandant consigné, mais jamais suffisant à lui seul, reste-t-il la bonne règle quand le sol est injoignable ?
4. La procédure « plusieurs signaux loin de la référence » n'a aucun prérequis matériel : la porte refuse donc la reprise (raison G7). Est-ce voulu, ou faut-il une liste de contrôles ?
5. Une valeur marquée artéfact (série constante) doit-elle bloquer la reprise au même titre qu'une valeur absente ?

---

## Suite

M4 signe la ligne du haut après lecture. Les quinze questions sont posées telles quelles à un spécialiste de médecine spatiale. Les réponses ne modifient pas `csync/rules.py` sans une décision M1 écrite dans `docs/OPEN_DECISIONS.md`.
