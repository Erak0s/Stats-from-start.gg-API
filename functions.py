import requests
from queries import *
from datetime import *
import pandas as pd

# Affiche les tournois dans lesquels sont les évènements analysés
def print_tournaments(events):
    print(len(events),"évènements analysés:")
    for event in events.items():
        # print(event[0])
        print(events[event[0]])
    print()

# Renvoie une date à partir du jour, mois et année donnés
def get_date(jour,mois,annee):
    return(int(datetime(annee,mois,jour).timestamp()))

# Affiche les n couples clé,valeur ayant la valeur la plus élevée 
def max_dico(n,dico):
    dico_trie=dict(sorted(dico.items(), key=lambda item: item[1], reverse=True))
    # print(dico_trie)
    j=0
    k=0
    for i in dico_trie:
        if j<n:
            k+=1
            print(k,") ",i,": ",dico_trie[i],sep="")
            j+=1
    print()

# Affiche les n couples clé,valeur ayant la valeur la plus faible 
def min_dico(n,dico):
    dico_trie=dict(sorted(dico.items(), key=lambda item: item[1]))
    # print(dico_trie)
    j=0
    k=0
    for i in dico_trie:
        if j<n:
            k+=1
            print(k,") ",i,": ",dico_trie[i],sep="")
            j+=1
    print()

# Vérifie si le nom de l'évènement donné correspond à un évènement de Simple (True par défaut)
def is_singles(Name):
    name = Name.lower()
    goodlist=["single","singles","1v1"]
    banlist=["double","doubles","squad strike","amateur","ladder","attente","2v2","redemption","spectateur","bin'goat"]
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
    # print("Paramètres:",params)
    response = requests.post(url, headers=headers, json={'query': get_event_standings, 'variables': params})
    request = response.json()
    standings={}
    for i in request['data']['event']['standings']['nodes']:
        standings[i['entrant']['name'],event_id] = i['placement']
    # print(standings, len(standings))
    return(standings)

# Récupère la liste des seedings de l'event donné dans la requête donnée
def get_seeding(event_id,url,headers):
    params = {"eventId": str(event_id), "perPage": 500, "page": 1}
    response = requests.post(url, headers=headers, json={'query': get_event_seeding, 'variables': params})
    request = response.json()
    seedings={}
    for j in request['data']['event']['phases'][0]['seeds']['nodes']:
        seedings[j['entrant']['name'],event_id] = j['seedNum']
    return(seedings)

# Récupère le nombre d'entrants du tournoi donné
def get_nb_entrants(event_id,params,url,headers):
    params["eventId"] = str(event_id)
    # print("Paramètres:",params)
    response = requests.post(url, headers=headers, json={'query': get_event_nb_entrants, 'variables': params})
    request = response.json()
    return(request['data']['event']['numEntrants'])

# Renvoie un dictionnaire des tableaux des résultats
def get_results(events,params,url,headers):
    results={}
    for event_id in (events):
        df = pd.DataFrame(columns=["Placement", "Player", "Seeding", "SPR"])        
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,url,headers)
        nb_entrants = get_nb_entrants(event_id, params, url, headers)
        for i in range (1,nb_entrants+1):
            for k, v in standings.items():
                if v ==i:
                    df.loc[len(df.index)]= [v, k[0], seeding[k], spr(seeding[k],v)]
        
        results[singles[event_id]] = df
    return(results)

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

# Calcule les n meilleure performance (en terme de SPR) sur les évènements donnés
def best_performances(n,events,params,url,headers):
    standings_dict={}
    seeding_dict={}
    perfs=[]
    for event_id in (events):
        standings_dict[event_id] = get_standings(event_id,params,url,headers)
        seeding_dict[event_id] = get_seeding(event_id,url,headers)
        for key in (standings_dict[event_id]):
            SPR = SPR_player(key[0], event_id, seeding_dict[event_id], standings_dict[event_id])
            perfs.append([key[0],standings_dict[event_id][key],seeding_dict[event_id][key],SPR,event_id])
    sorted_perfs=sorted(perfs, key=lambda x: x[3], reverse=True)
    best_perfs=sorted_perfs[:n]
    print("Meilleure(s) performance(s): ")            
    for i in range (len(best_perfs)):
        print(best_perfs[i][0]," à l'évènement ",events[best_perfs[i][4]],
              " (Seed " ,best_perfs[i][2],", placement ",best_perfs[i][1],
              ", SPR +",best_perfs[i][3],")", sep=''
              )
    print()

