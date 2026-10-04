#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

NUM_SIDES = 4          # 3 = triangle, 4 = square, 6 = hexagon ...
PERIOD = 0.5           # seconds per step (one move or one turn)
LINEAR_SPEED = 2.0     # 2.0 m/s x 0.5 s = 1 unit per side


class MoveTurtle(Node):
    def __init__(self):
        super().__init__('move_turtle')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer = self.create_timer(PERIOD, self.move_turtle)
        self.side_count_ = 0
        self.state_ = "move"
        # angle per corner = 2*pi / sides; angular speed = angle / time of the turn step
            self.turn_speed_ = (2 * math.pi / NUM_SIDES) / PERIOD

    def move_turtle(self):
        msg = Twist()                           # all zeros by default

        if self.side_count_ >= NUM_SIDES:       # shape finished: stop
            self.publisher_.publish(msg)        # zero velocity
            self.timer.cancel()
            self.get_logger().info("Shape done")
            return

        if self.state_ == "move":               # go forward
            msg.linear.x = LINEAR_SPEED
            self.side_count_ += 1               # count one side per move
            self.state_ = "turn"
        else:                                   # turn left
            msg.angular.z = self.turn_speed_
            self.state_ = "move"

        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MoveTurtle()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()