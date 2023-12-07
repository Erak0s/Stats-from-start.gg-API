import requests
from queries import *
from datetime import *

# Affiche les tournois dans lesquels sont les évènements analysés
def print_tournaments(events):
    print(len(events),"évènements analysés:")
    for event in events.items():
        print(events[event[0]])
    print()

def get_date(j,m,a):
    return(int(datetime(a,m,j).timestamp()))

# Vérifie si le nom de l'évènement donné correspond à un évènement de Simple (True par défaut)
def is_singles(Name):
    name = Name.lower()
    goodlist=["single","singles","1v1"]
    banlist=["double","doubles","squad strike","amateur","ladder","attente","2v2","redemption","spectateur"]
    for word in banlist:
        if (word in name):
            return(False)
    for word in goodlist:
        if (word in name):
            return(True)
    return(True)

# Récupère les évènements Simples parmis les évènements donnés
def get_singles_id(params,url,headers):
    event_ids={}
    if ("slug"in params):
        query=get_all_events_slug
    elif("distance" in params and "city" in params):
        query=get_all_events_location
    else:
        query=get_all_events_no_location
    
    response = requests.post(url, headers=headers, json={'query': query, 'variables': params})
    events = response.json()
    if ("slug"in params):
        for event in events['data']['tournament']['events']:
                if is_singles(event['name']):
                    event_ids[event['id']] = events['data']['tournament']['name']
    else:
        for tournament in events['data']['tournaments']['nodes']:
            for event in tournament['events']:
                if (is_singles(event['name'])):
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

# Calcule la/les meilleure performance (en terme de SPR) sur les évènements donnés
def best_performance(events,params,url,headers):
    max_SPR=-100
    standings_dict={}
    seeding_dict={}
    for event_id in (events):
        standings_dict[event_id] = get_standings(event_id,params,url,headers)
        seeding_dict[event_id] = get_seeding(event_id,params,url,headers)
        for key in (standings_dict[event_id]):
            SPR = SPR_player(key[0], event_id, seeding_dict[event_id], standings_dict[event_id])
            if SPR > max_SPR:
                max_SPR = SPR
                best_perf = [key]
                event = [event_id]
            else:
                if SPR == max_SPR:
                    best_perf.append(key)
                    event.append(event_id)
    print("Meilleure(s) performance(s): ")            
    for i in range (len(best_perf)):
        # print(best_perf[i])
        # print(event[i])
        # print(seeding_dict[event[i]][best_perf[i]])
        print(best_perf[i][0]," à l'évènement ",events[event[i]],
              " (Seed " ,seeding_dict[event[i]][best_perf[i]],", placement ",standings_dict[event[i]][best_perf[i]],
              ", SPR +",max_SPR,")", sep=''
              )

# Calcule la/les pire performance (en terme de SPR) sur les évènements donnés
def worst_performance(events,params,url,headers):
    min_SPR=100
    standings_dict={}
    seeding_dict={}
    for event_id in (events):
        standings_dict[event_id] = get_standings(event_id,params,url,headers)
        seeding_dict[event_id] = get_seeding(event_id,params,url,headers)
        for key in (standings_dict[event_id]):
            SPR = SPR_player(key[0], event_id, seeding_dict[event_id], standings_dict[event_id])
            if SPR < min_SPR:
                min_SPR = SPR
                worst_perf = [key]
                event = [event_id]
            else:
                if SPR == min_SPR:
                    worst_perf.append(key)
                    event.append(event_id)
    print("Pire(s) performance(s):")
    for i in range (len(worst_perf)):
        print(worst_perf[i][0]," à l'évènement ",events[event[i]],
              " (Seed " ,seeding_dict[event[i]][worst_perf[i]],", placement ",standings_dict[event[i]][worst_perf[i]],
              ", SPR ",min_SPR,")", sep='')