def get_dq_list(event_id, url, headers):
    dq_list=[]
    result = None
    parametres = {"perPage": 50, "eventId": str(event_id)}
    pages = requests.post(url, headers=headers, json={'query': get_sets_pages, 'variables': parametres}).json()['data']['event']['sets']['pageInfo']['totalPages']
    for i in range(1,pages+1):
        parametres["page"]=i
        request = requests.post(url, headers=headers, json={'query': get_sets_dq, 'variables': parametres}).json()
        if result == None:
            result = request
        else:
            result['data']['event']['sets']['nodes']+=(request['data']['event']['sets']['nodes'])

    data = result['data']['event']['sets']['nodes']

    for set in data:
        if set["displayScore"]=="DQ":
            winner_id = set['winnerId']
            for player in set["slots"]:
                if (player["entrant"]["id"]!=winner_id and player["entrant"]["name"].split("| ")[-1] not in dq_list):
                    dq_list.append(player["entrant"]["name"].split("| ")[-1])
    return(dq_list)    

# Calcule la/les pire performance (en terme de SPR) sur les évènements donnés
def worst_performances(n,events,params,url,headers):
    standings_dict={}
    seeding_dict={}
    perfs=[]
    k=0 
    i=0
    for event_id in (events):
        dq_list = get_dq_list(event_id, url, headers)
        standings_dict[event_id] = get_standings(event_id,params,url,headers)
        seeding_dict[event_id] = get_seeding(event_id,url,headers)

        for key in (standings_dict[event_id]):
            if key[0].split("| ")[-1] not in dq_list:
                SPR = SPR_player(key[0], event_id, seeding_dict[event_id], standings_dict[event_id])
                perfs.append([key[0],standings_dict[event_id][key],seeding_dict[event_id][key],SPR,event_id])
    worst_perfs=sorted(perfs, key=lambda x: x[3], reverse=False)

    result = None
    parametres = {"perPage": 50, "eventId": str(event_id)}
    pages = requests.post(url, headers=headers, json={'query': get_sets_pages, 'variables': parametres}).json()['data']['event']['sets']['pageInfo']['totalPages']
    for i in range(1,pages+1):
        parametres["page"]=i
        request = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': parametres}).json()
        if result == None:
            result = request
        else:
            result['data']['event']['sets']['nodes']+=(request['data']['event']['sets']['nodes'])

    print("Pire(s) performance(s): ")          
    for i in range (min(n, len(worst_perfs))):
        print(worst_perfs[i][0]," à l'évènement ",events[worst_perfs[i][4]],
            " (Seed " ,worst_perfs[i][2],", placement ",worst_perfs[i][1],
            ", SPR ",worst_perfs[i][3],")", sep=''
            )
    print()

