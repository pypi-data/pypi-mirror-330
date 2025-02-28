import argparse
import time
import json
import os
from pydantic import BaseModel, Field, ValidationError

# first part
from .point_mapping import point_mapping

# second part
from .benefit_calculation import benefit_calculation

# third part
from .path_finding import path_finding

# fourth part
from .route_finding import route_finding

#pydantic

class Config(BaseModel):
    segment_number: int = Field(2, alias="sn", ge=1, le=10, description="Must be between 1 and 10")
    lower_benefit_limit: float = Field(1, alias="lbf", ge=0.0, le=1.0, description="Must be between 0.0 and 1.0")
    time_limit: int = Field(8, alias="tl", gt=0, description="Must be a positive number")
    optimization_objective: str = Field("d", alias="oo", pattern="^(d|t)$", description="Must be 'd' or 't'")
    max_aco_iteration: int = Field(500, alias="mai", gt=0, description="Must be a positive integer")
    ant_no: int = Field(50, alias="an", gt=0, description="Must be a positive integer")
    total_number_of_classes: int = Field(6, alias="cn", gt=0, description="Must be a positive integer")
    is_reversed: bool = Field(False, alias="ir", description="Must be true or false")
    working_directory: str = Field("work_dir", alias="wd", description="Working directory path")
    
    class Config:
        populate_by_name = True

def load_or_create_parameters(working_dir="work_dir", filename="parameters.json"):
    """Loads parameters from a JSON file in the specified working directory or creates it with default values."""
    # Ensure the working directory exists
    os.makedirs(working_dir, exist_ok=True)
    
    parameters_path = os.path.join(working_dir, filename)
    
    print(f"Checking if {parameters_path} exists...")  # Debug print

    if not os.path.exists(parameters_path):
        print("File not found, creating it...")  # Debug print
        
        # Create an instance with default values
        default_config = Config(working_directory=working_dir)
        
        # Use model_dump() to convert the Pydantic model to a dictionary and then write to the file
        default_config_dict = default_config.model_dump(by_alias=True, exclude_unset=False)
        print("Serialized default config:", default_config_dict)  # Debug print

        # Write to the file (this should now work as per the test)
        try:
            with open(parameters_path, "w") as file:
                json.dump(default_config_dict, file, indent=4)
            print(f"⚡ Created default {parameters_path} with values")
        except Exception as e:
            print(f"❌ Error writing to file: {e}")

        # Confirm file creation with a check
        if os.path.exists(parameters_path):
            print(f"✅ File {parameters_path} successfully created!")
        else:
            print(f"❌ Failed to create file at {parameters_path}")

    # Load the parameters from the file
    with open(parameters_path, "r") as file:
        params = json.load(file)
    
    print(f"Loaded parameters from {parameters_path}: {params}")  # Debug print

    return Config(**params)

def parse_args():
    """Parses command-line arguments using argparse."""
    parser = argparse.ArgumentParser(description="Sensor routing program")
    
    parser.add_argument("--sn", "-segment_number", type=int, help="how many segments will be visited per cluster")
    parser.add_argument("--lbf", "-lower_benefit_limit", type=float, help="lower benefit limit for the benefit calculation")
    parser.add_argument("--tl", "-time_limit", type=int, help="time limit for the agent")
    parser.add_argument("--oo", "-optimization_objective", type=str, help="optimization objective for the agent (d for distance, t for time)")
    parser.add_argument("--mai", "-max_aco_iteration", type=int, help="max ACO iteration for the agent")
    parser.add_argument("--an", "-ant_no", type=int, help="ant number for the agent")
    parser.add_argument("--cn", "-total_number_of_classes", type=int, help="total number of classes")
    parser.add_argument("--ir", "-is_reversed", type=bool, help="is the road network reversed")
    parser.add_argument("--wd", "-working_directory", type=str, help="working directory")
    
    args = parser.parse_args()
    
    return {k: v for k, v in vars(args).items() if v is not None}  # Remove None values
    
def get_final_config():
    """Combines JSON config and command-line arguments, with CLI taking priority."""
    cli_args = parse_args()
    working_dir = cli_args.get("wd", "work_dir")  # Get working directory from CLI args or default to "work_dir"
    if __name__== '__main__':
        working_dir='work_dir/sample_data'
    json_config = load_or_create_parameters(working_dir=working_dir)  # Load parameters from JSON or create them
    merged_params = json_config.model_dump(by_alias=True)  # Use model_dump() to get the parameters as a dictionary
    merged_params.update(cli_args)  # Update with command-line args
    
    try:
        return Config(**merged_params)  # Validate final config
    except ValidationError as e:
        print("❌ Configuration Validation Error:", e)
        exit(1)

