import sys

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from turtlesim.action import RotateAbsolute


def main():
    rclpy.init()
    node = Node('rotate_client')
    client = ActionClient(node, RotateAbsolute, '/turtle1/rotate_absolute')
    client.wait_for_server()
    goal = RotateAbsolute.Goal()
    goal.theta = float(sys.argv[1])

    def on_feedback(msg):
        node.get_logger().info(f'Remaining: {msg.feedback.remaining:.2f} rad')

    send = client.send_goal_async(goal, feedback_callback=on_feedback)
    rclpy.spin_until_future_complete(node, send)
    handle = send.result()
    node.get_logger().info('Goal accepted' if handle.accepted else 'Goal rejected')
    result = handle.get_result_async()
    rclpy.spin_until_future_complete(node, result)
    node.get_logger().info(f'Done, turned {result.result().result.delta:.2f} rad')
    node.destroy_node()
    rclpy.try_shutdown()
