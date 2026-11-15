# FICHIER: pitch/deck/SCRIPT_EN.md
Date/heure : sam. 14/11/2026 ~15:00 UTC · Version v2 (15/11 : diapo 6 sur les graines tenues à l'écart) · Statut : TRADUIT PAR L'IA À PARTIR DE SCRIPT_FR.md v3 — PAS ENCORE RÉPÉTÉ NI VÉRIFIÉ À VOIX HAUTE

Oral en anglais (décision D11 : jury surtout anglophone ; diapos déjà en anglais). Version française de repli : `SCRIPT_FR.md`. 5:00, sans questions du jury.
Orateur A = M1 (diapos 1, 2, 3, 6, 7 = 190 s). Orateur B = M2 (diapos 4 et 5 = 110 s, dont la démo). Aucun nom dans ce fichier.
Règle : le contenu doit rester identique à SCRIPT_FR.md ; si l'un change, changer l'autre. Chaque affirmation chiffrée renvoie au README.

---

## Slide 1 · 0:00 → 0:25 (25 s) · speaker A
« Halfway to Mars, an astronaut reports sharp chest pain. A message takes up to twenty-two minutes to reach Earth, and there is no doctor on board. During that delay, who helps the crew measure, understand what is changing, and decide? We are team MONOLITH, and our answer is called C-Sync. »

## Slide 2 · 0:25 → 1:05 (40 s) · speaker A
« A message takes up to twenty-two minutes to reach Earth, according to NASA, and blackouts last days. The crew is alone. Our goal has four parts. Guide the emergency: built. Help the commander: a prototype ranks six simulated crew members by urgency, and decides nothing. Read NASA open data: built, for the habitat only. Connect real sensors: planned; the app already reads a data format, but no real device is connected. »

## Slide 3 · 1:05 → 1:55 (50 s) · speaker A
« Act one: a slow drift. C-Sync compares each astronaut with themselves, using their first five days, not a universal norm. During those five days, no drift alert is evaluated: the baseline is being built, and the screen says so. On day seven of our simulated story, reaction time and attention errors move away from their baseline two days in a row. The Attention card turns Degraded, and the Body card goes to Watch: two dimensions leave the normal range. C-Sync shows what changed, since when, and how certain it is. It opens a fatigue procedure and suggests reviewing the signals with the onboard medical officer. The decision stays human: it is shown as pending. »

## Slide 4 · 1:55 → 2:55 (60 s) · speaker B
« Act two, day nine: the emergency from the challenge video. The astronaut reports sharp chest pain. An event rule directly opens a critical procedure. The screen guides the measurements one by one: heart rate, blood pressure, temperature, blood glucose. For each one, it explains how to take it. Glucose is marked as having no NASA in-flight reference. C-Sync is designed without any drug recommendation or interpretation of the symptom: it records the values as measured, each with its time and origin. A fixed sentence reminds the crew to follow the onboard medical checklist and the medical officer. The report goes into a send queue, and the screen shows the link status. The link is down; when it comes back, the report is sent once, with no duplicate. On the left, the app's silhouette: the chest is selected, the habitat stays context only. »
**If running late: cut** « Glucose is marked as having no NASA in-flight reference. »

## Slide 5 · 2:55 → 3:45 (50 s) · speaker B
Demo: interface already open at day 10. Press « Request resume », then « Commander override ». If nothing shows within 10 s, switch to capture C5 and say the same text.

« Act three, day ten, live. I request the resume. Refused. [2 seconds of silence] The commander forces it. The override is logged, but the decision does not change: the last heart rate is fourteen minutes old, and the limit is ten. The system gives the reason in plain words on screen. Stale data is flagged as expired, not as normal. In our rules, an override alone is not enough to resume. »

## Slide 6 · 3:45 → 4:25 (40 s) · speaker A
« Our evidence, in the spirit of the Artemis II methods challenge: an individual baseline. We tuned the rule on one set of simulated crews, then ran it, unchanged, on three hundred new healthy crews: none triggered a procedure by mistake. Gradual drifts: ninety-three percent caught. Abrupt jumps: only fifty-seven percent, our known limit. Everything is simulated. The only real data is ISS cabin telemetry, where our quality check flags constant CO2 for more than six days. »
**If running late: cut** the last sentence (constant CO2).

## Slide 7 · 4:25 → 5:00 (35 s) · speaker A
« Our limits: the crew is simulated and nothing is clinically validated. Bones, immunity and the radiation dose received by the crew are not measured yet; they are shown as unknown. We chose a simple, tested, explainable engine over a black box. Next: expert review of the rules, a trial on simulated-isolation mission data, then real sensors. The interface shows only statistical deviations, with no medical label. C-Sync: offline, explainable, and the human decides. Thank you. »

---
## Word counts (script-computed)
| Slide | Time | Seconds | Words | Words/min |
|---|---|---|---|---|
| 1 | 0:00 → 0:25 | 25 | 50 | 120 |
| 2 | 0:25 → 1:05 | 40 | 71 | 106 |
| 3 | 1:05 → 1:55 | 50 | 114 | 137 |
| 4 | 1:55 → 2:55 | 60 | 151 | 151 |
| 5 | 2:55 → 3:45 | 50 | 75 | 90 |
| 6 | 3:45 → 4:25 | 40 | 76 | 114 |
| 7 | 4:25 → 5:00 | 35 | 75 | 129 |
| **Total** | **0:00 → 5:00** | **300** | **612** | **122** |

English is faster than French: about 150–160 words/min is a comfortable pace. Slide 5 is slow on purpose (two clicks and 2 s of silence). Time one full read-through aloud; if it exceeds 5:00, apply the two « cut » lines.

_Recalculated 15/11 ~10:50 UTC after the slide 2 rework (problem + goal) and the slide 4 and 7 changes; slide 2 is slow (106 words/min), time it at rehearsal._
