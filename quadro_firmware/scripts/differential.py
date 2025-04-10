#! /usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Bool, Int64
import lgpio
import math

h = lgpio.gpiochip_open(0)

class Differential(Node):
    def __init__(self):
        super().__init__("differential")

        # Subscriber
        self.cmd_sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)

        # Motor Pins
        self.leftEn = 12
        self.rightEn = 13
        self.left_1 = 23
        self.left_2 = 24
        self.right_1 = 25
        self.right_2 =16 

        # GPIO Setup
        lgpio.gpio_claim_output(h, self.leftEn)
        lgpio.gpio_claim_output(h, self.rightEn)
        lgpio.gpio_claim_output(h, self.left_1)
        lgpio.gpio_claim_output(h, self.left_2)
        lgpio.gpio_claim_output(h, self.right_1)
        lgpio.gpio_claim_output(h, self.right_2)


        # # PWM Setup
        # self.pwmL = GPIO.PWM(self.leftEn, 100)
        # self.pwmR = GPIO.PWM(self.rightEn, 100)
        # self.pwmL.start(0)
        # self.pwmR.start(0)

        # Robot Parameters
        self.wheelDia = 0.065  # Wheel diameter (m)
        self.wheelSep = 0.28   # Wheel separation (m)
        self.motorRPM = 60     # Motor RPM
        self.circumference = math.pi * self.wheelDia
        self.max_vel = (self.circumference * self.motorRPM) / 60

    def cmd_callback(self, data):
        linear_x = data.linear.x
        angular_z = data.angular.z

        self.v_left = linear_x - ((angular_z * self.wheelSep) / 2)
        self.v_right = linear_x + ((angular_z * self.wheelSep) / 2)
        # print("v_left = ",self.v_left)
        # print("v_right: ",self.v_right)

        lpwm = int(abs(self.v_left * 255) / self.max_vel)
        rpwm = int(abs(self.v_right * 255) / self.max_vel)


        # Cap PWM at 255
        if rpwm >= 255 :
            rpwm = 255

        if lpwm >= 255:
            lpwm = 255
        print("lpwm: ",lpwm)
        print("rpwm: ",rpwm)

        # Stop if no movement
        if linear_x == 0.0 and angular_z == 0.0:
            self.stop()
        else:
            self.move(lpwm, rpwm)

    def move(self, lpwm, rpwm):
        lpwm = lpwm
        rpwm = rpwm
        lpwmPer = int((lpwm / 255) * 100)
        rpwmPer = int((rpwm / 255) * 100)
        # if lpwmPer >= 100:
        #     lpwmPer = 100

        # if rpwmPer>=100
        print("lpwnPer: ",lpwmPer)
        print("rpwnPer: ",rpwmPer)

        # Left motor direction
        if self.v_left > 0:
            lgpio.gpio_write(h, self.left_1,1 )
            lgpio.gpio_write(h, self.left_2,0)
            print("v_left>0")
        elif self.v_left<0:
            lgpio.gpio_write(h, self.left_1,0)
            lgpio.gpio_write(h, self.left_2,1)
            print("v_left<0")

        # Right motor direction
        if self.v_right > 0:
            lgpio.gpio_write(h, self.right_1,1)
            lgpio.gpio_write(h, self.right_2,0)
            print("v_right>0")
        elif self.v_right<0:
            lgpio.gpio_write(h, self.right_1,0)
            lgpio.gpio_write(h, self.right_2,1)
            print("v_right<0")

        # Update PWM values
        lgpio.tx_pwm(h,self.leftEn,50,lpwmPer)
        lgpio.tx_pwm(h,self.rightEn,50, rpwmPer)

    def stop(self):
        lgpio.gpio_write(h, self.left_1,0)
        lgpio.gpio_write(h, self.left_2,0 )
        lgpio.gpio_write(h, self.right_1,0 )
        lgpio.gpio_write(h, self.right_2,0)

        lgpio.tx_pwm(h,self.leftEn,50,0)
        lgpio.tx_pwm(h,self.rightEn,50, 0)



def main(args=None):
    rclpy.init(args=args)
    node = Differential()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        lgpio.gpiochip_close(h) # Clean up GPIO
        rclpy.shutdown()

if __name__ == "__main__":
    main()