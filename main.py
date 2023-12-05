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

def get_singles_id(request, params):
    response = requests.post(url, headers=headers, json={'query': request, 'variables': params})
    events = response.json()

    event_ids=[]
    for tournament in events['data']['tournaments']['nodes']:
      for event in tournament['events']:
          if ("Single" in event['name']) or ("single" in event['name']) or ("Singles" in event['name']) or ("singles" in event['name']) :
              event_ids.append(event['id'])
    return(event_ids)

params={
  "name": "Miss'Tech"
}

singles = get_singles_id(get_all_events,params)

# Pour chaque event, on récupère le standing et le seeding
standings={}
seedings={}
for id in singles:
    params2={
      "eventId": id, "page": 1, "perPage": 8
    }

    response = requests.post(url, headers=headers, json={'query': get_standings_seed, 'variables': params2})
    print(response)
    standing_seeding = response.json
    print(standing_seeding)
    # for event in standing_seeding['data']['event']['standings']:
    #   print(event)

# Récup le seed et la perf de chaque jouer des évents singles des miss'tech des 30 derniers jours

# getPerformance = """
# """

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



# response = requests.post(url, headers=headers, json={'query': getPerfomance, 'variables': variables_perf})
# performance = response.json()

# response = requests.post(url, headers=headers, json={'query': getCharacterUsage, 'variables': variables_char})
# character_usage = response.json()

# response = requests.post(url, headers=headers, json={'query': getUpsets, 'variables': variables_upsets})
# upsets = response.json()

