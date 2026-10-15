import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_path = get_package_share_directory('my_first_car')
    xacro_path = os.path.join(pkg_path, 'urdf', 'robot.urdf.xacro')

    gz_pkg_path = get_package_share_directory('ros_gz_sim')
    gz_launch_path = os.path.join(gz_pkg_path, 'launch', 'gz_sim.launch.py')

    return LaunchDescription([
        # 1. Gazebo with an empty world, physics running
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(gz_launch_path),
            launch_arguments={'gz_args': '-r empty.sdf'}.items(),
        ),

        # 2. Publishes the robot description
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['xacro ', xacro_path]), value_type=str
                )
            }],
            output='screen',
        ),

        # 3. Spawns the robot into Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description',
                       '-name', 'my_robot',
                       '-z', '0.2'],
            output='screen',
        ),
    ])