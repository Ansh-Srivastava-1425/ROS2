#!/usr/bin/env python3                       
# # tells Linux to run this file with python3

import rclpy                                 # the ROS 2 Python library
from rclpy.node import Node                  # base class that every node inherits from
from example_interfaces.srv import AddTwoInts  # the service type (request: a, b / response: sum)


class AddTwoIntsClients(Node):               # our client is a node, so it inherits from Node
    def __init__(self):                      # runs once when the node is created
        super().__init__("add_two_ints_clients")   # start the Node part and give it a name
        self.client_ = self.create_client(AddTwoInts, "add_two_ints")
        # create a client: service type = AddTwoInts, service name = "add_two_ints"
        # the name must match the server's name exactly

    def call_add_two_ints(self, a, b):       # our own function: sends a request with numbers a and b
        while not self.client_.wait_for_service(1.0):   # check for the server for up to 1 second; repeat while it is missing
            self.get_logger().warn("Waiting for Add two ints Server")   # print a warning each time it is not found yet

        request = AddTwoInts.Request()       # create an empty request object (note the brackets)
        request.a = a                        # put the first number into the request
        request.b = b                        # put the second number into the request

        future = self.client_.call_async(request)   # send the request without waiting; returns a "future" (a receipt for the answer)
        future.add_done_callback(self.callback_call_add_two_ints)
        # when the answer arrives, automatically run callback_call_add_two_ints

    def callback_call_add_two_ints(self, future):   # runs by itself when the server's reply arrives
        response = future.result()           # take the server's reply out of the future
        self.get_logger().info(str(response.sum))   # print the sum (str() turns the number into text)


def main(args=None):                         # the starting point of the program
    rclpy.init(args=args)                    # start ROS 2
    node = AddTwoIntsClients()               # create our client node
    node.call_add_two_ints(2, 5)             # send the request: 2 + 5
    rclpy.spin(node)                         # keep the node alive so the reply and callback can be processed
    rclpy.shutdown()                         # shut ROS 2 down (reached after you press Ctrl+C)


if __name__ == "__main__":                   # true only when this file is run directly
    main()                                   # call main() to start everything