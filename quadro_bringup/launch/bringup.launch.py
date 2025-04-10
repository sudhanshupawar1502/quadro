import os
from ament_index_python import get_package_share_directory
from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    ydlidar_dir = os.path.join(get_package_share_directory('ydlidar_ros2_driver'),'launch','ydlidar_launch.py')

    ydlidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            ydlidar_dir
        )
    )

    firmware_node = Node(
        package='quadro_firmware',
        executable='differential.py',
        name='differential'
    )

    return LaunchDescription([
        ydlidar_launch,
        firmware_node
    ])