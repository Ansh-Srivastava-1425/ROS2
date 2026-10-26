import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    # 1. Where is our robot file after installing?
    urdf_path = os.path.join(
        get_package_share_directory('mybot'), 'urdf', 'mybot.urdf.xacro'
    )
    rviz_config = os.path.join(
        get_package_share_directory('mybot'), 'rviz', 'display.rviz'
    )
    # 2. Run the xacro command and keep its text output
    robot_description = ParameterValue(
        Command(['xacro ', urdf_path]), value_type=str
    )

    # 3. The three programs we want to start
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}],
    )

    joint_state_publisher_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
    )
        
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', rviz_config],
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher_gui,
        rviz,
    ])