# Calcule la somme du SPR pour chaque joueur sur les évènements donnés
def get_sum_spr(events,params,url,headers):
    sum_spr_dict={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if split_noms(key[0])[-1] not in sum_spr_dict:
                sum_spr_dict[split_noms(key[0])[-1]]=SPR
            else:
                sum_spr_dict[split_noms(key[0])[-1]]+=SPR
    return(sum_spr_dict)

def get_sum_abs_spr(events,params,url,headers):
    sum_spr_dict={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if split_noms(key[0])[-1] not in sum_spr_dict:
                sum_spr_dict[split_noms(key[0])[-1]]=abs(SPR)
            else:
                sum_spr_dict[split_noms(key[0])[-1]]+=abs(SPR)
    return(sum_spr_dict)

# Affiche la liste et le nombre des joueurs ayant fait au moins n évènements parmis ceux donnés
def taille_commu(n,events,params,url,headers):
    players_list={}
    commu=0
    total=0
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in (standings):
            if split_noms(player[0])[-1] not in players_list:
                players_list[split_noms(player[0])[-1]]=1
            else:
                players_list[split_noms(player[0])[-1]]+=1
    for player in players_list:
        total+=1
        if players_list[player]>=n:
            commu+=1
    print("Liste des joueurs:")
    print(players_list)
    print()
    print("Nombre de joueurs distincts:",total)
    print("Nombre de joueurs ayant fait plus de",n,"tournois:",commu)
    print()

# Retourne le nombre de tournois effectués par chaque joueur sur la période
def count_tournois(events,params,url,headers):
    nb_tournois={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in (standings):
            if split_noms(player[0])[-1] not in nb_tournois:
                nb_tournois[split_noms(player[0])[-1]]=1
            else:
                nb_tournois[split_noms(player[0])[-1]]+=1
    return(nb_tournois)

# Retourne le ou les joueurs ayant participé au plus de tournois sur les évènements donnés
def max_tournois(n,events,params,url,headers):
    nb_tourn = count_tournois(events,params,url,headers)
    print("Les",n,"joueurs ayant fait le plus de tournois:")
    max_dico(n,nb_tourn)
    print()

# Compte le nombre de placements dans le top x pour chaque participant dans les évènements donnés
def count_top_x(x,events,params,url,headers):
    nb_top_x={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in standings.items():
            if player[1]<=x:
                if split_noms(player[0][0])[-1] in nb_top_x:
                    nb_top_x[split_noms(player[0][0])[-1]]+=1
                else:
                    nb_top_x[split_noms(player[0][0])[-1]]=1
    return(nb_top_x)

# Affiche les n joueurs ayant fait le plus de top x
def max_top_x(n,x,events,params,url,headers):
    top_x = count_top_x(x,events,params,url,headers)
    print("Les",n,"joueurs ayant fait le plus de top",x,":")
    max_dico(n,top_x)
    print()

# Affiche les joueurs ayant fait au moins n tournois avec une somme du SPR la plus proche de 0 sur les évènements donnés
def most_regu(n,events,params,url,headers):
    sum_spr_dict=get_sum_abs_spr(events,params,url,headers)
    nb_tournois=count_tournois(events,params,url,headers)
    true_dict={}
    for key in sum_spr_dict:
        if nb_tournois[key]>=nb_tourn:
            true_dict[key]=sum_spr_dict[key]
    min_dico(n, true_dict)
    print()

# Affiche les n joueurs avec une somme du SPR la plus éloignée de 0 sur les évènements donnés, ayant fait au moins nb_tournois tournois.
def least_regu(n,nb_tourn,events,params,url,headers):
    sum_spr_dict=get_sum_abs_spr(events,params,url,headers)
    nb_tournois=count_tournois(events,params,url,headers)
    true_dict={}
    for key in sum_spr_dict:
        if nb_tournois[key]>=nb_tourn:
            true_dict[key]=(sum_spr_dict[key]/nb_tournois[key])
    max_dico(n, true_dict)
    min_dico(n, true_dict)
    print()

def surseed_sousseed(n,nb_tourn,events,params,url,headers):
    sum_spr_dict=get_sum_spr(events,params,url,headers)
    nb_tournois=count_tournois(events,params,url,headers)
    true_dict={}
    for key in sum_spr_dict:
        if nb_tournois[key]>=nb_tourn:
            true_dict[key]=(sum_spr_dict[key]/nb_tournois[key])
    print("Les plus sous-seed:")
    max_dico(n, true_dict)
    print()
    print("Les plus sur-seed:")
    min_dico(n, true_dict)
    print()

# Affiche les n premiers seeds des évènements donnés
def top_seed(n,events,params,url,headers):
    for event_id in (events):
        print("Top",n,"seeds in",events[event_id],":")
        seeding = get_seeding(event_id,url,headers)
        for i in range (1,n+1):
            for k, v in seeding.items():
                if v ==i:
                    print(v,": ",k[0], sep="")
        print()

# Affiche les n premiers joueurs des évènements donnés
def top_standings(n,events,params,url,headers):
    for event_id in (events):
        print("Top",n,"of",events[event_id],":")
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,url,headers)
        for i in range (1,n+1):
            for k, v in standings.items():
                if v ==i:
                    # print(seeding)
                    # print(k[0])
                    print(v,": ",k[0]," (seed ",seeding[k],", SPR ",spr(seeding[k],v),")", sep="")
        print()

# Renvoie un dictionnaire des tableaux des résultats
def get_results(events,params,url,headers):
    results={}
    for event_id in (events):

        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,url,headers)
        entrants = get_entrants(event_id, params, url, headers)
        for i in range (1,entrants+1):
            for k, v in standings.items():
                if v ==i:
                    # print(seeding)
                    # print(k[0])
                    print(v,": ",k[0]," (seed ",seeding[k],", SPR ",spr(seeding[k],v),")", sep="")
        print()

# Compte les sets dans les évènements donnés
def count_sets(events,params,url,headers):
    nb_sets=0
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nb, 'variables': params})
        request = response.json()
        nb_sets += request['data']['event']['sets']['pageInfo']['total']
    print("Nombre total de sets joués:",nb_sets)
    print()

