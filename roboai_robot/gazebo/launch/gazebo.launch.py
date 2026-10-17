import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, IncludeLaunchDescription,
                            SetEnvironmentVariable)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_directory('roboai_robot')
    ros_gz_sim = get_package_share_directory('ros_gz_sim')

    use_sim_time = LaunchConfiguration('use_sim_time')

    xacro_file = os.path.join(pkg_share, 'models', 'urdf', 'roboai_robot.xacro')
    world_file = 'empty.sdf'    

    robot_description = ParameterValue(
        Command(['xacro ', xacro_file]), value_type=str)

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time', default_value='false',
            description='Use simulation clock'),

        # lets Gazebo resolve package://roboai_robot/meshes/...
        SetEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(pkg_share, '..')),

        # start Gazebo with your world (-r = run immediately)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': ['-r -v 4 ', world_file]}.items(),
        ),

        # publish robot_description + TF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description,
                         'use_sim_time': use_sim_time}],
            output='screen',
        ),

        # spawn the robot into Gazebo
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=['-topic', 'robot_description',
                       '-name', 'roboai_robot',
                       '-z', '0.1'],
            output='screen',
        ),

    ])   