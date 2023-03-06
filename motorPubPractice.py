# Title: Motor Publisher Practice
# Author: Darya Clark
# Purpose: Basic outline code to practice creating a publisher. This code
#          continuously takes in user input and responds by moving the 
#          create3 the specified angle and direction

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class PublisherNode(Node):

    def __init__(self):
        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        # Set delay in seconds
        timer_period = 1

        # Creates a timer that triggers a callback function after the set timer_period
        self.timer = self.create_timer(timer_period, self.publish_velocities)


    # creates function for velocities 
    def publish_velocities(self):

        twist = Twist()

        # Set the linear velocity
        linVelocity = input('Enter a linear velocity (float): ') 
        twist.linear.x = float(linVelocity)
        print(twist.linear.x)
        
        # Set the angular velocity
        angVelocity = input('Enter an angular velocity (float): ')
        twist.angular.z = float(angVelocity)
        print(twist.angular.z)
        
        self.publisher_.publish(twist)


def main(args=None):
    
    rclpy.init(args=args)
    
    node1 = PublisherNode()

    try:
        # runs functions in publisher until keyboard interruption 
        rclpy.spin(node1)

    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')

        # Destroys the node that was created
        node1.destroy_node()
        # Resets 
        rclpy.shutdown()


if __name__ == '__main__':
    main()
