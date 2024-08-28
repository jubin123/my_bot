import os

from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
    # Modify this according to the camera packages used.(`v4l2_camera` is a popular package video for linux in short.)

        Node(
            package='v4l2_camera',  
            executable='v4l2_camera_node',
            output='screen',
            parameters=[{
                'image_size': [640,480],
                'camera_frame_id': 'camera_link_optical'
                }]
    )
    ])