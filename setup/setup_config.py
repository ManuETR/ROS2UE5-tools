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

def ask_position():
    """Ask the user for a robot position and parse it as a list."""
    response = input("Enter the robot position (format: [x, y, z], default: [0, 0, 0]): ")
    if not response:
        return [0, 0, 0]
    try:
        position = json.loads(response)
        if len(position) == 3 and all(isinstance(i, (int, float)) for i in position):
            return position
        else:
            print("Invalid position format. Please enter a list of three numbers.")
            return ask_position()
    except json.JSONDecodeError:
        print("Invalid format. Please enter in the format [x, y, z].")
        return ask_position()

def ask_add_robot():
    """Ask if the user wants to add a robot and gather its details."""
    robots = []
    while True:
        add_robot = input("Do you want to add a robot? (y/n, default: n): ").lower()
        if add_robot == 'y':
            robot_name = input("Enter the robot name (any string): ")

            position = ask_position()

            add_subscriber = input("Add default JointStateSubscriber? (y/n, default: y): ").lower() or 'y'
            if add_subscriber == 'y':
                topic = input("Enter the topic for JointStateSubscriber (default: /joint/states): ") or "/joint/states"
                subscribers = [{"type": "JointStateSubscriber", "topic": topic}]
            else:
                subscribers = []

            add_controller = input("Add default JointController? (y/n, default: y): ").lower() or 'y'
            if add_controller == 'y':
                controllers = [{"type": "JointController", "mode": "kinematic"}]
            else:
                controllers = []

            robot = {
                "robot": robot_name,
                "position": position,
                "subscribers": subscribers,
                "controllers": controllers
            }
            robots.append(robot)
        else:
            break
    return robots

def create_config():
    # Environment setup
    environment = {
        "map": ask_with_default("Enter the map",  default="''", allowed=None),
        "weather": ask_with_default("Enter the weather", default="sunny", allowed=["sunny", "cloudy", "rainy", "snow"]),
        "time": ask_with_default("Enter the time of day", default="noon", allowed=["noon", "night"])
    }

    # Robots setup
    robots = ask_add_robot()

    # ROS setup
    ros = {
        "bridge": {
            "ip": ask_with_default("Enter the ROS bridge IP", default="127.0.0.1"),
            "port": ask_with_default("Enter the ROS bridge port", default="9090")
        }
    }

    # Logging setup
    logging = {
        "enable": ask_with_default("Enable logging? (true/false)", default="true") == "true",
        "frequency": int(ask_with_default("Enter the log frequency", default="1")),
        "destination": {
            "type": ask_with_default("Enter log type (default: Seq)", default="Seq", allowed=["Seq"]),
            "endpoint": ask_with_default("Enter the log endpoint", default="http://localhost:5341")
        }
    }

    unreal_project = get_user_input("Enter the full path to your Unreal project (.uproject file)")


    # Combine everything into the final config
    config = {
        "environment": environment,
        "robots": robots,
        "ros": ros,
        "logging": logging,
        "unreal_project": unreal_project
    }

    # Write to JSON file
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)

    print("Configuration file 'config.json' has been created!")

if __name__ == "__main__":
    create_config()
