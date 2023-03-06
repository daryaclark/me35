import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class PublisherNode(Node):

    def __init__(self):

        super().__init__('publisher_node')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

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
        
        contVal = input('Continue? ')

        if contVal == 'y':
            cont = True
        else: 
            cont = False

        self.publisher_.publish(twist)

        return cont


def main(args=None):
    
    rclpy.init(args=args)
    
    node1 = PublisherNode()
    try:
        
        loop = True

        while loop:

            cont = node1.publish_velocities()

            if cont == False:

                node1.destroy_node()
                rclpy.shutdown()
                
                loop = False

        # PublisherNode.destroy_node()
        # rclpy.shutdown()
    except KeyboardInterrupt:
        print('\nCaught Keyboard Interrupt')

        # Destroys the node that was created
        node1.destroy_node()

        rclpy.shutdown()


if __name__ == '__main__':
    main()
