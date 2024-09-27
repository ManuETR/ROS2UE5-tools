import json

def ask_with_default(prompt, default=None, allowed=None):
    """Helper function to ask for input with a default value and optional allowed values."""
    if allowed:
        prompt += f" [{', '.join(allowed)}]"
    if default:
        prompt += f" (default: {default})"
    
    response = input(prompt + ": ")
    if not response and default is not None:
        return default
    if allowed and response not in allowed:
        print(f"Invalid input. Allowed options: {', '.join(allowed)}")
        return ask_with_default(prompt, default, allowed)
    return response

def create_json_file():
    restart_bridge = ask_with_default("Restart Bridge? (true/false)", "false", allowed=["true", "false"]).lower() == "true"
    ue_project = ask_with_default("Path to UE Project", "C:/Users/Manuel/Documents/Unreal Projects/RoboDemo/RoboDemo.uproject")
    
    iterations = int(ask_with_default("Number of iterations", "3"))
    name = ask_with_default("Name of simulation", "MoveIt2 Pick and Place Demo")
    ue_scenario = ask_with_default("UE Scenario file", "config.json")
    ros2_launch = ask_with_default("ROS 2 Launch command", "moveit2_tutorials pick_place_demo.launch.py")
    ros2_pkg = ask_with_default("ROS 2 Package", "moveit2_tutorials")
    timeout = int(ask_with_default("Timeout (in seconds)", "3"))
    max_sim_time = int(ask_with_default("Max simulation time (in seconds)", "10"))

    data = {
        "restartBridge": restart_bridge,
        "ueProject": ue_project,
        "simulations": [
            {
                "iterations": iterations,
                "name": name,
                "ueScenario": ue_scenario,
                "ros2Launch": ros2_launch,
                "ros2Pkg": ros2_pkg,
                "timeout": timeout,
                "maxSimTime": max_sim_time
            }
        ]
    }

    with open("simulation_config.json", "w") as json_file:
        json.dump(data, json_file, indent=4)

    print("JSON configuration file 'simulation_config.json' created successfully.")

if __name__ == "__main__":
    create_json_file()