# Compte le nombre de games dans les évènements donnés
def count_games(events,params,url,headers):
    nb_games=0
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_no_char, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            if (node['games']!=None):
                nb_games+=len(node['games'])
    print("Nombre total de games jouées:",nb_games)
    print()

# Calcule le setcount entre les joueurs donnés dans les évènements donnés
def get_setcount_players(playerA,playerB,events,params,url,headers):
    setcount={playerA:0,playerB:0}
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for i in request['data']['event']['sets']['nodes']:
            winner=i['winnerId']
            if (((split_noms(i['slots'][0]['entrant']['name'])[-1]==playerA) or (split_noms(i['slots'][0]['entrant']['name'])[-1]==playerB)) and ((split_noms(i['slots'][1]['entrant']['name'])[-1]==playerA) or (split_noms(i['slots'][1]['entrant']['name'])[-1]==playerB))) :
                if (i['slots'][0]['entrant']['id']==winner):
                    setcount[split_noms(i['slots'][0]['entrant']['name'])[-1]]+=1
                elif (i['slots'][1]['entrant']['id']==winner):
                    setcount[split_noms(i['slots'][1]['entrant']['name'])[-1]]+=1
    print(playerA,setcount[playerA],"-",setcount[playerB],playerB)
    print()

# récupère les n affrontements les plus fréquents sur les évènements donnés
def affrontements_freq(n,events,params,url,headers):
    h2h={}
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for i in request['data']['event']['sets']['nodes']:
            A=split_noms(i['slots'][0]['entrant']['name'])[-1]
            B=split_noms(i['slots'][1]['entrant']['name'])[-1]
            if (A,B) in h2h:
                h2h[A,B]+=1
            elif (B,A) in h2h:
                h2h[B,A]+=1
            else:
                h2h[A,B]=1
    max_dico(n,h2h)
    return(h2h)

# calcule les setcounts les plus one-sided sur les évènements donnés
def bracket_demon(top,min_h2h,events,params,url,headers):
    setcounts={}
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for i in request['data']['event']['sets']['nodes']:
            winner=i['winnerId']
            A_name=split_noms(i['slots'][0]['entrant']['name'])[-1]
            B_name=split_noms(i['slots'][1]['entrant']['name'])[-1]
            A_id=i['slots'][0]['entrant']['id']
            B_id=i['slots'][1]['entrant']['id']
            if (A_name,B_name) in setcounts:
                if winner==A_id:
                    setcounts[A_name,B_name][0]+=1
                else:
                    setcounts[A_name,B_name][1]+=1
            elif (B_name,A_name) in setcounts:
                if winner==A_id:
                    setcounts[B_name,A_name][1]+=1
                else:
                    setcounts[B_name,A_name][0]+=1
            else:
                if winner==A_id:
                    setcounts[A_name,B_name]=[1,0]
                elif winner==B_id:
                    setcounts[A_name,B_name]=[0,1]
    ordered_setcounts={}
    for i in setcounts:
        if setcounts[i][1]>setcounts[i][0]:
            ordered_setcounts[(i[1],i[0])]=[setcounts[i][1],setcounts[i][0]]
        else:
            ordered_setcounts[i]=setcounts[i]
    winrate={}
    for i in ordered_setcounts:
        winrate[i]=(ordered_setcounts[i][0]/(ordered_setcounts[i][0]+ordered_setcounts[i][1]))
    h2h={}
    for i in ordered_setcounts:
        h2h[i]=ordered_setcounts[i][0]+ordered_setcounts[i][1]
        
    winrate_trie=sorted(winrate.items(), key=lambda x: h2h[x[0]], reverse=True)
    winrate_trie=dict(sorted(winrate_trie, key=lambda x: x[1], reverse=True))

    j=0
    k=0
    for i in winrate_trie:
        if j<top and ordered_setcounts[i][0]+ordered_setcounts[i][1]>=min_h2h:
            k+=1
            print(k,") ",i[0]," sur ",i[1],": ",winrate_trie[i]*100,"% de winrate, nombre de sets:",ordered_setcounts[i][0]+ordered_setcounts[i][1],", setcount:",ordered_setcounts[i][0],"-",ordered_setcounts[i][1],sep="")
            j+=1
    print()

