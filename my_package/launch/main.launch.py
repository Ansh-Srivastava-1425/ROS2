from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        # node1
        Node(
            package='my_package',
            executable='pub.py',
            name='my_publisher',
            output='screen',
        ),
        # node2
        Node(
            package='my_package',
            executable='sub.py',
            name='my_subscriber',
            output='screen',
        )
    ])