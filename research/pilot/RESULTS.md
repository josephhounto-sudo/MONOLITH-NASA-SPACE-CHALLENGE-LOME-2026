> **SUPERSEDED (14/11/2026, pilot 3).** The recommendation below (EWMA as main detector) was **not adopted**: the engine is the rule v3 and EWMA is not coded. Current figures and decision: `docs/METHODES_NASA_DOSSIER.md` sections 7.3–7.10.

<!-- 14/11/2026 11:30 | PARTIELLEMENT OBSOLÈTE : les sections 1 à 5 recommandent EWMA ; elles sont remplacées par la section 7 de docs/METHODES_NASA_DOSSIER.md (comparaison calibrée, aucun gagnant démontré, EWMA non codée). -->
# Analysis pilot — results (14/11/2026)

**Question.** With only 5 days of personal baseline, which detector flags a real drift without raising false alarms on a crew member who is fine?

**Setup.** Synthetic astronauts from `synthetic/generator.py` (seeds 1000-1299 for controls, 5000-5149 for drifts). Every method sees exactly the same data and uses the same aggregation (1 flagged indicator = WATCH, 2+ = DEGRADED, 2 dimensions out of NORMAL = procedure). Reproduce: `python research/pilot/pilot.py && python research/pilot/figures.py` (≈ 2 min).

| Method | False procedures, no drift (300 runs) | Drift 1.0 SD detected | Drift 1.5 SD detected | Drift 2.0 SD detected | 1.5 SD with 10 % missing data | First procedure (median day) |
|---|---|---|---|---|---|---|
| A · current rule v3 (d ≥ 1) | 17.0 % | 95.3 % | 100 % | 100 % | 93.3 % | 7 |
| B · proposed rule (d ≥ 1.5 + SD floor) | 0.7 % | 71.3 % | 95.3 % | 100 % | 80.7 % | 7 |
| **C · EWMA trend (λ 0.3, 2.5 σ)** | **2.7 %** | **89.3 %** | **99.3 %** | **100 %** | **94.7 %** | **7** |
| D · CUSUM (k 0.5, h 3) | 4.3 % | 89.3 % | 99.3 % | 100 % | 94.0 % | 7 |
| E · combined score (diagonal χ²) | 0.3 % | 65.3 % | 84.7 % | 94.7 % | 66.7 % | 8 |

Drift days are 6-9, so day 7 is the earliest possible procedure with a two-day confirmation. Every method runs in about 11-14 ms per astronaut on a laptop — offline-compatible.

**What we learn**
1. The current rule (A) is too nervous: 1 healthy astronaut in 6 gets a false procedure. Short baselines on integer scales (sleepiness, stress) make the standard deviation tiny.
2. An absolute SD floor plus a stricter threshold (B) almost removes false alarms but loses sensitivity, and degrades the most when data are missing.
3. **EWMA (C) gives the best balance**: few false alarms, near-complete detection, and it stays robust when 10 % of the data are missing. It is still deterministic and explainable: *"your recent average has moved 2.5 times further than your usual day-to-day variation."*
4. A combined multivariate score (E) needs more baseline: a full covariance cannot be estimated from 5 days and 8 indicators, and the diagonal version misses drifts.

**Recommendation (decision for M1).** Use C (EWMA with SD floor) as the main detector, keep B as the simple, tested fallback. Keep 5 baseline days. Report the real control rate (2.7 %, 95 % interval 1.4-5.2 %, 8 of 300 runs) in the submission, not only the official seed.

**Inspiration, not endorsement.** NASA HRP's Artemis II Data Methodology Challenge (winners announced 11/09/2026) rewarded individual-level, small-sample methods (hierarchical/Bayesian N-of-1, normative modelling). C-Sync follows the same principle — each astronaut is compared to themselves — with a simpler deterministic method that runs offline. NASA has not reviewed or validated C-Sync.

**Limits.** Synthetic data and our own noise model; no real crew; no clinical meaning. The real NASA data in this project are ISS cabin telemetry (Habitat), used for context and quality checks.

---
## Résumé en français
Avec 5 jours de référence, la règle actuelle déclenche une fausse procédure chez 17 % des astronautes sans dérive. La moyenne mobile exponentielle (EWMA) avec plancher d'écart-type ramène ce taux à 2,7 %, détecte 99 % des dérives de 1,5 écart-type et reste à 95 % avec 10 % de données manquantes. Recommandation : EWMA comme détecteur principal, règle « d ≥ 1,5 + plancher » en repli. Décision de M1.
