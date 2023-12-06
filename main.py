from fonctions import *

# API de start.gg
url = "https://api.start.gg/gql/alpha"

# Token d'authentification
headers = {
  "Authorization": "Bearer 3622a9c31282bd7cea09d8c9874f18c4"
}

cCodes={"France":"FR","Japon":"JP","Etas-Unis":"US","Autriche":"AT"}
ville_coord={"Montpellier":"43.604652,3.907186"}
game_Ids={"Super Smash Bros. Ultimate":"1386"}

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
  # "distance": "10km", 
  # "city": ville_coord["Montpellier"],
  "name": "King Con", 
  "a_venir": True,
  "gameId": game_Ids["Super Smash Bros. Ultimate"],
  "perPage":1 , 
  "page": 2
}

params_standings_seedings={
  "perPage": 500,
  "page": 1
}

##################################################################
###           RECUPERATION DES EVENEMENTS A ANALYSER          ####
##################################################################
singles = get_singles_id(params_get_events, url, headers)
singles = {1017523: 'King Con'}
print(singles)

####################################
###           ANALYSES          ####
####################################

# get_distinct_players(singles,params_standings_seedings,url,headers)
# best_performance(singles,params_standings_seedings,url,headers)
# worst_performance(singles,params_standings_seedings,url,headers)
# most_regu(singles,params_standings_seedings,url,headers)
# least_regu(singles,params_standings_seedings,url,headers)
# top_seed(50,singles,params_standings_seedings,url,headers)
# top_standings(50,singles,params_standings_seedings,url,headers)