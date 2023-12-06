from fonctions import *
from variables import *

###################################################
###           PARAMETRES DES REQUETES          ####
###################################################

# $cCode pour chercher par pays
# $distance pour chercher dans un rayon autour de $city
# $name our chercher par nom
# $a_venir True pour ne voir que les tou rnois à venir
# $gameId pour filtrer par jeu
# $page et $perPage pour paginer les évènements

params_get_events={
  "cCode": cCodes["France"], 
  "distance": "10km", 
  "city": ville_coord["Montpellier"],
  "name": "Roll'Inn", 
  # "a_venir": True,
  "gameId": game_Ids["Super Smash Bros. Ultimate"],
  "perPage":5 , 
  "page": 1
}

params_standings_seedings={
  "perPage": 500,
  "page": 1
}

##################################################################
###           RECUPERATION DES EVENEMENTS A ANALYSER          ####
##################################################################
 
singles = get_singles_id(params_get_events, url, headers)

####################################
###           ANALYSES          ####
####################################

print_tournaments(singles)
# get_distinct_players(singles,params_standings_seedings,url,headers)
# best_performance(singles,params_standings_seedings,url,headers)
# worst_performance(singles,params_standings_seedings,url,headers)
# most_regu(singles,params_standings_seedings,url,headers)
# least_regu(singles,params_standings_seedings,url,headers)
# top_seed(32,singles,params_standings_seedings,url,headers)
# top_standings(32,singles,params_standings_seedings,url,headers)
# max_nb_tournois(singles,params_standings_seedings,url,headers)