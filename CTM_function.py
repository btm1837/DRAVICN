!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 15:04:24 2018

@author: benmarus88
"""

#Cell Transmission Model

## Inputs
# M - Manufacturer set of vehicles classes
# nim_t# - number in, cell ocupancy in cell i of car types m at time t# 0 or 1
# ni_t# - number in, cell ocupancy in cell i of all car types at time t# 0 or 1
# uif - speed free - free flow speed of cell i
# Ni - big number, max number of vehicles in cell i
# lm - vehicle length
# del_tm - reaction time for vehicle type m
# I - total number of cells
# t - current time period

##Variables Created
# wi_t - backwards wave speed of cell i at time t
# Qi_t - maximum flow through cell i at time t
# yim_t# - vehicles moving from cell i-1 into cell i of class m
# yi_t# - vehicles moving from cell i-1 to cell i of all classes

def CellTransmissionModel(M,nim_t0,ni_t0,uif,Ni,lm,del_tm,I,t):
    #Creating Empty Lists to hold variables
    wi_t=[]
    Qi_t=[]
    yim_t1=[]
    yi_t1=[]
    nim_t1=[]
    ni_t1=[]
    for i in range(I):
        #Calculate Backwards Wave Speed
        wi_t[i]=sum((lm*del_tm[:])/(nim_t0[i,:]/ni_t0[i]))
        #Calculate maximum flow through cell i
        Qi_t[i]=uif[i]*(1/(uif[i]*sum((nim_t0[i,:]/ni_t0[i])*del_tm[:]+lm)))
        for m in range(M):
            #calculate vehicles from cell i-1 moving into cell i of class m
            yim_t1[i,m] = min([nim_t0[i-1,m],(nim_t0[i-1,m]/ni_t0[i-1])*Qi_t[i],
                              (nim_t0[i-1,m]/ni_t0[i-1])*(wi_t[i]/uif[i])*(Ni[i]-sum(nim_t0[i,:]))])
        #Calculate the vehicles from cell i-1 moving into cell i
        yi_t1[i]=sum(yim_t1[i,:])
    for i in range(I):
        for m in range(M):
            #number of vehilces in cell i at next time t+1 of class m
            nim_t1[i,m] = nim_t0[i,m] + yim_t1[i,m] - yim_t1[i+1,t]
        #number of vehicles in cell i at next time t+1
        ni_t1[i] = sum(nim_t1[i,:])
    return(yi_t1,nim_t1)

