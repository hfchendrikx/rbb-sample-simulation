#include "ros/ros.h"
#include "std_msgs/String.h"
#include "geometry_msgs/PointStamped.h"
#include <string>

int main(int argc, char **argv) {
  ros::init(argc, argv, "sine_wave");
  ros::NodeHandle n;
  ros::NodeHandle private_node("~");

  float f = private_node.param("frequency", 1.0f);
  ROS_INFO("Running sine node for 20 seconds @ %f Hz", f);


  ros::Publisher pub_out;
  pub_out = n.advertise<geometry_msgs::PointStamped>("/imu/gyroscope", 1000);

  ros::Rate loop_rate(100);
  float t = 0.0f;
  while(ros::ok() && t < 20.0f) {
    t += 0.01f;

    geometry_msgs::PointStamped p;
    p.header.stamp = ros::Time::now();
    p.point.x = cos(t * M_PI * 2 * f);
    p.point.y = sin(t * M_PI * 2 * f);
    p.point.z = (fmod(t * f, 1.0f));
    pub_out.publish(p);

    ros::spinOnce();
    loop_rate.sleep();
  }

  ROS_INFO("Bye bye!");

  return 0;
}