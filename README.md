# quadro
Quadro is a fully integrated 4-wheel autonomous robot platform inspired from Tortoisebot by Rigbetel Labs developed using ROS 2. This repository includes all necessary packages, configurations, and launch files for both simulation and real-world deployment. It supports SLAM, autonomous navigation, sensor integration, and more.

✨ Features

🧭 **SLAM (Simultaneous Localization and Mapping) using [SLAM Toolbox]**

📍 Autonomous Navigation powered by the Nav2 Stack

🕹️ Teleoperation for manual control

🌍 Gazebo Simulation with a detailed URDF model

🔧 Ready for real robot deployment with hardware interfaces

🖥️ RViz2 for visualization and debugging

🗂️ Modular and well-organized ROS 2 workspace

🛠️ **Built With**

ROS 2 (Humble)

Gazebo

Nav2 Stack

SLAM Toolbox

Cartographer

RViz2

Custom URDF + xacro-based robot model

📂 **Structure**

quadro_description/ – URDF, meshes, and xacro files

quadro_bringup/ – Launch files for simulation and real-world usage

quadro_navigation/ – Navigation configs (Nav2)

quadro_slam/ – SLAM setup

quadro_firmware/ – Interface for motor drivers


# Install Dependencies
**YDLidar SDK**
In home directory
```shell
sudo apt install cmake pkg-config
sudo apt-get install python swig
sudo apt-get install python-pip
git clone https://github.com/YDLIDAR/YDLidar-SDK.git
```
```shell
mkdir -p YDLidar-SDK/build
cd YDLidar-SDK/build
cmake ..
make
sudo make install
cd ..
pip install .
```

**ydliar_ros2_driver**
```shell
cd /to_your_workspace/src
git clone https://github.com/YDLIDAR/ydlidar_ros2.git
```
```shell
cd to_your_workspace
colcon build
```

**Cartographer**
```shell
  sudo apt install ros-humble-cartographer*
```
