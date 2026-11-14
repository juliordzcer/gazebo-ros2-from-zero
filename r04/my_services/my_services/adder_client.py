import sys

import rclpy
from example_interfaces.srv import AddTwoInts
from rclpy.node import Node


def main():
    rclpy.init()
    node = Node('adder_client')
    client = node.create_client(AddTwoInts, 'add_two_ints')
    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('waiting for the server...')
    request = AddTwoInts.Request()
    request.a = int(sys.argv[1])
    request.b = int(sys.argv[2])
    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)
    node.get_logger().info(f'The answer: {future.result().sum}')
    node.destroy_node()
    rclpy.try_shutdown()
