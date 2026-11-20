# Pré-mortem du 15/11 (08:45) et prix visables

Source des critères : guide officiel Judging & Awards, https://www.spaceappschallenge.org/resources/judging-awards-guide (lu le 15/11/2026).

## 1. Pré-mortem : « 14:00, nous ne sommes pas retenus. Pourquoi ? »
| # | Scénario | État maintenant | Action |
|---|---|---|---|
| 1 | Le jury lit « données de santé d'équipage NASA » alors que seule la cabine ISS est réelle | Les panneaux disent « contexte seulement » | Garder cette phrase à l'oral |
| 2 | Validité : tout est synthétique, seuil réglé sur les mêmes scénarios | Évaluation hors échantillon faite (0,0 % faux, 92,7 % graduel, 57,3 % brusque) : `docs/VALIDATION_HOLDOUT.md` | Dire les 57,3 % tels quels |
| 3 | « Où sont les conseils de traitement ? » | Panneau contre-mesures NASA sourcées, aucune prescription | Dire que NASA classe les contre-mesures sommeil validées comme lacune de recherche |
| 4 | Départ avant l'ouverture officielle : permission orale, aucune trace écrite | **Ouvert** (AI_USAGE.md le déclare) | M1 : demander une confirmation écrite aux organisateurs |
| 5 | Fiches silhouette non relues par un médecin | **Ouvert** | M4 relit avant 11:00, sinon dire « non validé » |
| 6 | Démo qui plante | App locale, jours 7/9/10 testés, axe 0 | Garder une copie locale et le PDF |
| 7 | App vue dans un ancien état (onglet périmé ou clone non à jour) | Pied de page « Version abc1234 · capsules générées … » | Vérifier le numéro avant la démo |
| 8 | Deux sessions modifient `app.py` | Base unique : `main` | Une seule session écrit dans `app.py` |
| 9 | Soumission au dernier moment | Cible 15:00, limite 23:59 | M1 soumet, pas moi |
| 10 | Fatigue | n/a | Dormir avant 12:00 si possible |

## 2. Streamlit « pas actualisé, montre tout »
- Aucun déploiement n'existe dans le dépôt : tu vois une copie locale. `main` a bougé 5 fois ce matin ; une copie non mise à jour montre l'ancienne version.
- Streamlit ne recharge pas un module Python déjà importé ni les caches mémoire : après `git pull`, arrête (Ctrl+C) puis relance `streamlit run csync/ui/app.py`, puis recharge l'onglet.
- « Il montre tout » : c'était une seule longue page. Les panneaux secondaires sont maintenant regroupés en cinq onglets sous « More detail » ; l'action du jour reste en haut.
- Le numéro de version en bas de page dit quel code tourne.

## 3. Les données d'analyse sont-elles vraiment utilisées ?
| Donnée | Utilisation réelle |
|---|---|
| EDA brut (24 missions) | Panneau Habitat : 14 missions, CO2 en mmHg vs 3 mmHg, qualité, radiation ; adaptateur + mémoire locale testés |
| PhysioNet S10 | Seulement 2 paramètres du générateur (bruit 5,1 bpm, stress médian 3) ; **non affiché dans l'app** |
| `eda_mission_stats.csv`, `eda_quality_flags.csv`, `eda_radiation_summary.csv` | Non lus par le code (remplacés par `habitat_missions.csv`) : archives de contrôle |
| NLSP | Aucune donnée individuelle ouverte ; cité comme travaux antérieurs |
Limite : aucune donnée d'équipage réelle n'entre dans le moteur. C'est dit.

## 4. Prix visables (critères officiels : Influence, Creativity, Validity, Relevance, Presentation)
| Prix | Notre position | Pour y arriver |
|---|---|---|
| Global Nominee (jugement local) | **Réaliste** : défi traité de bout en bout, honnête, testé | Présentation nette, démo sans panne |
| Local Impact Award | Possible, **non travaillé** : la méthode « référence personnelle, hors ligne » vaut aussi pour des sites isolés au Togo | Une phrase au pitch, sans rien promettre |
| Best Use of Data | Possible : données EDA réelles + contrôle qualité | Dire exactement ce qui est réel |
| Best Use of Science | Faible : validité limitée au synthétique | Hors échantillon fait ; il faudrait des données réelles |
| Galactic Impact / Mission Concept | Faible à moyen | Non visé |
| Global Winner | **Peu probable** | Ne pas le promettre |
Écart avec le plan de départ : 23 promesses sur 32 tenues (72 %, `docs/PROMESSES.md`) ; manque surtout la validation externe (M4) et les données d'équipage réelles.
