# Stats from start.gg-API

# Bugs à fix 

- requêtes sur le nombre de persos pas possible dès qu'on dépasse un certain nombre de sets (pour environ 50 entrantes) -> fix en faisant plusieurs requêtes pour chaque tournoi ?

- least regu marche pas

# Améliorations à apporter

- calculer upsets réalisés/subis en proportion du nb de games jouées ?

# Fonctionnalités à ajouter

## Requêtes:

## Analyses:

- Perf moyenne en fonction du nombre d'entrants (placement/entrants)

- joueur le plus / moins régu (écart type minimal sur ses placements)

- Plus grand écart de perf moyenne entre miss'tech et bars
    -> utiliser fct perf moyenne 2 fois et comparer la différence pour chaque joueur

- Fonction calcul character usage 
    -> persos les plus/moins utilisés
    + winrate par personnage (ou juste pour Link)

## A demander à d'autres gens (Richard)

- least_regu: afficher moyenne du SPR plutôt que sa somme -> est-ce vraiment plus pertinent ?

## Problèmes connus mais résolution abandonnée

- requête par nombre d'entrants max -> pas possible de query sur les évènements

- Bien filtrer les évènements de type singles

- worst_perf: pire perf sur les gros tournois = top qui DQ -> comment filtrer les DQs ?

# Autres notes importantes

- Les placements sont calculés selon un système d'arbre à double élimination. Si vous finissez à des placements bizarres à cause d'un système particulier (41ème après des poules en ronde suisse par exemple), votre placement sera assimilé à celui que vous auriez eu en bracekt à double élimination (33ème dans ce cas).

- Les side-events ne sont pas traités pour l'instant, uniquement les singles(dans la mesure du possible).

- Ce programme étant conçu initialement pour Super Smash Bros. Ultimate, il peut y avoir des subtilités propres à certains jeux qui ne sont pas traitées ici.

- INORI A PAS MIS NLA EN TAG IL EST PAS COMPTÉ TANT PIS POUR LUI

# Disclaimer

Je ne suis ni développeur, ni expert en statistiques. Certaines mesures ne seront pas pertinentes et le programme est implémentée de manire tout au plus fonctionnelle. Si vous souhaitez l'améliorer, vous pouvez me contacter ou le faire de votre côté.

# Stats de l'avent

24: tableau du setcount entre teams (CTS,BxH,Her,NLA,BàL,NdL,????)

23: meilleure perf

22: max de top 8 (miss'tech, bars, total)

21: max de tournois (miss'tech, bars, total)

20: moins régu par rapport à son seed #si ça marche (inseedable)

19: plus régu par rapport à son seed

18: nombre de sets joués (miss'tech, roll'inn, melt, flamin'goat, total)

17: nombre de tournois (miss'tech, roll'inn, melt, flamin'goat, total)

16: Nombre d'upsets total (et nombre par tournois)

15: Plus gros upsets

14: Le plus d'upset réalisés/subis

13: