import networkx as nx
import json
import time
import math
from collections import defaultdict
import copy
# Constants
# MAX_DISTANCE = 50

# Load network and benefits data
def load_data(network_file_path, benefits_file_path):
    with open(network_file_path, "r") as f:
        roads_data = json.load(f)
    with open(benefits_file_path, "r") as f:
        benefits_data = json.load(f)
    benefits_data = benefits_data[1:]   
    return roads_data, benefits_data

# Calculate distance between two coordinates
def calculate_distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx ** 2 + dy ** 2)

# Build directed graph from roads data
def build_road_network(roads_data):
    road_network = nx.DiGraph()
    for road_id, road_data in roads_data.items():
        max_speed = road_data["maxspeed"]
        segments = road_data["segments"]
        is_oneway = road_data["is_oneway"]
        for segment_id, segment_info in segments.items():
            start = tuple(segment_info["segment_start_coordinate"])
            end = tuple(segment_info["segment_end_coordinate"])
            length = calculate_distance(start, end) / 1000  # in km
            time_cost = length / max_speed  # time = distance / speed
            benefit = segment_info["benefit"]
            class_id = int(max(benefit.items(), key=lambda x: x[1])[0])

            road_network.add_edge(start, end, road=road_id, segment=segment_id, benefit=benefit,
                                  distance=length, time_cost=time_cost, class_id=class_id)
            if not is_oneway:
                road_network.add_edge(end, start, road=road_id, segment=segment_id, benefit=benefit,
                                      distance=length, time_cost=time_cost, class_id=class_id)
    return road_network

# Is the segment valid?
def is_valid_segment(graph, node1, node2):
    return graph.has_edge(node1, node2)

#WHAT!?
# Find the shortest path with fallback for alternate start/end nodes
def find_shortest_path_with_fallback(road_network, start_nodes, end_nodes):
    shortest_path = None
    shortest_path_length = float('inf')
    s_true = None
    e_true = None
    
    for s, e in [(0, 0), (0, 1), (1, 0), (1, 1)]:
        start_0_added=False
        start_1_added=False
        end_0_added=False
        end_1_added=False
        try:
            path = nx.dijkstra_path(road_network, source=start_nodes[s], target=end_nodes[e], weight='distance')
            path_length = nx.dijkstra_path_length(road_network, source=start_nodes[s], target=end_nodes[e], weight='distance')
            if s==0:
                if len(path)==1 or path[1]!=start_nodes[1]:
                    if is_valid_segment(road_network, start_nodes[1], start_nodes[0]):
                        path.insert(0, start_nodes[1])
                        path_length += road_network[start_nodes[1]][start_nodes[0]]['distance']
                        start_1_added=True
                    else:
                        continue
            elif s==1:
                if len(path)==1 or path[1]!=start_nodes[0]:
                    if is_valid_segment(road_network, start_nodes[0], start_nodes[1]):
                        path.insert(0, start_nodes[0])
                        path_length += road_network[start_nodes[0]][start_nodes[1]]['distance']
                        start_0_added=True
                    else:
                        continue
            if e==0:
                if len(path)==1 or path[-2]!=end_nodes[1]:
                    if is_valid_segment(road_network, end_nodes[0], end_nodes[1]):
                        path.append(end_nodes[1])
                        path_length += road_network[end_nodes[0]][end_nodes[1]]['distance']
                        end_1_added=True
                    else:
                        continue
            elif e==1:
                if len(path)==1 or path[-2]!=end_nodes[0]:
                    if is_valid_segment(road_network, end_nodes[1], end_nodes[0]):
                        path.append(end_nodes[0])
                        path_length += road_network[end_nodes[1]][end_nodes[0]]['distance']
                        end_0_added=True
                    else:
                        continue                        
            
            if path_length < shortest_path_length:
                shortest_path_length = path_length
                shortest_path = path
                s_true = s
                e_true = e
                if start_0_added:
                    s_true=0
                if start_1_added:
                    s_true=1
                if end_0_added:
                    e_true=0
                if end_1_added:
                    e_true=1
            # if path[1]!=start_nodes[1] or path[1]!=start_nodes[0]:
            #     continue
            # if path[-2]!=end_nodes[1] or path[-2]!=end_nodes[0]:
            #     continue
            
        except nx.NetworkXNoPath:
            continue
    return shortest_path, s_true, e_true







