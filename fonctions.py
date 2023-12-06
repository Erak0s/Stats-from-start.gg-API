import requests
from queries import *

def get_singles_id(events):
    event_ids={}
    for tournament in events['data']['tournaments']['nodes']:
        for event in tournament['events']:
            if ("Single" in event['name']) or ("single" in event['name']) or ("Singles" in event['name']) or ("singles" in event['name']) or (("Double" not in event['name']) and ("Squad Strike" not in event['name']) and ("Amateur" not in event['name']) and ("Ladder" not in event['name'])):
                event_ids[event['id']] = tournament['name']
    return(event_ids)

# Récupère la liste des placement de l'event donné dans la requête donnée
def get_standings(event_id,params,url,headers):
    params["eventId"] = str(event_id)
    response = requests.post(url, headers=headers, json={'query': get_event_standings, 'variables': params})
    request = response.json()
    standings={}
    for i in request['data']['event']['standings']['nodes']:
        standings[i['entrant']['name'],event_id] = i['placement']
    return(standings)

# Récupère la liste des seedings de l'event donné dans la requête donnée
def get_seeding(event_id,params,url,headers):
    params["eventId"] = str(event_id)
    response = requests.post(url, headers=headers, json={'query': get_event_seeding, 'variables': params})
    request = response.json()
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

# Calcule la/les meilleure performance (en terme de SPR) sur les év_è
def best_performance(events,params,url,headers):
    max_SPR=-100
    print("Event(s) checked:")
    for k,v in events.items():
        print(events[k])
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,params,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if SPR > max_SPR:
                max_SPR = SPR
                best_perf = [key[0]]
                event = [event_id]
            else:
                if SPR == max_SPR:
                    best_perf.append(key[0])
                    event.append(event_id)
    print("Meilleure performance: ")            
    for i in range (len(best_perf)):
        print(best_perf[i]," à l'évènement ",events[event[i]]," (SPR +",max_SPR,")", sep='')

def worst_performance(events,params,url,headers):
    min_SPR=100
    print("Event(s) checked:")
    for k,v in events.items():
        print(events[k])
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,params,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if SPR < min_SPR:
                min_SPR = SPR
                worst_perf = [key[0]]
                event = [event_id]
            else:
                if SPR == min_SPR:
                    worst_perf.append(key[0])
                    event.append(event_id)
    print("Pire(s) performance(s):")
    for i in range (len(worst_perf)):
        print(worst_perf[i]," à l'évènement ",events[event[i]]," (SPR ",min_SPR,")", sep='')

def top_seed(n,events,params,url,headers):
    for event_id in (events):
        print("Top",n,"seeds in",events[event_id],":")
        seeding = get_seeding(event_id,params,url,headers)
        for i in range (1,n+1):
            for k, v in seeding.items():
                if v ==i:
                    print(v,": ",k[0], sep="")
        print()