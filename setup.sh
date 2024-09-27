#!/bin/bash

# Setup script for RoboDemo and its dependencies

echo "Starting setup for RoboDemo and dependencies..."

# Check for sudo permissions
if [ "$EUID" -ne 0 ]; then 
  echo "Please run as root or use sudo"
  exit
fi

# Update package list
echo "Updating package list..."
sudo apt update && sudo apt upgrade -y

# Install prerequisites for ROS2 and Docker
echo "Installing prerequisites..."
sudo apt install curl gnupg2 lsb-release software-properties-common -y

# Step 1: Install ROS2 Humble Hawksbill
echo "Installing ROS2 Humble Hawksbill..."

# Add ROS2 GPG key
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
# Add ROS2 source to the system
sudo sh -c 'echo "deb http://packages.ros.org/ros2/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/ros2-latest.list'

# Update package list and install ROS2
sudo apt update
sudo apt install ros-humble-desktop -y

# Source ROS2 in bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
source ~/.bashrc

# Step 2: Install ROS Bridge
echo "Installing ROS Bridge..."
sudo apt install ros-humble-rosbridge-suite -y

# Step 3: Install Docker
echo "Installing Docker..."
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt install docker.io -y

# Enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Step 4: Install Seq using Docker
echo "Installing Seq (Datalust) using Docker..."
sudo docker run --name seq -d --restart unless-stopped -e ACCEPT_EULA=Y -p 5341:80 datalust/seq

# Check if script is run from within ROS2UE5-tools repository
if [ -d ".git" ] && [ -f "README.md" ] && grep -q "ROS2UE5-tools" README.md; then
  echo "Detected that the script is running from within the ROS2UE5-tools repository."
  # Move one directory level up to clone the repositories there
  cd ..
else
  echo "Running script outside of ROS2UE5-tools repository."
fi

# Step 5: Clone the ROS2UE5 Plugin
echo "Cloning ROS2UE5 Plugin..."
git clone https://github.com/ManuETR/ROS2UE5.git

# Instructions for adding the plugin to Unreal
echo "ROS2UE5 Plugin cloned. Please copy it to your Unreal Project's Plugins directory."

# Step 6: Check if ROS2UE5-tools is installed
if [ -d "./ROS2UE5-tools" ]; then
  echo "ROS2UE5-tools repository already exists in the current directory."
else
  echo "Cloning ROS2UE5 Automation Tools..."
  git clone https://github.com/ManuETR/ROS2UE5-tools.git
  echo "ROS2UE5 Automation Tools repository cloned."
fi

# Step 7: Clone the SeqLog Plugin (Optional)
echo "Cloning SeqLog Plugin..."
git clone https://github.com/ManuETR/SeqLog.git
echo "SeqLog Plugin is now available. Copy it to your Unreal Project's Plugins directory if required."

# Step 8: Optional - Install Blender
echo "Blender is required for one of the tools. Would you like to install Blender now? (y/n)"
read -r install_blender

if [[ "$install_blender" == "y" || "$install_blender" == "Y" ]]; then
  echo "Installing Blender..."
  sudo apt install blender -y
  echo "Blender has been installed."
else
  echo "Skipping Blender installation."
fi

# Final message
echo "Setup complete. Please make sure to add the ROS2UE5 and SeqLog plugins to your Unreal Engine project."
echo "You can access Seq by visiting http://localhost:5341 in your browser."
echo "To launch ROS Bridge, run: ros2 launch rosbridge_server rosbridge_websocket_launch.xml"

echo "Setup script finished!"