# Calcule le setcount entre les teams données dans les évènements donnés
def get_setcount_prefix(teamA,teamB,events,params,url,headers):
    setcount={teamA:0,teamB:0}
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for i in request['data']['event']['sets']['nodes']:
            winner=i['winnerId']
            if ((teamA in split_noms(i['slots'][0]['entrant']['name'])[0]) and (teamB in split_noms(i['slots'][1]['entrant']['name'])[0])):
                # print(i['slots'][0]['entrant']['name'])
                # print(i['slots'][1]['entrant']['name'])
                if i['slots'][0]['entrant']['id']==winner:
                    setcount[teamA]+=1
                else:
                    setcount[teamB]+=1
            elif ((teamB in split_noms(i['slots'][0]['entrant']['name'])[0]) and (teamA in split_noms(i['slots'][1]['entrant']['name'])[0])):
                # print(i['slots'][0]['entrant']['name'])
                # print(i['slots'][1]['entrant']['name'])
                if i['slots'][0]['entrant']['id']==winner:
                    setcount[teamB]+=1
                else:
                    setcount[teamA]+=1
    print(teamA,setcount[teamA],"-",setcount[teamB],teamB)
    print()

# Compte le nombre d'utilisations de chaque personnage
def get_character_usage(events,url,headers):
    character_usage={}
    nb_games = 0
    for event_id in events:
        result = None
        parametres = {"perPage": 20, "eventId": str(event_id)}
        pages = requests.post(url, headers=headers, json={'query': get_sets_pages, 'variables': parametres}).json()['data']['event']['sets']['pageInfo']['totalPages']
        for i in range(1,pages+1):
            parametres["page"]=i
            request = requests.post(url, headers=headers, json={'query': get_characters, 'variables': parametres}).json()
            if result == None:
                result = request
            else:
                result['data']['event']['sets']['nodes']+=(request['data']['event']['sets']['nodes'])
        for node in result['data']['event']['sets']['nodes']:
            if (node['games']!=None):
                for game in node['games']:
                    winnerId = game["winnerId"]
                    if game['selections']!=None:
                        nb_games+=1
                        for selection in game['selections']:
                            if selection['character']['name'] not in character_usage:
                                character_usage[selection['character']['name']]=[1,0,0,0]
                            else:
                                character_usage[selection['character']['name']][0]+=1
                            if selection['entrant']['id'] == winnerId:
                                character_usage[selection['character']['name']][2]+=1
    for character in character_usage.keys():
        character_usage[character][1]=(character_usage[character][0]/(2*nb_games))
        character_usage[character][3]=(character_usage[character][2]/character_usage[character][0])

    df = pd.DataFrame.from_dict(character_usage, orient="index", columns=["Games","Usage rate","Wins","Winrate"])
    df.loc['Total']= df.sum()

    print(f"{nb_games} games played")
    
    return(df)

