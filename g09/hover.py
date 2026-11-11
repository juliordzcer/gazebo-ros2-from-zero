import time

from gz.msgs10.actuators_pb2 import Actuators
from gz.msgs10.pose_v_pb2 import Pose_V
from gz.transport13 import Node

TARGET = 1.0      # m
HOVER = 660.0     # rad/s
KP, KD = 80.0, 60.0

node = Node()
pub = node.advertise("/X3/gazebo/command/motor_speed", Actuators)
state = {"z": 0.0, "vz": 0.0, "t": None}


def on_pose(msg):
    for p in msg.pose:
        if p.name == "x3":
            t = msg.header.stamp.sec + msg.header.stamp.nsec * 1e-9
            if state["t"] is not None and t > state["t"]:
                state["vz"] = (p.position.z - state["z"]) / (t - state["t"])
            state["z"], state["t"] = p.position.z, t


node.subscribe(Pose_V, "/world/quadcopter/dynamic_pose/info", on_pose)

start = time.time()
while time.time() - start < 12:
    error = TARGET - state["z"]
    w = HOVER + KP * error - KD * state["vz"]
    w = max(0.0, min(800.0, w))
    cmd = Actuators()
    cmd.velocity.extend([w, w, w, w])
    pub.publish(cmd)
    print(f"z = {state['z']:.2f} m   motors = {w:.0f} rad/s", flush=True)
    time.sleep(0.1)
