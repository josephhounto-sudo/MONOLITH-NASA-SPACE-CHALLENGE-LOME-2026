# Relecture ChatGPT du 14/11/2026 (parties A–D) — STATUT : revue par Claude, NON validée par un humain
Date/heure : sam. 14/11/2026 ~14:10 UTC · Base : commit 6c0fdd7.
**Verdict de Claude après vérification contre le dépôt :**
- A (anglais) : 26 corrections proposées ; **5 retenues** (voir `docs/PREMORTEM_14-11.md`, tableau « Anglais »). Les autres sont de la préférence stylistique, ou abîment un libellé voulu (« Care Sync », « The human decides », « Resume »).
- B (minutage) : arithmétique juste (630 mots / 130 = 4:51) mais n'apporte rien au-delà du tableau du script ; « 3 passages à couper » = les 3 plus longs, sans analyse.
- C (questions) : 10 questions dont 5 reçoivent la même réponse ; Q9 utilise « ~22 min », alors que la source collectée (NASA HRP) dit « jusqu'à 20 minutes ». Remplacé dans le pré-mortem.
- D (README) : **les numéros de ligne cités (112–172) n'existent pas** — le README fait 73 lignes. Les citations existent, elles. 4 assouplissements retenus ; « exactly once » est couvert par `tests/test_sendqueue.py` ; l'attribution Artemis II est sourcée (`SOURCES.md`, page NASA relue le 14/11).
- Point important que ChatGPT a signalé sans le résoudre : « 37-hour frozen CO2 » (voir PREMORTEM R1 : la série brute est plus longue).
Texte ci-dessous = sortie brute de ChatGPT, non modifiée.

---
# **Relecture compilée — MONOLITH / C-Sync**

## **PARTIE A — Anglais des 7 diapositives**

| Diapo | Phrase d'origine                                     | Correction                                                | Raison en 5 mots                            |
| ----- | ---------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------- |
| 1     | Care Sync for deep-space crews                       | Care and synchronization for deep-space crews             | Formulation plus naturelle en anglais       |
| 1     | Offline health operations for a crew far from Earth  | Offline health operations for crews far from Earth        | Pluriel plus naturel ici                    |
| 1     | Each astronaut against their own baseline            | Each astronaut compared with their own baseline           | Comparaison exprimée plus naturellement     |
| 1     | The human decides                                    | The human makes the decision                              | Expression plus idiomatique en anglais      |
| 2     | Up to \~20 minutes one way                           | Up to \~20 minutes each way                               | Expression anglaise plus naturelle          |
| 2     | Communication blackouts that can last weeks          | Communication blackouts lasting weeks                     | Formulation plus concise et naturelle       |
| 2     | The crew must measure and act alone                  | The crew must measure and act independently               | Ton plus professionnel et précis            |
| 3     | Act 1 · Drift (day 7)                                | Act 1 · Drift (Day 7)                                     | Capitalisation cohérente des jours          |
| 3     | Compared with their own first 5 days                 | Compared with their own first five days                   | Nombre écrit en lettres ici                 |
| 3     | Attention Degraded: what changed, when, how sure     | Attention degraded: what changed, when, and how certain   | Grammaire et formulation plus naturelles    |
| 4     | Sharp chest pain reported → Critical procedure       | Sharp chest pain reported → Critical procedure initiated  | Verbe plus explicite dans ce contexte       |
| 4     | Guided measurements, one at a time: how to take each | Step-by-step guided measurements: how to perform each one | Formulation plus fluide en anglais          |
| 4     | Report queued, delivered once                        | Report queued and delivered once                          | Coordination grammaticale plus naturelle    |
| 4     | Static mock-up · not in the app yet                  | Static mock-up · not yet implemented in the app           | Formulation plus précise et professionnelle |
| 5     | Heart rate data 14 minutes old; limit 10             | Heart rate data: 14 minutes old; limit: 10 minutes        | Ponctuation et unité plus explicites        |

