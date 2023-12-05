import requests
from queries import *

def get_singles_id(events):
    event_ids={}
    for tournament in events['data']['tournaments']['nodes']:
        for event in tournament['events']:
            if ("Single" in event['name']) or ("single" in event['name']) or ("Singles" in event['name']) or ("singles" in event['name']) or (("Double" not in event['name']) and ("Squad Strike" not in event['name']) and ("Amateur" not in event['name']) and ("Ladder" not in event['name'])):
                event_ids[event['id']] = tournament['name']
    return(event_ids)

def get_seeding_standings(event_id,params,url,headers):
  params["eventId"] = str(event_id)
  response = requests.post(url, headers=headers, json={'query': get_standings_seed, 'variables': params})
  standing_seeding = response.json()
  standings = get_standings(standing_seeding, event_id)
  seedings = get_seedings(standing_seeding, event_id)
  return(standings,seedings)

# Récupère la liste des placement de l'event donné dans la requête donnée
def get_standings(request,event_id):
    standings={}
    for i in request['data']['event']['standings']['nodes']:
        standings[i['entrant']['name'],event_id] = i['placement']
    return(standings)

# Récupère la liste des seedings de l'event donné dans la requête donnée
def get_seedings(request,event_id):
    seedings={}
    for j in request['data']['event']['phases'][0]['seeds']['nodes']:
        seedings[j['entrant']['name'],event_id] = j['seedNum']
    return(seedings)

# Pour un seeding donné en entrée, la fonction renvoie le "tier" de seeding (9ème, 13ème, 17ème ...)
def seed_round(seed):
    tier=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025]
    if(seed>1024):
        print("Seeding too high")
        return()
    for i in range (len(tier)-1):
        if seed < tier[i+1]:
            return(tier[i])

# Calcul du SPR (Seed Performance Rating) pour un seed et placement donné: comparaison du placement et du tier de seeding
def spr(seed,perf):
    tier=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025]
    true_seed = seed_round(seed)
    true_perf = seed_round(perf)
    if (true_seed not in tier) or (true_perf not in tier):
        print("Erreur dans le seed ou le placement")
    else:
        for i in range (len(tier)):
            if true_seed == tier[i]:
                seed_r = i
            if true_perf == tier[i]:
                perf_r = i
    return(seed_r-perf_r)

# Calcule le SPR d'un joueur à un évènement donné
def SPR_player(player,event_id,dico_seed,dico_standings):
    return(spr(dico_seed[player, event_id],dico_standings[player, event_id]))

def best_performance(events,params,url,headers):
  max_SPR=-100
  print("Event(s) checked: ",events)
  for event_id in (events):
    [standings,seedings] = get_seeding_standings(event_id,params,url,headers)
    for key in (standings):
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
    print("Meilleure performance:",best_perf[i],"à l'évènement",events[event[i]],"(SPR",max_SPR,")")