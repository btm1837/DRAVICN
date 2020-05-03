

import Cell_Class
"""
Created on Wed Dec 12 15:04:24 2018

@author: benmarus88
"""
import numpy as np
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

# def cell_transmission_model(vehicle_total_num_types, nim_t0, number_in_time_i, free_flow_speed,
#                             max_vehicles, vehicle_length, reaction_time, total_num_cells, current_time_period):
#     #Creating Empty Lists to hold variables
#     wi_t=[]
#     Qi_t=[]
#     yim_t1=[]
#     yi_t1=[]
#     nim_t1=[]
#     ni_t1=[]
#     for i in range(total_num_cells):
#         #Calculate Backwards Wave Speed
#         wi_t[i]=sum((vehicle_length * reaction_time[:]) / (nim_t0[i, :] / number_in_time_i[i]))
#         #Calculate maximum flow through cell i
#         Qi_t[i]= free_flow_speed[i] * (1 / (free_flow_speed[i] * sum((nim_t0[i, :] / number_in_time_i[i])
#                                                                      * reaction_time[:] + vehicle_length)))
#         for m in range(vehicle_total_num_types):
#             #calculate vehicles from cell i-1 moving into cell i of class m
#             yim_t0   [i,m] = min([nim_t0[i-1,m], (nim_t0[i-1,m] / number_in_time_i[i - 1]) * Qi_t[i],
#                                (nim_t0[i-1,m] / number_in_time_i[i - 1]) * (wi_t[i] / free_flow_speed[i])
#                                * (max_vehicles[i] - sum(nim_t0[i, :]))])
#         #Calculate the vehicles from cell i-1 moving into cell i
#         yi_t1[i]=sum(yim_t1[i,:])
#     for i in range(total_num_cells):
#         for m in range(vehicle_total_num_types):
#             #number of vehilces in cell i at next time t+1 of class m
#             nim_t1[i,m] = nim_t0[i,m] + yim_t0[i,m] - yim_t0[i + 1, current_time_period]
#         #number of vehicles in cell i at next time t+1
#         ni_t1[i] = sum(nim_t1[i,:])
#     return(yi_t1,nim_t1)

# def calc_backwards_wave_speed(cell, vehicle_type_dict, vehicle_length):
#     backwards_wave_speed = 0
#     # is cell density defined by number in divided by max number or number in divided by length of cell?
#     #Backwards wave speed is used in the calulation of moving vehicles
#     # BWS is dependant on vehicle length and the number in as well as the
#     if cell.number_in_t_i == 0:
#         backwards_wave_speed = cell.free_flow_speed * 1000000000000
#         return backwards_wave_speed
#     backwards_wave_speed_sum=0
#     for vehicle_type in vehicle_type_dict.keys():
#         backwards_wave_speed_sum = backwards_wave_speed_sum + (
#             ( cell.number_in_t_i_make_dict[vehicle_type] / cell.max_vehicles)/
#             (cell.number_in_t_i / cell.max_vehicles)
#                                ) * vehicle_type_dict[vehicle_type]
#     # node vehicle_make_dict[vehicle_type] = reaction time
#     backwards_wave_speed = vehicle_length/backwards_wave_speed_sum
#     return backwards_wave_speed

def flow_density_bws(cell,vehicle_length,vehicle_type_dict):
    #take average reaction time
    reaction_time = np.average(list(vehicle_type_dict.values()))
    backwards_wave_speed = vehicle_length/ reaction_time
    return backwards_wave_speed


# def calc_max_flow(cell, vehicle_type_dict, vehicle_length,dt_val):
#     max_flow = 0
#     max_flow_sum = 0
#     # summation
#     for vehicle_type in vehicle_type_dict.keys():
#         max_flow_sum = max_flow_sum + (
#             (cell.number_in_t_i_make_dict[vehicle_type]/cell.max_vehicles)/
#             (cell.number_in_t_i/cell.max_vehicles)
#         ) * vehicle_type_dict[vehicle_type]
#     max_flow_calc = (1/((cell.free_flow_speed * max_flow_sum)+vehicle_length))
#     max_flow = cell.free_flow_speed * max_flow_calc
#     max_flow = max_flow * (dt_val/3600)
#     cell.set_cell_capacity(round(max_flow,0))
#     return round(max_flow,0)

