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
        if compare(infos,res,mieux_voisin,w,model) == res:
            return res
        res = mieux_voisin
    return res


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