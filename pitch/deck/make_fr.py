"""FICHIER: pitch/deck/make_fr.py · 15/11/2026 · FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ
Builds deck_fr.html from deck.html by exact string replacement (same layout, same captures, same tests). A missing source string
stops the script, so the French deck cannot silently drift from the English one. Captures keep the English app UI.
Run from the repo root: python pitch/deck/make_fr.py, then DECK=deck_fr python pitch/deck/embed_captures.py"""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
SB = "SYNTHETIC DATA — demo story, not a real astronaut"
MAP = [
 ("Care Sync for deep-space crews", "Care Sync pour les équipages de l'espace lointain"),
 ("Offline health operations for a crew far from Earth", "Santé de l'équipage hors ligne, loin de la Terre"),
 ("Each astronaut compared with their own baseline", "Chaque astronaute comparé à sa propre référence"),
 (">The human decides<", ">L'humain décide<"),
 ("C-Sync · Synthetic data · AI use declared", "C-Sync · Données synthétiques · Usage de l'IA déclaré"),
 ("AI use declared", "Usage de l'IA déclaré"),
 ("Our goal", "Notre objectif"), ("Far from help: 22 min delay", "Loin des secours : 22 min de délai"),
 ("Guide emergencies", "Guider l'urgence"), (">Built<", ">Fait<"), ("Support the commander", "Aider le commandant"),
 ("Read NASA open data", "Lire les données NASA"), ("Habitat only", "Habitat seulement"),
 ("Connect real sensors", "Brancher de vrais capteurs"), (">Planned<", ">Prévu<"),
 ('Source: NASA Technical Reports Server, ASCEND 2022 paper', 'Source : NASA Technical Reports Server, article ASCEND 2022'),
 ("Built = in the app today, Prototype = works on synthetic data, Planned = not started",
  "Fait = dans l'app aujourd'hui, Prototype = fonctionne sur données synthétiques, Prévu = pas commencé"),
 ("Act 1 ·", "Acte 1 ·"), ("Drift (day 7)", "Dérive (jour 7)"), ("Compared with their own first five days", "Comparé à ses cinq premiers jours"),
 ("Attention Degraded: what changed, when, how sure", "Attention dégradée : quoi, depuis quand, avec quelle certitude"),
 ("Human decision: pending", "Décision humaine : en attente"), (SB, "DONNÉES SYNTHÉTIQUES — histoire de démonstration, pas un vrai astronaute"),
 ("5 dimensions, day 7", "5 dimensions, jour 7"), ("Decision capsule, day 7", "Capsule de décision, jour 7"),
 ("Act 2 ·", "Acte 2 ·"), ("Emergency (day 9)", "Urgence (jour 9)"),
 ("Sharp chest pain reported → Critical procedure", "Douleur thoracique vive signalée → procédure critique"),
 ("Guided measurements, one at a time: how to take each", "Mesures guidées, une à la fois : comment les prendre"),
 ("Report queued, delivered once", "Rapport en file, livré une seule fois"),
 ("Guided emergency, day 9", "Urgence guidée, jour 9"), ("Report queue, link down then restored", "File d'envoi : liaison coupée puis rétablie"),
 ("LIVE DEMO", "DÉMO EN DIRECT"), ("Act 3 ·", "Acte 3 ·"), ("Return (day 10)", "Reprise (jour 10)"),
 ("Heart rate 14 minutes old; limit 10 minutes", "Fréquence cardiaque vieille de 14 min ; limite 10 min"),
 ("Commander override: logged. Resume: refused.", "Forçage du commandant : consigné. Reprise : refusée."),
 ("Stale data is flagged as expired", "Donnée périmée : signalée expirée"), ("Fallback if the live demo fails", "Repli si la démo en direct échoue"),
 (">Evidence<", ">Preuves<"),
 ("0 of 300 unseen healthy crews triggered a procedure", "0 sur 300 équipages sains inédits : aucune procédure"),
 ("Drifts caught: gradual 93%, abrupt 57%", "Dérives repérées : progressives 93 %, brusques 57 %"),
 ("All simulated; real ISS data: quality checks only", "Tout est simulé ; données ISS réelles : contrôle qualité seulement"),
 ("Real NASA ISS cabin telemetry (EDA, RR-1)", "Télémétrie réelle de cabine ISS (EDA, RR-1)"),
 ("Data courtesy of the Environmental Data App (EDA)", "Données : Environmental Data App (EDA)"), ("accessed 14 Nov 2026", "consulté le 14 nov. 2026"),
 (">Limits<", ">Limites<"), ("Synthetic crew data, not clinically validated", "Équipage synthétique, non validé cliniquement"),
 ("Not yet measured: bones, immunity, radiation dose", "Pas encore mesurés : os, immunité, dose de rayonnement"),
 ("Next: expert review, analog data, sensors", "Après : relecture d'experts, données d'analogue, capteurs"),
 ("Offline. Explainable. The human decides.", "Hors ligne. Explicable. L'humain décide."),
 (">Body<", ">Corps<"), (">Watch<", ">Surveillance<"), (">Degraded<", ">Dégradé<"), (">Morale<", ">Moral<"),
 ("Habitat · context only", "Habitat · contexte seulement"), (">gradual<", ">progressive<"), (">abrupt<", ">brusque<"),
 ('<html lang="en">', '<html lang="fr">'),
]
h = open(os.path.join(HERE, "deck.html"), encoding="utf8").read()
for a, b in MAP:
    if a not in h:
        raise SystemExit("MISSING in deck.html: " + a)
    h = h.replace(a, b)
open(os.path.join(HERE, "deck_fr.html"), "w", encoding="utf8").write(h)
print("OK: pitch/deck/deck_fr.html")
