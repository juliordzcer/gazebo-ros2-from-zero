import math

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from visualization_msgs.msg import Marker


class MarkerPub(Node):

    def __init__(self):
        super().__init__('marker_pub')
        self.publisher = self.create_publisher(Marker, 'markers', 10)
        self.t = 0.0
        self.timer = self.create_timer(0.05, self.tick)

    def make(self, id, kind, x, y, z, color):
        m = Marker()
        m.header.frame_id = 'world'
        m.header.stamp = self.get_clock().now().to_msg()
        m.id = id
        m.type = kind
        m.pose.position.x, m.pose.position.y, m.pose.position.z = x, y, z
        m.pose.orientation.w = 1.0
        m.scale.x = m.scale.y = m.scale.z = 0.5
        m.color.r, m.color.g, m.color.b = color
        m.color.a = 1.0
        return m

    def tick(self):
        self.t += 0.05
        x, y = 2.0 * math.cos(self.t), 2.0 * math.sin(self.t)
        self.publisher.publish(self.make(0, Marker.SPHERE, x, y, 0.25, (1.0, 0.4, 0.1)))
        self.publisher.publish(self.make(1, Marker.CUBE, 0.0, 0.0, 0.25, (0.2, 0.5, 1.0)))
        text = self.make(2, Marker.TEXT_VIEW_FACING, x, y, 0.9, (1.0, 1.0, 1.0))
        text.text = f'{math.degrees(self.t) % 360:.0f} deg'
        self.publisher.publish(text)


def main():
    rclpy.init()
    node = MarkerPub()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
