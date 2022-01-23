#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 15:20:38 2022

@author: yangzhuangzhuang
"""

import gurobipy as gr
import numpy as np
import time
#instance= read_file("2KP30-TA-6.dat")
def PL_SP(instance, w, verbose=False, M=1000000):
    t_start = time.time()
    N = len(instance['value'])
    item_count=instance['n']
    model = gr.Model("sacadoc")
    if not verbose:
        model.Params.LogToConsole = 0
    X = [model.addVar(vtype=gr.GRB.BINARY, name="objet"+str(i+1)) for i in range(item_count)]
    total_poids = 0
    for i in range(instance['n']):
        total_poids += X[i] * instance['weight'][i]
    model.addConstr(total_poids <= instance['W'])
    # for j in range(N):
    #     model.setObjectiveN(gr.quicksum(instance['value'][j][i]X[i] for i in range(item_count)), index=j, weight=w[j], name=str(j))
    # model.ModelSense = gr.GRB.MAXIMIZE
    obj = gr.LinExpr()
    for k in range(N):
        parti = gr.LinExpr()
        for i in range(item_count):
            parti+=instance['value'][k][i]*X[i]
        obj+=w[k]*parti
    model.setObjective(obj,gr.GRB.MAXIMIZE)
    model.update()
    model.optimize()
    return model.objVal,time.time() - t_start

def PL_OWA(instance, w, verbose=False, M=1000000):
    t_start = time.time()
    N = len(instance['value'])
    model = gr.Model("sacadoc")
    if not verbose:
        model.Params.LogToConsole = 0
    o = [model.addVar(vtype=gr.GRB.BINARY, name="objet"+str(i+1)) for i in range(instance['n'])]
    #model.update()
    total_poids = 0
    for i in range(instance['n']):
        total_poids += o[i] * instance['weight'][i]
    model.addConstr(total_poids <= instance['W'])
    x = []
    for i in range(N):
        value = 0
        for oi in range(instance['n']):
            value += o[oi] * instance['value'][i][oi]
        x.append(value)
    y = [model.addVar(vtype=gr.GRB.CONTINUOUS, name="y"+str(i+1)) for k in range(N)]
    b = []
    for k in range(N):
        b_tmp = []
        for i in range(N):
            b_tmp.append(model.addVar(vtype=gr.GRB.BINARY, name="b"+str(k+1)+"_"+str(i+1)))
        b.append(b_tmp)
    for k in range(N):
        for i in range(N):
            model.addConstr(x[k] - y[i] <= b[k][i])
    for k in range(N):
        model.addConstr( np.sum(b[k]) <= k )
    obj = gr.LinExpr()
    for k in range(N):
        obj += w[k]*x[k]
    model.setObjective(obj,gr.GRB.MAXIMIZE)
    model.update()
    model.optimize()

    return obj.getValue(),time.time() - t_start