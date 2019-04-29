
class Vehicle:
    """
    Used for defining individual vehicle attributes
    """
    def __init__(self,generator):
        # Vehicle tracking attributes:
        self.vehicle_ID = ''
        self.origin = ''
        self.dest = ''
        self.routing_arcs = ''


        self.routing_cells = ''

        # Cell transmission model attributes
        self.make = ''
        self.length = ''
        self.reaction_time = ''

        # transaction manager tracking
        self.cell_time_in = ''
        self.cell_time_out =''

        # Time keeping
        self.time_in_sim = ''
        self.time_out_sim = ''



