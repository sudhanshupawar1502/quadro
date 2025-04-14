# use slam toolbox only when you have odometery data from Wheel encoders, IMU, etc,.
# Can be used for simulation since odom data is provided by the gazebo plugin


from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

import os
from ament_index_python import get_package_share_directory


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time',
                                             default_value='true')
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    share_dir = get_package_share_directory('quadro_slam')
    slam_toolbox_path = os.path.join(get_package_share_directory('slam_toolbox'),'launch','online_async.launch.py')
    params_file = os.path.join(share_dir,'config','mapper_params_online_async.yaml')
    rviz_confifg = os.path.join(share_dir,'config','slam.rviz')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_confifg]

    )

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            slam_toolbox_path
        ),
        launch_arguments={
            'params_file' : params_file,
            'use_sim_time' : use_sim_time
        }.items()
    )

    return LaunchDescription([
        use_sim_time_arg,
        rviz_node,
        slam_toolbox_launch
    ])