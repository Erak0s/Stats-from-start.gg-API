def seed_round(seed):
    tier=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025]
    if(seed>1024):
        print("Seeding too high")
        return()
    for i in range (len(tier)-1):
        if seed < tier[i+1]:
            print("seed: ",seed, " tier: ",tier[i])
            return(tier[i])

def spr(seed,perf):
    tier=[1,2,3,4,5,7,9,13,17,25,33,49,65,97,129,193,257,385,513,769,1025]
    if (seed not in tier) or (perf not in tier):
        print("Erreur dans le seed ou le placement")
    else:
        for i in range (len(tier)):
            if seed == tier[i]:
                seed_r = i
            if perf == tier[i]:
                perf_r = i
    print("SPR: ",seed_r-perf_r)