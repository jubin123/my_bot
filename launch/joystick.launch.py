from launch import LaunchDescription
from launch_ros.actions import Node

import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='my_bot' #<---  CHANGE ME

    joy_params = os.path.join(get_package_share_directory(package_name),'config','joystick.yaml')

    joy_node = Node(
            package='joy',
            executable='joy_node',
            parameters=[joy_params],
         )
    
    teleop_node = Node(
            package='teleop_twist_joy', 
            executable='teleop_node',
            name = 'teleop_node', # We explicitly names the node teleop_node. This is because the default "node name" ("teleop_twist_joy_node")(that we need to set the parameters properly) doesn’t match the "executable name" which, while technically fine, is quite confusing. By explicitly naming it, we force everything to line up.
            parameters=[joy_params],
            remappings=[('/cmd_vel', '/diff_cont/cmd_vel_unstamped')]
            )

    return LaunchDescription([
        joy_node ,
        teleop_node       
    ])