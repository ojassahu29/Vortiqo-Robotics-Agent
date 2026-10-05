from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    package_dir = Path(get_package_share_directory("vortiqo_gazebo"))
    gazebo_launch = Path(get_package_share_directory("ros_gz_sim")) / "launch" / "gz_sim.launch.py"
    world = package_dir / "worlds" / "tabletop.sdf"
    headless = LaunchConfiguration("headless")

    return LaunchDescription(
        [
            DeclareLaunchArgument("headless", default_value="false"),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(gazebo_launch)),
                launch_arguments={"gz_args": f"-r {world}"}.items(),
                condition=UnlessCondition(headless),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(str(gazebo_launch)),
                launch_arguments={"gz_args": f"-s -r {world}"}.items(),
                condition=IfCondition(headless),
            ),
            Node(
                package="ros_gz_bridge",
                executable="parameter_bridge",
                name="table_camera_bridge",
                parameters=[{"config_file": str(package_dir / "config" / "camera_bridge.yaml")}],
                output="screen",
            ),
        ]
    )
