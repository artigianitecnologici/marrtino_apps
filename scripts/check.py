import sys, os, time
import rospy
import rosnode
import tf

from sensor_msgs.msg import LaserScan, Image
from nav_msgs.msg import Odometry

nodenames = []
topicnames = []

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

def printOK():
    print('%sOK%s' %(OKGREEN,ENDC))

def printFail():
    print('%sFAIL%s' %(FAIL,ENDC))

def check_ROS_q():
    r = True
    try:
        rosnode.get_node_names()
    except Exception as e:
        r = False
    return r


def check_ROS():
    global nodenames, topicnames
    print '----------------------------------------'
    print 'Check ROS...'
    nodenames = []
    topicnames = []
    r = True
    try:
        nodenames = rosnode.get_node_names()
        print '  -- Nodes: ',nodenames
        topicnames = rospy.get_published_topics()
        print '  -- Topics: ',topicnames
        printOK()
    except Exception as e:
        #print e
        r = False
        printFail()
    return r

def check_robot():
    global nodenames
    r = True
    print '----------------------------------------'
    print 'Check orazio robot ...'
    if '/orazio' in nodenames:
        printOK()
    else:
        printFail()
        r = False
    return r

def check_simrobot():
    global nodenames
    r = True
    print '----------------------------------------'
    print 'Check Stage simulator ...'
    if '/stageros' in nodenames:
        printOK()
    else:
        printFail()
        r = False
    return r


odomcount = 0
odomframe = ''

robot_pose = [0, 0, 0]

def odom_cb(data):
    global robot_pose, odomcount, odomframe
    robot_pose[0] = data.pose.pose.position.x
    robot_pose[1] = data.pose.pose.position.y
    o = data.pose.pose.orientation
    q = (o.x, o.y, o.z, o.w)
    euler = tf.transformations.euler_from_quaternion(q)
    robot_pose[2] = euler[2] # yaw
    odomcount += 1
    odomframe = data.header.frame_id


def check_odom():
    global topicnames, odomcount, odomframe
    r = True
    print '----------------------------------------'
    print 'Check odometry ...'
    if ['/odom', 'nav_msgs/Odometry'] in topicnames:
        odom_sub = rospy.Subscriber('odom', Odometry, odom_cb)
        dt = 1.0
        time.sleep(dt)
        odom_sub.unregister()
        print('  -- Odometry rate = %.2f Hz' %(odomcount/dt))
        print('  -- Odometry frame = %s' %(odomframe))
        printOK()
    else:
        printFail()
        r = False
    return r


        
lasercount = 0
laserframe = ''

def laser_cb(data):
    global lasercount, laserframe
    lasercount += 1
    laserframe = data.header.frame_id

def check_laser():
    global topicnames, lasercount, laserframe
    r = True
    print '----------------------------------------'
    print 'Check laser scan ...'
    if ['/scan', 'sensor_msgs/LaserScan'] in topicnames:
        lasercount = 0
        laser_sub = rospy.Subscriber('scan', LaserScan, laser_cb)
        dt = 1.0
        time.sleep(dt)
        laser_sub.unregister()
        print('  -- Laser scan rate = %.2f Hz' %(lasercount/dt))
        print('  -- Laser frame = %s' %(laserframe))
        printOK()
    else:
        printFail()
        r = False
    return r


cameracount = 0
cameraframe = ''

def image_cb(data):
    global cameracount, cameraframe
    cameracount += 1
    cameraframe = data.header.frame_id


def check_rgb_camera():
    global topicnames, cameracount, cameraframe
    r = True
    print '----------------------------------------'
    print 'Check RGB camera ...'
    if ['/rgb/image_raw', 'sensor_msgs/Image'] in topicnames:
        cameracount = 0
        camera_sub = rospy.Subscriber('/rgb/image_raw', Image, image_cb)
        dt = 1.0
        time.sleep(dt)
        camera_sub.unregister()
        print('  -- RGB camera rate = %.2f Hz' %(cameracount/dt))
        print('  -- RGB camera frame = %s' %(cameraframe))
        printOK()
    else:
        printFail()
        r = False
    return r


def check_depth_camera():
    global topicnames, cameracount, cameraframe
    r = True
    print '----------------------------------------'
    print 'Check depth camera ...'
    if ['/depth/image_raw', 'sensor_msgs/Image'] in topicnames:
        cameracount = 0
        camera_sub = rospy.Subscriber('/depth/image_raw', Image, image_cb)
        dt = 1.0
        time.sleep(dt)
        camera_sub.unregister()
        print('  -- Depth camera rate = %.2f Hz' %(cameracount/dt))
        print('  -- Depth camera frame = %s' %(cameraframe))
        printOK()
    else:
        printFail()
        r = False
    return r


tf_listener = None

def check_tf(source, target):
    global tf_listener
    r = check_ROS_q()
    if (not r):
        return r
    if (tf_listener == None):
        tf_listener = tf.TransformListener()
    print  "  -- TF %s -> %s  " %(source, target),
    try:
        tf_listener.waitForTransform(source, target, rospy.Time(), rospy.Duration(1.0))
        (posn, rotn) = tf_listener.lookupTransform(source, target, rospy.Time())
        # how much time ago we get a transform (secs)
        t = rospy.Time.now().secs - tf_listener.getLatestCommonTime(source, target).secs
        if (t<3):
            printOK()
        else:
            printFail()
            r = False
    except tf.Exception as e:
        #print e
        printFail()
        r = False
    return r


def check_tfs():
    print '----------------------------------------'
    print 'Check transforms ...'
    check_tf('map', 'odom')
    check_tf('odom', 'base_frame')
    check_tf('base_frame', 'laser_frame')
    check_tf('base_frame', 'rgb_camera_frame')
    check_tf('base_frame', 'depth_camera_frame')


def main():
    r = check_ROS()
    if (r):
        rospy.init_node('marrtino_check')
        check_simrobot()
        check_robot()
        check_odom()
        check_laser()
        check_rgb_camera()
        check_depth_camera()
        check_tfs()


if __name__=='__main__':
    main()
