import sys
import time

import rclpy
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor, SingleThreadedExecutor
from rclpy.node import Node
from std_msgs.msg import String


class SlowNode(Node):

    def __init__(self):
        super().__init__('slow_node')
        self.count = 0
        self.timer = self.create_timer(0.5, self.tick)
        self.create_subscription(String, 'work', self.on_work, 10,
                                 callback_group=MutuallyExclusiveCallbackGroup())

    def tick(self):
        self.count += 1
        self.get_logger().info(f'tick {self.count}')

    def on_work(self, msg):
        self.get_logger().info(f'working on {msg.data}...')
        time.sleep(3.0)
        self.get_logger().info('work done')


def main():
    rclpy.init()
    node = SlowNode()
    multi = len(sys.argv) > 1 and sys.argv[1] == 'multi'
    executor = MultiThreadedExecutor() if multi else SingleThreadedExecutor()
    executor.add_node(node)
    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