# Select top segments based on benefits and avoid problematic segments
def select_segments(benefits_data, problematic_segments, segment_number_per_class, total_number_of_classes):
    selected_segment_count = defaultdict(int)
    selected_segments = {}
    for i in range(1, total_number_of_classes + 1):
        selected_segment_count[i] = 0
    for data in benefits_data:
        class_id = data['class']
        if selected_segment_count[class_id] >= segment_number_per_class:
            continue
        start_id = data['segment_start_id']
        end_id = data['segment_end_id']
        if (start_id, end_id) in problematic_segments.values():
            continue
        
        # if any([start_id in values and end_id in values for values in problematic_segments.values()]):
        #     continue
        
        selected_segments[(start_id, end_id)] = data
        selected_segment_count[class_id] += 1
        if all(count >= segment_number_per_class for count in selected_segment_count.values()):
            break

    return selected_segments

def calculate_path_metrics(road_network, path):
    """Calculate total distance and time cost for a given path."""
    path_distance = 0
    path_time_cost = 0
    
    # Iterate over consecutive nodes in the path
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        
        # Ensure the edge exists in the road network
        if road_network.has_edge(current_node, next_node):
            edge_data = road_network[current_node][next_node]
            path_distance += edge_data.get('distance', 0)  # Add distance
            path_time_cost += edge_data.get('time_cost', 0)  # Add time cost
        else:
            raise ValueError(f"No edge between {current_node} and {next_node} in the road network.")
    
    return path_distance, path_time_cost


