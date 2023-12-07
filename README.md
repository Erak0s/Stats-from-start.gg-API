# Stats from start.gg-API

# Bugs à fix 

- least regu marche pas

# Améliorations à apporter

# Fonctionnalités à ajouter

## Requêtes:

- Entrants par sponsor/prefix: https://developer.start.gg/docs/examples/queries/attendees-by-sponsor/

## Analyses:

- Taille de la commu -> comme distinct players mais compter les apparitions et mettre un seuil

- Perf moyenne en fonction du nombre d'entrants (placement/entrants)

- Plus grand écart de perf moyenne entre miss'tech et bars

- Fonction calcul plus gros upset

- Fonction calcul du nombre de fois qu'un joueur s'est fait upset

- Calcul joueur qui upset/se fait upset le plus souvent

- Fonction calcul taux/nombre moyen d'upset par tournoi 

## A demander à d'autres gens (Richard)

- least_regu: afficher moyenne du SPR plutôt que sa somme -> est-ce vraiment plus pertinent ?

- taux d'utilisation d'un personnage: diviser par 2 fois le nombre de games ? sinon on pourrait avoir + de 100% de pickrate

## Problèmes connus mais résolution abandonnée

- requête par nombre d'entrants max -> pas possible de query les tournois par numEntrants 

- Bien filtrer les évènements de type singles

- worst_perf: pire perf sur les gros tournois = top qui DQ -> comment filtrer les DQs ?

- Fonction calcul character usage impossible car complexité trop élevée dès qu'on dépasse un certain nombre de games dans un évènement (possible de faire en 2 requêtes ?)

- Fonctions qui parse les games ne vont pas marchehr sur les gros events (flamin'goat notamment)

# Autres notes importantes

- Les placements sont calculés selon un système d'arbre à double élimination. Si vous finissez à des placements bizarres à cause d'un système particulier (41ème après des poules en ronde suisse par exemple), votre placement sera assimilé à celui que vous auriez eu en bracekt à double élimination (33ème dans ce cas).

- Les side-events ne sont pas traités pour l'instant, uniquement les singles(dans la mesure du possible).

- Ce programme étant conçu initialement pour Super Smash Bros. Ultimate, il peut y avoir des subtilités propres à certains jeux qui ne sont pas traitées ici.

# Disclaimer

Je ne suis ni développeur, ni expert en statistiques. Certaines mesures ne seront pas pertinentes et le programme est implémentée de manire tout au plus fonctionnelle. Si vous souhaitez l'améliorer, vous pouvez me contacter ou le faire de votre côté.