from functions import *
from variables import *
from datetime import *

###################################################
###           PARAMETRES DES REQUETES          ####
###################################################

# $cCode pour chercher par pays
# $distance pour chercher dans un rayon autour de $city
# $name pour chercher par nom
# $gameId pour filtrer par jeu
# $slug pour filtrer par "slug" (la partie à la fin du lien start.gg)
  # Par exemple dans le lien "https://www.start.gg/tournament/genesis-8/details", le slug est "tournament/genesis-8" ou juste "genesis-8"
# $after et $before pour chercher les évènements à garder avant ou après une certaine date
  # today pour aujourd'hui, get_date(jour,mois,année) pour une autre date
# $page et $perPage pour paginer les évènements

params_get_events={
  "cCode": "FR", 
  "distance": "10km", 
  "city": ville_coord["Montpellier"],
  # "name": "Miss", 
  "gameId": game_Ids["Super Smash Bros. Ultimate"],
  # "slug": "yggdrasil-1-1",
  "after": get_date(1,1,2023),
  "before":  today,
  "perPage": 500, 
  "page": 1
}

params_standings_seedings={
  # "eventId": 1033454,
  "perPage": 500,
  "page": 1
}

##################################################################
###           RECUPERATION DES EVENEMENTS A ANALYSER          ####
##################################################################
 
singles = get_singles_id(params_get_events, url, headers)
print(singles)

####################################
###           ANALYSES          ####
####################################

# print_tournaments(singles)
# taille_commu(1,singles,params_standings_seedings,url,headers)
# best_performance(singles,params_standings_seedings,url,headers)
# worst_performance(singles,params_standings_seedings,url,headers)
# most_regu(singles,params_standings_seedings,url,headers)
# least_regu(singles,params_standings_seedings,url,headers)
# top_seed(8,singles,params_standings_seedings,url,headers)
# top_standings(8,singles,params_standings_seedings,url,headers)
# max_tournois(5,singles,params_standings_seedings,url,headers)
# max_top_x(5,8,singles,params_standings_seedings,url,headers)

# count_sets(singles,params_standings_seedings,url,headers)
# count_games(singles,params_standings_seedings,url,headers)
# get_setcount_players('CTS | Erakos','BxH | Ewanz',singles,params_standings_seedings,url,headers)
# get_setcount_prefix("CTS","Her", singles, params_standings_seedings, url, headers)
# max_character_usage(5,singles,params_standings_seedings,url,headers)
# min_character_usage(5,singles,params_standings_seedings,url,headers)
# max_character_usage_rate(5,singles,params_standings_seedings,url,headers)
# min_character_usage_rate(5,singles,params_standings_seedings,url,headers)
# upsets=(get_upsets(singles,params_standings_seedings,url,headers))
# for i in upsets:
#     for j in range(len(i)):
#         print(i[j])
# count_upsets(singles,params_standings_seedings,url,headers)
# count_upsets_par_tournois(singles,params_standings_seedings,url,headers)
# biggest_upset(singles,params_standings_seedings,url,headers)
# max_upsets_realises(5,singles,params_standings_seedings,url,headers)
# max_upsets_subis(5,singles,params_standings_seedings,url,headers)
# min_upsets_subis(5,singles,params_standings_seedings,url,headers)
