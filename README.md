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

## Running simulation and controling the mobile robot

To start the simulation in gazebo world.In terminal go to `~/dev_ws` and run below command

    source install/setup.bash
    ros2 launch my_bot launch_sim.launch.py world:=./src/my_bot/worlds/obstacles.world

<!-- Reference-style-image:  -->
![Gazebo Output][ros2_controller_main_gazebo]


If you also want to see visulation in `rviz2`.In new terminal go to `~/dev_ws` and run below command

    rviz2 -d src/my_bot/config/main.rviz

<!-- Reference-style-image:  -->
![Rviz2 Output][ros2_controller_main_rviz2]

To Test the control the robot with keyboard.

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

[drive_bot_lidar_depth_camera_requirements]: resources/Images/drive_bot_lidar_depth_camera_requirements.png "drive_bot_lidar_depth_camera_requirements"