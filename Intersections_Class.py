

class Intersection:
    """


    """
    def __init__(self,located_at_node,intersection_data):
        #Node that the intersection is located at
        self.intersection_data = intersection_data
        self.located_at_node = located_at_node

        # the set of incoming links
        self.incoming_cells = set()

        # the set of outgoing links
        self.outgoing_cells = set()

        # Conflict regions present in each intersection
        self.list_conflict_regions = set(['cr1','cr2','cr3','cr4'])

        # Dictionary that describes the cr corresponding to an incoming or outgoing arc
        self.cr_for_arc_i = {}

        # Subset of CRs for incoming link i to out going link j
        self.cr_subset_from_i_to_j = {}

        # Conflict Region Capacity
        self.cr_capacity = {}

        #Capacity of turning movement
        self.turning_movement_capacity = {}

        #Equivialent flow entering cr
        self.cr_equivalent_flow = {}

        self.set_cr_for_arc_i()
        self.set_incoming_cells()
        self.set_outgoing_cells()
        self.set_intitial_cr_subset_from_i_to_j()


    def set_cr_for_arc_i(self):
        self.cr_for_arc_i[self.intersection_data[0]] =  'cr1'
        self.cr_for_arc_i[self.intersection_data[1]] =  'cr2'
        self.cr_for_arc_i[self.intersection_data[2]] =  'cr3'
        self.cr_for_arc_i[self.intersection_data[3]] =  'cr4'

        self.cr_for_arc_i[self.intersection_data[4]] =  'cr1'
        self.cr_for_arc_i[self.intersection_data[5]] =  'cr2'
        self.cr_for_arc_i[self.intersection_data[6]] =  'cr3'
        self.cr_for_arc_i[self.intersection_data[7]] =  'cr4'
        return

    def set_incoming_cells(self):
        self.incoming_cells.add(self.intersection_data[0])
        self.incoming_cells.add(self.intersection_data[1])
        self.incoming_cells.add(self.intersection_data[2])
        self.incoming_cells.add(self.intersection_data[3])
        return

    def set_outgoing_cells(self):
        self.outgoing_cells.add(self.intersection_data[4])
        self.outgoing_cells.add(self.intersection_data[5])
        self.outgoing_cells.add(self.intersection_data[6])
        self.outgoing_cells.add(self.intersection_data[7])
        return

    def set_intitial_cr_subset_from_i_to_j(self):
        for incoming_cell in self.incoming_cells:
            for outgoing_cell in self.outgoing_cells:
                if self.cr_for_arc_i[incoming_cell] == 'cr1':
                    if self.cr_for_arc_i[outgoing_cell] =='cr1':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1')
                    if self.cr_for_arc_i[outgoing_cell] =='cr2':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr2')
                    if self.cr_for_arc_i[outgoing_cell] =='cr3':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr3')
                    if self.cr_for_arc_i[outgoing_cell] =='cr4':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr3','cr4')
                if self.cr_for_arc_i[incoming_cell] == 'cr2':
                    if self.cr_for_arc_i[outgoing_cell] =='cr1':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2','cr1')
                    if self.cr_for_arc_i[outgoing_cell] =='cr2':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2')
                    if self.cr_for_arc_i[outgoing_cell] =='cr3':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2', 'cr2','cr3')
                    if self.cr_for_arc_i[outgoing_cell] =='cr4':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2','cr4')
                if self.cr_for_arc_i[incoming_cell] == 'cr3':
                    if self.cr_for_arc_i[outgoing_cell] =='cr1':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr1')
                    if self.cr_for_arc_i[outgoing_cell] =='cr2':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr4','cr2')
                    if self.cr_for_arc_i[outgoing_cell] =='cr3':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3')
                    if self.cr_for_arc_i[outgoing_cell] =='cr4':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr4')
                if self.cr_for_arc_i[incoming_cell] == 'cr4':
                    if self.cr_for_arc_i[outgoing_cell] =='cr1':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr3','cr1')
                    if self.cr_for_arc_i[outgoing_cell] =='cr2':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr2')
                    if self.cr_for_arc_i[outgoing_cell] =='cr3':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr3')
                    if self.cr_for_arc_i[outgoing_cell] =='cr4':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4')
        return

    def set_cr_capacity(self,new_capacity):
        self.cr_capacity = new_capacity
        return

    def set_turning_movement_capacity(self,new_capacity):
        self.turning_movement_capacity = new_capacity
        return

    def set_cr_equivalent_flow(self,new_equivalent_flow):
        self.cr_equivalent_flow = new_equivalent_flow

