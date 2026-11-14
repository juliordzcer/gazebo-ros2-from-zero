# R1 · Install ROS 2 Jazzy and your first commands

Every command from the video, in order.

```bash
locale
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
sudo apt update && sudo apt upgrade
sudo apt install ros-dev-tools
sudo apt install ros-jazzy-desktop
source /opt/ros/jazzy/setup.bash
echo 'source /opt/ros/jazzy/setup.bash' | tee -a ~/.bashrc
Official page: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
Commands used in the video:
ros2 run demo_nodes_cpp talker
ros2 run demo_nodes_py listener
ros2 node list
ros2 topic list
ros2 topic echo /chatter
ros2 topic info /chatter
ros2 topic hz /chatter
ros2 run turtlesim turtlesim_node
ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0}, angular: {z: 1.8}}"
ROS_DOMAIN_ID=5 ros2 node list
```
