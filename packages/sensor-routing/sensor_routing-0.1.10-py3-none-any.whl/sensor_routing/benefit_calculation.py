import json
import os
import time
import math
import copy
from collections import defaultdict

# number_of_classes = 6


# Utility Functions
def calculate_distance(point1, point2):
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx**2 + dy**2)


def normalize(value, min_value, max_value):
    """Normalizes a value given the minimum and maximum range."""
    if max_value == min_value:
        return 0  # Avoid division by zero
    return (value - min_value) / (max_value - min_value)

def inverted_normalize(value, min_value, max_value):
    """Normalizes a value given the minimum and maximum range."""
    if max_value == min_value:
        return 0  # Avoid division by zero
    return 1-((value - min_value) / (max_value - min_value))

def find_max_min(data):
    """Returns the maximum and minimum values from a dataset."""
    if not data:
        raise ValueError("The dataset is empty.")
    
    max_value = max(data)
    min_value = min(data)
    
    return max_value, min_value


def normalize_data(data):
    """Normalize distances and membership values (benefits) in the dataset."""
    
    point_class_value = {}
    normalized_point_membership_value_score = {}
    point_class = {}

    # Step 1: Collect distances and class membership values across all points
    distances = []
    membership_values = []

    for road_id, road_data in data.items():
        segments = road_data["segments"]

        for segment_id, segment_data in segments.items():
            points = segment_data.get('points', {})
            if not points:
                continue  # Skip segments without points
            
            for point_id, point_data in points.items():
                # Collect distance and membership values
                distance = point_data.get('distance_to_segment')
                membership_value = point_data['membership_values'][point_data['class'] - 1]
                
                # Check if valid distance and membership_value exist
                if distance is not None and membership_value is not None:
                    distances.append(distance)
                    membership_values.append(membership_value)

                    # Save to point_class_value and point_class for future use
                    point_class_value[(road_id, segment_id, point_id)] = membership_value
                    point_class[(road_id, segment_id, point_id)] = point_data['class']

    # Step 2: Ensure there are values to normalize
    if not distances or not membership_values:
        raise ValueError("No distances or membership values found for normalization.")

    # Step 3: Calculate max and min for distances and membership values
    max_distance_value, min_distance_value = find_max_min(distances)
    max_class_value, min_class_value = find_max_min(membership_values)

    # Step 4: Normalize distances and membership values
    for (road_id, segment_id, point_id), membership_value in point_class_value.items():
        # Normalize membership values
        normalized_membership_value = normalize(membership_value, min_class_value, max_class_value)
        normalized_point_membership_value_score[(road_id, segment_id, point_id)] = normalized_membership_value
        
        # Access point data
        road_key = str(road_id) if isinstance(road_id, int) else road_id
        segment_key = str(segment_id) if isinstance(segment_id, int) else segment_id
        point_data = data[road_key]['segments'][segment_key]['points'][point_id]
        
        # Normalize distance
        distance = point_data['distance_to_segment']
        normalized_distance = inverted_normalize(distance, min_distance_value, max_distance_value)
        
        # Step 5: Update the dataset with normalized values
        point_data['normalized_distance'] = normalized_distance
        point_data['normalized_benefit'] = normalized_membership_value

    return data

# Core Functions

def load_data(file_path):
    """Load JSON data from the specified file."""
    with open(file_path, "r") as f:
        return json.load(f)


def calculate_individual_benefits(data, number_of_classes):
    """Calculate benefits for each road and segment."""
    road_benefit_score = {}
    segment_benefit_score = {}
    
    for road_id, road_data in data.items():
        segments = road_data["segments"]
        
        # Initialize road benefit score
        road_benefit_score[road_id] = {i: 0 for i in range(1, number_of_classes)}
        segment_benefit_score[road_id] = {}

        for segment_id, segment_data in segments.items():
            points = segment_data.get("points", {})
            
            # Skip empty segments
            if not points:
                continue
            
            segment_key = int(segment_id)
            segment_benefit_score[road_id][segment_key] = {i: 0 for i in range(1, number_of_classes)}
            
            for point_id, point_data in points.items():
                point_class = point_data['class']
                membership_value = point_data['membership_values'][point_class - 1]
                distance = point_data['distance_to_segment']
                # Use normalized distance and membership values here
                normalized_value = point_data.get('normalized_benefit', 0)
                distance_multiplier = point_data.get('normalized_distance', 0)
                #distance_multiplier=1
                segment_benefit_score[road_id][segment_key][point_class] += normalized_value * distance_multiplier

            # Sum up benefits for the road
            for i in range(1, number_of_classes):
                road_benefit_score[road_id][i] += segment_benefit_score[road_id][segment_key][i]
    
    return road_benefit_score, segment_benefit_score


