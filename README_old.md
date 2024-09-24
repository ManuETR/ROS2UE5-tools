# Unreal Engine Setup and Launch Documentation

## Overview

This documentation outlines the process for setting up and launching an Unreal Engine project using a Python-based configuration system. The setup involves creating a configuration file that defines environment settings, robot specifications, logging preferences, and the Unreal project path. The configuration file is then utilized to launch the Unreal Engine editor.

## Scripts

### 1. `setup_config.py`

This script is responsible for gathering user inputs and generating a `config.json` file with the necessary configuration settings.

#### User Prompts:
- **Map Name**: Enter any string representing the map.
- **Weather**: Choose between `sunny`, `cloudy`, `rainy`, or `snow` (default: `sunny`).
- **Time**: Choose between `noon` or `night` (default: `noon`).
- **Robots**:
  - Ask if the user wants to add a robot.
  - For each robot, prompt for:
    - Robot Name: Any string.
    - Position: Enter in the format `[x, y, z]` (default: `[0, 0, 0]`).
    - Default subscribers and controllers (optional):
      - Topic for `JointStateSubscriber` (default: `/joint/states`).
      - Mode for `JointController` (default: `kinematic`).
- **ROS Bridge Settings**:
  - IP address (default: `127.0.0.1`).
  - Port (default: `9090`).
- **Logging Settings**:
  - Enable logging (default: `true`).
  - Logging frequency (default: `1`).
  - Logging endpoint (default: `http://localhost:5341`).
- **Unreal Project Path**: The full path to the Unreal project file (`.uproject`).

### 2. `read_config_and_convert.py`

This script reads the generated `config.json` file to identify robot names that are paths to STL or URDF files. If any such paths are found, it checks for their existence and invokes Blender for conversion to FBX format.

#### Functionality:
- Checks if Blender is installed on the system. If not, prompts the user to install it.
- For each robot path, checks if it exists. If it does, it runs:
  ```bash
  blender --background --python convert_to_fbx.py -- {path_to_robot}
  ```
- Processes subdirectories recursively to find all robot files.

### 3. `main_launch.py`

This script orchestrates the overall launch process of Unreal Engine based on the configuration setup.

#### Workflow:
1. **Check for Existing Config**: 
   - If a `config.json` file exists, prompts whether to override it.
   - If the user chooses not to override, it will use the existing config.
   - If no config exists, prompts the user to create one.
   
2. **Create Config**: 
   - Calls `setup_config.py` to generate a new configuration file.
   - If a new config is created, prompts the user to convert robot meshes to FBX.

3. **Prompt for Unreal Project**: 
   - If the Unreal project path is not found in the config file, prompts the user to enter it.

4. **Launch Unreal Engine**: 
   - Executes the Unreal Engine editor with the project path and configuration file as parameters.
   ```bash
   UnrealEditor {project_path} --config=config.json
   ```

### Example Usage

1. **Run the Setup Script**:
   To create a new configuration file:
   ```bash
   python setup_config.py
   ```

2. **Launch Unreal Engine**:
   To start the process and launch Unreal Engine:
   ```bash
   python main_launch.py
   ```

### Notes
- Ensure that Blender is installed for the conversion of robot meshes.
- The configuration file (`config.json`) will be created in the same directory as the scripts.
- Make sure to adjust permissions if executing scripts on Linux/MacOS (e.g., `chmod +x script.py`).

## Conclusion

This setup allows for a flexible and customizable way to configure your Unreal Engine project. By managing settings in a single JSON configuration file, it simplifies the process of launching and running your simulations with varying environments and robot configurations.
