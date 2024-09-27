import os
import subprocess
import sys
import json

# Path to necessary scripts
SETUP_CONFIG_SCRIPT = "config-creator/setup_config.py"
CONVERT_MESH_SCRIPT = "conversion-tool/read_config_and_convert.py"
CONFIG_FILE = "config.json"

def check_config_exists():
    """Check if the config.json file exists."""
    return os.path.exists(CONFIG_FILE)

def prompt_override_config():
    """Ask the user if they want to override the existing config file."""
    while True:
        user_input = input(f"A config file ({CONFIG_FILE}) already exists. Do you want to override it? (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def prompt_create_config():
    """Ask the user if they want to create a new config file if it doesn't exist."""
    while True:
        user_input = input("No config file found. Do you want to create a new config file? (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def create_config():
    """Run the setup_config.py script to create a new config file."""
    try:
        subprocess.run([sys.executable, SETUP_CONFIG_SCRIPT], check=True)
        print("Config file created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating config: {e}")
        sys.exit(1)

def prompt_convert_meshes():
    """Ask the user if they want to convert meshes to FBX."""
    while True:
        user_input = input("Do you want to convert robot meshes to FBX? (y/n): ").lower()
        if user_input == 'y':
            return True
        elif user_input == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def convert_meshes():
    """Run the read_config_and_convert.py script to convert robot meshes to FBX."""
    try:
        subprocess.run([sys.executable, CONVERT_MESH_SCRIPT], check=True)
        print("Robot meshes converted to FBX successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while converting meshes: {e}")
        sys.exit(1)

def get_unreal_project_from_config():
    """Load Unreal project path from the config file."""
    try:
        with open(CONFIG_FILE, 'r') as config_file:
            config = json.load(config_file)
        return config.get("unreal_project", None)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Failed to decode {CONFIG_FILE}.")
        return None

def prompt_unreal_project():
    """Ask the user for the Unreal project path if it's not in the config."""
    project_path = input("Enter the full path to your Unreal project (.uproject file): ").strip()
    if not os.path.exists(project_path):
        print(f"Error: The project file '{project_path}' does not exist.")
        sys.exit(1)
    return project_path

def launch_unreal(project_path, use_config):
    """Launch Unreal Editor with or without the config file as a parameter."""
    unreal_command = ['UnrealEditor', project_path]
    if use_config and os.path.exists(CONFIG_FILE):
        unreal_command += [f"--config={CONFIG_FILE}"]
    
    print(f"Launching Unreal Editor with command: {' '.join(unreal_command)}")
    
    try:
        subprocess.run(unreal_command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while launching Unreal Editor: {e}")
        sys.exit(1)

def main():
    """Main function to orchestrate the setup and launch process."""
    config_exists = check_config_exists()
    new_config_created = False  # Track if a new config file was created
    unreal_project = None

    # Step 1: Check if config file exists
    if config_exists:
        if prompt_override_config():
            create_config()
            new_config_created = True
            unreal_project = get_unreal_project_from_config()
        else:
            print("Using existing config file...")
            unreal_project = get_unreal_project_from_config()
    else:
        if prompt_create_config():
            create_config()
            new_config_created = True
            unreal_project = get_unreal_project_from_config()
        else:
            print("Proceeding without a config file...")

    # Step 2: Only ask about mesh conversion if a new config file was created
    if new_config_created:
        if prompt_convert_meshes():
            convert_meshes()

    # Step 3: Ask for Unreal project
    if unreal_project:
        project_path = unreal_project
    else:
        project_path = prompt_unreal_project()

    # Step 4: Launch Unreal Editor with or without the config file
    launch_unreal(project_path, use_config=config_exists or new_config_created)

if __name__ == "__main__":
    main()
