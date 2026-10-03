from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    threshold = LaunchConfiguration('threshold')

    return LaunchDescription([
        DeclareLaunchArgument(
            'threshold',
            default_value='30.0',
            description='Only pass temperatures above this value'),

        Node(
            package='filter_pkg',
            executable='temp_publisher',
            name='temp_publisher',
            output='screen',
        ),

        Node(
            package='filter_pkg',
            executable='filter_node',
            name='filter_node',
            output='screen',
            parameters=[{'threshold': threshold}],
        ),

        Node(
            package='filter_pkg',
            executable='display_sub',
            name='display_sub',
            output='screen',
        ),
    ])