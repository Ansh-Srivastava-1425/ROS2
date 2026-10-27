import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

class SeonsorReader(Node):
    def __init__(self):
        super().__init__('scan_reader')
        self.subscription = self.create_subscription(
            LaserScan , '/scan' , self.scan_callback , 10
        )
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

    def scan_callback (self , msg):
        front = min(msg.ranges[170:190])
        cmd = Twist()
        if front < 0.5:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.5
        else:
            cmd.linear.x = 0.15
            cmd.angular.z = 0.0
        self.cmd_pub.publish(cmd)
        self.get_logger().info(f'Front: {front:.2f} m')


def main(args=None):
    rclpy.init(args=args)
    node = SeonsorReader()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()