def structure_data(data, road_benefit_score, segment_benefit_score,number_of_classes):
    """Structure data into a dictionary ready for output."""
    structured_data = {}
    default_benefit = {i: 0 for i in range(1, number_of_classes)}
    for road_id, road_data in data.items():
        road_id = int(road_id)
        structured_data[road_id] = {
            'id': road_id,
            'name': road_data["name"],
            "maxspeed": road_data.get("maxspeed"),
            "is_oneway": road_data.get("is_oneway"),
            "highway_type": road_data["highway_type"],
            'total_benefit': road_benefit_score[str(road_id)],
            "segments": {}
        }

        segments = road_data['segments']
        for segment_id, segment_data in segments.items():
            segment_key = int(segment_id)
            benefit = segment_benefit_score[str(road_id)][segment_key] if segment_key in segment_benefit_score[str(road_id)] else None

            segment_structure = {
                "segment_start_id": segment_data["segment_start_id"],
                "segment_end_id": segment_data["segment_end_id"],
                "segment_start_coordinate": tuple(segment_data["segment_start_coordinate"][0]),
                "segment_end_coordinate": tuple(segment_data["segment_end_coordinate"][0]),
                "number_of_points": segment_data['number_of_points'],
                'points': {},
                "benefit": default_benefit if benefit is None else benefit,
            }
            structured_data[road_id]["segments"][segment_key] = segment_structure
            points = segment_data.get('points', {})
            for point_id, point_data in points.items():
                point_coordinates = tuple(point_data['point_coordinates'])
                point_benefit = point_data['normalized_benefit']

                structured_data[road_id]["segments"][segment_key]['points'][point_id] = {
                    'point_coordinates': point_coordinates,
                    'distance_to_segment': point_data['distance_to_segment'],
                    'point_benefit': point_benefit,
                    "class": point_data['class']
                }

    return structured_data


def save_json(data, file_path):
    """Save JSON data to a file."""
    with open(file_path, 'w') as f:
        json.dump(data, f)


def process_segments_by_class(structured_data, lower_benefit_limit,number_of_classes):
    """Sort and filter segments by benefit for each class."""
    # print(repr(structured_data))
    segment_benefits_by_class = defaultdict(list)

    for road_id, road_data in structured_data.items():
        for segment_id, segment_data in road_data['segments'].items():
            for class_id in range(1, number_of_classes):
                benefit = segment_data['benefit'][class_id]
                if benefit > lower_benefit_limit:
                    segment_benefits_by_class[class_id].append(
                        (segment_data["segment_start_id"], segment_data["segment_end_id"], road_id, segment_id, benefit)
                    )

    top_segments_by_class = {}
    for class_, segment_benefits in segment_benefits_by_class.items():
        sorted_segment_benefits = sorted(segment_benefits, key=lambda x: x[4], reverse=True)
        top_segments_by_class[class_] = sorted_segment_benefits

    return top_segments_by_class


def process_summary_data(all_data):
    """Summarize data by calculating the number of one-way and two-way segments."""
    number_of_one_way_segments = len([segment for segment in all_data if segment['is_oneway'] == 1])
    number_of_two_way_segments = len([segment for segment in all_data if segment['is_oneway'] == 0])

    return {
        'number_of_top_segments': len(all_data),
        'number_of_one_way_segments': number_of_one_way_segments,
        'number_of_two_way_segments': number_of_two_way_segments
    }


def benefit_calculation(working_directory, lower_benefit_limit,number_of_classes):
    # Start timer
    start_time = time.time()
    #number_of_classes+=1
    # Load data
    workdir = os.path.join(os.getcwd(), working_directory)
    transient_dir = os.path.join(workdir, "transient")
    read_file_path = os.path.join(transient_dir, "pm_output.json")
    benefits_path = os.path.join(transient_dir, "bc_benefits_output.json")
    data = load_data(read_file_path)
    number_of_classes+=1
    # Normalize distances and benefits
    normalized_data = normalize_data(data)
    
    # Calculate benefits
    road_benefit_score, segment_benefit_score = calculate_individual_benefits(normalized_data,number_of_classes)
    
    # Structure data
    structured_data = structure_data(data, road_benefit_score, segment_benefit_score,number_of_classes)
    
    # Save benefits data
    save_json(structured_data, benefits_path)
    
    debug_path = os.path.join(transient_dir, "debug")
    
    with open(os.path.join(debug_path,'bc_benefits_output_tabbed.json'), 'w') as f:
        json.dump(structured_data, f, indent=4)
    
    # Process top segments by class
    top_segments_by_class = process_segments_by_class(structured_data, lower_benefit_limit,number_of_classes)
    
    # Prepare data for top benefits output
    all_data = []
    for class_, segments in top_segments_by_class.items():
        for segment in segments:
            class_data = {
                'segment_start_id': segment[0],
                'segment_start_coordinate': structured_data[segment[2]]['segments'][segment[3]]['segment_start_coordinate'],
                'segment_end_id': segment[1],
                'segment_end_coordinate': structured_data[segment[2]]['segments'][segment[3]]['segment_end_coordinate'],
                'road_id': segment[2],
                'segment_id': segment[3],
                'benefit': segment[4],
                'class': class_,
                'highway_type': structured_data[segment[2]]['highway_type'],
                'is_oneway': structured_data[segment[2]].get('is_oneway')
            }
            all_data.append(copy.deepcopy(class_data))
    
    all_data_sorted=sorted(all_data, key=lambda x: x['benefit'], reverse=True)
    # Add summary data
    summary_data = process_summary_data(all_data)
    all_data_sorted=[summary_data]+all_data_sorted
    
    # Save top benefits data
    top_benefits_path = os.path.join(transient_dir, "bc_top_benefits_output.json")
    save_json(all_data_sorted, top_benefits_path)
    
    
    
    with open(os.path.join(debug_path,'bc_top_benefits_output_tabbed.json'), 'w') as f:
        json.dump(all_data_sorted, f, indent=4)
    
    # End timer and print execution time
    end_time = time.time()
    # print(f"Execution Time: {end_time - start_time:.2f} seconds")


# Call the main function with the file paths and other parameters
if __name__ == "__main__":
    benefit_calculation(
        working_directory = 'work_dir/sample_data', # This is the working directory
        lower_benefit_limit=1, # This is the lower benefit limit for filtering segments
        number_of_classes=6, # This is the number of classes
    )

