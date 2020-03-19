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

def ICP(intersection_list, cell_dict):
    # Defining data paramters to use
    # Makes it easier to move function outside of class if needed

    V = []
    sending_flow = []
    #For every intersection
    for intersection in intersection_list:
        # For every incoming cell in the intersection

        for incoming_cell in intersection.incoming_cells:
            # For every lane in the incoming cell
            for i in range(len(incoming_cell.num_lanes)):
                # Remove a vehicle from the cell and add it to the list V
                if len(incoming_cell.cell_queue) != 0:
                    vehicle = incoming_cell.cell_queue.pop()
                    if vehicle.move_status:
                        V.append(vehicle)
            # For all outgoing cells in the the intersection
            for outgoing_cell in intersection.outgoing_cells:
                # set the y or number entering the outgoing cell from the incoming cell to 0
                outgoing_cell.number_entering_cell_from_arc[incoming_cell] = 0
            for i in range(len(incoming_cell.cell_queue)):
                vehicle = incoming_cell.cell_queue.pop()
                if vehicle.move_status:
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
            i_cell = cell_dict[v.turning_move[0]]
            # get the cell the car is going to
            j_cell = cell_dict[v.turning_move[1]]
            if can_move(v,i_cell,j_cell):
                j_cell.number_entering_cell_from_arc[v.turning_move[0]] = j_cell.number_entering_cell_from_arc[v.turning_move[0]] +1
                v.move_status = False
                j_cell.cell_queue.appendleft(v)
                if v.is_autonomous:
                    for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,j_cell.cell_id]:
                        intersection.cr_equivalent_flow[conflict_region] = intersection.cr_equivalent_flow[conflict_region]+ \
                        (intersection.cr_capacity[conflict_region]/intersection.turning_movement_capacity[v.turning_move])
                else:
                    print('Need to add non-autonomous intersection logic')
                    for outgoing_cell in intersection.outgoing_cells:
                        for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,outgoing_cell]:
                            intersection.cr_equivalent_flow[conflict_region] = intersection.cr_equivalent_flow[conflict_region] + \
                                                                               (intersection.cr_capacity[conflict_region] /
                                                                                intersection.turning_movement_capacity[v.turning_move])
                V.append(sending_flow.pop())
    return





def can_move(v,i_cell,j_cell, intersection,hv_reaction_time,av_reaction_time,vehicle_length):
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

  