# ✅ Integrate this function into your main script
if __name__ == "__main__":
    
    config = get_final_config()
    
    # Now, `config` contains validated parameters and can be used in your program
    print("✅ Final Configuration Loaded:")
    print(config)



# parser = argparse.ArgumentParser(description="Sensor routing program")

# parser.add_argument(
#     "--sn", "-segment_number", type=int, help="how many segments will be visited per cluster", default=2
# )
# parser.add_argument(
#     "--lbf",
#     "-lower_benefit_limit",
#     type=int,
#     help="lower benefit limit for the benefit calculation",
#     default=0.5,
# )

# parser.add_argument('--tl', '-time_limit', type=int, help='time limit for the agent', default=8)
# parser.add_argument('--oo', '-optimization_objective', type=str, help='optimization objective for the agent (d for distance, t for time)', default='d')
# parser.add_argument('--mai', '-max_aco_iteration', type=int, help='max aco iteration for the agent', default=500)
# parser.add_argument('--an', '-ant_no', type=int, help='ant number for the agent', default=50)
# parser.add_argument('--cn', '-total_number_of_classes', type=int, help='total number of classes', default=6)
# parser.add_argument('--ir', '-is_reversed', type=bool, help='is the road network reversed (easting-northing reversed problem)', default=False)
# parser.add_argument('--wd', '-working_directory', type=str, help='working directory', default='work_dir')


# args=parser.parse_args()

# segments_number_per_class=args.sn
# lower_benefit_limit=args.lbf
# time_limit=args.tl
# optimization_objective=args.oo
# max_aco_iteration=args.mai
# ant_no=args.an
# total_number_of_classes=args.cn
# is_reversed=args.ir
# workdir=args.wd



# segments_number_per_class=2
# lower_benefit_limit=0.5
# time_limit=8
# optimization_objective='d'
# max_aco_iteration=500
# ant_no=50

#total_number_of_classes=9
max_distance=50

# osm_data="20240918-142800_osm_data_31468.geojson" 
# class_data="mems6_plain_ascii_EPSG31468.csv"
#osm_data= '20250109-124054_osm_data_25832.geojson' # Mueglitz osm data
#class_data='Mueglitz_extended_9Cluster_EPSG25832-2.csv' # 9 cluster Mueglitz data
# point_mapping_output='pm_output.json'
# benefit_calculation_output_benefit='bc_benefits_output.json'
# benefit_calculation_output_top_benefit='bc_top_benefits_output.json'
# path_finding_output='pf_output.json'
# solution_path='solution.json'



# parameters ={
#     total_number_of_classes=2
#     ...
# }
# sensor_routing(**parameters)
# with open("parameters.json", "w") as f:
#     parameters = json.load(f)
    
# sensor_routing(**parameters)

def sensor_routing(total_number_of_classes,segments_number_per_class, max_distance, working_directory,time_limit,optimization_objective,max_aco_iteration,ant_no, is_reversed, lower_benefit_limit):
    

    start_time = time.time()
    
    # benefit_calculation_input=point_mapping_output
    # path_finding_input_roads=benefit_calculation_output_benefit
    # path_finding_input_benefits=benefit_calculation_output_top_benefit
    # route_finding_input=path_finding_output
    
    point_mapping(
        working_directory,
        max_distance,
        is_reversed
    )
    
    print('point mapping done')
    
    benefit_calculation(
        working_directory,
        lower_benefit_limit,
        total_number_of_classes,
    )
    
    print('benefit_calculation done')
    
    path_finding(
        working_directory,
        segments_number_per_class,
        total_number_of_classes,
    )
    
    print('path finding done')
    
    route_finding(
        working_directory,
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
    
    config = get_final_config()
    #config.working_directory='work_dir/sample_data'
    config.is_reversed = True
    
    sensor_routing(
        config.total_number_of_classes,    # cn
        config.segment_number,             # sn
        config.lower_benefit_limit,        # lbf
        config.working_directory,          # wd
        config.time_limit,                 # tl
        config.optimization_objective,     # oo
        config.max_aco_iteration,          # mai
        config.ant_no,                     # an
        config.is_reversed                 # ir
    )
