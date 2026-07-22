#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class TemperatureMonitorNode(Node):
    def __init__(self):
       super().__init__("temperature_monitor")
       self.max_temp_ = 0.0
       self.get_logger().info("Temperature Started")
       self.tempreture_subscribe_ = self.create_subscription(
       Float64, "tempreature", self.callback_monitor_temperature, 10)

    def callback_monitor_temperature(self, msg: Float64):
       if msg.data > self.max_temp_:        
           self.max_temp_ = msg.data
       max_msg = Float64()
       max_msg.data = self.max_temp_
       self.max_temp_publisher_.publish(max_msg)


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureMonitorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()