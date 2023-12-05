import requests
from queries import *
from fonctions import *

# API de start.gg
url = "https://api.start.gg/gql/alpha"

# Token d'authentification
headers = {
  "Authorization": "Bearer 3622a9c31282bd7cea09d8c9874f18c4"
}

# Requetes retournant les nom et ids de tous les events souhaités

params={
  "cCode": "FR",
  "perPage": 3,
  "distance": "10km",
  "city": "43.604652,3.907186",
  "name": "Miss"
}

response = requests.post(url, headers=headers, json={'query': get_all_events_location, 'variables': params})
events = response.json()

singles = get_singles_id(events)

def best_performance(events):
  max_SPR=0
  print("Event(s) checked: ",events)
  for event_id in (events):
    params2={
      "eventId": str(event_id), 
    }
    response = requests.post(url, headers=headers, json={'query': get_standings_seed, 'variables': params2})
    standing_seeding = response.json()
    standings = get_standings(standing_seeding, event_id)
    seedings = get_seedings(standing_seeding, event_id)
    for key in (standings):
      # print("SEEDING:\\",seedings)
      # print("STANDING:\\",standings)
      SPR = SPR_player(key[0], event_id, seedings, standings)
      if SPR > max_SPR:
        max_SPR = SPR
        best_perf = [key[0]]
        event = [event_id]
      else:
        if SPR == max_SPR:
          best_perf.append(key[0])
          event.append(event_id)
  for i in range (len(best_perf)):
    print("Meilleure performance:",best_perf[i]," à l'évènement",events[event[i]],"(SPR",max_SPR,")")

# Transférer fonction best_perf dans fonctions.py
# Problème avec ickrox au bout de 4 misstech en arrière
# Faire une requête selon la date

best_performance(singles)

# print(SPR_player("NLA W'nS | Zelume", 1033454, seedings, standings))

# Récup le seed et la perf de chaque jouer des évents singles des miss'tech des 30 derniers jours

# variables_perf = {
# }

# getCharacterUsage = """
# """

# variables_char = {
# }

# getUpsets = """
# """

# variables_upsets = {
# }

# Joueur le plus régulier = plus autour de son seed en moyenne



# response = requests.post(url, headers=headers, json={'query': getPerfomance, 'variables': variables_perf})
# performance = response.json()

# response = requests.post(url, headers=headers, json={'query': getCharacterUsage, 'variables': variables_char})
# character_usage = response.json()

# response = requests.post(url, headers=headers, json={'query': getUpsets, 'variables': variables_upsets})
# upsets = response.json()

