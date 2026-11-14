import math

import rclpy
from geometry_msgs.msg import TransformStamped
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from tf2_ros import TransformBroadcaster
from turtlesim.msg import Pose


class TurtleTf(Node):

    def __init__(self):
        super().__init__('turtle_tf')
        self.broadcaster = TransformBroadcaster(self)
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)

    def on_pose(self, pose):
        t = TransformStamped()
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = 'world'
        t.child_frame_id = 'turtle1'
        t.transform.translation.x = pose.x
        t.transform.translation.y = pose.y
        t.transform.rotation.z = math.sin(pose.theta / 2)
        t.transform.rotation.w = math.cos(pose.theta / 2)
        self.broadcaster.sendTransform(t)


def main():
    rclpy.init()
    node = TurtleTf()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
