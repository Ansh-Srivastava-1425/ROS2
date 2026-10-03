#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class SensorPub(Node):
    def __init__(self):
        super().__init__('sensor_pub')
        self.pub = self.create_publisher(Float32, 'temperature', 10)
        self.create_timer(0.5, self.publish_temp)

    def publish_temp(self):
        msg = Float32()
        msg.data = round(random.uniform(15.0, 45.0), 2)
        self.pub.publish(msg)
        self.get_logger().info(f'Raw: {msg.data}')


def main():
    rclpy.init()
    rclpy.spin(SensorPub())
    rclpy.shutdown()


if __name__ == '__main__':
    main()