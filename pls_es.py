from pls import *
from tools import *

# une procedure ou elicitation incrementale et recherchelocale sont combinees
def PLS_EI(w,model,file = "2KP100-TA-0.dat",nb_objectif = 2):
    infos = read_file(file.format(0), nb_objectif)

    res = init_p(infos)[0]
    while 0:
        voisins = voisinage(res, infos)
        if len(voisins) == 0:
            return res
        voisins.append(res)
        mieux_voisin,_ = MMR(infos,voisins)
        if choisir_par_decideur(infos,res,mieux_voisin,w,model) == res:
            return res
        res = mieux_voisin
    return res

#utiliserez la recherche locale de Pareto (PLS) ,
#et plus une méthode d’aide à la décision par élicitation incrémentale des poids des critères
def procedure1(infos,pareto_index,w,model):
    hist = []
    old_res,res = MMR(infos, pareto_index)
    res1 = pareto_index.pop(old_res)
    if res is not None:
        if res > old_res:
            res += -1
        solu = pareto_index.pop(res)
        res1 = choisir_par_decideur(infos,res1,solu,w,model)
    hist.append(res1)
    while len(pareto_index) > 1:#and res != old_res:
        res,res2 = MMR(infos,pareto_index)
        solu1 = pareto_index.pop(res)
        solu2 = pareto_index.pop(res2)
        # print(solu)
        res = choisir_par_decideur(infos,solu1,solu2,w,model)
        pareto_index.append(res)
        hist.append(res)
    return res,hist

def procedure12(infos,pareto_index,w,model):
    res_values = []
    for s in pareto_index:
        # print("Solu:",s)
        res_values.append(get_y(infos,s))

    old_res,res = MMR2(np.array(res_values),w)
    # print(pareto_index)
    old_solu = pareto_index.pop(old_res)
    if res > old_res:
        res += -1
    solu = pareto_index.pop(res)
    res = choisir_par_decideur(infos,old_solu,solu,w,model)
    while res != old_res and len(pareto_index) > 0:
        res_values = []
        for s in pareto_index:
            # print("Solu:",s)
            res_values.append(get_y(infos, s))
        old_res = res
        res,_ = MMR2(np.array(res_values),w)
        solu = pareto_index.pop(res)
        res = choisir_par_decideur(infos,old_solu,solu,w,model)
    return res

#la procédure d’élicitation pour simuler les réponses du décideur
def Procedure_ES(infos,pareto_index, unknownWeights,model):
    front = []
    for s in pareto_index:
        # print("Solu:",s)
        front.append(get_y(infos,s))
    front = np.array(front)
    if front.shape[0] == 1:
        return 0, 0
    prefs = []
    oldSelected = None
    questionCount = 0

    while True:
        x, y, value = MMR2(front, prefs,model)
        print(f"Valeur du regret minimax: {value}")
        if value <= 0:
            return x, questionCount

        elif x == -1 or y == -1:
            return oldSelected, questionCount

        solutions = [front[x], front[y]]

        print(f"0: {solutions[0]} (Solution n°{x})")
        print(f"1: {solutions[1]} (Solution n°{y})")

        values = np.array([get_owa(solutions[0], unknownWeights), get_owa(solutions[1], unknownWeights)])
        selected = values.argmax()
        oldSelected = (selected + 1) % 2
        print(f"{selected} selected (Solution n°{oldSelected}).")
        questionCount += 1
        notSelected = 1 - selected
        #Tout les ensemble de poids tel que f(rez[selected]) > f(rez[notSelected])
        prefs.append( (solutions[selected], solutions[notSelected]) )