# R2 · Nodes and topics with turtlesim

Every command from the video, in order.

```bash
ros2 run turtlesim turtlesim_node
ros2 run turtlesim turtle_teleop_key
rqt_graph
ros2 node list
ros2 node info /turtlesim
ros2 topic list -t
ros2 topic echo /turtle1/pose
ros2 topic hz /turtle1/pose
ros2 interface show geometry_msgs/msg/Twist
ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}}"
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
ros2 service call /spawn turtlesim/srv/Spawn "{x: 2.0, y: 2.0, theta: 0.5, name: 'turtle2'}"
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel
```
