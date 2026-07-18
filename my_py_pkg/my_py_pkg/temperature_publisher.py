#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float64

class TemperaturNode(Node):
    def __init__(self):
       super().__init__("temperature")
       self.count_ = 20
       self.tempreture_publisher_ = self.create_publisher(
       Float64, "tempreature", 10)
       self.get_logger().info("Temperature Has Started")
       self.temperature_timer = self.create_timer(1.0, self.publish_temperature)

    def publish_temperature(self):
        msg = Float64()
        self.count_ += 0.5
        msg.data = self.count_
        self.tempreture_publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TemperaturNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

