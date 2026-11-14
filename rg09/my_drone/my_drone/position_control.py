import math

import rclpy
from geometry_msgs.msg import Point, Twist
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Bool


class PositionControl(Node):

    def __init__(self):
        super().__init__('position_control')
        self.declare_parameter('kp', 0.8)
        self.declare_parameter('max_speed', 1.5)
        self.goal = Point(x=0.0, y=0.0, z=2.0)
        self.pos = None
        self.cmd = self.create_publisher(Twist, '/x3/cmd_vel', 10)
        self.enable = self.create_publisher(Bool, '/x3/enable', 10)
        self.create_subscription(Odometry, '/x3/odom', self.on_odom, 10)
        self.create_subscription(Point, '/x3/goal', self.on_goal, 10)
        self.timer = self.create_timer(0.05, self.step)

    def on_odom(self, msg):
        self.pos = msg.pose.pose.position

    def on_goal(self, msg):
        self.goal = msg
        self.get_logger().info(f'new goal {msg.x:.1f}, {msg.y:.1f}, {msg.z:.1f}')

    def step(self):
        if self.pos is None:
            return
        kp = self.get_parameter('kp').value
        vmax = self.get_parameter('max_speed').value
        v = [kp * (self.goal.x - self.pos.x), kp * (self.goal.y - self.pos.y), kp * (self.goal.z - self.pos.z)]
        norm = math.sqrt(sum(c * c for c in v))
        if norm > vmax:
            v = [c * vmax / norm for c in v]
        twist = Twist()
        twist.linear.x, twist.linear.y, twist.linear.z = v
        self.enable.publish(Bool(data=True))
        self.cmd.publish(twist)


def main():
    rclpy.init()
    node = PositionControl()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
