from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('red', default_value='60', description='background red, 0-255'),
        Node(package='turtlesim', executable='turtlesim_node', namespace='leader', name='sim',
             parameters=[{'background_r': LaunchConfiguration('red')}]),
        Node(package='turtlesim', executable='turtlesim_node', namespace='follower', name='sim'),
        Node(package='turtlesim', executable='mimic', name='mimic',
             remappings=[('/input/pose', '/leader/turtle1/pose'),
                         ('/output/cmd_vel', '/follower/turtle1/cmd_vel')]),
    ])