# Calculate paths between selected segments
def calculate_paths(selected_segments, road_network, problematic_segments, no_path_count,no_path_count_per_id, total_number_of_classes):
    all_paths = []
    is_wend=True
    no_path=False
    calculated_paths = []
    calculated_ids = []
    calculated_id_data = {}
    #no_path_count_per_id={}
    # problematic_segments = {}
    i=1
    for (start_id, end_id), start_data in selected_segments.items():
        if (start_id,end_id) not in no_path_count_per_id.keys():
            no_path_count_per_id[(start_id,end_id)]=0
        start_nodes = [
            tuple(start_data["segment_start_coordinate"]),
            tuple(start_data["segment_end_coordinate"])
        ]
        start_class_id = start_data["class"]
        start_road_id = start_data["road_id"]
        start_segment_id = start_data["segment_id"]
        start_segment_benefit = start_data["benefit"]
        j=1
        for (end_start_id, end_end_id), end_data in selected_segments.items():
            if (end_start_id,end_end_id) not in no_path_count_per_id.keys():
                no_path_count_per_id[(end_start_id,end_end_id)]=0
            end_class_id  = end_data["class"]
            if (start_class_id == end_class_id) and (start_id == end_start_id) and (end_id == end_end_id):
                j+=1
                continue
            
            end_nodes = [
                tuple(end_data["segment_start_coordinate"]),
                tuple(end_data["segment_end_coordinate"])
            ]
            
            end_road_id = end_data["road_id"]
            end_segment_id = end_data["segment_id"]
            end_segment_benefit = end_data["benefit"]

            # Find the shortest path with fallback
            shortest_path, s, e = find_shortest_path_with_fallback(road_network, start_nodes, end_nodes)
            
            if not shortest_path:
                is_wend=False
                no_path=True
                if (start_id, end_id) or (end_start_id, end_end_id) not in problematic_segments:
                    no_path_count += 1
                    
                    
                    if i==1 and no_path_count_per_id[(start_id,end_id)]>=3 and all_paths==[]:
                        problematic_segments[no_path_count] = (start_id, end_id)
                        no_path_count_per_id[(start_id,end_id)]+=1
                        break
                    if i==1:
                        if j==2:
                            if start_segment_benefit>end_segment_benefit:
                                problematic_segments[no_path_count] = (end_start_id, end_end_id)
                                no_path_count_per_id[(end_start_id,end_end_id)]+=1
                                no_path_count_per_id[(start_id,end_id)]+=1
                            else:
                                problematic_segments[no_path_count] = (start_id, end_id)
                                no_path_count_per_id[(start_id,end_id)]+=1
                        else:
                            problematic_segments[no_path_count] = (end_start_id, end_end_id)
                            no_path_count_per_id[(end_start_id,end_end_id)]+=1
                            no_path_count_per_id[(start_id,end_id)]+=1

                    else:
                        problematic_segments[no_path_count] = (end_start_id, end_end_id)
                        no_path_count_per_id[(end_start_id,end_end_id)]+=1
                    # problematic_segments[no_path_count] = (start_id, end_id)
                    
                break
            if s==0:
                actual_start_id = start_id
                
            else:
                actual_start_id = end_id
                
            if e==0:
                actual_end_id=end_start_id
                
            else:
                actual_end_id=end_end_id
                
        
            # path_distance = nx.dijkstra_path_length(road_network, source=shortest_path[0], target=shortest_path[-1], weight='distance')
            # path_time_cost = nx.dijkstra_path_length(road_network, source=shortest_path[0], target=shortest_path[-1], weight='time_cost')
            
            path_distance, path_time_cost = calculate_path_metrics(road_network, shortest_path)
            
            if path_distance==0:
                print(actual_start_id, actual_end_id)
            # Calculate benefits
            benefits = {i: 0 for i in range(1, total_number_of_classes + 1)}
            benefits[start_class_id] += start_segment_benefit
            benefits[end_class_id] += end_segment_benefit
            if actual_start_id not in calculated_ids:
                calculated_ids.append(actual_start_id)
                calculated_id_data[actual_start_id] = start_data
                if actual_start_id==start_data['segment_start_id']:
                    calculated_id_data[actual_start_id]=copy.deepcopy(calculated_id_data[actual_start_id])
                    calculated_id_data[actual_start_id]['used'] = 'start'
                else:
                    calculated_id_data[actual_start_id]=copy.deepcopy(calculated_id_data[actual_start_id])
                    calculated_id_data[actual_start_id]['used'] = 'end'
                
            if actual_end_id not in calculated_ids:
                calculated_ids.append(actual_end_id)
                calculated_id_data[actual_end_id] = end_data
                if actual_end_id==end_data['segment_start_id']:
                    calculated_id_data[actual_end_id]=copy.deepcopy(calculated_id_data[actual_end_id])
                    calculated_id_data[actual_end_id]['used'] = 'start'
                else:
                    calculated_id_data[actual_end_id]=copy.deepcopy(calculated_id_data[actual_end_id])
                    calculated_id_data[actual_end_id]['used'] = 'end'
            calculated_paths.append((actual_start_id, actual_end_id))  # Fix: Use parentheses instead of square brackets
            all_paths.append({
                'start_road_id': start_road_id,
                "start_segment_id": start_segment_id,
                'actual_segment_start_id': actual_start_id,
                'end_road_id': end_road_id,
                "end_segment_id": end_segment_id,
                'actual_segment_end_id': actual_end_id,
                'number_of_segments': len(shortest_path),
                "distance": path_distance,
                "time": path_time_cost,
                "benefit": benefits,
                'start_segment_benefit': start_segment_benefit,
                'end_segment_benefit': end_segment_benefit,
                "path": shortest_path
            })
            j+=1
        i+=1
        if no_path:
            break
    return all_paths, problematic_segments, is_wend, no_path_count, calculated_paths,calculated_id_data,no_path_count_per_id

