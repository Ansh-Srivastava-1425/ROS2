#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


class AddTwoIntsClients(Node):
    def __init__(self):
        super().__init__("add_two_ints_clients")
        self.clients_ = self.create_client(AddTwoInts, "add_two_ints")

    def call_add_two_ints(self, a, b):
        while not self.clients_.wait_for_service(1.0):
            self.get_logger().warn("Waiting for Server.....")

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.clients_.call_async(request)
        future.add_done_callback(self.callback_call_add_two_ints)

    def callback_call_add_two_ints(self , future):
        response = future.result() 
        self.get_logger().info("Got response: " + str(response.sum))

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntsClients()
    node.call_add_two_ints(3,10)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()