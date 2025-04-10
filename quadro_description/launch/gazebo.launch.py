from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable,SetLaunchConfiguration,DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration,TextSubstitution
import os
import xacro
from ament_index_python.packages import get_package_share_directory
from pathlib import Path
from launch.substitutions import Command


def generate_launch_description():


    # declare_world_arg = DeclareLaunchArgument(
    #     name='world_file',
    #     default_value='industrial-warehouse.sdf',
    #     description='SDF world file to load'
    # )

    pkg_robot_description = 'quadro_description'

    urdf_file = os.path.join(
        get_package_share_directory('quadro_description'),
        'urdf',
        'quadro.urdf.xacro'
    )

    # Get URDF file path
    urdf_file = os.path.join(get_package_share_directory(pkg_robot_description), "urdf", "quadro.urdf.xacro")

    # Process the xacro file to get URDF
    urdf_doc = xacro.process_file(urdf_file)
    robot_desc = urdf_doc.toxml()

    world_path = PathJoinSubstitution([
        FindPackageShare(pkg_robot_description),
        'worlds',
        LaunchConfiguration('world_file')
    ])



    gazebo_resource_path = SetEnvironmentVariable(
        name="GZ_SIM_RESOURCE_PATH",
        value=[
            str(Path(get_package_share_directory(pkg_robot_description)).parent.resolve())
            ]
        )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'robot_description': robot_desc}
        ]
    )

    # joint_state_publisher_node = Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher'
    # )

    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
        ),
        launch_arguments={
            "gz_args": "-r empty.sdf"
        }.items(),
    )

    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-string", robot_desc,
            "-name", "quadro",
            "-allow_renaming", "true",
            "-x", "0.0",  # X position
            "-y", "0.0",  # Y position
            "-z", "0.5",  # Z position
            "-R", "0.0",  # Roll (rotation about X-axis)
            "-P", "0.0",  # Pitch (rotation about Y-axis)
            "-Y", "0.0"  # Yaw (rotation about Z-axis, 1.57 rad = 90 degrees)
        ],
        output="screen"
    )

    ros2_ign_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        # arguments=[
        #     "/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock",
        #     "/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan",
        #     "/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist",
        #     "/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V",
        #     "/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry"

        # ],
        parameters=[{
            'config_file': os.path.join(get_package_share_directory(pkg_robot_description), 'config', 'ros_gz_bridge.yaml')
        }],
        output="screen"
    )

    return LaunchDescription([
        # declare_world_arg,
        gazebo_resource_path,
        robot_state_publisher_node,
        # joint_state_publisher_node,
        spawn_robot,
        ros2_ign_bridge,
        gz_launch

    ])