#!/usr/bin/python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class TemperaturePublisherNode(Node):
    def __init__(self):
        super().__init__("temperature_publisher")
        self.get_logger().info("Node Started")
        self.publisher_ = self.create_publisher(String,"my_temperature",10 )
        self.timer_ = self.create_timer(2.0,self.publish_temperature)

    def publish_temperature(self):
        temp_c = 28.5
        temp_f = temp_c * 9/5 + 32
        msg = String()
        msg.data = f"Temperature: {temp_c} °C / {temp_f:.1f} °F"
        self.get_logger().info(msg.data)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TemperaturePublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()