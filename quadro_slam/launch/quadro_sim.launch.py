import os
from launch_ros.actions import Node
from launch import LaunchDescription
from ament_index_python import get_package_share_directory
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration,PathJoinSubstitution


def generate_launch_description():
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')

    share_dir = get_package_share_directory("quadro_slam")
    slam_toolbox_path = os.path.join(get_package_share_directory("slam_toolbox"), "launch", "online_async_launch.py")
    rviz_config_file = os.path.join(share_dir, 'config', 'slam.rviz')
    params_file = os.path.join(share_dir,'config','mapper_params_online_async.yaml')
    # robot_desc_dir = get_package_share_directory("quadro_description")
    # gazebo_launch_path = os.path.join(robot_desc_dir,'launch','gazebo.launch.py')

    # gazebo_launch  = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(gazebo_launch_path))

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_toolbox_path),
        launch_arguments={
            "params_file" : params_file,
            "use_sim_time" : use_sim_time
        }.items()

        )
    
    rviz_ = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=[
            '-d',rviz_config_file
        ]
    )
    


    return LaunchDescription([
        use_sim_time_arg,
        rviz_,
        # gazebo_launch,
        slam_toolbox_launch
    ])

