import rclpy                                  # the ROS 2 library for Python
from rclpy.node import Node                   # the base class every ROS node is built from
from sensor_msgs.msg import LaserScan         # the message type the lidar publishes
from geometry_msgs.msg import Twist           # the message type for speed commands


class SeonsorReader(Node):                    # our program is a ROS node
    def __init__(self):                       # runs once, when the node starts
        super().__init__('scan_reader')       # give the node its ROS name
        self.subscription = self.create_subscription(
            LaserScan, '/scan',               # listen for lidar scans on /scan
            self.scan_callback,               # call this function for every scan
            10                                # keep up to 10 scans if we fall behind
        )
        self.cmd_pub = self.create_publisher(
            Twist, '/cmd_vel', 10             # we will send speed commands on /cmd_vel
        )
        self.turning = False                  # memory: are we in the middle of a turn?
        self.turn_dir = 1.0                   # memory: +1.0 = turn left, -1.0 = turn right


    def sector_min(self, ranges, max_range):
        closest = max_range                  # start by assuming nothing is close
        for r in ranges:                     # look at each ray in the slice
            if r < closest:                  # this ray sees something closer
                closest = r                  # remember this distance
        return max(closest, 0.0)             # a "-inf" becomes 0.0 (very close)

    def scan_callback(self, msg):             # runs every time a new scan arrives (10 times/s)
        front = min(msg.ranges[170:190])      # nearest object in a narrow cone straight ahead
        left = min(msg.ranges[225:315])       # nearest object in the left quarter
        right = min(msg.ranges[45:135])       # nearest object in the right quarter

        if front < 0.5:                       # a wall is closer than 0.5 m ahead
            if not self.turning:              # and we are NOT already turning (a new turn starts)
                if left > right:              # the left side has more free room
                    self.turn_dir = 1.0       # so choose to turn left
                else:                         # otherwise the right side has more room
                    self.turn_dir = -1.0      # so choose to turn right
            self.turning = True               # remember: we are now turning
        elif front > 1.0:                     # the way ahead is clear (more than 1 m of room)
            self.turning = False              # remember: stop turning

        cmd = Twist()                         # make an empty speed command (all speeds 0)
        if self.turning:                      # we are in a turn
            cmd.angular.z = 0.5 * self.turn_dir   # spin on the spot, left (+) or right (-)
        else:                                 # we are not turning
            cmd.linear.x = 0.15               # drive straight ahead at 0.15 m/s

        self.cmd_pub.publish(cmd)             # send the command to the wheels
        self.get_logger().info(               # print a status line in the terminal
            f'F: {front:.2f}  L: {left:.2f}  R: {right:.2f}  turning: {self.turning}'
        )


def main(args=None):                          # the function ros2 run starts
    rclpy.init(args=args)                     # start ROS in this program
    node = SeonsorReader()                    # create our node
    rclpy.spin(node)                          # keep running, waiting for scans, until Ctrl+C
    node.destroy_node()                       # clean up the node
    rclpy.shutdown()                          # shut ROS down


if __name__ == '__main__':                    # only true when this file is run directly
    main()                                    # so start the program