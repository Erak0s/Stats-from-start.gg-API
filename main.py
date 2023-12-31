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
  # "name": "Downtown", 
  "gameId": game_Ids["Super Smash Bros. Ultimate"],
  # "slug": "yggdrasil-1-1",
  # "after": today,
  "after": get_date(1,1,2023),
  "before":  get_date(15,12,2023),
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
 
# singles = get_singles_id(params_get_events, url, headers)
singles=tournois_sauf_flamingoat
# singles=misstechs

####################################
###           ANALYSES          ####
####################################

print_tournaments(singles)
# taille_commu(10,singles,params_standings_seedings,url,headers)
# best_performances(20,singles,params_standings_seedings,url,headers)
# worst_performance(singles,params_standings_seedings,url,headers)
# most_regu(10,singles,params_standings_seedings,url,headers)
# least_regu(1,singles,params_standings_seedings,url,headers)
# print(least_regu(20,10,singles,params_standings_seedings,url,headers))
# top_seed(64,singles,params_standings_seedings,url,headers)
# top_standings(16,singles,params_standings_seedings,url,headers)
# max_tournois(50,singles,params_standings_seedings,url,headers)
# max_top_x(30,8,singles,params_standings_seedings,url,headers)
affrontements_freq(50,singles,params_standings_seedings,url,headers)
bracket_demon(100,5,singles,params_standings_seedings,url,headers)


# count_sets(singles,params_standings_seedings,url,headers)
# count_games(singles,params_standings_seedings,url,headers)
# get_setcount_players('Erakos','Ewanz',singles,params_standings_seedings,url,headers)
# get_setcount_prefix("BaL","NdL", singles, params_standings_seedings, url, headers)
# max_character_usage(500,singles,params_standings_seedings,url,headers)
# min_character_usage(500,singles,params_standings_seedings,url,headers)
# max_character_usage_rate(50,singles,params_standings_seedings,url,headers)
# min_character_usage_rate(50,singles,params_standings_seedings,url,headers)
# upsets=(get_upsets(singles,params_standings_seedings,url,headers))
# for i in upsets:
#     for j in range(len(i)):
#         print(i[j])
# count_upsets(singles,params_standings_seedings,url,headers, False)
# biggest_upsets(50,singles,params_standings_seedings,url,headers)
# max_upsets_realises(20,singles,params_standings_seedings,url,headers)
# max_upsets_subis(20,singles,params_standings_seedings,url,headers)
# max_upsets_subis_par_defaite(20,singles,params_standings_seedings,url,headers)
# min_upsets_subis(500,singles,params_standings_seedings,url,headers)

# placements=get_player_placement("El Tépe",singles,params_standings_seedings,url,headers)
# n=0
# for event in placements:
#   if placements[event] == 9:
#     n+=1
# print("El tépe a participé à",len(placements),"tournois")
# print("El Tépe a fini 9ème",n,"fois (",(n/len(placements))*100,"%)")