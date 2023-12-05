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
  "page": 4,
  "cCode": "FR",
  "perPage": 4,
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
    print(len(standing_seeding))
    # print(standing_seeding)
    standings = get_standings(standing_seeding, event_id)
    seedings = get_seedings(standing_seeding, event_id)
    for key in (standings):
      if key==('CTS | Ikcrow', 1021654):
        print(standing_seeding)
        # print(len(seedings))
        # print(len(standings))
        # print("SEEDING:",seedings)
        # print("STANDING:",standings)
        pass
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

# Problème avec la construction des listes standings/seedings: pas la bonne taille (devrait être égales au nombre d'entrants)
# PB vient SOIT de la requête SOIT des deux fonctions get_seedings et get_standings à la fois

best_performance(singles)
