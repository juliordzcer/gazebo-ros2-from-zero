import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Float64


class Pid(Node):

    def __init__(self):
        super().__init__('pid')
        for name, value in (('setpoint', 50.0), ('kp', 2.0), ('ki', 0.0), ('kd', 0.0)):
            self.declare_parameter(name, value)
        self.integral = 0.0
        self.last_error = None
        self.create_subscription(Float64, 'level', self.on_level, 10)
        self.valve = self.create_publisher(Float64, 'valve', 10)
        self.target = self.create_publisher(Float64, 'setpoint', 10)

    def on_level(self, msg):
        dt = 0.05
        p = {n: self.get_parameter(n).value for n in ('setpoint', 'kp', 'ki', 'kd')}
        error = p['setpoint'] - msg.data
        derivative = 0.0 if self.last_error is None else (error - self.last_error) / dt
        self.last_error = error
        output = p['kp'] * error + self.integral + p['kd'] * derivative
        if 0.0 < output < 100.0:
            self.integral += p['ki'] * error * dt
        self.valve.publish(Float64(data=min(max(output, 0.0), 100.0)))
        self.target.publish(Float64(data=p['setpoint']))


def main():
    rclpy.init()
    node = Pid()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        rclpy.try_shutdown()
