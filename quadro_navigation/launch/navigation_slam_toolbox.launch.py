from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution

from launch.launch_description_sources import PythonLaunchDescriptionSource
import os


def generate_launch_description():

    share_dir = get_package_share_directory('quadro_navigation')
    params_file_path = os.path.join(share_dir,'config','nav2_params.yaml')
    map_dir = os.path.join(get_package_share_directory('quadro_slam'),'maps','industrial_warehouse.yaml')
    rviz_config_file = os.path.join(share_dir,'config','nav.rviz')
    nav2_launch_path = os.path.join(get_package_share_directory('nav2_bringup'),'launch','bringup_launch.py')
    slam_toolbox_path = os.path.join(get_package_share_directory('slam_toolbox'),'launch','online_async_launch.py')
    params_file = os.path.join(share_dir,'config','mapper_params_online_async.yaml')

    use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false'
    )
    map_arg_cmd = DeclareLaunchArgument(
        'map',
        default_value = map_dir
    )
    params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value = params_file_path
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    map_ = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            nav2_launch_path
        ),
        launch_arguments={
            "use_sim_time" : use_sim_time,
            "map" : map_,
            "params_file" : params_file
        }.items()
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
        use_sim_time_cmd,
        map_arg_cmd,
        params_file_cmd,
        rviz_node,
        navigation_launch
        #slam_toolbox_launch

    ])