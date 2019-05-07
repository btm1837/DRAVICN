
import pandas
import collections

class Cell:
    """
    Basic Format for what a cell in the model is comprised of

    Takes in Node and Arc Data and coverts to cell based discretized network

    Uses Method Move_Vehicles to move vehicles through cells

    Uses Setter methods to set various atributes, these are used in the Transaction Manager to update the cells values

    Uses Getter Methods to get various atribute values.

    """

    def __init__(self):
        #asdf
        #Cell ocupancy
        data = pandas.read_csv('Cells.csv')

        #Cell ocupancy at in time period prior to CTM equaltions, initial
        # n_i(t0)
        self.number_in_t_i = ''

        #Number of vehicles in the cell after CTM equations, final
        # n_i(t1)
        self.number_in_t_f = ''

        # Number of vehicles entering cell from cell i-1 at time t
        # Y
        self.number_entering_cell_from_arc = {}

        #Queue of vehicles in the cell
        self.cell_queue = collections.deque([])

        # uf , speed if vehicles are moving freely
        self.free_flow_speed =''
        self.max_vehicles = ''
        self.reaction_time = ''
        self.num_vehicle_types = ''
        self.start_node = 'NA'
        self.end_node = 'NA'
        self.num_lanes = 1

    #Getters Block
    def get__(self):
        #asdf

    #Setters Block
    def set_(self):
        #asdf

    #Methods


# Subclass of Intersection Cells
class Intersection_Cell (Cell):
    """
    specific subclass for intersection cells
    """

    def __init__(self):
        self.number_entering_cell_from_i = {}