# Renvoie la liste des upsets dans les évènements donnés     
def get_upsets(events,url,headers):
    upsets=[]
    seeding={}
    for event_id in events:
        result = None
        parametres = {"perPage": 50, "eventId": str(event_id)}
        dict_seeding=get_seeding(event_id, url, headers)
        for i in dict_seeding:
            seeding[i[0]]=dict_seeding[i]

        pages = requests.post(url, headers=headers, json={'query': get_sets_pages, 'variables': parametres}).json()['data']['event']['sets']['pageInfo']['totalPages']
        for i in range(1,pages+1):
            parametres["page"]=i
            request = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': parametres}).json()
            if result == None:
                result = request
            else:
                result['data']['event']['sets']['nodes']+=(request['data']['event']['sets']['nodes'])

        for node in result['data']['event']['sets']['nodes']:
            winner_id=node['winnerId']
            if node['displayScore']!='DQ':
                for entrant in node['slots']:
                    if winner_id!=None:
                        if(entrant['entrant']['id'])==winner_id:
                            winner_name=entrant['entrant']['name']
                        else:
                            loser_name=entrant['entrant']['name']
                    else:
                        print("Winner non-renseigné pour le match:", event_id, "set:", node)
                if winner_id!=None:
                    if seed_round(seeding[(winner_name)])>seed_round(seeding[(loser_name)]):
                        upsets.append([winner_name,loser_name,spr(seeding[winner_name],seeding[loser_name]),event_id])
    return(upsets)

# Compte les upsets dans les évènements donnés
def count_upsets(events,params,url,headers,silent):
    upsets=get_upsets(events,url,headers)
    if silent is not True:
        print("Nombre d'upsets:",len(upsets))
        print()
    return(len(upsets))

# Renvoie les n plus gros upsets dans les évènements donnés
def biggest_upsets(n,events,url,headers):
    upsets=get_upsets(events,url,headers)
    sorted_upsets = sorted(upsets, key=lambda x: x[2], reverse=True)
    biggest_upsets = sorted_upsets[:n]
    for upset in biggest_upsets:
        print(upset[0]," upset ",upset[1],", UF +",upset[2]," à l'évènement ",events[upset[3]],sep="")
    print()


# Récupère le nombre d'upsets réalisés par chaque joueur
def get_upsets_realises(events,params,url,headers):
    nb_upsets={}
    seeding={}
    for event_id in events:
        dict_seeding=get_seeding(event_id, url, headers)
        for i in dict_seeding:
            seeding[i[0]]=dict_seeding[i]
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            winner_id=node['winnerId']
            for entrant in node['slots']:
                if(entrant['entrant']['id'])==winner_id:
                    winner_name=entrant['entrant']['name']
                else:
                    loser_name=entrant['entrant']['name']
            if seed_round(seeding[(winner_name)])>seed_round(seeding[(loser_name)]):
                if split_noms(winner_name)[-1] in nb_upsets:
                    nb_upsets[split_noms(winner_name)[-1]]+=1
                else:
                    nb_upsets[split_noms(winner_name)[-1]]=1
    # nb_tournois=count_tournois(events,params,url,headers)
    # for player in nb_upsets:
    #     nb_upsets[player]=((nb_upsets[player]/nb_tournois[player])*100)
    return(nb_upsets)

# Récupère le nombre d'upsets subis par chaque joueur
def get_upsets_subis(events,params,url,headers):
    nb_upsets={}
    seeding={}
    for event_id in events:
        dict_seeding=get_seeding(event_id, url, headers)
        seeding={}
        for i in dict_seeding:
            seeding[i[0]]=dict_seeding[i]
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            winner_id=node['winnerId']
            for entrant in node['slots']:
                if(entrant['entrant']['id'])==winner_id:
                    winner_name=entrant['entrant']['name']
                else:
                    loser_name=entrant['entrant']['name']
            if seed_round(seeding[(winner_name)])>seed_round(seeding[(loser_name)]):
                if split_noms(loser_name)[-1] in nb_upsets:
                    nb_upsets[split_noms(loser_name)[-1]]+=1
                else:
                    nb_upsets[split_noms(loser_name)[-1]]=1
    return(nb_upsets)

