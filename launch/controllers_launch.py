from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
from launch.substitutions import Command
import os


def generate_launch_description():
    package_name='wheelchair_bot'

    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','controllers.yaml')

    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file]
    )

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments = ["diff_cont"]
    )

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=['joint_broad']
    )

    twist_mux_starter = Node(
        package="twist_mux",
        executable="twist_mux",
        arguments = ['--ros-args', '--params-file', './src/wheelchair_bot/config/cmd_vel_remap.yaml',
         '-r','cmd_vel_out:=/diff_cont/cmd_vel_unstamped']
    )

    return LaunchDescription([
        controller_manager,
        diff_drive_spawner,
        joint_broad_spawner,
        twist_mux_starter,
    ])