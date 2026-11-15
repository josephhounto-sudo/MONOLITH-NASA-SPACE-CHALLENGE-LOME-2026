# Ressources officielles du défi et ce qui est dans le dépôt (15/11/2026 18:20)

Source : page du défi « Create Health Monitoring Software for Astronauts on Space Missions », rubrique « NASA Data & Resources », lue le 15/11/2026 (le site bloque la lecture automatique : lecture faite dans le navigateur connecté).
Le défi ne fournit **aucun jeu de données chiffré** : il fournit des pages de référence (NASA HRP) et deux pages de l'agence spatiale canadienne.

| # | Ressource officielle du défi | Adresse | Dans le dépôt | Utilisée dans C-Sync |
|---|---|---|---|---|
| 1 | NASA HRP, 5 Hazards of Human Spaceflight | https://www.nasa.gov/hrp/hazards/ | **copie du texte** `data/nasa_official/nasa_hrp_hazards.txt` | oui : fiches d'aide, panneau contre-mesures (reformulées) |
| 2 | NASA HRP, Risks of Human Spaceflight | https://www.nasa.gov/hrp/risks/ | **copie du texte** `data/nasa_official/nasa_hrp_risks.txt` (liste des 18 risques ; les pages de détail de chaque risque ne sont pas copiées) | oui : sommeil, santé comportementale, cardiovasculaire |
| 3 | NASA HRP, Ongoing HRP Research in Space | https://www.nasa.gov/hrp/ongoing-hrp-research/ | **copie du texte** `data/nasa_official/nasa_hrp_ongoing_research.txt` (liste des études ; pages de détail non copiées) | non cité avant ce jour ; ajouté à `SOURCES.md` |
| 4 | CSA, Monitoring Radiation for Astronaut Health | https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp | **lien seulement** (texte sous droits de la Couronne canadienne, non recopié) | non utilisée |
| 5 | CSA, Why Do We Conduct Science Experiments in Space? | https://www.asc-csa.gc.ca/eng/iss/science/why-do-we-conduct-science-experiments-in-space.asp | **lien seulement** | non utilisée |

## Données NASA que l'équipe a utilisées en plus (hors liste du défi)
| Donnée | Dans le dépôt |
|---|---|
| NASA OSDR Environmental Data App (ISS, 20 missions, 759 525 points) | brut compressé `data/real/raw/eda_all_missions.json.gz` (empreinte dans `data/real/raw/SHA256SUMS.txt`) et tables dérivées `data/real/eda_*.csv`, `habitat_*.csv` |
| NASA ASCEND, retard de communication Mars (NTRS 20220013418) | lien dans `SOURCES.md` (résumé lu le 15/11) ; texte non copié |
| Gagnants Artemis II Data Methodology Challenge | lien dans `SOURCES.md` ; inspiration méthodologique |
| NASA Life Sciences Portal (catalogue) | lien dans `SOURCES.md` |

## Limites à connaître
- Les pages de détail des 18 risques et des études en cours ne sont pas copiées : seulement les pages que le défi cite.
- Copie du texte affiché le 15/11/2026 : les pages NASA peuvent changer.
- Texte NASA : réutilisation généralement libre ; images non copiées.
