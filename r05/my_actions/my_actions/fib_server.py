import time

import rclpy
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer, CancelResponse
from rclpy.executors import ExternalShutdownException, MultiThreadedExecutor
from rclpy.node import Node


class FibonacciServer(Node):

    def __init__(self):
        super().__init__('fibonacci_server')
        self.server = ActionServer(self, Fibonacci, 'fibonacci', self.execute,
                                   cancel_callback=lambda goal: CancelResponse.ACCEPT)

    def execute(self, goal_handle):
        order = goal_handle.request.order
        self.get_logger().info(f'Goal: {order} numbers')
        feedback = Fibonacci.Feedback()
        feedback.sequence = [0, 1]
        for i in range(1, order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Canceled')
                return Fibonacci.Result()
            feedback.sequence.append(feedback.sequence[i] + feedback.sequence[i - 1])
            goal_handle.publish_feedback(feedback)
            time.sleep(1.0)
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback.sequence
        return result


def main():
    rclpy.init()
    node = FibonacciServer()
    try:
        rclpy.spin(node, executor=MultiThreadedExecutor())
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
