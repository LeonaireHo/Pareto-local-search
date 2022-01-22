from tools import *

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
    # print('Trouver voisins:',len(voisins))
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

