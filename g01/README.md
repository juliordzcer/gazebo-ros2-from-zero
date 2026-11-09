# G1 · Install Gazebo Harmonic and first steps

Install steps: see the [main README](../README.md#install-gazebo-harmonic-on-ubuntu-2404).

Commands used in the video:

```bash
cat /etc/os-release | head -4          # which Ubuntu you have
gz sim --versions                      # Gazebo version
gz sim --help | grep -E '^ +-(r|s|g|v) '

gz sim                                 # quick start window → choose "Empty" → RUN

# (second terminal) lift a model 3 m with the set_pose service
gz service -s /world/empty/set_pose --reqtype gz.msgs.Pose --reptype gz.msgs.Boolean \
  --timeout 1000 --req 'name: "box", position: {x: -1, z: 3}'

# a world that comes with Gazebo: two robots with two wheels
gz sim -r diff_drive.sdf
gz topic -l | grep cmd_vel
gz topic -t /model/vehicle_blue/cmd_vel -m gz.msgs.Twist -p 'linear: {x: 1.0}, angular: {z: 0.5}'
gz topic -t /model/vehicle_blue/cmd_vel -m gz.msgs.Twist -p 'linear: {x: 0}'

# server and GUI are two programs
gz sim -s -r shapes.sdf &
gz sim -g
```

Mini challenge: open a featured world or `gz sim tunnel.sdf` and count its models.
