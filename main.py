from pls_es import *
if __name__ == "__main__":
    # nb_objectif = 3
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
    # # pareto_index = PLS_EI(w,'ponderee',file,nb_objectif = nb_objectif)
    # # print("Procedure2:",get_v_total(infos,pareto_index,w = w,model = 'ponderee'))

    nb_objectif = 3
    file = "2KP50-TA-0.dat"
    w = (0.2, 0.3,0.5)
    nb_objet = 20
    # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    infos = read_file(file, nb_objectif,nb_objet)
    print("Solu_random:", get_v_total(infos, init_p(infos)[0], w=w, model='ponderee'))
    pareto_index = PLS(file, nb_objectif=nb_objectif, nb_objet=nb_objet)
    print(len(pareto_index), " solutions")
    for s in pareto_index:
        # print(s)
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'ponderee'))
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
        pass
    res,nb_q = Procedure_ES(infos, pareto_index, w,PMROWA)
    print(res,nb_q)
    # pareto_index,hist = procedure1(infos, pareto_index, w, 'ponderee')
    # for i in hist:
    #     print("Procedure2:", get_v_total(infos, i, w=w, model='ponderee'))