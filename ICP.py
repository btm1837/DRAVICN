"""
This file is the intersection control policy functions:
it is broken down into modular functions that can be run with given inputs
then a larger function that runs all of them
"""



def Intersection_Control_Policy():
    incoming_links_set = {}
    outgoing_links_set = {}
    conflict_regions = {}
    cr_