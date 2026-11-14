# FICHIER: RAPPORT_PHASE3.md
Date/heure : sam. 14/11/2026 09:00 Lomé (UTC) · Commit de référence : dc61786 · Version v1
Statut : FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ

## 0. À lire en premier
1. Le zip rev4 a été reçu et lu. Il **ne contient pas de dossier `.git`** : je ne peux pas vérifier que son contenu correspond au commit `dc61786`. Je me fie à l'étiquette.
2. **La liste officielle des mots interdits n'est pas dans `csync/config/strings_en.json`.** Elle se trouve dans `csync/language.py` (`BANNED_EN`, `BANNED_FR`) et dans le champ `banned_words` de `data/scenarios/*.json`. J'ai utilisé `csync.language.banned_hits()`, la fonction du dépôt (voir §4).

## 1. Tableau T1–T5
| Tâche | État | Livrables | Ce qui reste |
|---|---|---|---|
| T1 Silhouette | **Fait** | `pitch/silhouette/silhouette.svg`, `fiches.json`, `build_silhouette.py`, `silhouette_demo.html` (généré, autonome) | Test sur place par M1. Rubrique « Why » : « No NASA in-flight reference » partout, en attente des sources d'un autre chat |
| T2 Deck v2 | **Fait** (captures en attente) | `pitch/deck/deck.html`, `captures_map.md`, `embed_captures.py` | Captures C1–C6 ; logo (`LOGO_À_FOURNIR`) ; numéro de version EDA |
| T3 Script oral | **Fait** | `pitch/deck/SCRIPT_FR.md` : 630 mots en 5:00 ; 130–139 mots/min sur les diapos parlées | Répétition chronométrée à voix haute |
| T4 Vidéo 30 s | **Fait** (production facultative) | `pitch/video/SHOTLIST_30S.md` : 6 plans, 30,0 s, voix off de 70 mots | Voix de synthèse, musique et licence si la vidéo est produite |
| T5 Fiches | **Fait** | `FICHES_MESURES.md` v2 | « SOURCE À AJOUTER » sur toutes les rubriques « Pourquoi » sauf PH09 (URL HRP présente, phrase manquante) et PH12 (étiquette du dépôt) |
| Revue des fichiers de phase 2 | **Fait** | `phase2_maj/STORYBOARD_v4.md` (v4.1) | Voir §5 |

## 2. Ce que j'ai réellement exécuté ou testé
| Quoi | Commande ou outil | Résultat |
|---|---|---|
| Tests du dépôt | `python -m pytest -q` (zip rev4, Python 3, dépendances installées) | **91 passed** |
| Histoire de démo | `python scripts/run_story.py --out /tmp/story` | `histoire -> 3 procedure day(s) \| events: 1 \| capsules: 12`. Jour 7 : Body WATCH, **Attention DEGRADED**, Morale NORMAL, PROC-FATIGUE-01 IMPORTANT (jours 7–9). Jour 10 : `G3: PH01 is stale (14 min > 10 min)` ; avec override : `G6: … never authorises a resume on its own` |
| Chiffre de la diapo 6 | Lecture de `research/pilot/pilot3_sweep.csv`, ligne « Rule (d>=thr, 2 days, SD floor) », seuil 1.5 ; comparaison des planchers de `research/pilot/pilot.py` (ABS_FLOOR) avec `csync/rules.py` (Params) | Témoins 0,7 % (IC 0,2–2,4) ; graduel 95,3 % ; brutal 59,3 %. **Mêmes planchers que le code de la démo** : le chiffre est bien celui de ce que la démo exécute |
| Gel réel du CO2 | `flag_plateaus` sur `data/real/eda_rr1_iss_hourly_*.csv` | 1 série figée de 37 h à 2 646 ppm (comme `tests/test_quality.py`) |
| Silhouette | Test jsdom (`test_silhouette.js`, 45 contrôles) | **Tout passe** : 8 régions avec role=button, tabindex=0, aria-label ; un clic → fiche à 4 rubriques ; touche Entrée ; liste de repli de 8 boutons avec aria-pressed ; bandeau SYNTHETIC DATA ; étiquette « À CONFIRMER M1 — non codée » ; aucune ressource externe |
| Silhouette (rendu) | Playwright + Chrome headless, 1280×800, clic sur Chest | Capture vérifiée à l'œil ; 0 erreur JS ; 0 requête réseau |
| Deck | Test jsdom (`test_deck.js`, 24 contrôles) | **Tout passe** : 7 diapos ; ≤ 25 mots par diapo (de 22 à 25, compteur automatique) ; bandeau sur chaque cadre de capture ; navigation ← → Début Fin ; absence de « EWMA », « 17 % », « 2.7 », « 23 tests », « 13/13 », « validated by NASA » |
| Deck (rendu et impression) | Playwright : captures d'écran des 7 diapos ; export PDF en média `print` | 3 défauts de mise en page corrigés (diapo 2 : trait sur « 20:00 » ; diapo 4 : silhouette sur le pied de page ; diapo 6 : ligne source sur le cadre). PDF : **7 pages, 16:9** ; 0 requête réseau |
| Insertion des captures | `embed_captures.py` sur une **copie temporaire**, avec une image factice nommée C2 | C2 insérée en data URI, les 5 autres gardées en cadre ; `deck.html` non modifié. Le fichier factice n'a pas été livré |
| Comptes de mots | Script sur `SCRIPT_FR.md` et `SHOTLIST_30S.md` | Oral : 630 mots / 300 s. Vidéo : 70 mots / 30 s |

