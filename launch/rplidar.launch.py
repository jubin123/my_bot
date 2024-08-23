import os
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    return LaunchDescription([
# Modify this according to the lidar package used.
        Node(
            package='rplidar_ros',
            executable='rplidar_composition',
            output='screen',
            parameters=[{
                # 'serial_port': '/dev/ttyUSB0',
                #we can instead use "/dev/serial/by-id" or "/dev/serial/by-path" to assign the same serial ports each time when we are having multiple devices.
                'serial_port': '/dev/serial/by-path/platform-fd500000.pcie-pci-0000:01:00.0-usb-0:1.3:1.0-port0', 
                'frame_id': 'laser_frame', 
                'angle_compensate': True,
                'scan_mode': 'Standard'
            }]
        )
    ])