

import Cell_Class
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

def cell_transmission_model(vehicle_total_num_types, nim_t0, number_in_time_i, free_flow_speed,
                            max_vehicles, vehicle_length, reaction_time, total_num_cells, current_time_period):
    #Creating Empty Lists to hold variables
    wi_t=[]
    Qi_t=[]
    yim_t1=[]
    yi_t1=[]
    nim_t1=[]
    ni_t1=[]
    for i in range(total_num_cells):
        #Calculate Backwards Wave Speed
        wi_t[i]=sum((vehicle_length * reaction_time[:]) / (nim_t0[i, :] / number_in_time_i[i]))
        #Calculate maximum flow through cell i
        Qi_t[i]= free_flow_speed[i] * (1 / (free_flow_speed[i] * sum((nim_t0[i, :] / number_in_time_i[i])
                                                                     * reaction_time[:] + vehicle_length)))
        for m in range(vehicle_total_num_types):
            #calculate vehicles from cell i-1 moving into cell i of class m
            yim_t0   [i,m] = min([nim_t0[i-1,m], (nim_t0[i-1,m] / number_in_time_i[i - 1]) * Qi_t[i],
                               (nim_t0[i-1,m] / number_in_time_i[i - 1]) * (wi_t[i] / free_flow_speed[i])
                               * (max_vehicles[i] - sum(nim_t0[i, :]))])
        #Calculate the vehicles from cell i-1 moving into cell i
        yi_t1[i]=sum(yim_t1[i,:])
    for i in range(total_num_cells):
        for m in range(vehicle_total_num_types):
            #number of vehilces in cell i at next time t+1 of class m
            nim_t1[i,m] = nim_t0[i,m] + yim_t0[i,m] - yim_t0[i + 1, current_time_period]
        #number of vehicles in cell i at next time t+1
        ni_t1[i] = sum(nim_t1[i,:])
    return(yi_t1,nim_t1)

def calc_backwards_wave_speed(cell,vehicle_make_dict,vehicle_length):
    backwards_wave_speed = 0
    backwards_wave_speed_sum=0
    for vehicle_type in vehicle_make_dict.keys()
        backwards_wave_speed_sum = backwards_wave_speed_sum + (
            ( cell.number_in_t_i_make_dict[vehicle_type] / cell.length)/
            (cell.number_in_t_i / cell.length)
                               )*vehicle_make_dict[vehicle_type]
    backwards_wave_speed = vehicle_length/backwards_wave_speed_sum
    return backwards_wave_speed


def calc_max_flow(cell,vehicle_make_dict,vehicle_length):
    max_flow = 0
    max_flow_sum = 0
    # summation
    for vehicle_type in vehicle_make_dict.keys():
        max_flow_sum = max_flow_sum + (
            (cell.number_in_t_i_make_dict[vehicle_type]/cell.length)/
            (cell.number_in_t_i[vehicle_type]/cell.length)
        ) * vehicle_make_dict[vehicle_type]
    max_flow_calc = (1/(cell.free_flow_speed * max_flow_sum))
    max_flow = cell.free_flow_speed * max_flow_calc
    return max_flow

def calc_vehicles_moving_cells_type():
    item1 =

def ctm_function(cell_dict,cell_iteration_dict,vehicle_make_dict,exper_vehicle_length):
    # function to use to evaluate CTM
    for start_cell in cell_iteration_dict.keys():
        for cell in cell_iteration_dict[start_cell]:

            backwards_wave_speed = calc_backwards_wave_speed(cell,vehicle_make_dict,exper_vehicle_length)
            max_flow = calc_max_flow(cell,vehicle_make_dict,exper_vehicle_length)
