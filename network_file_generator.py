import pandas as pd
import numpy as np
import os
import sys
import itertools
from string import ascii_lowercase
import yaml
import pandas as pd
import matplotlib.pyplot as plt

def get_string():
    for size in itertools.count(1):
        for string in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(string)

def iter_all_strings():
    size = 1
    while True:
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)
        size +=1

gen = iter_all_strings()
def label_gen():
    for s in gen:
        return s

def get_string_list(size):
    list_s = []
    for s in itertools.islice(get_string(), size):
        # print(s)
        list_s.append(s)
    return list_s

# for s in iter_all_strings():
#     print(s)
#     if s == 'bb':
#         break

# list_s = []
# for s in itertools.islice(get_string(), 54):
#     print(s)
#     list_s.append(s)

# def make_network(set_up_file,path):
if __name__ == '__main__':
    path = r'C:\Users\bmaru\Documents\Thesis Docs\experiment_files'
    set_up_file = r'set_up1.yaml'
    # network and source/sinks file
    file_path = os.path.join(path,set_up_file)
    with open(file_path, 'r') as f:
        data_dict = yaml.load(f, Loader=yaml.CLoader)

    total_horizontal_roads = data_dict['horizontal_roads']['total_number']
    total_vertical_roads = data_dict['vertical_roads']['total_number']

    simulation_time_interval = data_dict['experiment_constants']['simulation_time_interval'] /3600

    #road spacing
    horizontal_road_length = data_dict['grid_dimensions']['horizontal_length']
    vertical_road_length = data_dict['grid_dimensions']['vertical_length']

    horizontal_road_segments_count = total_vertical_roads - 1
    vertical_road_segments_count = total_horizontal_roads - 1

    horizontal_road_section_length = horizontal_road_length/horizontal_road_segments_count
    vertical_road_section_length = vertical_road_length/vertical_road_segments_count

    # arc number counter
    arc_counter = 0
    horizontal_road_data_dict = {}
    counter=0
    for road_set in data_dict['horizontal_roads']:
        if road_set =='total_number':
            continue
        print(road_set)
        number = data_dict['horizontal_roads'][road_set]['number']
        if number == 'fill':
            number = total_horizontal_roads - len(horizontal_road_data_dict)
        for road in range(int(number)):
            horizontal_road_data_dict[counter] = {}
            horizontal_road_data_dict[counter]['speed'] = data_dict['horizontal_roads'][road_set]['speed']
            counter = counter +1

    vertical_road_data_dict = {}
    counter=0
    for road_set in data_dict['vertical_roads']:
        if road_set =='total_number':
            continue
        number = int(data_dict['vertical_roads'][road_set]['number'])
        if number == 'fill':
            number = total_vertical_roads - len(vertical_road_data_dict)
        for road in range(number):
            vertical_road_data_dict[counter] = {}
            vertical_road_data_dict[counter]['speed'] = data_dict['vertical_roads'][road_set]['speed']
            counter = counter +1

# not needed because of label gen
    #get the number of total arcs needed to then be able to get the correct number of label
    # arc_counter = 0
    # for road_key in horizontal_road_data_dict:
    #     arc_length = horizontal_road_data_dict[road_key]* simulation_time_interval
    #     arc_counter = arc_counter + (horizontal_road_length/arc_length)
    #
    # for i in range(total_vertical_roads):
    #     arc_length = vertical_road_data_dict[road_key] * simulation_time_interval
    #     arc_counter = arc_counter + (vertical_road_length / arc_length)
    #
    # arc_counter = arc_counter * 2

    # need to calulate number of cells on each road according to distance of road and speed

    # need to assign arcs and start building the network

    # need to form a check for the length of the road and the length of arcs
    #   showing where the splits are, there will be at least 3 arcs and if not increasing the splits to make this true

    #
    # to do that I need:
    # the cell length for each road
    # the split distance
    # then increase split distance if split distance/cell length is not >3, add cell length to split distance until it is


    # dictionary with key of set # / road #
    # then value is dictionary with values:
        # cell length
        # speed
########################################################################################################################
    # check road section lengths meet minimum arc requirements
    for road_key in horizontal_road_data_dict:
        arc_length = horizontal_road_data_dict[road_key]['speed'] * simulation_time_interval
        horizontal_road_data_dict[road_key]['arc_length'] = arc_length
        # horizontal_road_section_length = round(horizontal_road_section_length/arc_length,0) * arc_length
        while horizontal_road_section_length < arc_length * 3:
            horizontal_road_section_length = horizontal_road_section_length + arc_length
            horizontal_road_length = horizontal_road_section_length * horizontal_road_segments_count

########################################################################################################################
    for road_key in vertical_road_data_dict:
        arc_length = vertical_road_data_dict[road_key]['speed'] * simulation_time_interval
        vertical_road_data_dict[road_key]['arc_length'] = arc_length
        # vertical_road_section_length = round(vertical_road_section_length/arc_length,0) * arc_length
        while vertical_road_section_length < arc_length * 3:
            vertical_road_section_length = vertical_road_section_length + arc_length
            vertical_road_length = vertical_road_section_length * vertical_road_segments_count

