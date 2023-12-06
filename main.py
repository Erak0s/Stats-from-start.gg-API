import requests
from queries import *
from fonctions import *

# API de start.gg
url = "https://api.start.gg/gql/alpha"

# Token d'authentification
headers = {
  "Authorization": "Bearer 3622a9c31282bd7cea09d8c9874f18c4"
}

ccodes={"France":"FR"}
ville_coord={"Montpellier":"43.604652,3.907186"}

###################################################
###           PARAMETRES DES REQUETES          ####
###################################################

# $cCode pour chercher par pays 
# $distance pour chercher dans un rayon autour de $city
# $name our chercher par nom
# $page et $perPage pour paginer les évènements
params_get_events={
  "cCode": ccodes["France"], 
  # "distance": "10km", 
  # "city": ville_coord["Montpellier"],
  "name": "Miss", 
  "perPage": 3, 
  "page": 1
}

params_standings_seedings={
  "perPage": 500,
  "page": 1
}

# Récupération des évènements à analyser

if("distance" in params_get_events and "city" in params_get_events):
    response = requests.post(url, headers=headers, json={'query': get_all_events_location, 'variables': params_get_events})
else:
    response = requests.post(url, headers=headers, json={'query': get_all_events_no_location, 'variables': params_get_events})
events = response.json()

singles = get_singles_id(events)

# Analyses

best_performance(singles,params_standings_seedings,url,headers)
worst_performance(singles,params_standings_seedings,url,headers)
# top_seed(50,singles,params_standings_seedings,url,headers)