def flow_density_max_flow(cell, vehicle_type_dict, vehicle_length,dt_val):
    # relaxing density assumption going with uniform vehicle
    reaction_time = np.average(list(vehicle_type_dict.values()))
    max_flow = ((cell.free_flow_speed * reaction_time) + vehicle_length)
    max_flow = (1/max_flow) * cell.free_flow_speed
    max_flow = max_flow * (dt_val/3600)
    cell.set_cell_capacity(round(max_flow, 0))
    return round(max_flow,0)

def calc_vehicles_moving_cells_type(cell,prior_cell,vehicle_type_dict,max_flow,backwards_wave_speed):
    for vehicle_type in vehicle_type_dict.keys():
        item1 = prior_cell.number_in_t_i_make_dict[vehicle_type]
        item2 = (prior_cell.number_in_t_i_make_dict[vehicle_type]/
                 prior_cell.number_in_t_i) * (max_flow)
        item3_1 = (prior_cell.number_in_t_i_make_dict[vehicle_type]/
                 prior_cell.number_in_t_i) * (backwards_wave_speed/prior_cell.free_flow_speed)
        item3_2 = cell.max_vehicles - cell.number_in_t_i
        item3 = item3_1 * item3_2
        cell.number_entering_cell_from_arc_make_dict[vehicle_type] = round(min(item1,item2,item3),0)
    return

def calc_number_in_t_f_make_dict(cell,next_cell):
    for vehicle_type in cell.number_in_t_i_make_dict:
        cell.number_in_t_f_make_dict[vehicle_type]= cell.number_in_t_i_make_dict[vehicle_type] + \
                                                    cell.number_entering_cell_from_arc_make_dict[vehicle_type] - \
                                                    next_cell.number_entering_cell_from_arc_make_dict[vehicle_type]

    return

def ctm_function_t_i_heterogenous(data,simulation_time):
    # function to use to evaluate CTM
    for start_cell in data.cell_iteration_dict.keys():
        for cell_key in data.cell_iteration_dict[start_cell]:
            cell = data.cell_dict[cell_key]
            prior_cell=data.cell_dict[cell.prior_cell]
            if prior_cell.number_in_t_i == 0:
                cell.number_entering_cell_from_arc[prior_cell.cell_id] = 0
            elif cell.number_in_t_i == 0:
                # use flow-density relationships relaxing heterogenous flow assumptions
                backwards_wave_speed= flow_density_bws(cell=cell,
                                                       vehicle_length=data.exper_vehicle_length,
                                                       vehicle_type_dict=data.vehicle_type_dict)
                max_flow = flow_density_max_flow(cell=cell,
                                                 vehicle_type_dict=data.vehicle_type_dict,
                                                 vehicle_length=data.exper_vehicle_length,
                                                 dt_val = data.exper_simulation_time_interval)
                # This function sets cell.number_entering_cell_from_arc_make_dict
                calc_vehicles_moving_cells_type(cell,prior_cell,data.vehicle_type_dict,max_flow,backwards_wave_speed)
                cell.number_entering_cell_from_arc[prior_cell.cell_id] = cell.get_number_entering_cell_from_arc(prior_cell.cell_id)
            else:
                max_flow = cell.cell_capacity
                backwards_wave_speed = cell.backwards_wave_sp
                # backwards_wave_speed = calc_backwards_wave_speed(cell, data.vehicle_type_dict, data.exper_vehicle_length)
                backwards_wave_speed = flow_density_bws(cell=cell,
                                                        vehicle_length=data.exper_vehicle_length,
                                                        vehicle_type_dict=data.vehicle_type_dict)
                # max_flow = calc_max_flow(cell, data.vehicle_type_dict, data.exper_vehicle_length,
                #                          dt_val = data.exper_simulation_time_interval)
                max_flow = flow_density_max_flow(cell=cell,
                                                 vehicle_type_dict=data.vehicle_type_dict,
                                                 vehicle_length=data.exper_vehicle_length,
                                                 dt_val=data.exper_simulation_time_interval)
                # This function sets cell.number_entering_cell_from_arc_make_dict
                calc_vehicles_moving_cells_type(cell,prior_cell,data.vehicle_type_dict,max_flow,backwards_wave_speed)
                cell.number_entering_cell_from_arc[prior_cell.cell_id] = cell.get_number_entering_cell_from_arc(prior_cell.cell_id)

            # this is where the multi type would need to be reimplemented but for my purposes I do not need to

            #should move to transaction manage portion
            # temp = []
            for i in range(int(cell.number_entering_cell_from_arc[prior_cell.cell_id])):
                vehicle = prior_cell.cell_queue.pop()
                # if vehicle.move_status == True:
                #removed logic for now each iteration is just running ICP then CTM
                # temp.append(vehicle)
                vehicle.cell_time_out = simulation_time
                travel_time = vehicle.cell_time_out - vehicle.cell_time_in
                prior_cell.cell_travel_time_list.append(travel_time)
                vehicle.cell_time_in = simulation_time
                vehicle.set_current_cell_location(cell.cell_id)
                vehicle.route_traveled.add(cell.cell_id)
                    # vehicle.move_status = False
                cell.cell_queue.appendleft(vehicle)

    return

