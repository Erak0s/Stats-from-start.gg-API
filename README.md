# Stats from start.gg-API

# Bugs à fix 

# Améliorations à apporter

- Filtrer les DQ dans get_standings

- CHANGER LA STRUCUTRE: FAIRE LA REQUETE UNE FOIS PUIS LA STOCKER ET TOUT CALCULER A PARTIR DE CA
- PASSER SOUS R
- Interfacer avec shiny

# Fonctionnalités à ajouter

## Requêtes:

## Analyses:

- joueur ayant joué le plus de persos différents
- les plus souvent sous-seed (nb de fois ou ils font SPR+2 / nb de tournois)
- tournois avec le plus/moins d'upsets 

## A demander à d'autres gens (Richard)

- least_regu: afficher moyenne du SPR plutôt que sa somme -> est-ce vraiment plus pertinent ?

## Problèmes connus mais résolution abandonnée

- requête par nombre d'entrants max -> pas possible de query sur les évènements -> tout récup et filtrer ensuite

- Bien filtrer les évènements de type singles

- Winrate par personnage

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

# Disclaimer

Je ne suis ni développeur, ni expert en statistiques. Certaines mesures ne seront peut-être pas pertinentes et le programme est implémentée de manière à peine fonctionnelle. Si vous souhaitez l'améliorer, vous pouvez me contacter ou le faire de votre côté.
