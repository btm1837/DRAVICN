
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
        data = pandas.read_csv(Cells.csv)
        self.number_in_t0 = pandas.read_csv()

        self.cell_queue = collections.deque([])
        self.free_flow_speed =
        self.max_vehicles



    #Getters Block
    def get__(self):
        #asdf

    #Setters Block
    def set_(self):
        #asdf

    #Methods