def ctm_function_t_i_homogenous(data,simulation_time):
    # function to use to evaluate CTM
    for start_cell in data.cell_iteration_dict.keys():
        for cell_key in data.cell_iteration_dict[start_cell]:
            cell = data.cell_dict[cell_key]
            prior_cell=data.cell_dict[cell.prior_cell]
            if prior_cell.number_in_t_i == 0:
                cell.number_entering_cell_from_arc[prior_cell.cell_id] = 0

                calc_vehicles_moving_cells_type(cell,prior_cell,data.vehicle_type_dict,cell.max_flow,cell.backwards_wave_speed)
                cell.number_entering_cell_from_arc[prior_cell.cell_id] = cell.get_number_entering_cell_from_arc(prior_cell.cell_id)

            for i in range(int(cell.number_entering_cell_from_arc[prior_cell.cell_id])):
                vehicle = prior_cell.cell_queue.pop()
                # if vehicle.move_status == True:
                #removed logic for now each iteration is just running ICP then CTM
                # temp.append(vehicle)
                vehicle.cell_time_out = simulation_time
                travel_time = vehicle.cell_time_out - vehicle.cell_time_in
                prior_cell.cell_travel_time_list.append(travel_time)
                vehicle.cell_time_in = simulation_time
                vehicle.set_current_cell_location(cell.cell_id)
                vehicle.route_traveled.add(cell.cell_id)
                    # vehicle.move_status = False
                cell.cell_queue.appendleft(vehicle)

    return

def ctm_function_t_f(data):
            #number in cell at next time
            #setting number in cell

    for start_cell in data.cell_iteration_dict:
        for cell_key in data.cell_iteration_dict[start_cell]:
            cell = data.cell_dict[cell_key]
            next_cell = data.cell_dict[cell.next_cell]
            calc_number_in_t_f_make_dict(cell,next_cell)

            #setting number_in_t_i_make_dict for next iteration
            #### NOTE
            # might want to check here against the actual value in the cell
            for make in cell.number_in_t_f_make_dict:
                value = cell.number_in_t_f_make_dict[make]
                cell.number_in_t_i_make_dict[make] = value
            cell.get_number_in_t_f()
            # cell.number_in_t_i = cell.number_in_t_f
    return


def test1(this):
    test2(this.vehicle_dict)
    return

def test2(that):
    test3(that['start_to_end_@t_0_#0'])
    return

def test3(the_other_thing):
    the_other_thing.cell_time_in = 'jibber jabber'
    return