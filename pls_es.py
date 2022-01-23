from pls import *
from tools import *
#utiliserez la recherche locale de Pareto (PLS) ,
#et plus une méthode d’aide à la décision par élicitation incrémentale des poids des critères
def Procedure_Mix(w,model="ponderee",file = "2KP200-TA-0.dat",nb_objectif = 2,nb_objet = 20):
    t_start = time.time()
    infos = read_file(file.format(0),nb_objectif = nb_objectif,nb_objet=nb_objet )
    Xe = init_p(infos)[0]
    hist_solu = []
    nb_q = 0
    nb_voisinage = 0
    while True:
        nb_voisinage += 1
        ens_solution = [Xe]
        voisins = voisinage(Xe, infos)
        for voisin in voisins:
            ens_solution.append(get_voisins(Xe, voisin))
        values = []
        for s in ens_solution:
            # print(s)
            values.append(get_y(infos,s))
        if model == 'pondere':
            x,xv, nb_ques,_,hist = Procedure_PoseQues(np.array(values),w,model,5)
        else:
            x, xv, nb_ques, _, hist = Procedure_PoseQues(np.array(values), w, model)
        nb_q += nb_ques
        hist_solu.append(hist)
        if x == 0:
            return Xe,nb_q,hist_solu,nb_voisinage,time.time() - t_start
        Xe = xv
        if model == 'OWA':
            Xe = ens_solution[x]
    # print('')

#la procédure d’élicitation pour simuler les réponses du décideur
def Procedure_PoseQues(values, w,model,max_nb_pose = 100):
    if values.shape[0] == 1:
        return 0,0,0,0,0
    prefs = []
    old_solu = None
    nb_ques = 0
    hist_mmr = []
    hist_value = []
    indx_solu = -1
    i = 0
    max_nb_pose = -max_nb_pose
    while max_nb_pose <= 0:
        max_nb_pose += 1
        nb_ques+=1
        x, y, value = MMR(values, prefs, model)
        hist_mmr.append(value)
        if model == 'ponderee':
            if x == -1 or y == -1:
                return 0,old_solu, nb_ques, hist_mmr,hist_value
            old_solu = indx_solu
            solutions = [values[x], values[y]]
            solu_values = np.array([sum(solutions[0] * w), sum(solutions[1] * w)])
            solu = solu_values.argmax()
            indx_solu = x * (1 - solu) + y * solu
            non_solu = y * (1 - solu) + x * solu
            # print(solu,solu_values)
            #delete le seconde mieux
            values = np.delete(values,non_solu,axis = 0)
            if non_solu < indx_solu:
                indx_solu += -1
            if non_solu < old_solu:
                old_solu += -1

            # print(i,old_solu, indx_solu)
            i += 1
            hist_value.append(values[indx_solu])
            if old_solu == indx_solu and max_nb_pose >= 0 or len(values)<=2:
                return 0,values[indx_solu], nb_ques, hist_mmr,hist_value

        elif model == 'OWA':
            if value <= 0:
                return x,values[x], nb_ques, hist_mmr,hist_value

            elif x == -1 or y == -1:
                return old_solu,values[old_solu], nb_ques, hist_mmr,hist_value

            solutions = [values[x], values[y]]
            solu_values = np.array([get_owa(solutions[0], w), get_owa(solutions[1], w)])
            solu = solu_values.argmax()
            old_solu = x * (1 - solu) + y * solu
            solu2 = 1 - solu
            prefs.append((solutions[solu], solutions[solu2]))
            hist_value.append(solu_values[solu])
    return 0,values[indx_solu], nb_ques, hist_mmr, hist_value