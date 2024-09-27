import json
import subprocess
import time
import os
import sys
import argparse

def read_config(config_file):
    """Read the JSON config file and return the data."""
    with open(config_file, 'r') as f:
        return json.load(f)

def start_rosbridge():
    """Start ROS Bridge using the appropriate ROS2 launch command."""
    print("Starting ROS Bridge...")
    rosbridge_cmd = ["ros2", "launch", "rosbridge_server", "rosbridge_websocket_launch.xml"]
    return subprocess.Popen(rosbridge_cmd)

def start_unreal_engine(unreal_exec_path, ue_project, ue_scenario, iteration):
    """Start Unreal Engine with the specified project and scenario."""
    print(f"Starting Unreal Engine (iteration {iteration})...")
    ue_cmd = [
        unreal_exec_path,  # Unreal Engine executable path
        ue_project,
        f'-config="{ue_scenario}"',
        "-autostart=true",
        f"-iteration={iteration}"
    ]
    return subprocess.Popen(ue_cmd)

def wait_for_unreal_to_start(timeout):
    """Wait for Unreal Engine to be ready with a timeout."""
    print("Waiting for Unreal Engine to start...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        time.sleep(1)
        # TODO: Implement Unreal Engine readiness check here
        # For now, we just wait for the timeout
    print("Unreal Engine is ready.")

def start_ros2_launch(ros2_pkg, ros2_launch):
    """Start the ROS2 launch file for the simulation."""
    print(f"Starting ROS2 launch: {ros2_pkg} {ros2_launch}...")
    ros2_cmd = ["ros2", "launch", ros2_pkg, ros2_launch]
    return subprocess.Popen(ros2_cmd)

def run_simulation(simulation, ue_project, unreal_exec_path):
    """Run the simulation and manage Unreal/ROS processes."""
    iterations = simulation["iterations"]
    ue_scenario = simulation["ueScenario"]
    ros2_pkg = simulation["ros2Pkg"]
    ros2_launch = simulation["ros2Launch"]
    timeout = simulation["timeout"]
    max_sim_time = simulation["maxSimTime"]

    for i in range(1, iterations + 1):
        print(f"\n--- Starting Iteration {i} ---")
        
        # Start Unreal Engine
        unreal_process = start_unreal_engine(unreal_exec_path, ue_project, ue_scenario, i)
        wait_for_unreal_to_start(timeout)

        # Start ROS2 launch process
        ros2_process = start_ros2_launch(ros2_pkg, ros2_launch)
        ros2_start_time = time.time()

        # Monitor processes with max simulation time
        while True:
            unreal_running = unreal_process.poll() is None
            ros2_running = ros2_process.poll() is None
            elapsed_time = time.time() - ros2_start_time

            if not unreal_running or not ros2_running:
                print("One of the processes has stopped.")
                break

            if elapsed_time > max_sim_time:
                print("Max simulation time reached. Stopping processes.")
                break

            time.sleep(1)

        # Stop both Unreal Engine and ROS2 processes if still running
        if unreal_running:
            print("Stopping Unreal Engine...")
            unreal_process.terminate()
            unreal_process.wait()

        if ros2_running:
            print("Stopping ROS2 process...")
            ros2_process.terminate()
            ros2_process.wait()

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Automated Simulation Runner")
    parser.add_argument(
        "--config", 
        type=str, 
        default="simulation_config.json", 
        help="Path to the simulation configuration file (default: simulation_config.json)"
    )
    parser.add_argument(
        "--unreal-path", 
        type=str, 
        required=False, 
        help="Path to the Unreal Engine executable"
    )
    
    # Parse the arguments
    args = parser.parse_args()

    # Default Unreal Engine paths for different platforms
    if sys.platform == "win32":
        default_unreal_exec_path = r"C:\Program Files\Epic Games\UE_5.3\Engine\Binaries\Win64\UnrealEditor.exe"
    elif sys.platform == "linux":
        default_unreal_exec_path = "/path/to/UnrealEditor"  # Replace this with the actual path on your Linux system
    else:
        print("Unsupported platform. This script only supports Windows and Linux.")
        sys.exit(1)

    # Use the command-line argument if provided, otherwise use the default path
    unreal_exec_path = args.unreal_path if args.unreal_path else default_unreal_exec_path

    # Read the configuration
    config = read_config(args.config)

    # Start ROS Bridge
    rosbridge_process = start_rosbridge()

    try:
        # Iterate over all simulations
        for simulation in config["simulations"]:
            run_simulation(simulation, config["ueProject"], unreal_exec_path)
    finally:
        # Ensure that ROS Bridge is stopped at the end
        if rosbridge_process.poll() is None:
            print("Stopping ROS Bridge...")
            rosbridge_process.terminate()
            rosbridge_process.wait()

if __name__ == "__main__":
    main()
