<p align="center">
<img width="250" alt="ROS2UE5" src="https://github.com/user-attachments/assets/3b8fb4f0-2fba-44ae-9528-c8fc1e182ccb" />
</p>

# ROS2UE5-tools
![Under Construction](https://img.shields.io/badge/status-under%20construction-orange?logo=vlcmediaplayer&logoColor=ffffff)
![Author](https://img.shields.io/badge/author-Manuel%20Eiter-blue)
![Static Badge](https://img.shields.io/badge/Patiiiiiii-UNSAFE-red?logo=pipx&logoColor=red&logoSize=Auto)
![Using Unreal Engine](https://img.shields.io/badge/Unreal%20Engine-purple?logo=unrealengine)
![Using ROS2 Humble](https://img.shields.io/badge/ROS2%20Humble-green?logo=ros)


# Unreal Engine Configuration and Launch Workflow

This repository contains scripts for setting up and managing configurations for launching an Unreal Engine project. The scripts allow you to create a configuration file (`config.json`), convert robot meshes to FBX for compatibility with Unreal, and finally launch the Unreal Engine project with the appropriate configuration.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Overview of Scripts](#overview-of-scripts)
    - [setup_config.py](#setup_configpy)
    - [read_config_and_convert.py](#read_config_and_convertpy)
    - [main_launch.py](#main_launchpy)
3. [Configuration Process](#configuration-process)
4. [Conversion to FBX](#conversion-to-fbx)
5. [Launching Unreal Engine](#launching-unreal-engine)
6. [How to Use](#how-to-use)
7. [Example Workflow](#example-workflow)

---

## Getting Started

To quickly set up **ROS2UE5** and all its dependencies, including **ROS2**, **ROS Bridge**, **SeqLog**, and optional tools like **Blender**, follow the steps outlined in our [Setup Guide](SETUP.md). This guide includes a ready-to-use setup script that automates the installation of all required software, making it easy to get started with simulations.

### Quick Setup Instructions

1. Clone this repository and navigate to the project directory:
   ```bash
   git clone https://github.com/ManuETR/ROS2UE5-tools.git
   cd ROS2UE5-tools
   ```

2. Run the setup script to install all dependencies:
   ```bash
   sudo ./setup.sh
   ```

3. During the installation, you will be asked if you want to install **Blender**, which is required for certain tools. If you're planning to use those tools, choose "Yes" when prompted.

For detailed installation instructions and information about the tools and plugins included in this project, refer to the [Setup Guide](SETUP.md).

### Manual Setup

If you prefer to manually install the dependencies, refer to the step-by-step instructions in the [Setup Guide](SETUP.md) for more information on how to install ROS2, ROS Bridge, and other tools necessary for the **ROS2UE5** plugin.


## Overview of Scripts

### `setup_config.py`

The `setup_config.py` script is used to create the main configuration file (`config.json`). This script asks the user for various settings, including the environment, robots, ROS bridge settings, logging configuration, and the Unreal project path. It saves all these settings in a structured JSON format that is later used when launching the Unreal Engine project.

**Key Features:**
- Prompts for environment settings (map, weather, time).
- Allows the addition of multiple robots with customizable positions, subscribers, and controllers.
- Configures ROS bridge settings (IP and port).
- Enables logging options (logging frequency, destination).
- Prompts for the Unreal project path, which will be stored in the `config.json` file.

### `read_config_and_convert.py`

This script processes the `config.json` file and checks if any robots' names refer to `.sdf` or `.urdf` files. If these files are detected, the script verifies whether they exist, then launches a Blender command to convert them to FBX format. This conversion ensures that the robot meshes are compatible with Unreal Engine.

**Key Features:**
- Reads the `config.json` file.
- Identifies robot names that refer to `.sdf` or `.urdf` files.
- Checks if the specified files exist.
- Launches Blender in background mode to convert the files to FBX.

### `main_launch.py`

This is the main script that orchestrates the entire process of setting up, converting, and launching the Unreal Engine project. 

**Process Flow:**
1. **Check for `config.json`**: If the config file exists, the user is prompted whether they want to override it.
2. **Create Config**: If no config file exists or the user wants to override it, `setup_config.py` is executed to create a new config.
3. **Convert to FBX**: If a new config file is created, the user is asked whether they want to convert robot meshes to FBX using `read_config_and_convert.py`.
4. **Launch Unreal Engine**: The script launches Unreal Editor with the specified project and config file.

**Key Features:**
- Ensures that a config file is present (creates one if necessary).
- Prompts for FBX conversion only when a new config is created.
- Reads the Unreal project path from the config file.
- Launches Unreal Engine with or without the config file.

---

## Configuration Process

### Step 1: Config Creation

The `setup_config.py` script is used to create a new configuration file (`config.json`). The script will ask for the following:

1. **Environment Settings**:
   - Map: A string name for the environment map.
   - Weather: Options include "sunny" (default), "cloudy", "rainy", or "snow".
   - Time: Options are "noon" (default) or "night".

2. **Robot Setup**:
   - You can add one or more robots.
   - Robot names can be either strings or paths to `.sdf` or `.urdf` files.
   - Positions for each robot are specified as `[x, y, z]` coordinates (default: `[0, 0, 0]`).
   - You can add default JointStateSubscribers and JointControllers with customizable topics and modes.

3. **ROS Settings**:
   - Set the IP address and port for the ROS bridge (default IP: `127.0.0.1`, default port: `9090`).

4. **Logging Configuration**:
   - Enable or disable logging (default: enabled).
   - Set the logging frequency (default: 1).
   - Specify the logging destination (only "Seq" is supported, with default endpoint `http://localhost:5341`).

5. **Unreal Project Path**:
   - The full path to your Unreal project file (`.uproject`).

Once this information is provided, the configuration is saved in `config.json`.

---

## Conversion to FBX

When robot files are specified as `.sdf` or `.urdf`, they need to be converted to FBX format for Unreal compatibility. 

The `read_config_and_convert.py` script is responsible for reading the `config.json` file and checking if any robot names point to such files. If the files exist, the script will:

1. Use Blender to convert the files to FBX format.
2. Ensure that the converted FBX files are ready for Unreal Engine use.

Blender needs to be installed for this process, and the script will run Blender in background mode to perform the conversions.

---

## Launching Unreal Engine

The `main_launch.py` script handles the launch of Unreal Engine. It uses the Unreal project path and optional config file to launch the Unreal Editor. 

- **With a config file**: If a `config.json` file exists, it will be passed as a parameter to Unreal Engine.
- **Without a config file**: If no config is found or the user opts not to create one, Unreal will be launched without the config parameter.

The Unreal project path is either read from the config file or provided by the user during setup.

---

## How to Use

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/your-repository.git
   cd your-repository
   ```

2. Install **Blender** if you plan to convert `.sdf` or `.urdf` files to FBX.

3. Run the main script to launch the setup, conversion, and Unreal Engine:
   ```bash
   python main_launch.py
   ```

---

## Example Workflow

1. **Check for Configuration**:
   - If no `config.json` is found, the script will prompt to create a new one:
     ```
     No config file found. Do you want to create a new config file? (y/n): y
     ```

2. **Create Config**:
   - If the user chooses to create a new config, the script will ask for various environment settings, robots, ROS, and logging options, as well as the Unreal project path:
     ```
     Enter map name: MyMap
     Enter weather (sunny/cloudy/rainy/snow) [sunny]: sunny
     Enter time (noon/night) [noon]: night
     Do you want to add a robot? (y/n): y
     Enter robot name: /path/to/robot.urdf
     Enter robot position [x, y, z] [0, 0, 0]: [1, 2, 3]
     Add default JointStateSubscriber? (y/n) [y]: y
     Enter JointStateSubscriber topic [/joint/states]: /robot/joint/states
     Add default JointController? (y/n) [y]: y
     Enter the full path to your Unreal project (.uproject file): /path/to/MyUnrealProject.uproject
     ```

3. **Convert Meshes to FBX**:
   - After creating a new config, the user is prompted whether to convert robot meshes to FBX:
     ```
     Do you want to convert robot meshes to FBX? (y/n): y
     ```

4. **Launch Unreal**:
   - Once the setup and conversion are done, the Unreal Editor is launched:
     ```
     Launching Unreal Editor with command: UnrealEditor /path/to/MyUnrealProject.uproject --config=config.json
     ```

If no config file is created or found, Unreal is launched without the `--config` parameter.

---
