import requests
from queries import *
from datetime import *

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
                    # print(event['id'])
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
    print()

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
              ", SPR ",min_SPR,")", sep=''
              )
    print()

# Calcule la somme du SPR pour chaque joueur sur les évènements donnés
def get_sum_spr(events,params,url,headers):
    sum_spr_dict={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        seeding = get_seeding(event_id,params,url,headers)
        for key in (standings):
            SPR = SPR_player(key[0], event_id, seeding, standings)
            if split_noms(key[0])[1] not in sum_spr_dict:
                sum_spr_dict[split_noms(key[0])[1]]=SPR
            else:
                sum_spr_dict[split_noms(key[0])[1]]+=SPR
    return(sum_spr_dict)

# Affiche la liste et le nombre des joueurs ayant fait au moins n évènements parmis ceux donnés
def taille_commu(n,events,params,url,headers):
    players_list={}
    commu=0
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in (standings):
            if split_noms(player[0])[1] not in players_list:
                players_list[split_noms(player[0])[1]]=1
            else:
                players_list[split_noms(player[0])[1]]+=1
    for player in players_list:
        if players_list[player]>=n:
            commu+=1
    print("Liste des joueurs:")
    print(players_list)
    print()
    print("Nombre de joueurs distincts:",commu)
    print()

# Retourne le nombre de tournois effectués par chaque joueur sur la période
def count_tournois(events,params,url,headers):
    nb_tournois={}
    for event_id in (events):
        standings = get_standings(event_id,params,url,headers)
        for player in (standings):
            if split_noms(player[0])[1] not in nb_tournois:
                nb_tournois[split_noms(player[0])[1]]=1
            else:
                nb_tournois[split_noms(player[0])[1]]+=1
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
                if split_noms(player[0][0])[1] in nb_top_x:
                    nb_top_x[split_noms(player[0][0])[1]]+=1
                else:
                    nb_top_x[split_noms(player[0][0])[1]]=1
    return(nb_top_x)

# Affiche les n joueurs ayant fait le plus de top x
def max_top_x(n,x,events,params,url,headers):
    top_x = count_top_x(x,events,params,url,headers)
    print("Les",n,"joueurs ayant fait le plus de top",x,":")
    max_dico(n,top_x)
    print()

# Affiche les joueurs ayant fait au moins n tournois avec une somme du SPR la plus proche de 0 sur les évènements donnés
def most_regu(n,events,params,url,headers):
    max_ecart_spr=100
    sum_spr_dict=get_sum_spr(events,params,url,headers)
    nb_tournois=count_tournois(events,params,url,headers)
    for key in sum_spr_dict.items():
        if nb_tournois[key[0]]>=n:
            if abs(key[1])<max_ecart_spr:
                max_ecart_spr=abs(key[1])
                most_regu=[key[0]]
            else:
                if abs(key[1])==max_ecart_spr:
                    most_regu.append(key[0])
    print("Joueur(s) le plus régulier:","(somme du SPR sur ces évènements:",max_ecart_spr,")")
    for i in most_regu:
        print(i)   
    print()

# Affiche les joueurs avec une somme du SPR la plus éloignée de 0 sur les évènements donnés
def least_regu(n,events,params,url,headers):
    min_ecart_spr=-1
    sum_spr_dict=get_sum_spr(events,params,url,headers)
    nb_tournois=count_tournois(events,params,url,headers)
    for key in sum_spr_dict.items():
        if nb_tournois[key[0]]>=n:
            if abs(key[1])>min_ecart_spr:
                min_ecart_spr=key[1]
                least_regu=[key]
            else:
                if abs(key[1])==abs(min_ecart_spr):
                    least_regu.append(key)
    # print("least_regu:",least_regu)
    # print("sum_spr_dict",sum_spr_dict)
    # nb_tourn=count_tournois(events,params,url,headers)
    # print("nb_tournois", nb_tourn)
    print("Joueur(s) le moins régulier:")
    # print(least_regu)
    for joueur in least_regu:
        print(joueur[0]," (somme du SPR: ",joueur[1],")", sep="")        
        # /nb_tourn[joueur[0]]
    print()

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
    print(nb_games)
    return(nb_games)

# Calcule le setcount entre les joueurs donnés dans les évènements donnés
def get_setcount_players(playerA,playerB,events,params,url,headers):
    setcount={playerA:0,playerB:0}
    for event_id in (events):
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_sets_nogames, 'variables': params})
        request = response.json()
        for i in request['data']['event']['sets']['nodes']:
            winner=i['winnerId']
            if (((split_noms(i['slots'][0]['entrant']['name'])[1]==playerA) or (split_noms(i['slots'][0]['entrant']['name'])[1]==playerB)) and ((split_noms(i['slots'][1]['entrant']['name'])[1]==playerA) or (split_noms(i['slots'][1]['entrant']['name'])[1]==playerB))) :
                if (i['slots'][0]['entrant']['id']==winner):
                    setcount[split_noms(i['slots'][0]['entrant']['name'])[1]]+=1
                elif (i['slots'][1]['entrant']['id']==winner):
                    setcount[split_noms(i['slots'][1]['entrant']['name'])[1]]+=1
    print(playerA,setcount[playerA],"-",setcount[playerB],playerB)
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
            if ((teamA in i['slots'][0]['entrant']['name']) and (teamB in i['slots'][1]['entrant']['name'])):
                if i['slots'][0]['entrant']['id']==winner:
                    setcount[teamA]+=1
                else:
                    setcount[teamB]+=1
            elif ((teamB in i['slots'][0]['entrant']['name']) and (teamA in i['slots'][1]['entrant']['name'])):
                if i['slots'][0]['entrant']['id']==winner:
                    setcount[teamB]+=1
                else:
                    setcount[teamA]+=1
    print(teamA,setcount[teamA],"-",setcount[teamB],teamB)
    print()

