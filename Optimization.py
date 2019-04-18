import pyomo
import pandas
import numpy as np
import pyomo.opt
import pyomo.environ as pe


class MinCostFlow:
    """This class implements a standard min-cost-flow model.

    It takes as input two csv files, providing data for the nodes
    and the arcs of the network.  The nodes file should have columns:

    Node, Imbalance

    that specify the node name and the flow imbalance at the node.
    The arcs file should have columns:

    Start, End, Cost, UpperBound, LowerBound

    that specify an arc start node, an arc end node, a cost for the arc,
    and upper and lower bounds for the flow."""

    def __init__(self, nodesfile, arcsfile):
        """Read in the csv data."""
        # Read in the nodes file
        self.node_data = pandas.read_csv('nodes.csv')

        # Read in the arcs file
        self.arc_data = pandas.read_csv('arcs.csv')

        # Read in the trips file
        self.trip_data = pandas.read_csv('trips.csv')

        # Create Node_set
        self.node_set = set(self.node_data['Node'])

        #Create trip_set and attributes
        self.trip_set = set(self.trip_data['Trip'])
        self.trip_net_demand = {}


        #Create all arc related data attributes
        self.arc_capacity = {}
        self.arc_cost = {}
        self.arc_set = set()

        self.set_trip_attributes_from_pandas()
        self.set_arc_attributes_from_pandas()
        self.set_node_set_from_pandas()

        self.createModel()

    def set_node_set_from_pandas(self):
        """
        Uses the pandas object created by pandas.read_csv('arcs.csv') to populate:
        self.node_set
        :return:
        """
        self.node_set = set(self.node_data['Node'])

    def set_node_set(self,new_node_set):
        """
        changes the node_set data to new_node_set
        :param new_node_set:
        :return:
        """
        self.node_set = new_node_set

    def set_arc_attributes_from_pandas(self):
        """
        Uses the pandas object created by pandas.read_csv('arcs.csv') to populate:
        self.arc_capacity
        self.arc_cost
        self.arc_set

        :return:
        """
        for item in self.arc_data.iterrows():
            self.arc_capacity[item[1][0],item[1][1]]=item[1][3]
            self.arc_cost[item[1][0],item[1][1]]=item[1][2]
            self.arc_set.add((item[1][0],item[1][1]))
        return

    def set_arc_capacity(self,new_arc_capacity):
        self.arc_capacity = new_arc_capacity

    def set_arc_cost(self,new_arc_cost):
        self.arc_cost = new_arc_cost

    def set_arc_set(self,new_arc_set):
        self.arc_set = new_arc_set

    def set_trip_attributes_from_pandas(self):
        """
        Uses the pandas object created by pandas.read_csv('trips.csv') to populate:
        self.trip_net_demand
        self.trip_set
        :return:
        """
        for item in self.trip_data.iterrows():
            self.trip_net_demand[item[1][0], item[1][1]] = item[1][2]
        self.trip_set = set(self.trip_data['Trip'])
        return

    def set_trip_net_demand(self,new_trip_net_demand):
        self.trip_net_demand = new_trip_net_demand

    def set_trip_set(self,new_trip_set):
        self.trip_set = new_trip_set

    def createModel(self):
        """Create the pyomo model given the csv data."""
        self.m = pe.AbstractModel()

        # Create sets
        self.m.node_set = pe.Set(initialize=self.node_set)
        self.m.arc_set = pe.Set(initialize=self.arc_set, dimen=2)
        #Addition of Commodity set
        self.m.trip_set = pe.Set(initialize=self.trip_set)

        #Create Params
        self.m.Cost_param = pe.Param(self.m.arc_set, initialize=self.arc_cost)
        self.m.Capacity_param = pe.Param(self.m.arc_set, initialize=self.arc_capacity)
        self.m.Net_demand_param = pe.Param(self.m.node_set,self.m.trip_set, initialize=self.trip_net_demand)

        # Create variables
        self.m.Y = pe.Var(self.m.arc_set , self.m.trip_set, domain=pe.NonNegativeReals)

        # Create objective

        def obj_rule(m):
            return sum(self.m.Y[(start,end), Trip] * self.m.Cost_param[start,end] \
                       for (start, end) in self.m.arc_set\
                       for Trip in self.m.trip_set)

        self.m.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

        # Flow Balance rule
        def flow_bal_rule(m, n,t):
            lhs = sum(self.m.Y[(into,n),t] for into in self.m.node_set if (into,n) in self.m.arc_set ) \
                  - sum(self.m.Y[(n,out),t] for out in self.m.node_set if (n,out) in self.m.arc_set )
            constr = (lhs == self.m.Net_demand_param[n,t])
            return  constr


        self.m.FlowBal = pe.Constraint(self.m.node_set, self.m.trip_set, rule=flow_bal_rule)

        #Capacity Joint Constraint
        def joint_capacity_rule(m,i,j):
            return sum(self.m.Y[i,j,k] for k in self.m.trip_set) <= self.m.Capacity_param[i,j]

        self.m.Capacity = pe.Constraint(self.m.arc_set,rule=joint_capacity_rule,)

        # # Upper bounds rule
        # def upper_bounds_rule(m, n1, n2):
        #     e = (n1, n2)
        #     if self.arc_data.loc[e, 'UpperBound'] < 0:
        #         return pe.Constraint.Skip
        #     return m.Y[e] <= self.arc_data.loc[e, 'UpperBound']
        #
        # self.m.UpperBound = pe.Constraint(self.m.arc_set, rule=upper_bounds_rule)
        #
        # # Lower bounds rule
        # def lower_bounds_rule(m, n1, n2):
        #     e = (n1, n2)
        #     if self.arc_data.loc[e, 'LowerBound'] < 0:
        #         return pe.Constraint.Skip
        #     return m.Y[e] >= self.arc_data.ix[e, 'LowerBound']
        #
        # self.m.LowerBound = pe.Constraint(self.m.arc_set, rule=lower_bounds_rule)

    def solve(self):
        """Solve the model."""
        self.m.construct()
        self.i = self.m.create_instance()
        solver = pyomo.opt.SolverFactory('gurobi')
        results = solver.solve(self.i, tee=True, keepfiles=False,
                               options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")

        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            pe.logger.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):
            pe.logger.warning('Check solver optimality?')
    def get_Var(self):
        """Get the variable value and put into dictionary Y"""
        Y={}
        for var in sp.i.Y:
            Y[var]=sp.i.Y[var].value
        return Y


if __name__ == '__main__':
    sp = MinCostFlow('nodes.csv', 'arcs.csv')
    sp.solve()
    print('\n\n---------------------------')
    print('Cost: ', sp.i.OBJ())
