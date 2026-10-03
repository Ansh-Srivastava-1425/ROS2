#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MySubscriber(Node):
    def __init__(self):
        super().__init__("my_subscriber")
        self.subscriber = self.create_subscription(
            String, "my_topic", self.callback, 10
        )

    def callback(self, msg):
        self.get_logger().info(msg.data)


def main(args=None):
    rclpy.init(args=args)
    my_subscriber = MySubscriber()
    rclpy.spin(my_subscriber)
    my_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()