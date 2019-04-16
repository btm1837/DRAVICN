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
        self.node_data.set_index(['Node'], inplace=True)
        self.node_data.sort_index(inplace=True)
        # Read in the arcs file
        self.arc_data = pandas.read_csv('arcs.csv')
        self.arc_data.set_index(['Start', 'End'], inplace=True)
        self.arc_data.sort_index(inplace=True)

        self.trip_data = pandas.read_csv('trips.csv')
        self.trip_data.set_index(['Node','Trip'], inplace=True)
        self.trip_data.sort_index(inplace=True)

        self.node_set = self.node_data.index.unique()
        self.arc_set = self.arc_data.index.unique()
        self.trip_set = self.trip_data.index.unique()
        self.trip_set = self.trip_data.index.levels[1].unique()

        self.createModel()

    def createModel(self):
        """Create the pyomo model given the csv data."""
        self.m = pe.AbstractModel()

        # Create sets
        self.m.node_set = pe.Set(initialize=self.node_set)
        self.m.arc_set = pe.Set(initialize=self.arc_set, dimen=2)
        #Addition of Commodity set
        self.m.trip_set = pe.Set(initialize=self.trip_set)

        #Construct Sets for iteration
        #self.m.node_set.construct()
        #self.m.arc_set.construct()
        #self.m.trip_set.construct()

        #Create Params
        #df_cost =
        self.m.Cost_param = pe.Param(self.m.arc_set, initialize=self.arc_data['Cost'].to_frame)
        self.m.Capacity_param = pe.Param(self.m.arc_set, initialize=self.arc_data['Capacity'].to_frame)

        #initialize Parameters
        self.m.Cost_param.construct()
        self.m.Capacity_param.construct()


        # Create variables
        self.m.Y = pe.Var(self.m.arc_set * self.m.trip_set, domain=pe.NonNegativeReals)
        self.m.Y.construct()

        # Create objective
        def obj_rule(m):
            return sum(sum(self.m.Y[start,end,Trip] * self.m.Cost_param[start,end] for start,end in self.m.arc_data.iterrows()) for Trip in self.m.trip_set)

        self.m.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

        # Flow Balance rule
        def flow_bal_rule(m, n,t):
            arcs = self.arc_data.reset_index()
            preds = arcs[arcs.End == n]['Start']
            succs = arcs[arcs.Start == n]['End']
            lhs = sum(m.Y[(p, n, t)] for p in preds) - sum(m.Y[(n, s, t)] for s in succs)
            imbalance = self.trip_data['SupplyDemand'].get((n,t),0)
            constr = (lhs == imbalance)
            if isinstance(constr,bool):
                return pe.Constraint.Skip
            return  constr


        self.m.FlowBal = pe.Constraint(self.m.node_set * self.m.trip_set, rule=flow_bal_rule)

        #Capacity Joint Constraint
        def joint_capacity_rule(m,i,j):
            capacity = self.arc_data['Capacity'].get((i,j),-1)
            if capacity < 0 :
                return pe.Constraint.Skip
            return sum(self.m.Y[i,j,k] for k in self.trip_set) <= capacity
        self.m.Capacity = pe.Constraint(self.m.arc_set,rule=joint_capacity_rule)

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
        self.i = self.m.create_instance()
        solver = pyomo.opt.SolverFactory('gurobi')
        results = solver.solve(self.i, tee=True, keepfiles=False,
                               options_string="mip_tolerances_integrality=1e-9 mip_tolerances_mipgap=0")

        if (results.solver.status != pyomo.opt.SolverStatus.ok):
            logging.warning('Check solver not ok?')
        if (results.solver.termination_condition != pyomo.opt.TerminationCondition.optimal):
            logging.warning('Check solver optimality?')
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
