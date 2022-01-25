from pls_es import *
from outil_pl_opt import *
if __name__ == "__main__":
    # nb_objectif = 6
    # file = "2KP50-TA-0.dat"
    # nb_objet = 20
    # pareto_index = PLS(file,nb_objectif = nb_objectif,nb_objet = nb_objet)
    # print(len(pareto_index)," solutions")
    # w = [0.2,0.3,0.5]
    # # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    # infos = read_file(file,nb_objectif,nb_objet)
    # # print(infos["value"])
    # res_values = []
    # for s in pareto_index:
    #     # print("Solu:",s)
    #     res_values.append(get_y(infos,s))
    #     # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
    #     pass
    # print("w",infos['W'])
    # print("Solu_Initi:",get_v_total(infos,init_p(infos)[0],w = w,model = 'ponderee'))
    # res = procedure1(infos,pareto_index,w = w,model = 'OWA')
    # print("Procedure1:",get_v_total(infos,res,w = w,model = 'OWA'))
    #
    # #
    # res = procedure12(infos,pareto_index,w = w,model = 'OWA')
    # print("Procedure12:",get_v_total(infos,res,w = w,model = 'OWA'))
    #
    #
    # pareto_index = PLS_EI(w,'ponderee',file,nb_objectif = nb_objectif)
    # print("Procedure2:",get_v_total(infos,pareto_index,w = w,model = 'ponderee'))
    nb_objectif = 3
    file = "2KP200-TA-0.dat"
    w = np.random.random(nb_objectif)
    w = w / w.sum()
    nb_objet = 20
    # model = "ponderee"
    infos = read_file(file, nb_objectif,nb_objet)

    res_gurobi, temp = PL_SP(infos, w)
    res_gurobi_OWA, temp = PL_OWA(infos, w)
    print("*****\nResultat de Gurobi:",res_gurobi,res_gurobi_OWA)
    # print(w)

    model = "ponderee"
    t_start = time.time()
    pareto_index = PLS(file, nb_objectif=nb_objectif, nb_objet=nb_objet)
    print("*****\nPLS a trouve",len(pareto_index), " solutions")
    # print(pareto_index[0])
    values = [get_y(infos,s) for s in pareto_index]
    _,res,nb_q,_,hist = Procedure_PoseQues(np.array(values), w,model)
    value = sum(res*w)
    erreur = round((1 - value/res_gurobi),4)*100
    print("*****\nProcedure1 avec somme ponderee:\nValue:",round(value,2),"(erreur:"+erreur.__str__()+"%)","en",round(time.time() - t_start,2),"secondes,pose",nb_q,"questions")

    model = "OWA"
    values = [get_y(infos, s) for s in pareto_index]
    res,_, nb_q, _, hist = Procedure_PoseQues(np.array(values), w, model)
    res_v = values[res]
    res_v.sort(reverse=True)
    value = sum(res_v * w)
    erreur = round(abs(1 - value/res_gurobi_OWA),4)*100
    print("*****\nProcedure1 avec OWA:\nValue:", round(value,2),"(erreur:"+erreur.__str__()+"%)", "en", round(time.time() - t_start,2), "secondes,pose",
          nb_q, "questions")

    model = "ponderee"
    Xe, nb_q, hist_solu, nb_voisinage, t = Procedure_Mix(w, model, file, nb_objectif, nb_objet)
    value = get_v_total(infos,Xe,w,model)
    erreur = round(abs(1 - value/res_gurobi),4)*100
    print("*****\nProcedure2 avec somme ponderee:\nValue:",round(value,2),"(erreur:"+erreur.__str__()+"%)", "en", round(t,2), "secondes,pose",
          nb_q, "questions")

    model = "OWA"
    Xe, nb_q, hist_solu, nb_voisinage, t = Procedure_Mix(w, model, file, nb_objectif, nb_objet)
    value = get_v_total(infos, Xe, w, model)
    erreur = round(abs(1 - value/res_gurobi_OWA),4)*100
    print("*****\nProcedure2 avec OWA:\nValue:", round(value,2),"(erreur:"+erreur.__str__()+"%)", "en", round(t),"secondes,pose",
          nb_q, "questions")

    model = "ponderee"
    Xe, nb_q, hist_solu, nb_voisinage, t = Procedure_Mix2(w, model, file, nb_objectif, nb_objet)
    value = get_v_total(infos, Xe, w, model)
    erreur = round(abs(1 - value/res_gurobi_OWA),4)*100
    print("*****\nRBLS avec ponderee:\nValue:", round(value,2),"(erreur:"+erreur.__str__()+"%)", "en", round(t),"secondes,pose",
          nb_q, "questions")