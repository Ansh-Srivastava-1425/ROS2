import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class DisplaySub(Node):
    def __init__(self):
        super().__init__('display_sub')

        self.subscription = self.create_subscription(
            Float32, 'filtered_temperature', self.callback, 10)

    def callback(self, msg):
        self.get_logger().warn(f'HIGH TEMP ALERT: {msg.data}')


def main(args=None):
    rclpy.init(args=args)
    node = DisplaySub()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()  