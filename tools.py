import numpy as np
import random
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