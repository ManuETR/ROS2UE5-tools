import json
import os
import subprocess

# The path to the Python script that needs to be run via Blender
CONVERT_SCRIPT_PATH = "conversion-tool/convert_to_fbx.py"

def is_robot_a_file(robot_name):
    """Check if the robot name is a file path to an .sdf or .urdf file."""
    return robot_name.lower().endswith(('.sdf', '.urdf'))

def check_file_exists(file_path):
    """Check if the given file path exists on the file system."""
    return os.path.isfile(file_path)

def get_file_directory(file_path):
    """Extract the directory from the file path."""
    return os.path.dirname(file_path)

def check_blender_installed():
    """Check if Blender is installed on the system by calling it."""
    try:
        subprocess.run(['blender', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def prompt_blender_install():
    """Prompt the user to install Blender if it's not found."""
    print("Blender is not installed. Please install Blender from: https://www.blender.org/download/")

def run_blender_command(directory_path):
    """Run the Blender command to convert the file using the specified script."""
    try:
        # Run Blender in background mode with the given Python script
        result = subprocess.run([
            'blender', '--background', '--python', CONVERT_SCRIPT_PATH, '--', directory_path
        ], check=True, capture_output=True)
        print(f"Processed {directory_path} with Blender (output hidden).")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running Blender command: {e.stderr.decode('utf-8')}")

def process_config():
    """Main function to process the config.json file."""
    config_file = "config.json"

    # Read the config.json file
    if not os.path.exists(config_file):
        print(f"Error: {config_file} not found.")
        return

    with open(config_file, 'r') as f:
        config = json.load(f)

    # Check if Blender is installed
    if not check_blender_installed():
        prompt_blender_install()
        return

    # Check each robot's name in the robots array
    robots = config.get("robots", [])
    for robot in robots:
        robot_name = robot.get("robot", "")

        if is_robot_a_file(robot_name):
            print(f"Robot '{robot_name}' appears to be a file path.")

            # Check if the file exists
            if check_file_exists(robot_name):
                print(f"File '{robot_name}' exists.")
                directory_path = get_file_directory(robot_name)
                print(f"Passing directory '{directory_path}' to Blender.")

                run_blender_command(directory_path)
            else:
                print(f"Error: File '{robot_name}' does not exist.")
        else:
            print(f"Robot '{robot_name}' is not a file path, skipping.")

if __name__ == "__main__":
    process_config()
