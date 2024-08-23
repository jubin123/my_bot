# `my_bot` package

### Introduction

This is a ROS2 project of a two wheel robot with simulation in Gazebo. The project is build and tested for ROS_DISTRO `humble`.Can run in `foxy` after installing right package for foxy.You can verify your `ROS_DISTRO` and `ROS_VERSION` with below command (assuming you have sourced proper ROS underlay if You are having Different ROS installion)

    printenv | grep -i ROS

### Setting up the project with dependency

Open a terminal (should be in the home directory by default)

    mkdir dev_ws/src
    git clone https://github.com/jubin123/my_bot.git
    cd ..
    colcon build --symlink-install

Install the required package and dependency.(note: change  `humble` to `foxy` to run in fROS_DISTRO foxy)

    sudo apt install ros-humble-xacro ros-humble-joint-state-publisher-gui

Installing Gazebo 

    sudo apt install ros-humble-gazebo-ros-pkgs

### Running simulation and controling the mobile robot

To start the simulation in gazebo world.In terminal go to `~/dev_ws` and run below command

    source install/setup.bash
    ros2 launch my_bot launch_sim.launch.py world:=./src/my_bot/worlds/obstacles.world

If you also want to see visulation in `rviz2`.In new terminal go to `~/dev_ws` and run below command

    rviz2 -d src/my_bot/config/drive_bot.rviz

To Test the control the robot with keyboard.

    ros2 run teleop_twist_keyboard teleop_twist_keyboard