# TODO: Calculate other paths
def calculate_other_paths(calculated_paths,road_network,all_paths,calculated_id_data,total_number_of_classes):
    for actual_start_id,start_data in calculated_id_data.items():
        if calculated_id_data[actual_start_id]['used']=='start':
            start_nodes = tuple(calculated_id_data[actual_start_id]["segment_start_coordinate"])
        else:
            start_nodes = tuple(calculated_id_data[actual_start_id]["segment_end_coordinate"]    )
        start_road_id = calculated_id_data[actual_start_id]["road_id"]
        start_segment_id = calculated_id_data[actual_start_id]["segment_id"]
        start_segment_benefit = calculated_id_data[actual_start_id]["benefit"]
        start_segment_class_id = calculated_id_data[actual_start_id]["class"]
        
        for actual_end_id, end_data in calculated_id_data.items():
            if actual_start_id==actual_end_id:
                continue
            if (actual_start_id, actual_end_id) in calculated_paths:
                continue
            if calculated_id_data[actual_end_id]['used']=='start':
                end_nodes = tuple(calculated_id_data[actual_end_id]["segment_start_coordinate"])
            else:
                end_nodes = tuple(calculated_id_data[actual_end_id]["segment_end_coordinate"])
            end_road_id = calculated_id_data[actual_end_id]["road_id"]
            end_segment_id = calculated_id_data[actual_end_id]["segment_id"]
            end_segment_benefit = calculated_id_data[actual_end_id]["benefit"]
            end_segment_class_id = calculated_id_data[actual_end_id]["class"]
            try:
                shortest_path= nx.dijkstra_path(road_network, source=start_nodes, target=end_nodes, weight='distance')
            except nx.NetworkXNoPath:
                shortest_path = None
            benefits = {i: 0 for i in range(1, total_number_of_classes + 1)}
            if not shortest_path:
                path_distance=float('inf')
                path_time_cost=float('inf')
                start_segment_benefit=0
                end_segment_benefit=0
            else:
                path_distance=nx.dijkstra_path_length(road_network, source=start_nodes, target=end_nodes, weight='distance')
                path_time_cost=nx.dijkstra_path_length(road_network, source=start_nodes, target=end_nodes, weight='time_cost')
                benefits[start_segment_class_id] += start_segment_benefit
                benefits[end_segment_class_id] += end_segment_benefit
            all_paths.append({
                'start_road_id': start_road_id,
                "start_segment_id": start_segment_id,
                'actual_segment_start_id': actual_start_id,
                'end_road_id': end_road_id,
                "end_segment_id": end_segment_id,
                'actual_segment_end_id': actual_end_id,
                'number_of_segments': len(shortest_path),
                "distance": path_distance,
                "time": path_time_cost,
                "benefit": benefits,
                'start_segment_benefit': start_segment_benefit,
                'end_segment_benefit': end_segment_benefit,
                "path": shortest_path
            })
    return all_paths
# Main function
def path_finding(roads_data_file, benefits_data_file, segment_number_per_class, total_number_of_classes, write_path):
    start_time = time.time()
    roads_data, benefits_data = load_data(roads_data_file, benefits_data_file)
    road_network = build_road_network(roads_data)
    problematic_segments = {}
    is_wend=False
    no_path_count=0
    no_path_count_per_id={}
    while True:
        selected_segments = select_segments(benefits_data, problematic_segments, segment_number_per_class, total_number_of_classes)
        all_paths, problematic_segments, is_wend, no_path_count, calculated_paths, calculated_id_data,no_path_count_per_id = calculate_paths(selected_segments, road_network, problematic_segments, no_path_count,no_path_count_per_id, total_number_of_classes)
        
        if is_wend:
            # calculated_id_data = [data for data in benefits_data if data['segment_start_id'] in calculated_ids or data['segment_end_id'] in calculated_ids]
            all_paths=calculate_other_paths(calculated_paths,road_network,all_paths,calculated_id_data,total_number_of_classes)
            print('done')
            break
        print('not done',no_path_count)
    # all_paths.append(selected_segments)
    write_output(write_path, all_paths)
    with open('c6paths_tabbed.json', 'w') as f:
        json.dump(all_paths, f, indent=4)
    end_time = time.time()
    # print(f"Execution Time: {end_time - start_time:.2f} seconds")
    # print("Paths calculation completed.")

# Write output to JSON file
def write_output(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

# Run the main function
if __name__ == "__main__":
    path_finding(
        roads_data_file='bc_benefits_output.json', #This is the file that contains the road data
        benefits_data_file='bc_top_benefits_output.json', #This is the file that contains the benefits data
        segment_number_per_class=3, #This is the number of segments per class
        total_number_of_classes=16, #This is the total number of classes
        write_path='pf_output.json' #This is the file that will contain the paths
        )
