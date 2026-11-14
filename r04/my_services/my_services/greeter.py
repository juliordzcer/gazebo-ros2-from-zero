import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node


class Greeter(Node):

    def __init__(self):
        super().__init__('greeter')
        self.declare_parameter('greeting', 'Hello')
        self.declare_parameter('period', 1.0)
        period = self.get_parameter('period').value
        self.timer = self.create_timer(period, self.tick)

    def tick(self):
        greeting = self.get_parameter('greeting').value
        self.get_logger().info(f'{greeting}, ROS 2!')


def main():
    rclpy.init()
    node = Greeter()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
