import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class FilterNode(Node):
    def __init__(self):
        super().__init__('filter_node')

        self.declare_parameter('threshold', 30.0)
        
        self.subscription = self.create_subscription(
            Float32, 'temperature', self.callback, 10)
        
        self.publisher_ = self.create_publisher(
            Float32, 'filtered_temperature', 10)

    def callback(self, msg):
        threshold = self.get_parameter('threshold').value
        if msg.data > threshold:
            self.publisher_.publish(msg)
            self.get_logger().info(f'PASSED: {msg.data} > {threshold}')

        else:
            self.get_logger().info(f'dropped: {msg.data} <= {threshold}')

def main(args=None):
    rclpy.init(args=args)
    node = FilterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()