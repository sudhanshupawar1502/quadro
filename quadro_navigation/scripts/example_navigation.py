#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from nav2_simple_commander.robot_navigator import BasicNavigator
from geometry_msgs.msg import PoseStamped
import tf_transformations
import math

class ExampleNavigation(Node):
    def __init__(self):
        super().__init__("example_navigation")
        self.pose = PoseStamped()


    def create_pose_stamped(self, navigator : BasicNavigator, pos_x, pos_y, orientation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)

        self.pose.header.frame_id = "map"
        self.pose.header.stamp = navigator.get_clock().now().to_msg()
        self.pose.pose.position.x = pos_x
        self.pose.pose.position.y = pos_y
        self.pose.pose.position.z = 0.0
        self.pose.pose.orientation.x = q_x
        self.pose.pose.orientation.y = q_y
        self.pose.pose.orientation.z = q_z
        self.pose.pose.orientation.w = q_w
        return 0
    
    def waypoints(self, navigator : BasicNavigator):

        #set initial pose
        initial_pose = self.create_pose_stamped(0.0, 0.0, 0.0)
        navigator.setInitialPose(initial_pose)

        #wait for nav2
        navigator.waitUntilNav2Active()

        #set waypoints
        goal_pose_1 = self.create_pose_stamped(2.0, 5.0, (math.pi)/2)
        goal_pose_2 = self.create_pose_stamped(-2.0, 3.0, math.pi)
        goal_pose_3 = self.create_pose_stamped(2.0, -5.0, -(math.pi)/2)


        waypoints  = [goal_pose_1, goal_pose_2, goal_pose_3]

        #follow waypoints
        navigator.followWaypoints(waypoints)

        # get feedback
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            print(feedback)

        print(navigator.getResult()) 

def main(args = None):
    rclpy.init(args=args)
    node = ExampleNavigation()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()

