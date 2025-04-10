from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

import os
from ament_index_python import get_package_share_directory


def generate_launch_description():

    use_sim_time_arg = DeclareLaunchArgument('use_sim_time',
                                             default_value='false')
    
    use_sim_time = LaunchConfiguration('use_sim_time')
    
    share_dir = get_package_share_directory('quadro_slam')
    rviz_launch_path = os.path.join(get_package_share_directory('quadro_description'),'launch','display.launch.py')
    slam_toolbox_path = os.path.join(get_package_share_directory('slam_toolbox'),'launch','online_async.launch.py')
    params_file = os.path.join(share_dir,'config','mapper_params_online_async.yaml')



    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            rviz_launch_path
        )
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
        rviz_launch,
        slam_toolbox_launch
    ])