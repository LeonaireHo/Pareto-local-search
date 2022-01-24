from pls_es import *
if __name__ == "__main__":
    nb_objectif = 6
    file = "2KP50-TA-0.dat"
    nb_objet = 20
    pareto_index = PLS(file,nb_objectif = nb_objectif,nb_objet = nb_objet)
    print(len(pareto_index)," solutions")
    w = [0.2,0.3,0.5]
    # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    infos = read_file(file,nb_objectif,nb_objet)
    # print(infos["value"])
    res_values = []
    for s in pareto_index:
        # print("Solu:",s)
        res_values.append(get_y(infos,s))
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
        pass
    print("w",infos['W'])
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


    # nb_objectif = 6
    # file = "2KP200-TA-0.dat"
    # w = np.random.random(nb_objectif)
    # w = w / w.sum()
    # nb_objet = 20
    # # model = "ponderee"
    # infos = read_file(file, nb_objectif,nb_objet)
    #
    # model = "OWA"
    # # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    # Xe,nb_q,hist_solu,nb_voisinage,t= Procedure_Mix(w, model,file,nb_objectif,nb_objet)
    # print(get_v_total(infos,Xe,w,model))
    # pareto_index = PLS(file, nb_objectif=nb_objectif, nb_objet=nb_objet)
    # print(len(pareto_index), " solutions")
    # values = []
    # for s in pareto_index:
    #     # print(s)
    #     # print(get_v_total(infos,s,w = (0.2,0.8),model = 'ponderee'))
    #     # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
    #     values.append(get_y(infos,s))
    #     pass
    # print("Solu_random_Pondere:", get_v_total(infos, init_p(infos)[0], w=w, model=model),\
    #       " avec poids:",get_v_total(infos, init_p(infos)[0], w=w, model='poids'),'/',infos['W'])
    #
    # res,_,nb_q,_,hist = Procedure_PoseQues(np.array(values), w,model)
    # print(res,nb_q)
    # print("Solu_ES:", sum(res*w))#," avec poids:",get_v_total(infos, pareto_index[res], w=w, model='poids'),'/',infos['W'])
