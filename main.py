import requests
from queries import *
from fonctions import *

# API de start.gg
url = "https://api.start.gg/gql/alpha"

# Token d'authentification
headers = {
  "Authorization": "Bearer 3622a9c31282bd7cea09d8c9874f18c4"
}

###################################################
###           PARAMETRES DES REQUETES          ####
###################################################

params_get_events={
  "cCode": "FR", # Pour chercher par pays
  "distance": "10km", # Pour chercher par géographique, avec $city
  "city": "43.604652,3.907186",
  # "name": "Flamin", # Pour chercher par nom
  "perPage": 2 # Requête va inclure les x derniers events
}

params_best_perf={
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

best_performance(singles,params_best_perf,url,headers)
