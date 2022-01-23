import numpy as np
import random
import gurobipy as gp
from gurobipy import GRB
#initialiser une solution
def init_p(infos):
    p, W = [], 0
    index_objects = list(range(infos["n"]))
    while len(index_objects) > 0:
        new_index_obj = random.choice(index_objects)
        index_objects.remove(new_index_obj)
        W += infos["weight"][new_index_obj]
        if W <= infos['W']:
            p.append(new_index_obj)
        else:
            W += -infos["weight"][new_index_obj]
    return [p]

#get values d’agrégation
def get_y(infos, x):
    return [sum([infos["value"][v][i] for i in x]) for v in range(len(infos["value"]))]

#si x domine y
def dominer(score_x, score_y):
    return all([score_x[k] <= score_y[k] for k in range(len(score_x))])

def read_file(filename,nb_objectif = 2,nb_objet = 100):
    with open(filename, 'r') as f:
        content = [[c for c in l.split(' ') if c not in ["\t", "\n"]] for l in f.readlines()]
    nb = nb_objet
    infos = {"n": None, "W": None, "weight": [],"value": [[] for _ in range(nb_objectif) ]}
    for ligne in content:
        if ligne[0] == 'i':
            if nb <= 0:
                continue
            nb += -1
            infos["weight"].append(int(ligne[1]))

            for k in range(nb_objectif):
                infos["value"][k].append(int(ligne[k+2]))
        elif ligne[0] == 'n':
            infos["n"] = int(ligne[1])
        # elif ligne[0] == 'W':
        #     infos["W"] = int(ligne[1])
    infos["n"] = nb_objet
    infos["W"] = sum(infos["weight"]) // nb_objectif
    return infos

def get_owa(v,w):
    v.sort()
    return np.sum(v * np.array(w))

def get_v_total(infos,solu,w = None,model = None):
    if model is None:
        v = get_y(infos, solu)
        return sum(v)
    elif model == 'ponderee':
        v = get_y(infos, solu)
        return np.sum(v * np.array(w))
    elif model == 'OWA':
        v = get_y(infos,solu)
        return get_owa(v,w)
    elif model == 'poids':
        poids = infos["weight"]
        return sum(poids[i] for i in solu)

def PMR(x, y, prefs, f_type):
    # print("x",x,y)
    n = len(x)

    model = gp.Model("MMR")
    model.Params.LogToConsole = 0
    #creation des variables X
    X = [model.addVar(vtype=GRB.CONTINUOUS, name="X"+str(i+1)) for i in range(n)]
    model.update()
    #contraint non null
    for i in range(n):
        model.addConstr(X[i] >= 0)

    if f_type == "OWA":
        x.sort()
        y.sort()
        for i in range(n - 1):
            model.addConstr(X[i] >= X[i + 1])

        model.addConstr(np.sum(X) == 1)

        for a,b in prefs:
            sa = np.sort(a)
            sb = np.sort(b)
            model.addConstr(np.sum([np.sum(X[i]) * sa[i] for i in range(n)]) >= np.sum([np.sum(X[i]) * sb[i] for i in range(n)]))
    elif f_type == "ponderee":
        model.addConstr(np.sum(X) == 1)
    #l'objectif
    obj = gp.LinExpr()
    obj += np.sum([ X[i] * y[i] for i in range(n)]) - np.sum( [X[i] * x[i] for i in range(n)])

    model.setObjective(obj,GRB.MAXIMIZE)
    model.optimize()
    # print(obj)
    return obj.getValue()

def MR(x, values, prefs,model):
    nb_solution = values.shape[0]
    max_value = float('-inf')
    max_index = -1
    for y_index in range(nb_solution):
        if y_index != x:
            value = PMR(values[x], values[y_index], prefs, model)
            if value > max_value:
                max_value = value
                max_index = y_index
    return max_index, max_value

def MMR(values, prefs, model):
    nb_solution = values.shape[0]
    min_value = float('inf')
    min_x_index = -1
    min_y_index = -1

    for x_index in range(nb_solution):
        y_index, y_value = MR(x_index, values, prefs,model)
        if y_value < min_value:
            min_value = y_value
            min_x_index = x_index
            min_y_index = y_index

    return min_x_index, min_y_index, round(min_value,2)

