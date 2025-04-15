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
        
        self.get_logger().info("Navigation_script started")


    def create_pose_stamped(self, navigator: BasicNavigator, pos_x, pos_y, orientation_z):
        q_x, q_y, q_z, q_w = tf_transformations.quaternion_from_euler(0.0, 0.0, orientation_z)
        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = navigator.get_clock().now().to_msg()
        pose.pose.position.x = pos_x
        pose.pose.position.y = pos_y
        pose.pose.position.z = 0.0
        pose.pose.orientation.x = q_x
        pose.pose.orientation.y = q_y
        pose.pose.orientation.z = q_z
        pose.pose.orientation.w = q_w
        return pose
    
    def waypoints(self):
        navigator = BasicNavigator()
        #set initial pose
        initial_pose = self.create_pose_stamped(navigator,0.0, 0.0, 0.0)
        navigator.setInitialPose(initial_pose)
        self.get_logger().info("Initial Pose Set")

        #wait for nav2
        navigator.waitUntilNav2Active()
        self.get_logger().info("waiting for nav2 to be active")

        #set waypoints
        goal_pose_1 = self.create_pose_stamped(navigator, 2.0, 5.0, 1.57)
        goal_pose_2 = self.create_pose_stamped(navigator, 0.0, 0.0, 0.0)
        goal_pose_3 = self.create_pose_stamped(navigator, 2.0, -5.0, 1.57)


        waypoints  = [goal_pose_1, goal_pose_2, goal_pose_3]

        #follow waypoints
        navigator.followWaypoints(waypoints)
        print("following waypoints")

        # get feedback
        while not navigator.isTaskComplete():
            feedback = navigator.getFeedback()
            print(feedback)

        print(navigator.getResult()) 

def main(args = None):
    rclpy.init(args=args)
    node = ExampleNavigation()
    node.waypoints()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