# Calcule la somme du SPR pour chaque joueur sur les évènements donnés
def get_sum_spr(events,params,url,headers):
    sum_spr_dict={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,params,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if key[0] not in sum_spr_dict:
                sum_spr_dict[key[0]]=SPR
            else:
                sum_spr_dict[key[0]]+=SPR
    return(sum_spr_dict)

# Affiche la liste et le nombre des joueurs distincts sur les évènements donnés
def get_distinct_players(events,params,url,headers):
    players_list=[]
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for key in (standings):
            if key[0] not in players_list:
                players_list.append(key[0])
    print("Liste des joueurs:")
    print(players_list)
    print()
    print("Nombre de joueurs distincts:",len(players_list))

# Retourne le nombre de tournois effectués par chaque joueur sur la période
def count_tournois(events,params,url,headers):
    nb_tournois={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in (standings):
            if player[0] not in nb_tournois:
                nb_tournois[player[0]]=1
            else:
                nb_tournois[player[0]]+=1
    return(nb_tournois)

# Retourne le ou les joueurs ayant participé au plus de tournois sur les évènements donnés
def max_tournois(n,events,params,url,headers):
    nb_tourn = count_tournois(events,params,url,headers)
    max_dico(n,nb_tourn)

# Affiche les joueurs avec une somme du SPR la plus proche de 0 sur les évènements donnés
def most_regu(events,params,url,headers):
    max_ecart_spr=100
    sum_spr_dict=get_sum_spr(events,params,url,headers)
    for key in sum_spr_dict.items():
        if abs(key[1])<max_ecart_spr:
            max_ecart_spr=abs(key[1])
            most_regu=[key[0]]
        else:
            if abs(key[1])==max_ecart_spr:
                most_regu.append(key[0])
    print("Joueur(s) le plus régulier:","(somme du SPR sur ces évènements:",max_ecart_spr,")")
    for i in most_regu:
        print(i)   

# Affiche les joueurs avec une somme du SPR la plus éloignée de 0 sur les évènements donnés
def least_regu(events,params,url,headers):
    min_ecart_spr=-1
    sum_spr_dict=get_sum_spr(events,params,url,headers)
    for key in sum_spr_dict.items():
        if abs(key[1])>abs(min_ecart_spr):
            min_ecart_spr=key[1]
            least_regu=[key]
        else:
            if abs(key[1])==abs(min_ecart_spr):
                least_regu.append(key)
    print("least_regu:",least_regu)
    print("sum_spr_dict",sum_spr_dict)
    nb_tourn=count_tournois(events,params,url,headers)
    print("nb_tournois", nb_tourn)
    print("Joueur(s) le moins régulier:")
    for joueur in least_regu:
        print(joueur[0]," (somme du SPR: ",joueur[1],")", sep="")        
        # /nb_tourn[joueur[0]]

# Affiche les n premiers seeds des évènements donnés
def top_seed(n,events,params,url,headers):
    for event_id in (events):
        print("Top",n,"seeds in",events[event_id],":")
        seeding = get_seeding(event_id,params,url,headers)
        for i in range (1,n+1):
            for k, v in seeding.items():
                if v ==i:
                    print(v,": ",k[0], sep="")
        print()

# Affiche les n premiers seeds des évènements donnés
def top_standings(n,events,params,url,headers):
    for event_id in (events):
        print("Top",n,"of",events[event_id],":")
        standings = get_standings(event_id,params,url,headers)
        for i in range (1,n+1):
            for k, v in standings.items():
                if v ==i:
                    print(v,": ",k[0], sep="")
        print()

# Compte le nombre de placements dans le top x pour chaque participant dans les évènements donnés
def count_top_x(x,events,params,url,headers):
    nb_top_x={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in standings.items():
            if player[1]<=x:
                if player[0][0] in nb_top_x:
                    nb_top_x[player[0][0]]+=1
                else:
                    nb_top_x[player[0][0]]=1
    return(nb_top_x)

# Affiche les n couples clé,valeur ayant la valeur la plus élevée 
def max_dico(n,dico):
    dico_trie=dict(sorted(dico.items(), key=lambda item: item[1], reverse=True))
    # print(dico_trie)
    j=0
    for i in dico_trie:
        if j<n:
            print(i,dico_trie[i])
            j+=1

# Affiche les n couples clé,valeur ayant la valeur la plus faible 
def min_dico(n,dico):
    dico_trie=dict(sorted(dico.items(), key=lambda item: item[1]))
    # print(dico_trie)
    j=0
    for i in dico_trie:
        if j<n:
            print(i,dico_trie[i])
            j+=1

# Affiche les n joueurs ayant fait le plus de top x
def max_top_x(n,x,events,params,url,headers):
    top_x = count_top_x(x,events,params,url,headers)
    max_dico(n,top_x)