# Compte le nombre d'utilisations de chaque personnage
def get_character_usage(events,params,url,headers):
    character_usage={}
    for event_id in events:
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_characters, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            if (node['games']!=None):
                for game in node['games']:
                    for selection in game['selections']:
                        if selection['character']['name'] not in character_usage:
                            character_usage[selection['character']['name']]=1
                        else:
                            character_usage[selection['character']['name']]+=1
    return(character_usage)

# Calcule le tauxx d'utilisation de chaque personnage sur les évènements donnés
def get_character_usage_rate(events,params,url,headers):
    character_usage_rate={}
    nb_games=count_games(events,params,url,headers)
    for event_id in events:
        params["eventId"] = str(event_id)
        response = requests.post(url, headers=headers, json={'query': get_characters, 'variables': params})
        request = response.json()
        for node in request['data']['event']['sets']['nodes']:
            if (node['games']!=None):
                for game in node['games']:
                    for selection in game['selections']:
                        if selection['character']['name'] not in character_usage_rate:
                            character_usage_rate[selection['character']['name']]=1
                        else:
                            character_usage_rate[selection['character']['name']]+=1
    for i in character_usage_rate:
        character_usage_rate[i]=(character_usage_rate[i]/(2*nb_games))*100
    return(character_usage_rate)

# Affiche les n personnages les plus utilisés (nombre d'utilisations)
def max_character_usage(n,events,params,url,headers):
    character_usage=get_character_usage(events,params,url,headers)
    print("Les",n,"personnages les plus joués:")
    max_dico(n,character_usage)
    print()

# Affiche les n personnages les moins utilisés (mais pick au moins une fois) (nombre d'utilisations)
def min_character_usage(n,events,params,url,headers):
    character_usage=get_character_usage(events,params,url,headers)
    print("Les",n,"personnages les moins joués:")
    min_dico(n,character_usage)
    print()

# Affiche les n personnages les plus utilisés (taux d'utilisation)
def max_character_usage_rate(n,events,params,url,headers):
    character_usage_rate=get_character_usage_rate(events,params,url,headers)
    print("Les",n,"personnages les plus joués:")
    max_dico(n,character_usage_rate)
    print()

# Affiche les n personnages les moins utilisés (mais pick au moins une fois) (taux d'utilisation)
def min_character_usage_rate(n,events,params,url,headers):
    character_usage_rate=get_character_usage_rate(events,params,url,headers)
    print("Les",n,"personnages les moins joués:")
    min_dico(n,character_usage_rate)
    print()

# Renvoie la liste des upsets dans les évènements donnés     
def get_upsets(events,params,url,headers):
    upsets=[]
    seeding={}
    for event_id in events:
        dict_seeding=get_seeding(event_id, params, url, headers)
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
                upsets.append([winner_name,loser_name,spr(seeding[winner_name],seeding[loser_name]),event_id])
    return(upsets)

# Compte les upsets dans les évènements donnés
def count_upsets(events,params,url,headers,silent):
    upsets=get_upsets(events,params,url,headers)
    if silent is not True:
        print("Nombre d'upsets:",len(upsets))
        print()
    return(len(upsets))

# Renvoie le/les plus gros upsets dans les évènements donnés
def biggest_upset(events,params,url,headers):
    UF_max=0
    upsets=get_upsets(events,params,url,headers)
    for upset in upsets:
        if upset[2]>UF_max:
            biggest_upset=[]
            biggest_upset.append(upset)
            UF_max=upset[2]
        elif upset[2]==UF_max:
            biggest_upset.append(upset)
    for upset in biggest_upset:
        print(upset[0]," upset ",upset[1],", UF +",upset[2]," à l'évènement ",events[upset[3]],sep="")
        print()

# Renvoie le nombre moyen d'upset par tournois
def count_upsets_par_tournois(events,params,url,headers):
    nb_upset=count_upsets(events,params,url,headers,True)
    nb_tournois=len(events)
    print(nb_upset/nb_tournois)
    print()

# Récupère le nombre d'upsets réalisés par chaque joueur
def get_upsets_realises(events,params,url,headers):
    nb_upsets={}
    seeding={}
    for event_id in events:
        dict_seeding=get_seeding(event_id, params, url, headers)
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
                if split_noms(winner_name)[1] in nb_upsets:
                    nb_upsets[split_noms(winner_name)[1]]+=1
                else:
                    nb_upsets[split_noms(winner_name)[1]]=1
    # nb_tournois=count_tournois(events,params,url,headers)
    # for player in nb_upsets:
    #     nb_upsets[player]=((nb_upsets[player]/nb_tournois[player])*100)
    return(nb_upsets)

# Récupère le nombre d'upsets subis par chaque joueur
def get_upsets_subis(events,params,url,headers):
    nb_upsets={}
    seeding={}
    for event_id in events:
        dict_seeding=get_seeding(event_id, params, url, headers)
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
                if split_noms(loser_name)[1] in nb_upsets:
                    nb_upsets[split_noms(loser_name)[1]]+=1
                else:
                    nb_upsets[split_noms(loser_name)[1]]=1
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
                    if (split_noms(entrant['entrant']['name'])[1]) not in nb_defaite:
                        nb_defaite[split_noms(entrant['entrant']['name'])[1]]=1
                    else:
                        nb_defaite[split_noms(entrant['entrant']['name'])[1]]+=1
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
    if "|" in nom:
        return(nom.split("| "))
    else:
        return["",nom]
