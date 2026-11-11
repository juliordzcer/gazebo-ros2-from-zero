import time

from gz.msgs10.odometry_pb2 import Odometry
from gz.msgs10.twist_pb2 import Twist
from gz.transport13 import Node

node = Node()
pub = node.advertise("/cmd_vel", Twist)
here = {}


def on_odom(msg):
    here["x"], here["y"] = msg.pose.position.x, msg.pose.position.y


node.subscribe(Odometry, "/model/robot/odometry", on_odom)


def drive(linear, angular, seconds):
    cmd = Twist()
    cmd.linear.x = linear
    cmd.angular.z = angular
    pub.publish(cmd)
    time.sleep(seconds)


time.sleep(1)
for side in range(4):
    drive(0.5, 0.0, 2.0)
    drive(0.0, 0.785, 2.0)
    print(f"corner {side + 1}: x = {here['x']:.2f}, y = {here['y']:.2f}")
drive(0.0, 0.0, 0.5)
print("done")
