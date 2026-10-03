#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class PoseSubscriberNode(Node):
    def __init__(self):
        super().__init__("pose_suubscriber")
        self.subscriber = self.create_subscription(Pose ,"/turtle1/pose",self.callback ,10)

    def callback(self , msg:Pose):
        self.get_logger().info(str(msg))

def main(args = None):
    rclpy.init(args=args)
    node = PoseSubscriberNode()
    rclpy.spin(node)
    # node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()