| Diapo | Phrase d'origine                                           | Correction                                                     | Raison en 5 mots                           |
| ----- | ---------------------------------------------------------- | -------------------------------------------------------------- | ------------------------------------------ |
| 5     | Commander override: logged. Resume: refused.               | Commander override: logged. Resumption: refused.               | Nom plus naturel dans ce contexte          |
| 5     | Stale data is never shown as normal                        | Stale data is never presented as normal                        | Verbe plus naturel en anglais              |
| 5     | Fallback if the live demo fails                            | Fallback plan if the live demo fails                           | Nom plus explicite pour l'audience         |
| 6     | 0.7 % of healthy simulated crews triggered a procedure     | 0.7% of healthy simulated crews triggered a procedure          | Format typographique anglais standard      |
| 6     | Real NASA ISS cabin telemetry used for data-quality checks | Real NASA ISS cabin telemetry was used for data-quality checks | Verbe manquant dans la phrase              |
| 6     | Synthetic data, 300 simulated healthy crews                | Synthetic data from 300 simulated healthy crews                | Préposition plus naturelle en anglais      |
| 6     | Real NASA ISS cabin telemetry (EDA, RR-1), English figure  | Real NASA ISS cabin telemetry (EDA, RR-1) — figure in English  | Formulation plus claire pour l'audience    |
| 7     | Synthetic crew data, not clinically validated              | Synthetic crew data; not clinically validated                  | Ponctuation plus claire entre propositions |
| 7     | Not measured yet: bones, immunity, radiation dose          | Not yet measured: bone health, immunity, and radiation dose    | Termes plus naturels et précis             |
| 7     | Next: real data, sensor adapters                           | Next steps: real data and sensor adapters                      | Coordination plus naturelle en anglais     |
| 7     | Offline. Explainable. The human decides.                   | Offline. Explainable. Human decisions remain in human hands.   | Formulation plus idiomatique et explicite  |

## **PARTIE B — Chronométrage à 130 mots/minute**

Le tableau fourni totalise **630 mots**. À 130 mots/minute, cela représente **4 min 51 s** environ : dans la fenêtre demandée de 4:50 à 5:10, mais avec très peu de marge. Le minutage réel dépendra des manipulations et transitions.

| Paragraphe          | Mots annoncés | Minutes cumulées à 130 mots/min |
| ------------------- | ------------- | ------------------------------- |
| Diapo 1 — orateur A | 54            | 0:25                            |
| Diapo 2 — orateur A | 87            | 1:05                            |
| Diapo 3 — orateur A | 116           | 1:59                            |
| Diapo 4 — orateur B | 135           | 3:01                            |
| Diapo 5 — orateur B | 71            | 3:34                            |
| Diapo 6 — orateur A | 88            | 4:14                            |
| Diapo 7 — orateur A | 79            | 4:51                            |
| **Total**           | **630**       | **4:51**                        |

**Trois passages les plus longs à couper en priorité :**

| Paragraphe             | Mots annoncés | Minutes cumulées |
| ---------------------- | ------------- | ---------------- |
| Diapo 4 — urgence      | 135           | 3:01             |
| Diapo 3 — dérive lente | 116           | 1:59             |
| Diapo 6 — preuves      | 88            | 4:14             |

Les coupes déjà prévues en diapos 4 et 6 sont pertinentes. Pour une troisième coupe, raccourcir une phrase de la diapo 3 sans toucher aux données ni à la logique de démonstration. **Attention :** les comptes annoncés sont repris du fichier, pas recalculés indépendamment ici.

## **PARTIE C — Questions difficiles du jury**

1. **Vos résultats proviennent-ils de vrais astronautes ?** — « donnée synthétique »
2. **Votre outil a-t-il été testé en mission habitée ?** — « pas validé sur de vrais équipages »
3. **Comment avez-vous validé la détection de la baisse de vigilance ?** — « pas de donnée PVT ouverte »
4. **Pourquoi choisir une ligne de base individuelle ?** — « donnée synthétique »
5. **Comment justifiez-vous le seuil de 1,5 écart-type sur deux jours ?** — « donnée synthétique »
6. **Comment distinguez-vous une dérive réelle d'une variation normale ?** — « pas validé sur de vrais équipages »
7. **Comment savez-vous que les alertes correspondent à un risque opérationnel ?** — « pas validé sur de vrais équipages »
8. **Comment évaluez-vous les fausses alertes ?** — « donnée synthétique »
9. **Comment l'équipage communique-t-il avec la Terre malgré le délai ?** — « délai Terre-Mars jusqu'à \~22 min »
10. **Vos résultats sont-ils généralisables à des conditions réelles ?** — « pas validé sur de vrais équipages »

