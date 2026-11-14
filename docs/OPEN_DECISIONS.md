# Décisions ouvertes — M1, samedi 09:30-10:30
> **État au 14/11 14:50 :** tableau d'origine ; les chiffres de la colonne « pilote » datent d'avant la calibration. Fait foi : `csync/rules.py` (seuil 1,5 + planchers) et `docs/PREMORTEM_14-11.md` §7 (D1–D12). Mesure actuelle (synthétique, seuil réglé sur les mêmes scénarios) : 0,7 % de faux déclenchements, 95,3 % dérive progressive.
| N° | Question | Défaut proposé | Chiffres du pilote | Décision M1 |
|---|---|---|---|---|
| 1 | Détecteur de dérive | Recommandé : EWMA + plancher d'écart-type (repli : d ≥ 1,5 + plancher). **Codé aujourd'hui : règle v3 seule, seuil 1,5 + planchers absolus (csync/rules.py, Params(), calibré le 14/11). EWMA n'est pas codée ; ne la coder que si M1 le décide.** | fausses procédures 17 % → 2,7 % ; détection 1,5 ET 99,3 % ; 94,7 % avec 10 % de données manquantes (research/pilot/RESULTS.md) | |
| 2 | Amplitude de la dérive de l'histoire | 2,5 ET (provisoire, passé explicitement : drift_amp=2.5 ; le défaut du générateur reste 1,5) | DEGRADED atteint dans 99 % des tirages (200 graines, amplitude 2,5, Params() calibré ; 94 % à 2,0). Vérifié graine 42, jour 7, Attention : Params() calibré (seuil 1,5 + planchers) : amplitude 2,5 → DEGRADED (jours 7–9) ; 2,0 → WATCH le jour 7, DEGRADED le jour 9 ; 1,5 → NORMAL | |
| 3 | Référence de 5 ou 7 jours | 5 jours | 7 jours : aucune amélioration (12 % de fausses procédures) | |
| 4 | UNKNOWN compte-t-il comme « hors NORMAL » ? | Non | sinon 8 procédures au lieu de 3 dans l'histoire | |
| 5 | Sens de l'humeur ; tension et température dans la règle ? | humeur ↓ défavorable ; TA et T affichées seulement | — | |
| 6 | Mission et Habitat dans le décompte des dimensions ? | Non (contexte) | — | |
| 7 | Criticité d'un épisode ouvert | garder le niveau le plus haut (déjà codé) | — | |
| 8 | Tension : une mesure par valeur ou value_text ? | une mesure par valeur, value_text SYS/DIA (déjà codé) | — | |

**Valeurs provisoires ajoutées le 14/11 (M1 valide) :** `ui_hint` : CONTINUE → NOMINAL ; OPEN_PROCEDURE CRITICAL → ACTION ; OPEN_PROCEDURE ROUTINE/IMPORTANT, PAUSE, REFUSE_RESUME → FOCUS. `ground_delay_min` = 20 est la valeur de démonstration figée par le contrat (le délai réel vers Mars va jusqu'à ~22 min). Texte de livraison : seule source = `delivered_once` dans `csync/config/strings_en.json`.
