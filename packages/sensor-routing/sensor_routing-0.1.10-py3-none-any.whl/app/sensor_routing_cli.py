import argparse
import time

# first part
from point_mapping import point_mapping

# second part
from benefit_calculation import benefit_calculation

# third part
from path_finding import path_finding

# fourth part
from route_finding import route_finding


#pydantic Look it up


parser = argparse.ArgumentParser(description="Sensor routing program")
parser.add_argument(
    "--sn", "-segment_number", type=int, help="how many segments will be visited per cluster", default=2
)
parser.add_argument(
    "--lbf",
    "-lower_benefit_limit",
    type=int,
    help="lower benefit limit for the benefit calculation",
    default=0.5,
)

parser.add_argument('--tl', '-time_limit', type=int, help='time limit for the agent', default=8)
parser.add_argument('--oo', '-optimization_objective', type=str, help='optimization objective for the agent (d for distance, t for time)', default='d')
parser.add_argument('--mai', '-max_aco_iteration', type=int, help='max aco iteration for the agent', default=500)
parser.add_argument('--an', '-ant_no', type=int, help='ant number for the agent', default=50)

args=parser.parse_args()

segments_number_per_class=args.sn
lower_benefit_limit=args.lbf
time_limit=args.tl
optimization_objective=args.oo
max_aco_iteration=args.mai
ant_no=args.an

# segments_number_per_class=2
# lower_benefit_limit=0.5
# time_limit=8
# optimization_objective='d'
# max_aco_iteration=500
# ant_no=50

total_number_of_classes=9
max_distance=50

# osm_data="20240918-142800_osm_data_31468.geojson" 
# class_data="mems6_plain_ascii_EPSG31468.csv"
osm_data= '20250109-124054_osm_data_25832.geojson' # Mueglitz osm data
class_data='Mueglitz_extended_9Cluster_EPSG25832-2.csv' # 9 cluster Mueglitz data
point_mapping_output='pm_output.json'
benefit_calculation_output_benefit='bc_benefits_output.json'
benefit_calculation_output_top_benefit='bc_top_benefits_output.json'
path_finding_output='pf_output.json'
solution_path='solution.json'



# parameters ={
#     total_number_of_classes=2
#     ...
# }
# sensor_routing(**parameters)
# with open("parameters.json", "w") as f:
#     parameters = json.load(f)
    
# sensor_routing(**parameters)

def sensor_routing(total_number_of_classes,segments_number_per_class, max_distance, osm_data,class_data,time_limit,optimization_objective,max_aco_iteration,ant_no, point_mapping_output, benefit_calculation_output_benefit, benefit_calculation_output_top_benefit, path_finding_output,solution_path): #add paths!
    

    start_time = time.time()
    
    benefit_calculation_input=point_mapping_output
    path_finding_input_roads=benefit_calculation_output_benefit
    path_finding_input_benefits=benefit_calculation_output_top_benefit
    route_finding_input=path_finding_output
    
    point_mapping(
        osm_data,
        class_data,
        point_mapping_output,
        max_distance
    )
    
    print('point mapping done')
    
    benefit_calculation(
        benefit_calculation_input,
        benefit_calculation_output_benefit,
        benefit_calculation_output_top_benefit,
        lower_benefit_limit,
        total_number_of_classes,
    )
    
    print('benefit_calculation done')
    
    path_finding(
        path_finding_input_roads,
        path_finding_input_benefits,
        segments_number_per_class,
        total_number_of_classes,
        path_finding_output
    )
    
    print('path finding done')
    
    route_finding(
        route_finding_input,
        solution_path,
        total_number_of_classes,
        time_limit,
        optimization_objective,
        max_aco_iteration,
        ant_no
    )
    
    print('route finding done')
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time, "seconds")
    print("Execution time:", execution_time / 60, "minutes")
    print("all done")

if __name__ == "__main__":
    sensor_routing(
        total_number_of_classes,
        segments_number_per_class,
        max_distance,
        osm_data,
        class_data,
        time_limit,
        optimization_objective,
        max_aco_iteration,
        ant_no,
        point_mapping_output,
        benefit_calculation_output_benefit,
        benefit_calculation_output_top_benefit,
        path_finding_output,
        solution_path,
    )