## **PARTIE D — Cohérence du README**

| Ligne | Phrase                                                              | Pourquoi risqué                                            | Formulation prudente                                                    |
| ----- | ------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------- |
| 112   | “protects the decision to resume work”                              | Peut suggérer une garantie de sécurité.                    | “includes a prototype gate for resume requests”                         |
| 112   | “guides them step by step in an emergency”                          | La procédure est indiquée en cours.                        | “demonstrates a step-by-step emergency workflow”                        |
| 112   | “shows how sure it is”                                              | Calibration de confiance non démontrée.                    | “displays an indication of uncertainty”                                 |
| 112   | “never hides missing data”                                          | Promesse absolue sur toute l'interface.                    | “is designed to display missing data”                                   |
| 114   | “points to fixed procedure files”                                   | Disponibilité et intégration non confirmées.               | “is designed to reference procedure files”                              |
| 119   | “C-Sync learns this astronaut's normal”                             | Confusion possible avec une norme médicale.                | “C-Sync builds this astronaut's personal baseline”                      |
| 121   | “opens instantly”                                                   | Performance instantanée non mesurée.                       | “opens in the simulated scenario”                                       |
| 121   | “arrives exactly once”                                              | Garantie de livraison forte non démontrée.                 | “uses a queue designed to prevent duplicate delivery”                   |
| 138   | “a real 37-hour frozen CO2 value is flagged ARTIFACT”               | Fait à confirmer dans les données et le code.              | “a frozen CO2 value in the selected dataset is flagged ARTIFACT”        |
| 144   | “NASA HRP's Artemis II Data Methodology Challenge, which favoured…” | Attribution et interprétation **NON VÉRIFIÉES** ici.       | Retirer l'attribution ou citer la source exacte et préciser son statut. |
| 140   | “no team or personal data is ever collected”                        | Promesse absolue sur les journaux et la collecte.          | “the demo uses synthetic crew data”                                     |
| 172   | “implemented, tested”                                               | Les tests ne démontrent pas une validation opérationnelle. | “implemented; automated tests available”                                |

## **SORTIE FINALE**

| Partie | Problème                                                                                        | Action à faire                                                                                                                    |
| ------ | ----------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| B      | Le tableau annonce 630 mots, soit environ 4:51 à 130 mots/min.                                  | Faire une répétition chronométrée complète, avec les clics et le silence de la démo.                                              |
| B      | La diapo 4 est le passage le plus long.                                                         | Préparer une version courte de secours pour l'orateur B.                                                                          |
| B      | La diapo 3 est le deuxième passage le plus long.                                                | Préparer une coupe courte sans supprimer l'explication de la baseline.                                                            |
| B      | Le débit de la démo est volontairement lent.                                                    | Répéter les manipulations avec l'orateur B et chronométrer les transitions.                                                       |
| A      | Certaines formulations anglaises sont peu naturelles.                                           | Appliquer les corrections linguistiques proposées, sans changer les chiffres.                                                     |
| A      | Les mentions de données réelles et synthétiques doivent rester distinctes.                      | Vérifier que chaque légende de diapositive décrit exactement la capture affichée.                                                 |
| C      | Le jury peut demander la justification du seuil 1,5 et des deux jours.                          | Préparer une explication honnête fondée sur les essais réellement réalisés ; ne pas présenter cela comme une validation clinique. |
| C      | Le délai de communication ne répond pas à lui seul à la question des coupures.                  | Distinguer délai de propagation et interruption de liaison dans la réponse orale.                                                 |
| D      | Le README contient des garanties techniques fortes.                                             | Réviser en priorité les lignes 112, 121 et 172 après vérification du code.                                                        |
| D      | L'attribution au défi méthodologique Artemis II est insuffisamment étayée dans le texte fourni. | Vérifier la source exacte ou retirer cette attribution.                                                                           |

**Limite générale :** cette relecture porte sur les textes fournis. Le code au commit `dc61786`, les données sources, les captures et les références externes n'ont pas été audités ici. Les corrections proposées ne constituent donc pas une validation technique ou scientifique.