########################################################################################################################
    for road_key in horizontal_road_data_dict:
        horizontal_road_data_dict[road_key]['arcs_in_section'] = round(horizontal_road_section_length / \
                                                                       horizontal_road_data_dict[road_key]['arc_length'], 0)
        horizontal_road_data_dict[road_key]['total_arcs'] = int(
            horizontal_road_data_dict[road_key]['arcs_in_section'] * horizontal_road_segments_count)

########################################################################################################################
    for road_key in vertical_road_data_dict:
        vertical_road_data_dict[road_key]['arcs_in_section'] = round(vertical_road_section_length / \
                                                                 vertical_road_data_dict[road_key]['arc_length'],0)
        vertical_road_data_dict[road_key]['total_arcs'] = int(vertical_road_data_dict[road_key]['arcs_in_section'] * vertical_road_segments_count)


########################################################################################################################
    # so lets start building the arcs
    col_list = ['Start','End','Free_Flow_Speed','Direction']
    data_df = pd.DataFrame(columns=col_list)
    for road_key in horizontal_road_data_dict:
        start = label_gen()
        horizontal_road_data_dict[road_key]['start'] = start
        section_counter = 0
        arc_section_counter = 1
        # horizontal_road_data_dict[road_key]['arcs_in_section'] = round(horizontal_road_section_length / \
        #                                                          horizontal_road_data_dict[road_key]['arc_length'],0)
        # horizontal_road_data_dict[road_key]['total_arcs'] = int(horizontal_road_data_dict[road_key]['arcs_in_section'] * horizontal_road_segments_count)
        horizontal_road_data_dict[road_key]['intersection'] = {}
        for node in range(horizontal_road_data_dict[road_key]['total_arcs']):

            if node == 0:
                node1 = start
            else:
                node1 = node2
            node2 = label_gen()

            # print(node)
            if node == horizontal_road_data_dict[road_key]['total_arcs']-1:
                horizontal_road_data_dict[road_key]['end'] = node2

            # get the break nodes
            if node==horizontal_road_data_dict[road_key]['total_arcs']:
                print(node)
            if arc_section_counter == horizontal_road_data_dict[road_key]['arcs_in_section'] or (arc_section_counter==1 and node==0):
                if arc_section_counter==1 and node==0:
                    horizontal_road_data_dict[road_key]['intersection'][section_counter] = node1
                else:
                    horizontal_road_data_dict[road_key]['intersection'][section_counter] = node2
                    arc_section_counter = 0
                section_counter = section_counter+1

            arc_section_counter = arc_section_counter + 1

            temp_list_e = [node1, node2,horizontal_road_data_dict[road_key]['speed'],'E' ]
            temp_list_w = [node2, node1, horizontal_road_data_dict[road_key]['speed'], 'W']
            temp_df = pd.DataFrame([temp_list_e,temp_list_w], columns=col_list)
            data_df = data_df.append(temp_df)

########################################################################################################################
    for road_key in vertical_road_data_dict:
        # start = label_gen()
        # vertical_road_data_dict[road_key]['start'] = start
        section_counter = 0
        arc_section_counter = 1
        # vertical_road_data_dict[road_key]['arcs_in_section'] = round(vertical_road_section_length / \
        #                                                          vertical_road_data_dict[road_key]['arc_length'],0)
        # vertical_road_data_dict[road_key]['total_arcs'] = int(vertical_road_data_dict[road_key]['arcs_in_section'] * vertical_road_segments_count)
        vertical_road_data_dict[road_key]['intersection'] = {}
        for node in range(vertical_road_data_dict[road_key]['total_arcs']):

            # get the break nodes
            if arc_section_counter == vertical_road_data_dict[road_key]['arcs_in_section']  or (arc_section_counter==1 and node==0):
                # vertical_road_data_dict[road_key]['intersection'][section_counter] = node2
                if arc_section_counter==1 and node==0:
                    node1 = horizontal_road_data_dict[section_counter]['intersection'][road_key]
                    vertical_road_data_dict[road_key]['intersection'][section_counter] = node1
                    start = node1
                    vertical_road_data_dict[road_key]['start'] = start
                    node2 = label_gen()
                else:
                    arc_section_counter = 0
                    node1 = node2
                    node2 = horizontal_road_data_dict[section_counter]['intersection'][road_key]
                    vertical_road_data_dict[road_key]['intersection'][section_counter] = node2

                section_counter = section_counter+1
            else:
                node1 = node2
                node2 = label_gen()

            arc_section_counter = arc_section_counter + 1

            if node == vertical_road_data_dict[road_key]['total_arcs'] - 1:
                vertical_road_data_dict[road_key]['end'] = node2

            temp_list_e = [node1, node2,vertical_road_data_dict[road_key]['speed'],'W' ]
            temp_list_w = [node2, node1, vertical_road_data_dict[road_key]['speed'], 'E']
            temp_df = pd.DataFrame([temp_list_e,temp_list_w], columns=col_list)
            data_df = data_df.append(temp_df)

