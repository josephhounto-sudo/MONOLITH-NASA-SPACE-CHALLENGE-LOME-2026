# Contrats techniques entre IA — 19/11/2026

Ces contrats ne touchent pas `contracts/` (schémas JSON gelés, accord de M1 requis) ni `csync/rules.py` / `csync/gate.py` (règle v3 gelée).
Python cible: 3.10 (ruff target py310). Dépendances nouvelles: seulement `cryptography` et `numpy` si absentes de requirements.txt; sinon bibliothèque standard. Toute dépendance ajoutée = ligne dans requirements.txt et THIRD_PARTY_NOTICES.md.
Texte affiché au jury en anglais. Mots interdits dans chaînes, README, procédures: cause, diagnos*, prove/proves, guarantee, disease.
Toute donnée non réelle porte le mot SIMULATED. Aucune référence, chiffre ou licence inventé: écrire NON VÉRIFIÉ.

## Propriété des fichiers (disjoints)
| IA | Branche | Fichiers possédés |
|---|---|---|
| Claude Code | glass-navy puis tech-integ | csync/ui/*, csync/tech/*, docs/*, fusion |
| Cursor | tech-modules | csync/analytics/changepoint.py, csync/crypto/capsule_sign.py, csync/sync/crdt_sim.py, csync/physio/hrv.py, tests/test_<module>.py |
| ChatGPT | aucune (markdown) | research/tech/*.md |
| Gemini | aucune (rapport) | research/review/*.md |
Cursor crée `csync/analytics/__init__.py`, `csync/crypto/__init__.py`, `csync/sync/__init__.py`, `csync/physio/__init__.py` vides. Il ne modifie aucun autre fichier.

## 1. csync/analytics/changepoint.py
```python
def cusum(values: list[float], baseline_mean: float, baseline_sd: float, k: float = 0.5, h: float = 4.0) -> dict:
    """One-sided upward CUSUM on z=(x-mean)/sd. Returns {"alarm_index": int | None, "scores": list[float]}.
    Raises ValueError if baseline_sd <= 0 or values is empty. None values are not accepted (caller filters)."""
def bocpd(values: list[float], hazard: float = 1/20) -> dict:
    """Bayesian online change-point (Gaussian, unknown mean, known unit variance on z-scores). Returns
    {"change_prob": list[float], "most_likely_index": int | None}. Pure python or numpy. Deterministic."""
```
Réglage de k, h, hazard: uniquement sur `synthetic/generator.py` avec graine A. Contrôle: autre graine B et la capsule jour 1-10 de `data/out/trends_histoire.json` (indicateur CO01). Les deux jeux et les paramètres figés sont écrits dans le test. Un résultat réglé et évalué sur le même jeu est refusé.
Tests obligatoires: série plate = aucune alarme; saut net = alarme au bon indice ±1; pente lente détectée avant le seuil fixe 284.553 sur CO01 (indice rendu, sans promettre de délai); entrée vide/sd nulle = ValueError; déterminisme.

## 2. csync/crypto/capsule_sign.py
```python
def sign_capsule(capsule: dict, private_key: bytes, prev_hash: str | None) -> dict:
    """Returns {"payload_sha256": str, "prev_hash": str | None, "signature": str(hex), "public_key": str(hex)}.
    Canonical JSON: sort_keys=True, separators=(",", ":"), ensure_ascii=False. Ed25519 via `cryptography`."""
def verify_capsule(capsule: dict, envelope: dict, expected_prev_hash: str | None) -> tuple[bool, str]:
    """(True, "ok") or (False, reason). Never raises on malformed input; returns (False, "malformed")."""
def generate_keypair() -> tuple[bytes, bytes]: ...
```
Tests: ok; un octet changé dans la capsule = False; mauvaise clé; chaîne cassée (prev_hash différent); enveloppe tronquée = (False, "malformed"); déterminisme de l'empreinte. Texte public: « detects modification », jamais « proves ».

## 3. csync/sync/crdt_sim.py
```python
class Replica:
    def __init__(self, replica_id: str): ...
    def set(self, key: str, value, ts: int) -> None: ...   # last-writer-wins register, ties broken by replica_id
    def state(self) -> dict: ...
    def merge(self, other: "Replica") -> None: ...        # commutative, associative, idempotent
def simulate_link(a: Replica, b: Replica, delay_steps: int, outage: tuple[int, int] | None, steps: int, seed: int) -> list[dict]:
    """Returns one record per step: {"step", "a", "b", "converged": bool}. Messages arrive after delay_steps; none during outage."""
```
Tests propriétés (hypothesis si déjà installé, sinon boucles à graine fixe): commutativité, associativité, idempotence, convergence après la fin de la coupure. Étiqueter l'objet « simulation ».

## 4. csync/physio/hrv.py
```python
def rmssd(rr_ms: list[float]) -> float: ...   # raises ValueError if fewer than 3 intervals or any <= 0
def sdnn(rr_ms: list[float]) -> float: ...
def simulated_rr(seconds: int, mean_hr: float, seed: int, stress: float = 0.0) -> list[float]:
    """SIMULATED RR series in ms; stress in [0,1] lowers variability. Deterministic."""
def clean_rr(rr_ms: list[float], low: float = 300.0, high: float = 2000.0) -> tuple[list[float], int]:
    """Drops out-of-range intervals; returns (kept, dropped_count)."""
```
Aucun jeu PhysioNet chargé tant que la licence n'est pas confirmée par research/tech/licences.md et vérifiée par Claude.
Tests: valeurs calculées à la main sur 4 intervalles; ValueError; déterminisme; stress plus haut = RMSSD plus bas (sur 20 graines, pas une seule).

## Acceptation commune
`python -m pytest -q` vert, `ruff check csync tests` propre, aucun message de développeur affiché, couverture des lignes ajoutées, une phrase de rapport par module: quoi, vérifié comment, non vérifié.
