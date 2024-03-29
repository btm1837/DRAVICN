
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
        self.initial_routing = routing_arcs

        self.move_status = True

        # Route Traveled
        self.route_traveled = set()

        # Node Location
        self.current_node_location = ''
        self.last_node_location=''
        #self.next_node_location=''


        # Cell Location
        self.current_cell_location =''
        self.last_cell_location=''
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
        return

    def set_time_out_sim(self,time):
        self.time_out_sim = time
        return

    def set_current_node_location(self,node):
        #self.route_traveled.add((self.current_node_location,node))
        self.last_node_location = self.current_node_location
        self.current_node_location = node
        return

    def set_current_cell_location(self,cell):
        # if vehicle is starting at origin then it is modeled at the begingin of a cell
        # otherwise the vehicle is put at the node at the end of its cell
        #new?
        # if self.current_cell_location != cell:
        #     if self.current_cell_location[0] == self.current_node_location:
        #         self.last_node_location = self.current_node_location
        #         self.last_cell_location = self.current_cell_location
        #     elif self.current_cell_location[1]
        if self.current_cell_location == cell:
            return
        self.last_cell_location = self.current_cell_location
        self.last_node_location = self.current_node_location
        self.current_cell_location = cell
        self.current_node_location = self.current_cell_location[1]
        return
        #old
        # if self.current_cell_location[0] == self.origin:
        #     self.last_node_location = self.origin
        # else:
        #     self.last_node_location = self.current_node_location
        #
        # self.last_cell_location = self.current_cell_location
        # self.current_cell_location = cell
        # # if self.current_cell_location[0] == self.origin:
        # #     self.current_node_location =
        # self.current_node_location = self.current_cell_location[1]


    def set_origin_cell_location(self,cell):
        # if vehicle is starting at origin then it is modeled at the begingin of a cell
        # otherwise the vehicle is put at the node at the end of its cell
        self.last_cell_location = cell
        self.last_node_location = self.origin
        self.current_cell_location = cell
        self.current_node_location = self.origin
        return

    def set_next_cell_location(self):
        for item in self.route:
            if self.current_cell_location[1] == item[0]:
                self.next_cell_location = item
        return

    def set_turning_move(self):
        """
        to be run when vehicle is at intersection, otherwise gives the next node the vehicle is traveling to
        :return:
        """
        self.set_next_cell_location()
        self.turning_move = (self.current_cell_location,self.next_cell_location)
        return
