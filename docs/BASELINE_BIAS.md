# Référence fatiguée — biais mesuré, piste non adoptée

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ. Équipages SYNTHÉTIQUES. Ce n'est pas une validation.

Question : si les jours 1 à 5, qui servent de référence, sont déjà décalés du mauvais côté, quelle part des dérives vues avec une référence propre disparaît ?

Script : `research/biased_baseline.py`. Sortie brute : `research/biased_baseline_results.json`. Graines 65000–65149 (150 équipages), jamais utilisées pour régler la règle. Générateur `csync-synth-0.1`, variante `histoire`, `drift_amp=1.5`, sans événement, mode rapide. La règle appelée est `csync.rules.evaluate` avec `Params()` livré. Rien n'a été changé dans `csync/rules.py`.

Le décalage est ajouté après génération, sur le tableau quotidien : pour chaque indicateur de la règle, les jours 1 à 5 bougent de 0,5, 1,0 ou 1,5 écart-type personnel (écart-type corrigé de ces cinq jours) dans le sens défavorable. Les jours 6 à 10 restent ceux du générateur. Une détection est au moins une `OPEN_PROCEDURE`.

## Chiffre

Référence propre : 146/150 détectés, 97,3 % (Wilson 95 % : 93,3–99,0).

| Décalage de la référence | Détectés | Part des détections propres qui disparaissent |
|---|---|---|
| 0,5 ET | 123/150, 82,0 % (75,1–87,3) | 23/146, 15,8 % (10,7–22,5) |
| 1,0 ET | 92/150, 61,3 % (53,3–68,8) | 54/146, 37,0 % (29,6–45,1) |
| 1,5 ET | 53/150, 35,3 % (28,1–43,3) | 93/146, 63,7 % (55,6–71,1) |

À 1,5 ET de décalage, environ deux détections propres sur trois disparaissent. Sur ces 150 graines, le décalage n'a créé aucune détection nouvelle : chaque équipage encore détecté l'était déjà avec la référence propre (146 − 23 = 123, 146 − 54 = 92, 146 − 93 = 53).

## Limite

Un seul générateur, dix jours, et un décalage ajouté sur le tableau quotidien : les plafonds d'échelle du générateur (sommeil, entiers) ne sont pas réappliqués. Le 97,3 % de référence propre n'est pas le 95,3 % du pilote 3 : autres graines, même histoire simulée. Rien de ceci ne dit ce que ferait une référence fatiguée chez un équipage réel.

## Piste testée, pas adoptée : référence avant mission

Le script place cinq jours propres avant la fenêtre fatiguée, puis les jours de dérive. `evaluate` reste celui du dépôt, avec une référence de 5 jours : il lit donc les jours propres du début. Ce branchement n'est pas dans `csync/rules.py`.

La dérive injectée (jours 11 à 15 de cette série allongée) est détectée chez 146/150, 97,3 % (93,3–99,0), aux trois niveaux de décalage : le même compte que la référence propre.

Pendant la fenêtre fatiguée elle-même (jours 6 à 10), avant la rampe injectée, une procédure s'ouvre chez 1/150 (0,7 %, 0,1–3,7) à 0,5 ET, 10/150 (6,7 %, 3,7–11,8) à 1,0 ET, et 76/150 (50,7 %, 42,7–58,6) à 1,5 ET. Une référence d'avant mission rend la fatigue du début de mission visible ; à 1,5 ET elle ouvre une procédure dans la moitié de ces équipages simulés avant même la rampe de l'histoire.

Non adopté : le moteur livré continue de prendre les jours 1 à 5 de la mission comme référence.
