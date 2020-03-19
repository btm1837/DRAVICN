
class Vehicle:
    """
    Used for defining individual vehicle attributes
    """
    def __init__(self,vehicle_ID,make,origin,destination,routing_arcs):


        # Vehicle tracking attributes:
        self.vehicle_ID = vehicle_ID
        self.origin = origin
        self.destination = destination
        self.route = routing_arcs
        self.initial_routing = set()

        self.move_status = True

        # Route Traveled
        self.route_traveled = set()

        # Node Location
        self.current_node_location = ''
        self.last_node_location=''
        #self.next_node_location=''


        # Cell Location
        self.current_cell_location =''
        self.next_cell_location = ''
        self.turning_move = ''

        # Cell transmission model attributes
        self.make = make
        self.length = ''
        self.reaction_time = ''

        # transaction manager tracking
        self.cell_time_in = 0
        self.cell_time_out = 0

        # is autonmous
        # all vehicles assumed autonmous for this simulation
        self.is_autonomous = True

        # Time keeping
        self.time_in_sim = ''
        self.time_out_sim = ''

    def set_time_in_sim(self,time):
        self.time_in_sim = time

    def set_time_out_sim(self,time):
        self.time_out_sim = time

    def set_current_node_location(self,node):
        #self.route_traveled.add((self.current_node_location,node))
        self.last_node_location = self.current_node_location
        self.current_node_location = node

    def set_current_cell_location(self,cell):
        self.current_cell_location = cell

    def set_next_cell_location(self):
        for item in self.route:
            if self.current_cell_location[1] == item[0]:
                self.next_cell_location = item

    def set_turning_move(self):
        """
        to be run when vehicle is at intersection, otherwise gives the next node the vehicle is traveling to
        :return:
        """
        self.set_next_cell_location()
        self.turning_move = (self.current_cell_location,self.next_cell_location)
        return
