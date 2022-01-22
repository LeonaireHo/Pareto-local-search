from pls_es import *
if __name__ == "__main__":
    nb_objectif = 2
    file = "2KP50-TA-0.dat"
    pareto_index = PLS(file,nb_objectif = nb_objectif)
    print(len(pareto_index)," solutions")
    w = (0.2,0.8)
    # w = [0.2,0.1,0.2,0.3,0.15,0.05]
    infos = read_file(file,nb_objectif)
    for s in pareto_index:
        # print(s)
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'ponderee'))
        # print(get_v_total(infos,s,w = (0.2,0.8),model = 'OWA'))
        pass
    print("Solu_Initi:",get_v_total(infos,init_p(infos)[0],w = w,model = 'ponderee'))
    res = procedure1(infos,pareto_index,w = w,model = 'ponderee')
    print("Procedure1:",get_v_total(infos,res,w = w,model = 'ponderee'))


    pareto_index = PLS_EI(w,'ponderee',file,nb_objectif = nb_objectif)
    print("Procedure2:",get_v_total(infos,pareto_index,w = w,model = 'ponderee'))