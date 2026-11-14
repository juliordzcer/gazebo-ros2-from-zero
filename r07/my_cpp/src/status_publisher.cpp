#include <chrono>
#include <memory>

#include "my_interfaces/msg/robot_status.hpp"
#include "rclcpp/rclcpp.hpp"

using namespace std::chrono_literals;

class StatusPublisher : public rclcpp::Node
{
public:
  StatusPublisher()
  : Node("status_publisher")
  {
    publisher_ = create_publisher<my_interfaces::msg::RobotStatus>("status", 10);
    timer_ = create_wall_timer(500ms, [this]() {tick();});
  }

private:
  void tick()
  {
    my_interfaces::msg::RobotStatus msg;
    msg.name = "rover";
    msg.battery = battery_;
    msg.charging = battery_ < 20.0;
    publisher_->publish(msg);
    RCLCPP_INFO(get_logger(), "battery %.1f %%", battery_);
    battery_ = msg.charging ? 100.0 : battery_ - 5.0;
  }

  rclcpp::Publisher<my_interfaces::msg::RobotStatus>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
  double battery_ = 100.0;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<StatusPublisher>());
  rclcpp::shutdown();
  return 0;
}
