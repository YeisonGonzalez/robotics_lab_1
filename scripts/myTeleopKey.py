#!/usr/bin/env

import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi
import genpy

TERMIOS = termios

def getkey():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
    new[6][TERMIOS.VMIN] = 1
    new[6][TERMIOS.VTIME] = 0
    termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
    c = None
    try:
        c = os.read(fd, 1)
    finally:
        termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
    return c

def pubVel(velLineal=0,velAngular=0):
    try:
        pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        rospy.init_node('velPub', anonymous=False)
        vel = Twist()
        vel.linear.x = velLineal
        vel.angular.z = velAngular
        rospy.loginfo(vel)
        pub.publish(vel)
    except rospy.ROSInterruptException:
       pass

def clear():
    print("TODO")
    # rospy.wait_for_service('/clear')
    # try:
    #     teleportA = rospy.ServiceProxy('/clear',Clear)
    #     resp1 = teleportA()
    # except rospy.ServiceException as e:
    #     print(str(e))

def teleportAbsolute(x, y, ang):
    rospy.wait_for_service('/turtle1/teleport_absolute')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_absolute', TeleportAbsolute)
        teleportA(x, y, ang)
        print('Teleported to x: {}, y: {}, ang: {}'.format(str(x),str(y),str(ang)))
    except rospy.ServiceException as e:
        print(str(e))

def teleportRelative(linear, angular):
    rospy.wait_for_service('/turtle1/teleport_relative')
    try:
        teleportA = rospy.ServiceProxy('/turtle1/teleport_relative', TeleportRelative)
        teleportA(linear, angular)
        print('Teleported {} units forward and rotated {} radians'.format(str(linear),str(angular)))
    except rospy.ServiceException as e:
        print(str(e))

# class Clear(object):
#   _type          = 'clear'
#   _md5sum = 'a130bc60ee6513855dc62ea83fcc5b20'
#   _request_class  = genpy.Message
#   _response_class = genpy.Message

if __name__ == "__main__":
    linearVelocity = 0.5
    angularVelocity = 0.3
    while(not rospy.is_shutdown()):
        key = str(getkey())[2].lower()
        if key == "w":
            pubVel(linearVelocity,0)
        if key == "s":
            pubVel(-linearVelocity,0)
        if key == "a":
            pubVel(0,angularVelocity)
        if key == "d":
            pubVel(0,-angularVelocity)
        if key == "r":
            teleportAbsolute(5.5,5.5,0)
        if key == " ":
            teleportRelative(0,pi)
        if key == "c":
            clear()
        if key == "q":
            break