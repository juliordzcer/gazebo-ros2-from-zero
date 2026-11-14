import time

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class TimeCheck(Node):

    def __init__(self):
        super().__init__('time_check')
        self.wall0 = None
        self.ros0 = None
        self.timer = self.create_timer(1.0, self.tick)

    def tick(self):
        if self.ros0 is None:
            self.wall0 = time.time()
            self.ros0 = self.get_clock().now().nanoseconds / 1e9
            return
        ros = self.get_clock().now().nanoseconds / 1e9 - self.ros0
        wall = time.time() - self.wall0
        self.get_logger().info(f'ROS time {ros:6.1f} s   wall time {wall:6.1f} s')


def main():
    rclpy.init()
    node = TimeCheck()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
