

class Intersection:
    """


    """
    def __init__(self):
        #Node that the intersection is located at
        self.located_at_node = 'NA'

        # the set of incoming links
        self.incoming_links = set()

        # the set of outgoing links
        self.outgoing_links = set()

        # Conflict regions present in each intersection
        self.list_conflict_regions = set(['C1','C2','C3','C4'])

        # Dictionary that describes the cr corresponding to an incoming or outgoing arc
        self.cr_for_arc_i = {}

        # Subset of CRs for incoming link i to out going link j
        self.cr_subset_from_i_to_j = {}

    def ICP(self,):


