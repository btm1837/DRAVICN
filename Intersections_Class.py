

class Intersection:
    """


    """
    def __init__(self,located_at_node):
        #Node that the intersection is located at
        self.located_at_node = located_at_node

        # the set of incoming links
        self.incoming_cells = set()

        # the set of outgoing links
        self.outgoing_cells = set()

        # Conflict regions present in each intersection
        # self.list_conflict_regions = set(['cr1','cr2','cr3','cr4'])

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


        # self.set_cr_for_arc_i()
        # self.set_incoming_cells()
        # self.set_outgoing_cells()
        # self.set_intitial_cr_subset_from_i_to_j()


    # def set_cr_for_arc_i(self):
    #     self.cr_for_arc_i[self.intersection_data[0]] =  'cr1'
    #     self.cr_for_arc_i[self.intersection_data[1]] =  'cr2'
    #     self.cr_for_arc_i[self.intersection_data[2]] =  'cr3'
    #     self.cr_for_arc_i[self.intersection_data[3]] =  'cr4'
    #
    #     self.cr_for_arc_i[self.intersection_data[4]] =  'cr1'
    #     self.cr_for_arc_i[self.intersection_data[5]] =  'cr2'
    #     self.cr_for_arc_i[self.intersection_data[6]] =  'cr3'
    #     self.cr_for_arc_i[self.intersection_data[7]] =  'cr4'
    #     return
    def set_cr_for_arc_i(self,arc,cr):
        self.cr_for_arc_i[arc]=cr
        return


    # def set_incoming_cells(self):
    #     self.incoming_cells.add(self.intersection_data[0])
    #     self.incoming_cells.add(self.intersection_data[1])
    #     self.incoming_cells.add(self.intersection_data[2])
    #     self.incoming_cells.add(self.intersection_data[3])
    #     return
    #
    def set_incoming_cells(self,list_of_cells):
        for cell in list_of_cells:
            self.incoming_cells.add(cell)
        return
    # def set_outgoing_cells(self):
    #     self.outgoing_cells.add(self.intersection_data[4])
    #     self.outgoing_cells.add(self.intersection_data[5])
    #     self.outgoing_cells.add(self.intersection_data[6])
    #     self.outgoing_cells.add(self.intersection_data[7])
    #     return
    def set_outgoing_cells(self,list_of_cells):
        for cell in list_of_cells:
            self.outgoing_cells.add(cell)
        return

    # def set_intitial_cr_subset_from_i_to_j(self):
    #     for incoming_cell in self.incoming_cells:
    #         for outgoing_cell in self.outgoing_cells:
    #             if self.cr_for_arc_i[incoming_cell] == 'cr1':
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr1':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr2':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr2')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr3':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr3')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr4':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr1','cr3','cr4')
    #             if self.cr_for_arc_i[incoming_cell] == 'cr2':
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr1':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2','cr1')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr2':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr3':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2', 'cr2','cr3')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr4':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr2','cr4')
    #             if self.cr_for_arc_i[incoming_cell] == 'cr3':
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr1':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr1')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr2':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr4','cr2')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr3':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr4':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr3','cr4')
    #             if self.cr_for_arc_i[incoming_cell] == 'cr4':
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr1':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr3','cr1')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr2':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr2')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr3':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4','cr3')
    #                 if self.cr_for_arc_i[outgoing_cell] =='cr4':
    #                     self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('cr4')
    #     return
    def set_intitial_cr_subset_from_i_to_j(self):
        for incoming_cell in self.incoming_cells:
            for outgoing_cell in self.outgoing_cells:
                if self.cr_for_arc_i[incoming_cell] == 'NW':
                    if self.cr_for_arc_i[outgoing_cell] =='NW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NW')
                    if self.cr_for_arc_i[outgoing_cell] =='NE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NW','NE')
                    if self.cr_for_arc_i[outgoing_cell] =='SW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NW','SW')
                    if self.cr_for_arc_i[outgoing_cell] =='SE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NW','SW','SE')
                if self.cr_for_arc_i[incoming_cell] == 'NE':
                    if self.cr_for_arc_i[outgoing_cell] =='NW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NE','NW')
                    if self.cr_for_arc_i[outgoing_cell] =='NE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NE')
                    if self.cr_for_arc_i[outgoing_cell] =='SW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NE', 'NE','SW')
                    if self.cr_for_arc_i[outgoing_cell] =='SE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('NE','SE')
                if self.cr_for_arc_i[incoming_cell] == 'SW':
                    if self.cr_for_arc_i[outgoing_cell] =='NW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SW','NW')
                    if self.cr_for_arc_i[outgoing_cell] =='NE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SW','SE','NE')
                    if self.cr_for_arc_i[outgoing_cell] =='SW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SW')
                    if self.cr_for_arc_i[outgoing_cell] =='SE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SW','SE')
                if self.cr_for_arc_i[incoming_cell] == 'SE':
                    if self.cr_for_arc_i[outgoing_cell] =='NW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SE','SW','NW')
                    if self.cr_for_arc_i[outgoing_cell] =='NE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SE','NE')
                    if self.cr_for_arc_i[outgoing_cell] =='SW':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SE','SW')
                    if self.cr_for_arc_i[outgoing_cell] =='SE':
                        self.cr_subset_from_i_to_j[incoming_cell,outgoing_cell] = ('SE')
        return



    def set_cr_capacity(self,cr,new_capacity):
        self.cr_capacity[cr] = new_capacity
        return

    # def set_turning_movement_capacity(self,turning_move,new_capacity):
    #     self.turning_movement_capacity[turning_move] = new_capacity
    #     return

    def set_cr_equivalent_flow(self,cr,new_equivalent_flow):
        self.cr_equivalent_flow[cr] = new_equivalent_flow
        return

    # make a one time calculation instead of a constant calculation look up
    def calc_turning_movement_capacity(self,i_cell,j_cell):
        self.turning_movement_capacity[i_cell.cell_id,j_cell.cell_id] = min(i_cell.max_vehicles,j_cell.max_vehicles)
        return

    def calc_cr_capacity(self,cr):
        # max of turning movement capcities for any turning movements such that cr is on the subset of crs on that turn
        self.cr_capacity[cr] = 0
        for turning_move in self.cr_subset_from_i_to_j:
            # get any turning move containing this cr
            if cr in list(self.cr_subset_from_i_to_j[turning_move]):
                self.cr_capacity[cr] = max(self.cr_capacity[cr],self.turning_movement_capacity[turning_move])
        return

