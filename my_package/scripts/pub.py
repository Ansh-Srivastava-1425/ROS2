#! /usr/bin/env python3      
#-------------------------->shebang line to specify the interpreter

import rclpy                 #-------------------------->importing the rclpy library for ROS 2 Python client library
from rclpy.node import Node  #-------------------------->importing the Node class from rclpy.node module
from std_msgs.msg import String  #-------------------------->importing the String message type from std_msgs.msg module

class MyPublisher(Node):  #-------------------------->defining a class MyPublisher that inherits from Node
    def __init__(self):  #-------------------------->constructor method for the class
        super().__init__('my_publisher')  #-------------------------->initializing the Node with the name 'my_publisher'
        self.publisher_ = self.create_publisher(String, 'my_topic', 10)  #-------------------------->creating a publisher for String messages on 'my_topic' with a queue size of 10
        timer_period = 1.0  # seconds  #-------------------------->setting the timer period to 1 second
        self.timer = self.create_timer(timer_period, self.timer_callback)  #-------------------------->creating a timer that calls timer_callback every second

    def timer_callback(self):  #-------------------------->defining the callback function for the timer
        msg = String()  #-------------------------->creating a new String message
        msg.data = 'Hello, ROS 2!'  #-------------------------->setting the data field of the message
        self.publisher_.publish(msg)  #-------------------------->publishing the message
        self.get_logger().info('Publishing: "%s"' % msg.data)  #-------------------------->logging the published message

def main(args=None):  #-------------------------->defining the main function
    rclpy.init(args=args)  #-------------------------->initializing the ROS 2 Python client library
    my_publisher = MyPublisher()  #-------------------------->creating an instance of MyPublisher

    rclpy.spin(my_publisher)  #-------------------------->spinning the node to keep it alive and processing callbacks

    my_publisher.destroy_node()  #-------------------------->destroying the node when done
    rclpy.shutdown()  #-------------------------->shutting down the ROS 2 Python client library

if __name__ == '__main__':  #-------------------------->checking if the script is being run directly
    main()  #-------------------------->calling the main function