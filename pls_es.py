from pls import *
from tools import *
#utiliserez la recherche locale de Pareto (PLS) ,
#et plus une méthode d’aide à la décision par élicitation incrémentale des poids des critères
def Procedure_PoseQues(w,model,file = "2KP100-TA-0.dat",nb_objectif = 2):
    pass

#la procédure d’élicitation pour simuler les réponses du décideur
def Procedure_ES(values, unknownWeights,model):
    if values.shape[0] == 1:
        return 0, 0
    prefs = []
    old_solu = None
    nb_ques = 0

    while True:
        x, y, value = MMR(values, prefs, model)
        print(f"Valeur du regret minimax: {value}")
        if value <= 0:
            return x, nb_ques

        elif x == -1 or y == -1:
            return old_solu, nb_ques

        solutions = [values[x], values[y]]
        solu = np.array([get_owa(solutions[0], unknownWeights), get_owa(solutions[1], unknownWeights)]).argmax()
        if not solu:#solu = 0
            old_solu = 1
            np.delete(values, y)
            notSelected = 1
        else:
            old_solu = 0
            np.delete(values, x)
            notSelected = 0
        nb_ques += 1
        #Tout les ensemble de poids tel que f(rez[solu]) > f(rez[notSelected])
        prefs.append((solutions[solu], solutions[notSelected]) )