# Récupère le nombre de défaite par joueur
def get_defaites(events,params,url,headers):
    nb_defaite={}
    for event_id in events:
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_players, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            winner_id=node['winnerId']
            for entrant in node['slots']:
                # print(entrant)
                if(entrant['entrant']['id'])!=winner_id:
                    if (split_noms(entrant['entrant']['name'])[-1]) not in nb_defaite:
                        nb_defaite[split_noms(entrant['entrant']['name'])[-1]]=1
                    else:
                        nb_defaite[split_noms(entrant['entrant']['name'])[-1]]+=1
    return(nb_defaite)

# Affiche les n joueurs ayant le plus réalisé d'uppsets
def max_upsets_realises(n,events,params,url,headers):
    upsets_realises=get_upsets_realises(events,params,url,headers)
    print("Les",n,"joueurs ayant réalisé le plus d'upsets:")
    max_dico(n,upsets_realises)
    print()

# Affiche les n joueurs ayant le plus subis d'upsets par défaite
def max_upsets_subis(n,events,params,url,headers):
    upsets_subis=get_upsets_subis(events,params,url,headers)
    print("Les",n,"joueurs ayant subis le plus d'upsets:")
    max_dico(n,upsets_subis)
    print()

# Affiche les n joueurs ayant le plus subis d'upsets par défaite
def max_upsets_subis_par_defaite(n,events,params,url,headers):
    upsets_subis=get_upsets_subis(events,params,url,headers)
    defaites=get_defaites(events,params,url,headers)
    upsets_par_defaite={}
    for player in upsets_subis:
        print("upsets subis par",player,":",upsets_subis[player])
        print("Nb défaites:",defaites[player])
        upsets_par_defaite[player]=(upsets_subis[player]/defaites[player])
    print("Les",n,"joueurs ayant subis le plus d'upsets par défaite:")
    max_dico(n,upsets_par_defaite)
    print()

# Affiche les n joueurs ayant le moins subis d'uppsets
def min_upsets_subis(n,events,params,url,headers):
    upsets_subis=get_upsets_subis(events,params,url,headers)
    print("Les",n,"joueurs ayant subis le moins d'upsets:")
    min_dico(n,upsets_subis)
    print()

def split_noms(nom):
    if "| " in nom:
        return(nom.split(" | "))
    else:
        return["",nom]
    
def get_player_placement(player,events,params,url,headers):
    placements={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for nplayer in standings.items():
            if split_noms(nplayer[0][0])[-1] == player:
                placements[event_id]=nplayer[1]
    return(placements)

# Compte le nombre d'utilisations de chaque personnage
def player_most_characters(events,url,headers):
    players_character={}
    nb_characters_per_player={}
    players_per_character={}
    nb_players_per_character={}
    for event_id in events:
        result = None
        parametres = {"perPage": 20, "eventId": str(event_id)}
        pages = requests.post(url, headers=headers, json={'query': get_sets_pages, 'variables': parametres}).json()['data']['event']['sets']['pageInfo']['totalPages']
        for i in range(1,pages+1):
            parametres["page"]=i
            request = requests.post(url, headers=headers, json={'query': get_characters, 'variables': parametres}).json()
            if result == None:
                result = request
            else:
                result['data']['event']['sets']['nodes']+=(request['data']['event']['sets']['nodes'])

        for node in result['data']['event']['sets']['nodes']:
            if (node['games']!=None):
                for game in node['games']:
                    if game['selections']!=None:
                        for selection in game['selections']:
                            if selection['entrant']['name'].split("| ")[-1] not in players_character:
                                players_character[selection['entrant']['name'].split("| ")[-1]] = []
                            if selection['character']['name'] not in players_character[selection['entrant']['name'].split("| ")[-1]]:
                                players_character[selection['entrant']['name'].split("| ")[-1]].append(selection['character']['name'])

    for player in players_character.keys():
        nb_characters_per_player[player] = len(players_character[player])
    #     for charac in players_character[player]:
    #         if charac not in players_per_character:
    #             players_per_character[charac]=[]
    #         players_per_character[charac].append(player)
    # for charac in players_per_character:
    #     nb_players_per_character[charac]=len(players_per_character[charac])

    print(players_character)

    dico_trie=dict(sorted(nb_characters_per_player.items(), key=lambda item: item[1], reverse=True))

    return(dico_trie)