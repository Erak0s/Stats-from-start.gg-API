# Stats from start.gg-API

# Bugs à fix 

- requêtes sur le nombre de persos pas possible dès qu'on dépasse un certain nombre de sets (pour environ 50 entrantes) -> fix en faisant plusieurs requêtes pour chaque tournoi ?

# Améliorations à apporter

Biggest upsets : TEJ LES WINS PAR DQ !!!!

# Fonctionnalités à ajouter

## Requêtes:

## Analyses:

- les plus souvent sous-seed (nb de fois ou ils font SPR+2 / nb de tournois)
- tournois avec le plus/moins d'upsets 

## A demander à d'autres gens (Richard)

- least_regu: afficher moyenne du SPR plutôt que sa somme -> est-ce vraiment plus pertinent ?

## Problèmes connus mais résolution abandonnée

- requête par nombre d'entrants max -> pas possible de query sur les évènements

- Bien filtrer les évènements de type singles

- worst_perf: pire perf sur les gros tournois = top qui DQ -> comment filtrer les DQs ?

- Fonction calcul character usage 
    -> persos les plus/moins utilisés
    + winrate par personnage (ou juste pour Link)

## Abandonné car osef

- Perf moyenne en fonction du nombre d'entrants (placement/entrants)

- joueur le plus / moins régu (écart type minimal sur ses placements)

- Plus grand écart de perf moyenne entre miss'tech et bars
    -> utiliser fct perf moyenne 2 fois et comparer la différence pour chaque joueur

# Autres notes importantes

- Les placements sont calculés selon un système d'arbre à double élimination. Si vous finissez à des placements bizarres à cause d'un système particulier (41ème après des poules en ronde suisse par exemple), votre placement sera assimilé à celui que vous auriez eu en bracekt à double élimination (33ème dans ce cas).

- Les side-events ne sont pas traités pour l'instant, uniquement les singles(dans la mesure du possible).

- Ce programme étant conçu initialement pour Super Smash Bros. Ultimate, il peut y avoir des subtilités propres à certains jeux qui ne sont pas traitées ici.

- INORI A PAS MIS NLA EN TAG IL EST PAS COMPTÉ TANT PIS POUR LUI

- les joueurs qui ont changé de pseudos auront leurs stats faussées, chaque nom différent sera compté comme 2 joueurs

- pas pu faire de stats sur les personnages car requête trop limitée par l'API

# Disclaimer

Je ne suis ni développeur, ni expert en statistiques. Certaines mesures ne seront pas pertinentes et le programme est implémentée de manire tout au plus fonctionnelle. Si vous souhaitez l'améliorer, vous pouvez me contacter ou le faire de votre côté.
