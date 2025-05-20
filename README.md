# `my_bot` package

## Introduction

This is a ROS2 project of a two wheel robot with simulation in Gazebo. The project is build and tested for ROS_DISTRO `humble`.Can run in `foxy` after installing right package for foxy.You can verify your `ROS_DISTRO` and `ROS_VERSION` with below command (assuming you have sourced proper ROS underlay if You are having Different ROS installion)

    printenv | grep -i ROS

## Setting up the project with dependency

Open a terminal (should be in the home directory by default)

    mkdir dev_ws/src
    git clone https://github.com/jubin123/my_bot.git
    cd ..
    colcon build --symlink-install

Install the required package and dependency.(note: change  `humble` to `foxy` to run in ROS_DISTRO foxy)

    sudo apt install ros-humble-xacro ros-humble-joint-state-publisher-gui

Installing Gazebo 

    sudo apt install ros-humble-gazebo-ros-pkgs

Installing ros2_control dependency

    sudo apt install ros-humble-ros2-control ros-humble-ros2-controllers ros-humble-gazebo-ros2-control

### Setting up and adding dependency for rasperypi

Camera used is `Pi Camera V2`.

In terminal run 

    sudo apt install libraspberrypi-bin v4l-utils ros-humble-v4l2-camera ros-humble-image-transport-plugins

Also, use the `groups` command to confirm you are already in the `video` group (to allow camera access). If not, run `sudo usermod -aG video $USER` (this requires log out/restart to take effect).

To check if it thinks the camera is connected .run 

    vcgencmd get_camera

and we should see `supported=1 detected=1` in response.

We can run `raspistill -k` and the camera stream should come up on the screen, then press `x` and `Enter` to exit.

Then, we can run:

    v4l2-ctl --list-devices

And there should be an entry for `mmal service`, platform `bcm2835-v4l2`, device `/dev/video0`. That tells us that the V4L2 subsystem can see the camera.

To get serial depentency,In terminal run

    sudo apt-get install libserial-dev

In mobile robot add aditional repo and build

    git clone https://github.com/jubin123/serial.git
    git clone -b humble https://github.com/jubin123/diffdrive_arduino.git

Change `humble` to `main` if using foxy ros distro.

## Controling the mobile robot (_Simulation_ or *Physical Robot*)

Start running in either _physical robot_ mode or in _simulation_ mode

- To start the Physical Robot.In terminal go to `~/dev_ws` and run below command

        source install/setup.bash
        ros2 launch my_bot launch_robot.launch.py

    **OR**

- To start the simulation in gazebo world.In terminal go to `~/dev_ws` and run below command

        source install/setup.bash
        ros2 launch my_bot launch_sim.launch.py world:=./src/my_bot/worlds/obstacles.world

<!-- Reference-style-image:  -->
![Gazebo Output][ros2_controller_main_gazebo]


If you also want to see visulation in `rviz2`.In new terminal go to `~/dev_ws` and run below command (_optional step_)

    rviz2 -d src/my_bot/config/main.rviz

<!-- Reference-style-image:  -->
![Rviz2 Output][ros2_controller_main_rviz2]

Robot (In _physical_ or _simulation_ mode) can be controled with either _Controller_  or with _keyboard_ .

- To use _controller_.In terminal run below command (note : it is automatly launched in _simulation_ mode ,not required to run seperatly.)

        source install/setup.bash
        ros2 launch my_bot joystick.launch.py

    **OR**

- TTo use _keyboard_.In terminal go to `~/dev_ws` and run below command

        ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/diff_cont/cmd_vel_unstamped


## Additional infomation :

### Decompressing and republishing image data

Installing plugins `image_transport` 

    sudo apt install ros-humble-image-transport-plugins

Installing plugins `rqt-image-view` for viewing compressed image.

    sudo apt install ros-humble-rqt-image-view

To run `rqt-image-view` for viewing compressed image.

    ros2 run rqt_image_view rqt_image_view

To list all the image_transport avliable currently 

    ros2 run image_transport list_transports

#### How to create a compressed_image or uncompressed_image and topics (creating a image transport):

Then, to republish a topic we need to specify the type of the input, then the type of the output. We also need to remap some topics, which are in the format `{in/out}/{type}` (with no type for uncompressed/raw). For example, to remap from a `compressed` input topic to a `raw` output topic we use:

    ros2 run image_transport republish compressed raw --ros-args -r in/compressed:=/camera/image_raw/compressed -r out:=/camera/my_uncompressed_image

Note, with `image_transport`, `raw` means "uncompressed" and has nothing to do with the "raw" in `image_raw`.

