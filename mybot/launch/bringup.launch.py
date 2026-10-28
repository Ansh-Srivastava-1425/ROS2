import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():
    pkg = get_package_share_directory('mybot')

    # 1. The simulation: reuse our existing launch file
    simulation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg, 'launch', 'gazebo.launch.py'))
    )

    # 2. RViz, on the simulation clock
    rviz_config = os.path.join(pkg, 'rviz', 'display.rviz')
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': True}],
    )

    avoider = Node(
        package='mybot_control',
        executable='scan_reader',
        output='screen',
    )

    return LaunchDescription([simulation, rviz, avoider])