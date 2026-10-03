#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class TemperatureSubscriber(Node):
    def __init__(self):
        super().__init__("temperature_subscriber")
        self.subscription = self.create_subscription(
            String, "my_temperature", self.callback, 10
        )
        self.get_logger().info("Listening on my_temperature")

    def callback(self, msg: String):
        self.get_logger().info(f"Received: {msg.data}")


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSubscriber()
    rclpy.spin(node)
    # node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()