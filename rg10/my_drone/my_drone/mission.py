import rclpy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Bool

LEGS = [(1.0, 0.0), (0.0, 1.0), (-1.0, 0.0), (0.0, -1.0)]


class Mission(Node):

    def __init__(self):
        super().__init__('mission')
        self.cmd = self.create_publisher(Twist, '/x3/cmd_vel', 10)
        self.enable = self.create_publisher(Bool, '/x3/enable', 10)
        self.create_subscription(Odometry, '/x3/odom', self.on_odom, 10)
        self.z = 0.0
        self.state = 'takeoff'
        self.leg = 0
        self.t0 = None
        self.timer = self.create_timer(0.1, self.step)

    def on_odom(self, msg):
        self.z = msg.pose.pose.position.z

    def now(self):
        return self.get_clock().now().nanoseconds / 1e9

    def go(self, state):
        self.get_logger().info(f'{self.state} → {state}')
        self.state, self.t0 = state, self.now()

    def step(self):
        self.enable.publish(Bool(data=True))
        twist = Twist()
        if self.state == 'takeoff':
            twist.linear.z = 0.5
            if self.z > 2.0:
                self.go('square')
        elif self.state == 'square':
            twist.linear.x, twist.linear.y = LEGS[self.leg]
            if self.now() - self.t0 > 3.0:
                self.leg += 1
                if self.leg == len(LEGS):
                    self.go('land')
                else:
                    self.t0 = self.now()
        elif self.state == 'land':
            twist.linear.z = -0.4
            if self.z < 0.15:
                self.go('done')
        self.cmd.publish(twist)


def main():
    rclpy.init()
    node = Mission()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
