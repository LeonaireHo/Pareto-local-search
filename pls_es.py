import pls.py
# une procedure ou elicitation incrementale et recherchelocale sont combinees
def PLS_EI(w,model,file = "2KP100-TA-0.dat",nb_objectif = 2):
    infos = read_file(file.format(0),nb_objectif)
    res = init_p(infos)[0]
    while 0:
        voisins = voisinage(p, infos)
        if len(voisins) == 0:
            return res
        voisins.append(res)
        mieux_voisin,_ = MMR(infos,voisins)
        if compare(infos,res,mieux_voisin,w,model) == res:
            return res
        res = mieux_voisin
    return res