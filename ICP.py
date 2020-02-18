"""
This file is the intersection control policy functions:
it is broken down into modular functions that can be run with given inputs
then a larger function that runs all of them
"""
import Vehicles_Class
import Cell_Class


def Intersection_Control_Policy():
    incoming_links_set = {}
    outgoing_links_set = {}
    conflict_regions = {}
    cr_

def ICP(intersection_list,intersection_cells_list,num_lanes,num_vehicles_from_i_to_j, cell_dict):
    # Defining data paramters to use
    # Makes it easier to move function outside of class if needed

    V = []
    #For every intersection
    for intersection in intersection_list:
        # For every incoming cell in the intersection
        for incoming_cell in intersection.incoming_cells:
            # For every lane in the incoming cell
            for i in range(len(incoming_cell.num_lanes)):
                # Remove a vehicle from the cell and add it to the list V
                V.append(incoming_cell.cell_queue.pop())
            # For all outgoing cells in the the intersection
            for outgoing_cell in intersection.outgoing_cells:
                # set the y or number entering the outgoing cell from the incoming cell to 0
                outgoing_cell.number_entering_cell_from_arc[incoming_cell] = 0
        # Sort V by a FIFO priority function
        V.sort(key=lambda x: x.cell_time_in)
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
                if v.is_autonomous:
                    for conflict_region in intersection.cr_subset_from_i_to_j[i_cell.cell_id,j_cell.cell_id]:
                        intersection.cr_equivalent_flow[conflict_region] = intersection.cr_equivalent_flow[conflict_region]+ \
                        (intersection.cr_capacity[conflict_region]/intersection.turning_movement_capacity[v.turning_move])




def can_move(v,i_cell,j_cell):

    # must return TRUE if the vehicle can move
    # False otherwise
    return

    # incoming_links = self.incoming_links
    # sending_flow = sending_flow
    # # Actual Function
    #
    # for incmoing_link in incoming_links:
    #     # sort sending flow by arival time


def get_qc_qij():



    return
