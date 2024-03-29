"""
This file is the intersection control policy functions:
it is broken down into modular functions that can be run with given inputs
then a larger function that runs all of them
"""
import Vehicles_Class
import Cell_Class
from collections import deque


def Intersection_Control_Policy():
    incoming_links_set = {}
    outgoing_links_set = {}
    conflict_regions = {}

def ICP(data,simulation_time):
    # Defining data paramters to use
    # Makes it easier to move function outside of class if needed


    #For every intersection
    for i in data.intersection_dict:
        V = []
        sending_flow = []
        # For every incoming cell in the intersection
        intersection = data.intersection_dict[i]
        for incoming_cell_key in intersection.incoming_cells:
            # For every lane in the incoming cell
            incoming_cell = data.cell_dict[incoming_cell_key]
            for i in range(incoming_cell.num_lanes):
                # Remove a vehicle from the cell and add it to the list V
                if len(incoming_cell.cell_queue)!= 0:
                    if list() in incoming_cell.cell_queue: incoming_cell.cell_queue.clear()
                if len(incoming_cell.cell_queue) != 0:
                    vehicle = incoming_cell.cell_queue.pop()
                    if vehicle.cell_time_in == simulation_time:
                        incoming_cell.cell_queue.append(vehicle)
                    else:
                        V.append(vehicle)
                    # if vehicle.move_status:

            # For all outgoing cells in the the intersection
            for outgoing_cell_key in intersection.outgoing_cells:
                outgoing_cell = data.cell_dict[outgoing_cell_key]
                # set the y or number entering the outgoing cell from the incoming cell to 0
                outgoing_cell.number_entering_cell_from_arc[incoming_cell_key] = 0
            for i in range(len(incoming_cell.cell_queue)):
                if len(incoming_cell.cell_queue)!= 0:
                    if list() in incoming_cell.cell_queue: incoming_cell.cell_queue.clear()
                vehicle = incoming_cell.cell_queue.pop()
                # if vehicle.move_status:
                if vehicle.cell_time_in == simulation_time:
                    incoming_cell.cell_queue.append(vehicle)
                else:
                    sending_flow.append(vehicle)
        # Sort V by a FIFO priority function
        V.sort(key=lambda x: x.cell_time_in)
        # sort sending flow by same priority
        sending_flow.sort(key = lambda x: x.cell_time_in,reverse=True)
        for v in V:
        # let (i,j) be turning movement of v
        # let v.turning_move[0] = i , v.turning_move[1] = j
            # Get the vehicles route
            v.set_turning_move()
            # get the cell it is leaving from
            # i_cell_id = intersection.incoming_cells[v.turning_move[0]]
            i_cell = data.cell_dict[v.turning_move[0]]
            # get the cell the car is going to
            j_cell = data.cell_dict[v.turning_move[1]]
            if can_move(v,i_cell,j_cell,intersection,data.exper_vehicle_length):
                j_cell.number_entering_cell_from_arc[v.turning_move[0]] = j_cell.number_entering_cell_from_arc[v.turning_move[0]] +1
                # v.move_status = False
                #removing check on vehicle movement logic
                #added cell location logic for whenver a vehicle does move
                #simulation travel time
                v.cell_time_out = simulation_time

                #cell travel time considerations
                travel_time = v.cell_time_out - v.cell_time_in
                i_cell.cell_travel_time_list.append(travel_time)
                v.cell_time_in = simulation_time
                #set current cell location and add to route travel the new cell
                v.set_current_cell_location(j_cell.cell_id)
                v.route_traveled.add(j_cell.cell_id)
                j_cell.cell_queue.appendleft(v)

                if v.is_autonomous:
                    for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,j_cell.cell_id]:
                        intersection.cr_equivalent_flow[conflict_region] = intersection.cr_equivalent_flow[conflict_region]+ \
                        (intersection.cr_capacity[conflict_region]/intersection.turning_movement_capacity[v.turning_move])
                else:
                    print('Need to add non-autonomous intersection logic')
                    for outgoing_cell_key in intersection.outgoing_cells:
                        for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,outgoing_cell_key]:
                            intersection.cr_equivalent_flow[conflict_region] = intersection.cr_equivalent_flow[conflict_region] + \
                                                                               (intersection.cr_capacity[conflict_region] /
                                                                                intersection.turning_movement_capacity[v.turning_move])
                if len(sending_flow)>0:
                    V.append(sending_flow.pop())
            else:
                v.set_current_cell_location(i_cell.cell_id)
                i_cell.cell_queue.append(v)
                j_travel_time_delay = j_cell.cell_travel_time
                j_travel_time_delay = j_travel_time_delay + data.exper_simulation_time_interval
                j_cell.cell_travel_time_list.append(j_travel_time_delay)
        if len(sending_flow)>0:
            for v in sending_flow:
                v.set_turning_move()
                # get the cell it is leaving from
                # i_cell_id = intersection.incoming_cells[v.turning_move[0]]
                i_cell = data.cell_dict[v.turning_move[0]]
                # get the cell the car is going to
                j_cell = data.cell_dict[v.turning_move[1]]
                v.set_current_cell_location(i_cell.cell_id)
                i_cell.cell_queue.append(v)
                j_travel_time_delay = j_cell.cell_travel_time
                j_travel_time_delay = j_travel_time_delay + data.exper_simulation_time_interval
                j_cell.cell_travel_time_list.append(j_travel_time_delay)

    return





def can_move(v,i_cell,j_cell, intersection,vehicle_length,hv_reaction_time=1.5,av_reaction_time=0.5):
    #calculation for cr values and turning movement caluce

    #receiving flow calculation baked into class
    receiving_flow =  j_cell.get_receiving_flow()
    expression1_1 = j_cell.get_receiving_flow() - sum(j_cell.number_entering_cell_from_arc.values())
    expression1_2 =( i_cell.free_flow_speed * av_reaction_time ) + vehicle_length
    expression1_3 = ( i_cell.free_flow_speed * hv_reaction_time ) + vehicle_length

    #for test1
    expression1 = expression1_1 < (expression1_2/expression1_3)

    #for test2
    # free flow speed, reaction time and length fraction
    free_flow_reaction_time_length_fraction = expression1_2/expression1_3


    # test 1
    # is there room in the cell considering speed and reaction times
    if expression1:
        return False

    #autonomus separatoin
    if v.is_autonomous:
        for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,j_cell.cell_id]:
            capacity_fraction =  (intersection.cr_capacity[conflict_region] / intersection.turning_movement_capacity[v.turning_move])
            expression2_1 = intersection.cr_capacity[conflict_region] - intersection.cr_equivalent_flow[conflict_region]
            expression2 = expression2_1 < (free_flow_reaction_time_length_fraction * capacity_fraction)
            if expression2 :
                return False
    else:
        for outgoing_cell in intersection.outgoing_cells:
            for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id, outgoing_cell]:
                capacity_fraction = (intersection.cr_capacity[conflict_region] / intersection.turning_movement_capacity[
                    v.turning_move])
                expression2_1 = intersection.cr_capacity[conflict_region] - intersection.cr_equivalent_flow[
                    conflict_region]
                expression2 = expression2_1 < (free_flow_reaction_time_length_fraction * capacity_fraction)
                if expression2:
                    return False
    return True

  