import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

DRONES = [
    {'ns': 'x3', 'gz': 'X3', 'model': 'x3', 'cmd': 'gazebo/command/twist', 'start': [0.0, 0.0, 2.0]},
    {'ns': 'x4', 'gz': 'X4', 'model': 'X4', 'cmd': 'gazebo/command/twist', 'start': [0.0, 0.0, 3.0]},
]


def drone_nodes(d):
    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge', name='bridge', namespace=d['ns'],
        arguments=[f"/{d['gz']}/{d['cmd']}@geometry_msgs/msg/Twist]gz.msgs.Twist",
                   f"/{d['gz']}/enable@std_msgs/msg/Bool]gz.msgs.Boolean",
                   f"/model/{d['model']}/odometry@nav_msgs/msg/Odometry[gz.msgs.Odometry"],
        remappings=[(f"/{d['gz']}/{d['cmd']}", f"/{d['ns']}/cmd_vel"),
                    (f"/{d['gz']}/enable", f"/{d['ns']}/enable"),
                    (f"/model/{d['model']}/odometry", f"/{d['ns']}/odom")])
    control = Node(
        package='my_drone', executable='position_control', namespace=d['ns'],
        parameters=[{'use_sim_time': True, 'start': d['start']}])
    return [bridge, control]


def generate_launch_description():
    gz_share = get_package_share_directory('ros_gz_sim')
    actions = [
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(gz_share, 'launch', 'gz_sim.launch.py')),
            launch_arguments={'gz_args': '-r multicopter_velocity_control.sdf'}.items()),
        Node(package='ros_gz_bridge', executable='parameter_bridge', name='clock_bridge',
             arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock']),
    ]
    for d in DRONES:
        actions += drone_nodes(d)
    return LaunchDescription(actions)