#### How to add `depth_camera` support : (Is not be used in current projects,might be intrigated in future)

To see add depth camera . In `robot.urdf.xacro` ,comment `<xacro:include filename="camera.xacro" />` and uncomment `<xacro:include filename="depth_camera.xacro" />` shown below as requirement.

<!-- Reference-style-image:  -->
![Rviz2 Output][drive_bot_lidar_depth_camera_requirements]

If you also want to see visulation in `rviz2`.In new terminal go to `~/dev_ws` and run below command

    rviz2 -d src/my_bot/config/drive_bot_lidar_depth_camera.rviz

<!-- Reference-style-image:  -->
![Rviz2 Output][drive_bot_lidar_depth_camera_rviz2]

### Gamepads in Linux

To check our gamepad works in Linux, we want to install some useful tools:

    sudo apt install joystick jstest-gtk evtest

We can test if the linux is seeing gamepad in 2 ways:

1. Running `evtest` in terminal.(new driver)

2. Experiment with `jstest` and its graphical counterpart `jstest-gtk`. (old driver)

### Connecting to Joysticks/Gamepads in ROS

To see all avaliable device:

    ros2 run joy joy_enumerate_devices

To get gamepad input in ros topic:

    ros2 run joy joy_node # <-- Run in first terminal and it will provide controler's value in topic '/joy'.
    ros2 topic echo /joy # <-- Run in second terminal and will display output

If you want to get values in a GUI :

Install package:

    git clone https://github.com/jubin123/joy_tester.git

Once installed, it can be run with 
    
    ros2 run joy_tester test_joy

### twist_stamper

Install twist_stamper:

    sudo apt install ros-humble-twist-stamper

### Setting up SLAM

Install slam-toolbox:

    sudo apt install ros-humble-slam-toolbox

Set up config (can use referrnce copy and mofify it)

    cp /opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml src/my_bot/config/

Run slam_toolbox (after launching gazebo and add map in rviz to see map generation add slam_toolbox panel to save the map(or can use ros services))

    ros2 launch slam_toolbox online_async_launch.py slam_params_file:=./src/my_bot/config/mapper_params_online_async.yaml use_sim_time:=true

Run the slam_toolbox again after updating the config file with file name to load the map

<!-- Reference-style-image:  -->
![Rviz2 Output][drive_bot_lidar_camera_slam_toolbox_rviz2]

### Setting up Nav2

Install Nav2:

    sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*

Localization with AMCL:

1. seting up map_server (make sure fixframe in rviz is in map and set map topic Durability Policy to Transient Local):

        ros2 run nav2_map_server map_server --ros-args -p yaml_filename:=my_map_save.yaml -p use_sim_time:=true

2. lifecycle_bringup of map_server:

        ros2 run nav2_util lifecycle_bringup map_server

3. seting up Amcl:

        ros2 run nav2_amcl amcl --ros-args -p use_sim_time:=true

4. lifecycle_bringup of amcl:

        ros2 run nav2_util lifecycle_bringup amcl

Give a initial pose estimate in rviz if required.


<!-- Image References:  -->
[drive_bot_lidar_gazebo]: resources/Images/drive_bot_lidar_gazebo.png "Gazebo Output"
[drive_bot_camera_gazebo]: resources/Images/drive_bot_camera_gazebo.png "Gazebo Output"
[drive_bot_lidar_camera_gazebo]: resources/Images/drive_bot_lidar_camera_gazebo.png "Gazebo Output"
[ros2_controller_main_gazebo]: resources/Images/ros2_controller_main_gazebo.png "Gazebo Output"

[drive_bot_lidar_rviz2]: resources/Images/drive_bot_lidar_rviz2.png "Rviz2 Output"
[drive_bot_camera_rviz2]: resources/Images/drive_bot_camera_rviz2.png "Rviz2 Output"
[drive_bot_lidar_camera_rviz2]: resources/Images/drive_bot_lidar_camera_rviz2.png "Rviz2 Output"
[ros2_controller_main_rviz2]: resources/Images/ros2_controller_main_rviz2.png "Rviz2 Output"
[drive_bot_lidar_depth_camera_rviz2]: resources/Images/drive_bot_lidar_depth_camera_rviz2.png "Rviz2 depth_camera Output"
[drive_bot_lidar_camera_slam_toolbox_rviz2]: resources/Images/drive_bot_lidar_camera_rviz2_slam_slamtoolbox.png "Rviz2 slam_toolbox Output"

[drive_bot_lidar_depth_camera_requirements]: resources/Images/drive_bot_lidar_depth_camera_requirements.png "drive_bot_lidar_depth_camera_requirements"