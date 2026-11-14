import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64


class Tank(Node):

    def __init__(self):
        super().__init__('tank')
        self.level = 20.0
        self.valve = 0.0
        self.opening = 0.0
        self.create_subscription(Float64, 'valve', self.on_valve, 10)
        self.publisher = self.create_publisher(Float64, 'level', 10)
        self.timer = self.create_timer(0.05, self.step)

    def on_valve(self, msg):
        self.valve = min(max(msg.data, 0.0), 100.0)

    def step(self):
        dt = 0.05
        self.opening += (self.valve - self.opening) * dt / 1.5
        inflow = 0.12 * self.opening
        outflow = 0.9 * math.sqrt(max(self.level, 0.0))
        self.level = min(max(self.level + (inflow - outflow) * dt, 0.0), 100.0)
        self.publisher.publish(Float64(data=self.level))


def main():
    rclpy.init()
    node = Tank()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