########################################################################################################################
    # set up source and sink
    total_source = data_dict['source_nodes']['total_number']
    del data_dict['source_nodes']['total_number']
    total_sink = data_dict['sink_nodes']['total_number']
    del data_dict['sink_nodes']['total_number']

    # add them onto the correct side of the grid
    outer_intersections = {}
    outer_intersections['N'] = horizontal_road_data_dict[0]['intersection']
    outer_intersections['N_A'] = list(outer_intersections['N'].keys())
    outer_intersections['S'] = horizontal_road_data_dict[total_horizontal_roads-1]['intersection']
    outer_intersections['S_A'] = list(outer_intersections['S'].keys())
    outer_intersections['W'] = vertical_road_data_dict[0]['intersection']
    outer_intersections['W_A'] = list(outer_intersections['W'].keys())
    outer_intersections['E'] = vertical_road_data_dict[total_vertical_roads-1]['intersection']
    outer_intersections['E_A'] = list(outer_intersections['E'].keys())

    outer_intersections['N_rk'] =

    for source_set in data_dict['source_nodes']:
        source_set_dict = data_dict['source_nodes'][source_set]
        grid_location = source_set_dict['grid_location']
        road_loaction = source_set_dict['road_location']
        ufph = source_set_dict['uniform_flow_per_hour']
        if road_loaction=="mid":
            pop_l = lambda x: round(len(x)/2)
        elif road_loaction=="top":
            pop_l = lambda x: len(x)-1
        else: # road_loaction == "bottom":
            pop_l = lambda x: 0
        try:
            node_index = outer_intersections[grid_location+"_A"].pop(pop_l(outer_intersections[grid_location+"_A"]))
            node = outer_intersections[grid_location][node_index]
        except:
            print("no more intersection nodes on:\t" + str(grid_location))
            print("fatal data entry error")
            # return
        sink_node = label_gen()

        # need to get the road it is on for the speed
        # need to determine how to link it into the network
        node1 =
        node2 =
        road_key =

        # self.length = self.free_flow_speed * simulation_time_interval
        # self.max_vehicles = self.length / vehicle_length
        # self.cell_travel_time = simulation_time_unit
        # self.cell_travel_time_list= [self.cell_travel_time]
        # #
        # self.max_flow = CTM_function.flow_density_max_flow(cell=self,
        #                                                    vehicle_type_dict=vehicle_type_dict,
        #                                                    vehicle_length=vehicle_length,
        #                                                    dt_val=simulation_time_unit)
        # self.backwards_wave_speed = CTM_function.flow_density_bws(cell=self,
        #                                          vehicle_length= vehicle_length,
        #                                          vehicle_type_dict=vehicle_type_dict)
        # self.cell_capacity = self.max_vehicles



        temp_list1 = [node1, node2, vertical_road_data_dict[road_key]['speed'], 'W']
        temp_df1 = pd.DataFrame([temp_list1], columns=col_list)
        data_df1 = data_df.append(temp_df1)

    for sink_set in data_dict['sink_nodes']:
        sink_set_dict = data_dict['sink_nodes'][sink_set]
        grid_location = sink_set_dict['grid_location']
        road_loaction = sink_set_dict['road_location']
        ufph = sink_set_dict['uniform_flow_per_hour']
        if road_loaction=="mid":
            pop_l = lambda x: round(len(x)/2)
        elif road_loaction=="top":
            pop_l = lambda x: len(x)-1
        else: # road_loaction == "bottom":
            pop_l = lambda x: 0
        try:
            node_index = outer_intersections[grid_location+"_A"].pop(pop_l(outer_intersections[grid_location+"_A"]))
            node = outer_intersections[grid_location][node_index]
        except:
            print("no more intersection nodes on:\t" + str(grid_location))
            print("fatal data entry error")
            # return

    temp_list = [node1, node2, vertical_road_data_dict[road_key]['speed'], 'W']
    temp_df = pd.DataFrame([temp_list1], columns=col_list)
    data_df = data_df.append(temp_df1)

# Then create the sink file with that designation, and insert the uniform flow per hour

########################################################################################################################
    # write to file
    # filename = data_dict['filename']
    # path = data_dict['path']
    # data_df.to_csv(os.path.join(path,filename),sep=',')

    arc_capacity = {}
    arc_cost = {}
    arc_set = set()
    for item in data_df.iterrows():
        # arc_capacity[item[1][0], item[1][1]] = item[1][3]
        arc_cost[item[1][0], item[1][1]] = item[1][2]
        arc_set.add((item[1][0], item[1][1]))

    import networkx as nx

    network_graph = nx.from_pandas_edgelist(data_df, 'Start', 'End', edge_attr='Free_Flow_Speed',
                                                 create_using=nx.DiGraph)
    pos = nx.kamada_kawai_layout(network_graph)
    nx.draw(network_graph, pos=pos, with_labels=True, node_size=200, alpha=0.3, arrows=True)
    nx.draw_networkx_edge_labels(network_graph, pos, edge_labels=arc_cost, label_pos=0.3, font_size=7)
    ax = plt.gca()
    ax.set_ylim(-1,1)
    ax.set_xlim(-1, 1)
    #build a df
    #write to file

    # return
