# Licences et références — 19/11/2026
Source de départ: réponse de ChatGPT (navigateur). Chaque ligne ci-dessous est étiquetée selon ce que Claude a rouvert lui-même le 19/11/2026.

## Jeux de signaux cardiaques
| Jeu | Licence | Accès | Statut |
|---|---|---|---|
| MIT-BIH Arrhythmia Database 1.0.0 | ODC-By v1.0 | ouvert | VÉRIFIÉ (page officielle https://physionet.org/content/mitdb/1.0.0/) |
| PTB-XL 1.0.3 | CC BY 4.0 | ouvert | VÉRIFIÉ (https://physionet.org/content/ptb-xl/1.0.3/) |
| MIT-BIH Noise Stress Test 1.0.0 | ODC-By v1.0 (annoncé par ChatGPT) | ouvert | NON VÉRIFIÉ par Claude |
| MIMIC-IV-ECG 1.0 | ODbL v1.0 (annoncé par ChatGPT) | ouvert | NON VÉRIFIÉ par Claude; partage à l'identique, à éviter pour la démo |

Décision d'usage: aucun signal réel n'est chargé dans le dépôt. Si un jour un extrait l'est, ce sera MIT-BIH ou PTB-XL avec attribution écrite, après relecture du texte de la licence. Les ECG ne donnent pas directement des intervalles RR: il faut les extraire des annotations de battements (non fait).

## Références primaires
| Référence | Ce qu'elle établit | Statut |
|---|---|---|
| RFC 9171, Bundle Protocol Version 7 (Burleigh, Fall, Birrane III; janvier 2022) https://www.rfc-editor.org/rfc/rfc9171.html | Définit le format et les procédures des « bundles » dans les réseaux tolérants aux délais | VÉRIFIÉ (page officielle relue) |
| Task Force ESC/NASPE, Circulation 93(5):1043-1065, 1er mars 1996, DOI 10.1161/01.CIR.93.5.1043 | Standards de mesure de la variabilité cardiaque; RMSSD et SDNN y sont définis | VÉRIFIÉ par PubMed https://pubmed.ncbi.nlm.nih.gov/8598068/ (le DOI direct n'a pas répondu) |
| Page 1954, Continuous Inspection Schemes, Biometrika 41(1-2):100-115, DOI 10.1093/biomet/41.1-2.100 | Schémas de détection continue de changement (origine du CUSUM) | NON VÉRIFIÉ par Claude |
| Shapiro, Preguiça, Baquero, Zawirski, INRIA RR-7506, janvier 2011 | Conditions de convergence des répliques (CRDT) | NON VÉRIFIÉ par Claude |

Limite: ces références justifient des méthodes et un protocole, pas la validité clinique. Les données restent SIMULATED.
