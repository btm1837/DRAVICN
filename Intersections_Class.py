

class Intersection:
    """


    """
    def __init__(self):
        #Node that the intersection is located at
        self.located_at_node = 'NA'

        # the set of incoming links
        self.incoming_cells = ['']

        # the set of outgoing links
        self.outgoing_cells = ['']

        # Conflict regions present in each intersection
        self.list_conflict_regions = set(['C1','C2','C3','C4'])

        # Dictionary that describes the cr corresponding to an incoming or outgoing arc
        self.cr_for_arc_i = {}

        # Subset of CRs for incoming link i to out going link j
        self.cr_subset_from_i_to_j = {}

    def ICP(self,sending_flow_,num_lanes,num_vehicles_from_i_to_j, ):
        # Defining data paramters to use
        # Makes it easier to move function outside of class if needed
        incoming_links = self.incoming_links
        sending_flow = sending_flow
        # Actual Function

        for incmoing_link in incoming_links:
            # sort sending flow by arival time



