# Référence « normale » faussée — un second regard avec des seuils publiés (SIMULÉ)

FAIT PAR L'IA — PAS ENCORE VÉRIFIÉ PAR UN TIERS. Script `research/baseline_check.py`, sortie `research/baseline_check_results.json`, 150 équipages simulés par case, graines 65000–65149.

Question (Joseph, 18/11): si la période prise comme « normale » est déjà décalée, la règle personnelle mesure contre du faux. Le décalage était déjà mesuré (`docs/BASELINE_BIAS.md`: à 1,5 écart-type, 63,7 % des détections disparaissent).
Test: sur les jours 1 à 5, noter « référence à confirmer » si le sommeil moyen est sous 7 h (AASM et SRS, Watson et al. 2015) ou si les lapses moyens sont à 11 ou plus (Basner et Rubinstein). Ce n'est jamais une alerte: c'est une demande « ces cinq jours étaient-ils normaux ? ».

| Écart entre personnes f | référence propre | décalée 0,5 ET | 1,0 ET | 1,5 ET |
|---|---|---|---|---|
| 0 | 15,3 % | 59,3 % | 82,0 % | 92,7 % |
| 1 | 32,0 % | 49,3 % | 66,0 % | 79,3 % |
| 2 | 40,7 % | 50,0 % | 62,0 % | 72,0 % |
| 3 | 44,7 % | 53,3 % | 66,0 % | 72,7 % |

Lecture honnête: le contrôle repère bien une référence très décalée quand tout le monde se ressemble (92,7 % à 1,5 ET, f = 0), mais il signale aussi 15 à 45 % des références propres (dormeurs courts, bruit de cinq jours). Quand les gens diffèrent (f ≥ 1), il discrimine mal (72 % contre 41 % à f = 2). Il ne répare pas la référence: il demande une confirmation.
Limites: générateur et règle conçus ensemble; f non sourcé; seuils publiés pour d'autres usages.
Piste plus solide, déjà testée et non adoptée (docs/BASELINE_BIAS.md): référence d'avant mission prise sur Terre, au repos.