**Non testé :**
- Lecteur d'écran réel (NVDA ou VoiceOver).
- Affichage sur téléphone réel.
- Impression sur imprimante physique.
- Interface Streamlit lancée : je n'ai pas fait de captures d'écran de l'application, c'est le rôle de l'autre chat.

## 3. Écarts avec le dépôt ou avec les consignes reçues
| # | Écart | Ce que j'ai fait | Décision attendue |
|---|---|---|---|
| E1 | Mots interdits : la liste est dans `csync/language.py`, pas dans `strings_en.json` | J'ai utilisé `language.py` | Corriger la consigne |
| E2 | **Consigne A6** (« capteur figé = vrai seulement dans la démo synthétique ») **contredite par le dépôt.** Le capteur figé est **réel** : CO2 RR-1 figé 37 h, signalé par `csync/quality.py` et testé. La variante synthétique « capteur » est autre chose : une panne PH01 (donnée manquante → UNKNOWN), pas une valeur figée | Le fait réel est dans le script oral (diapo 6), avec une ligne « coupe » et la mention [À VALIDER M1]. Il n'est pas sur la diapo | M1 garde ou coupe |
| E3 | `scripts/run_story.py` **ne charge pas** la télémétrie réelle : dans l'histoire, la carte Habitat est grise (« Context only — not evaluated ») | La diapo 6 dit « used for data-quality checks », pas « Habitat view ». C6 = figure EDA, pas un écran de l'application | — |
| E4 | La figure `pitch/figures/nasa_eda_habitat_fr.png` est **en français**, et aucun script du zip ne la produit | C6 demandée en anglais (`captures_map.md`) | Qui la refait ? |
| E5 | L'écran d'urgence de l'application montre « How to measure / Why / NASA source », **pas « when to alert »** | Puce de la diapo 4 réécrite (« Guided measurements, one at a time: how to take each ») ; « when to alert » reste seulement dans la maquette de silhouette | — |
| E6 | L'étape 2 de PROC-EMERGENCY-01 demande de « select the body zone », **sans interface codée** | La silhouette est la réponse naturelle, mais elle reste « non codée » partout | Brancher la silhouette sur l'étape 2 : décision M1 |
| E7 | **PS01 = somnolence (KSS)**, pas « sommeil » ; le sommeil est PH09 | Corrigé dans les fiches | — |
| E8 | `pitch/OUTLINE.md` (dans le dépôt) contient encore « no cause, no diagnosis », les chiffres EWMA 17 % → 2,7 %, « 13/13 » et « CDSS ». `banned_hits` détecte : cause, diagnosis | Non modifié (pas d'accès en écriture) ; remplacé par `deck.html` | Supprimer ou remplacer `OUTLINE.md` |
| E9 | `research/pilot/RESULTS.md` recommande toujours l'EWMA (sections 1–5), contredit par le §7 du dossier de méthodes | Seuls les chiffres du §7.3 et du CSV sont utilisés | Ajouter une ligne « remplacé par le §7 » dans RESULTS.md |
| E10 | La vue sol garde la première copie reçue, un doublon à 19:25 ; la première réception physique est à 19:20 (noté dans `run_story.py`) | La diapo dit seulement « delivered once », ce qui est exact | Déjà notifié à M1 dans le code |
| E11 | Le storyboard v3 parlait de « deux lignes de journal » ; l'application en ajoute **une par override** | Corrigé (storyboard v4.1, `captures_map.md`) | — |
| E12 | `docs/PROGRAMME_OFFICIEL.md` : la FAQ officielle dit « aucun travail avant samedi 09:00 » ; la trace écrite de l'autorisation orale manque | Rien à faire de mon côté | Trace écrite à obtenir |

## 4. Recherche des mots interdits (liste officielle `csync/language.py`)
Liste cherchée :
- EN : cause, caused by, because of, diagnosis, diagnose, disease, disorder, suffers from, proves, guaranteed ;
- FR : cause, causé par, à cause de, diagnostic, diagnostique, maladie, pathologie, souffre de, prouve, garanti.

Méthode : `csync.language.banned_hits()`. Elle repère le début de mot (`\b` + mot), donc aussi les formes niées et les dérivés, par exemple « prouvé ».

| Fichier | Résultat |
|---|---|
| `pitch/deck/deck.html` (source et texte rendu) | **0** |
| `pitch/deck/SCRIPT_FR.md` | **0** |
| `pitch/deck/captures_map.md`, `embed_captures.py` | **0** |
| `pitch/video/SHOTLIST_30S.md` | **0** |
| `pitch/silhouette/*` (SVG, JSON, script, HTML et texte rendu des 8 fiches) | **0** |
| `FICHES_MESURES.md` | **0** |
| `phase2_maj/STORYBOARD_v4.md` | **0** |
| `RAPPORT_PHASE3.md` (ce fichier, interne) | Contient la liste elle-même (§4) et la citation du défaut E8 : **seules occurrences, toutes dans ce rapport interne**, jamais dans un texte affiché ou dit |
| Pour information : `pitch/OUTLINE.md` du dépôt | **3** (cause, diagnosis, cause), voir E8 |

Autres phrases interdites cherchées : « NASA uses our methods », « validated by NASA », « validé par la NASA », EWMA, 17 %, 2,7 %, 23 tests, 13/13.
- Absentes de tous les textes affichés ou dits.
- Présentes seulement dans ce rapport, comme sujet du contrôle (et dans le storyboard, dans le tableau des changements de version).

## 5. État des fichiers de la phase 2
| Fichier | État |
|---|---|
| `STORYBOARD_v4.md` | Mis à jour en **v4.1** (`phase2_maj/`) : drift_amp 2.5, sous-titres alignés sur la shotlist, captures. `SCRIPT_FR.md` et `SHOTLIST_30S.md` priment |
| `SLIDES_EN_v1.md` | **Remplacé** par `pitch/deck/deck.html` (ne plus l'utiliser) |
| `CAPTURES_A_FAIRE.md` | **Remplacé** par `pitch/deck/captures_map.md` (les options `--seed` et `--drift-amp` n'existent pas) |
| `MAQUETTE_PLAN.md` | **Remplacé** par `captures_map.md` et la silhouette (E6 construite) |
| `FICHES_MESURES.md` | **v2** dans ce rendu |
| `QUESTIONS_OUVERTES.md` | **Clos** par les réponses de M1 ; ce qui reste est au §6 |

## 6. Ce qui reste ouvert (bloquant pour le PDF final seulement)
1. Captures C1–C6 (autre chat), dont C6 en anglais (E4).
2. Logo de l'équipe et numéro de version EDA (crédit, diapo 6).
3. Validation E2 (capteur CO2 réel dans l'oral).
4. Sources « why » par mesure (autre chat) : remplir `fiches.json`, puis `python pitch/silhouette/build_silhouette.py`.
5. Si la vidéo est faite : voix de synthèse, musique libre de droits et licence.
