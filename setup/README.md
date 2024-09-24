# Setup Configuration Script

This repository contains a Python script that generates a configuration file (`config.json`) based on user input. The configuration includes settings for the environment, robots, ROS bridge, and logging options.

## Features

- Prompts the user for various settings such as environment, robots, ROS bridge details, and logging preferences.
- Allows the addition of multiple robots with customizable positions, subscribers, and controllers.
- Default values are provided where applicable for ease of use.
- The final configuration is saved as a `config.json` file.

## Configuration Structure

The generated `config.json` file will have the following structure:

```json
{
    "environment": {
        "map": "PandaMap",
        "weather": "sunny",
        "time": "noon"
    },
    "robots": [
        {
            "robot": "panda",
            "position": [0, 0, 5],
            "subscribers": [
                {
                    "type": "JointStateSubscriber",
                    "topic": "/joint/states"
                }
            ],
            "controllers": [
                {
                    "type": "JointController",
                    "mode": "kinematic"
                }
            ]
        }
    ],
    "ros": {
        "bridge": {
            "ip": "127.0.0.1",
            "port": 9090
        }
    },
    "logging": {
        "enable": true,
        "frequency": 1,
        "destination": {
            "type": "Seq",
            "endpoint": "http://localhost:5341"
        }
    }
}
```

## Setup Instructions

To use this script and generate a configuration file, follow these steps:

### Prerequisites

- Python 3.x installed on your system.
- Basic knowledge of terminal/command line usage.

### Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/ManuETR/ROS2UE5-tools.git
cd ROS2UE5-tools/setup
```

### Running the Script

Run the Python script from the command line:

```bash
python setup_config.py
```

### Follow the Prompts

The script will prompt you for various settings:

1. **Environment Settings**:
   - **Map**: Enter any string for the map name.
   - **Weather**: Choose from "sunny" (default), "cloudy", "rainy", or "snow".
   - **Time**: Choose between "noon" (default) or "night".

2. **Robot Configuration**:
   - You will be asked whether you want to add a robot.
   - **Robot Name**: Any string value.
   - **Position**: Enter a list of three numbers in the format `[x, y, z]` (default: `[0, 0, 0]`).
   - **Subscribers**: Optionally add a default `JointStateSubscriber` with a customizable topic (default: `/joint/states`).
   - **Controllers**: Optionally add a default `JointController` with kinematic mode.
   - You can repeat the process to add multiple robots.

3. **ROS Settings**:
   - **IP Address**: Enter the IP address for the ROS bridge (default: `127.0.0.1`).
   - **Port**: Enter the port for the ROS bridge (default: `9090`).

4. **Logging Settings**:
   - **Enable Logging**: Choose whether to enable logging (default: `true`).
   - **Log Frequency**: Set the frequency of logging (default: `1`).
   - **Log Type**: Currently, only `Seq` is supported (default: `Seq`).
   - **Endpoint**: Enter the endpoint for logging (default: `http://localhost:5341`).

### Output

After answering all prompts, the script will generate a `config.json` file with the specified settings in the repository folder.

### Example

An example terminal interaction might look like this:

```bash
$ python setup_config.py
Enter the map: MyCustomMap
Enter the weather [sunny, cloudy, rainy, snow] (default: sunny): 
Enter the time of day [noon, night] (default: noon): night
Do you want to add a robot? (y/n, default: n): y
Enter the robot name (any string): panda1
Enter the robot position (format: [x, y, z], default: [0, 0, 0]): [1, 2, 3]
Add default JointStateSubscriber? (y/n, default: y): y
Enter the topic for JointStateSubscriber (default: /joint/states): /panda1/joint/states
Add default JointController? (y/n, default: y): y
Do you want to add another robot? (y/n, default: n): n
Enter the ROS bridge IP (default: 127.0.0.1): 
Enter the ROS bridge port (default: 9090): 
Enable logging? (true/false, default: true): 
Enter the log frequency (default: 1): 
Enter log type (default: Seq) [Seq]: 
Enter the log endpoint (default: http://localhost:5341): 
Configuration file 'config.json' has been created!
```
