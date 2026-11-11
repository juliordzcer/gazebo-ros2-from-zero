#include <gz/math/Vector3.hh>
#include <gz/plugin/Register.hh>
#include <gz/sim/Link.hh>
#include <gz/sim/Model.hh>
#include <gz/sim/System.hh>

namespace wind
{
class WindPush : public gz::sim::System,
                 public gz::sim::ISystemConfigure,
                 public gz::sim::ISystemPreUpdate
{
public:
  void Configure(const gz::sim::Entity &_entity,
                 const std::shared_ptr<const sdf::Element> &_sdf,
                 gz::sim::EntityComponentManager &_ecm,
                 gz::sim::EventManager &) override
  {
    gz::sim::Model model(_entity);
    std::string linkName = _sdf->Get<std::string>("link_name", "link").first;
    this->force = _sdf->Get<gz::math::Vector3d>("force", {1, 0, 0}).first;
    this->link = gz::sim::Link(model.LinkByName(_ecm, linkName));
    gzmsg << "WindPush: " << this->force << " N on " << linkName << std::endl;
  }

  void PreUpdate(const gz::sim::UpdateInfo &_info,
                 gz::sim::EntityComponentManager &_ecm) override
  {
    if (_info.paused)
      return;
    this->link.AddWorldForce(_ecm, this->force);
  }

private:
  gz::sim::Link link;
  gz::math::Vector3d force;
};
}  // namespace wind

GZ_ADD_PLUGIN(wind::WindPush,
              gz::sim::System,
              wind::WindPush::ISystemConfigure,
              wind::WindPush::ISystemPreUpdate)
