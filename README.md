# robotics_lab_1
First laboratory in robotics course in the Universidad Nacional de Colombia, the laboratory ist composed by ROS basics and the conection with MATLAB and Python.
# Linux recommended commands

## pwd
With this command you can see the route from where you are.

![Image text](img/Screenshot%20from%202022-04-06%2014-51-02.png)

## cd

This command will let you navigate through the folders in you enviroment 

![Image text](img/cd.png)

## ls 

By his own will let you to see the folders and files in your current position. It can also show the ones of other routes.

![Image text](img/ls.png)

## touch

This will allow you to create a file with the name you want. 

![Image text](img/touch.png)

## rm 

This command will let you destroy a file.

![Image text](img/rm.png)

## mkdir y rmdir

mkdir will let you to create a folder and rmdir to eliminate it. 

![Image text](img/dir.png)

## mv 

The mv command let you move a file from the position you are, or the one you specified to another location and it also lets you change the name of the file.

![Image text](img/mv.png)

## cp 

The cp command let you copy a file and as with mv rename it. 

![Image text](img/cp.png)

## man 

This command is very important because it will give you all the information about the option you can use with a command, to fulfill your needs. 

![Image text](img/man.png)

# Conecting ROS with Matlab
## roscore
In first place we launch the ROS core and initialize the turtle example.

![Image text](img/roscore.png)

## Publishing with Matlab

For this example we will publish the velocity of the turtle in order to do this, we have to create the publisher, specifying the message type and then configuring the message to give it a value and send it. 

![Image text](img/turtle_vel_matlab.png)

## Subscribing to a topic

For subscribe it is important to use the ```rossuscriber``` method giving it the topic and the message type, and in order to see the results, we can use the LatestMessage function. 

```matlab
posSubs = rossubscriber("/turtle1/pose",'turtlesim/Pose');
posSubs.LatestMessage
```

## Executing a service

For execute a service we use the ```rossvcclient``` function, passing the name of the service as a parameter. Then we create a message with the function ```rosmessage``` and define the parameters in its structure:
```
posServiceCliente = rossvcclient("/turtle1/teleport_absolute")
poseMsg = rosmessage(posServiceCliente)
poseMsg.X = 4
poseMsg.Y = 10
poseMsg.Theta = pi/2
```
It not necessary to define all parameters, just the ones we want to change. Finally we send the message to the service with ```call```:
```matlab
posResp = call(posServiceCliente,poseMsg)
```
## Killing master node

To shutdown the ros network in matlab we use the command ```rosshutdown```.

# Using Python

## Creating python script

First thing we have to do is create a new ```.py``` file inside the ```scripts``` folder and type the following text in the first line:
```python
#!/usr/bin/env
```
This line defines this file as a script. Then we need to import rospy and the messages types and services we need to use:
```python
import rospy
from geometry_msgs.msg import Twist
from turtlesim.srv import TeleportAbsolute, TeleportRelative
import termios, sys, os
from numpy import pi
import genpy
```
Also we can import other no ros releated python modules for acomplish our goal.

## Defining our goal

- Moving forward and backwards with the W and S keys, respectively
- Moving clockwise and counter-clockwise with the A and D keys
- Come back to the original central position and orientation with the R key
- A 180 degrees turn with the key SPACE

## For accomplish that goal 

- Define a function to read the user input
- Define a function to publish the velocity in the velocity node
- Define a function to use the service teleport_absolute and teleport_relative
- Use the functions define to acomplish each goal

## Function to read the user input

To do this we use the Termios recommended function:

```python
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
```

## Function to publish the velocity

In order to publish the velocity, where we create the publisher and initialize the node ```velPub```, at the same time it is neccesary to define the variable we are going to publish that it must be a Twist class instance, with is own parameters,```velLineal``` and ```velAngular``` that are entries in our function, once everything is defined we can publish with our publisher the message vel. 

```py
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
```

## Functions to teleport

In this case we have two types of teleport each one with their own parameters, nevertheless the methodology is similar.

```py
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
```
We wait for a response from the service and  use ```ServiceProxy``` to call it, once called we can give it the parameters related with each teleport.

## Defining the movement

In our main we are going to use every function that we have described:

```py
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
        if key == "q":
            break
```
We define two varibles ```linearVelocity``` and ```angularVelocity``` each one to define the linear and angular movement with the keys WASD, the r and SPACE key are define with the exact position or rotation that will be maked, additionaly we used the key Q to end or quit the script.

![Alt text](img/test.gif)