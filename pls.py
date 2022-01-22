import random
import numpy as np

def get_y(infos, x):
    return [sum([infos["value"][v][i] for i in x]) for v in range(len(infos["value"]))]

def dominer(score_x, score_y):
    return all([score_x[k] <= score_y[k] for k in range(len(score_x))])

def read_file(filename,nb_objectif = 2):
    with open(filename, 'r') as f:
        content = [[c for c in l.split(' ') if c not in ["\t", "\n"]] for l in f.readlines()]

    infos = {"n": None, "W": None, "weight": [],"value": [[] for _ in range(nb_objectif) ]}
    for ligne in content:
        if ligne[0] == 'i':
            infos["weight"].append(int(ligne[1]))

            for k in range(nb_objectif):
                infos["value"][k].append(int(ligne[k+2]))

        elif ligne[0] == 'n':
            infos["n"] = int(ligne[1])
        elif ligne[0] == 'W':
            infos["W"] = int(ligne[1])

    return infos

#initialiser une solution
def init_p(infos):
    p, W = [], 0
    index_objects = list(filter(lambda i: infos["weight"][i] <= infos['W'], range(infos["n"])))

    while W <= infos['W'] and len(index_objects) > 0:
        new_index_obj = random.choice(index_objects)
        index_objects.remove(new_index_obj)

        p.append(new_index_obj)
        W += infos["weight"][new_index_obj]

        index_objects = list(filter(lambda i: infos["weight"][i] <= infos['W'], index_objects))

    return [p]

#fonction voisinage
def voisinage( current, infos):
    objet_dehor = set(range(infos["n"])) - set(current) # The other pickable objects
    W = sum([infos["weight"][i] for i in current]) # The total weight of the current solution

    voisins = []

    for obj_index in current:
        objet_liber = set(filter(lambda i: infos["weight"][i] <= infos["W"] - W + infos["weight"][obj_index], objet_dehor))
        for obj in objet_liber:
            copy_objet_liber = objet_liber.copy()
            copy_objet_liber.remove(obj)

            chosen_index_others = [obj]
            new_W =  W - infos["weight"][obj_index] + infos["weight"][obj]

            copy_objet_liber = set(filter(lambda i: infos["weight"][i] <= infos['W'] - new_W, copy_objet_liber))

            voisins.append(([obj_index], chosen_index_others))

            while new_W <= infos['W'] and len(copy_objet_liber) > 0:
                new_index_other = random.choice(list(copy_objet_liber))
                copy_objet_liber.remove(new_index_other)

                chosen_index_others.append(new_index_other)
                new_W += infos["weight"][new_index_other]

                copy_objet_liber = set(filter(lambda i: infos["weight"][i] <= infos['W'] - new_W, copy_objet_liber))
    print('Trouver voisins:',len(voisins))
    return voisins

def get_voisins( current_index, voisin):
    ens_solu = current_index[:] + voisin[1]
    for v in voisin[0]:
        ens_solu.remove(v)

    return ens_solu

#fonction mise a jour
def MSJ(infos, ens, x):
    if sum(infos["weight"][i] for i in x) > infos["W"]:
        return False

    score_x, liste_remove = get_y(infos, x), []
    for y in ens:
        score_y = get_y(infos, y)
        if dominer(score_y, score_x):
            liste_remove.append(y)
        elif dominer(score_x, score_y):
            return False

    for y in liste_remove:
        ens.remove(y)
    ens.append(x)
    return True

def PLS(file = "2KP100-TA-0.dat",nb_objectif = 2):
    infos = read_file(file.format(0),nb_objectif)
    Xe = init_p(infos)
    ens_p = Xe[:]

    ens_aux = []
    ens_deja = [ens_p]

    while len(ens_p) != 0:
        for p in ens_p:
            current_y = get_y(infos, p)

            voisins = voisinage(p, infos)
            for voisin in voisins:
                new_p = get_voisins(p, voisin)

                new_y = get_y(infos, new_p)
                if not dominer(new_y, current_y):
                    if MSJ(infos, Xe, new_p):
                        MSJ( infos, ens_aux, new_p)
            p_solu = set(p)
            if p_solu not in ens_deja:
                ens_deja.append(p_solu)

        ens_p = [p for p in ens_aux if set(p) not in ens_deja]
        ens_aux = []

    return Xe

def compare(infos,solu1,solu2,w = None,model = None):
    if get_v_total(infos,solu1,w,model) >= get_v_total(infos,solu2,w,model):
        return solu1
    return solu2

def MMR(infos, solus):
    if len(solus) == 1:
        return None
    if len(solus) == 1:
        return solus[0]
    ens_values = np.array([get_y(infos,x) for x in solus])
    ens_max = [max(line) for line in ens_values.T]
    mmr = [max(line) for line in (ens_max - ens_values)]
    copy = mmr.copy()
    min1 = mmr.index(min(copy))
    copy.remove(min(copy))
    min2 = mmr.index(min(copy))
    # print(mmr)
    return min1,min2

def get_v_total(infos,solu,w = None,model = None):
    if model is None:
        v = get_y(infos, solu)
        return sum(v)
    elif model == 'ponderee':
        v = get_y(infos, solu)
        return np.sum(v * np.array(w))
    elif model == 'OWA':
        v = get_y(infos,solu)
        v.sort()
        return np.sum(v * np.array(w))

def procedure1(infos,pareto_index,w,model):
    old_res,res = MMR(infos, pareto_index)
    old_solu = pareto_index.pop(old_res)
    solu = pareto_index.pop(res)
    res = compare(infos,old_solu,solu,w,model)
    while res != old_res and len(pareto_index) > 0:
        old_res = res
        res,_ = MMR(infos,pareto_index)
        solu = pareto_index.pop(res)
        res = compare(infos,old_solu,solu,w,model)
    return res



if __name__ == "__main__":
    nb_objectif = 2
    file = "2KP50-TA-0.dat"
    pareto_index = PLS(file,nb_objectif = nb_objectif)
    print(len(pareto_index)," solutions")
    w = (0.2,0.8)
    # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    infos = read_file(file,nb_objectif)
    for s in pareto_index:
        # print(s)
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'ponderee'))
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
        pass
    print("Solu_Initi:",get_v_total(infos,init_p(infos)[0],w = w,model = 'ponderee'))
    res = procedure1(infos,pareto_index,w = w,model = 'ponderee')
    print("Procedure1:",get_v_total(infos,res,w = w,model = 'ponderee'))


    pareto_index = PLS_EI(w,'ponderee',file,nb_objectif = nb_objectif)
    print("Procedure2:",get_v_total(infos,pareto_index,w = w,model = 'ponderee'))