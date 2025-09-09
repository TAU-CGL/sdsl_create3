from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, TextSubstitution

def generate_launch_description():
    ld = []

    ld.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('create3_lidar_slam'),
                'launch',
                'sensors_launch.py'
            ])
        ])
    ))
    ld.append(IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('teleop_twist_joy'),
                'launch',
                'teleop-launch.py'
            ])
        ]),
        launch_arguments={'joy_config': 'ps5'}.items()
    ))

    # Launch the R3 horn node
    ld.append(Node(
        package='sdsl_create3',
        executable='r3_horn',
        name='r3_horn_node',
    ))

    # Launch the sparse distance sampling (SDS) node
    ld.append(Node(
        package='sdsl_create3',
        executable='sds_publisher',
        name='sds_publisher_node',
    ))

    return LaunchDescription(ld)
