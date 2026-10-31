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

    # 4. SLAM: builds the map from /scan and /odom
    slam_config = os.path.join(pkg, 'config', 'slam.yaml')
    slam_launch = os.path.join(
        get_package_share_directory('slam_toolbox'),
        'launch', 'online_async_launch.py')
    slam = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(slam_launch),
        launch_arguments={
            'slam_params_file': slam_config,
            'use_sim_time': 'true',
        }.items(),
    )
    nav2_pkg = get_package_share_directory('nav2_bringup')
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_pkg, 'launch', 'navigation_launch.py')),
        launch_arguments={
            'params_file': os.path.join(pkg, 'config', 'nav2_params.yaml'),
            'use_sim_time': 'true',
        }.items(),
    )
    return LaunchDescription([simulation, rviz, slam, nav2])