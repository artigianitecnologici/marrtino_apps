import sys, os
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import rospy
import rosnode
import kinematics as kn
import numpy as np
# import servo_controller
import time
import math

from std_msgs.msg import String,Float64

TOPIC_sfr05 = "sfr05_controller/command"
TOPIC_sfr04 = "sfr04_controller/command"
TOPIC_sfr03 = "sfr03_controller/command"

TOPIC_sfl02 = "sfl02_controller/command"
TOPIC_sfl01 = "sfl01_controller/command"
TOPIC_sfl00 = "sfl00_controller/command"

TOPIC_sbr11 = "sbr11_controller/command"
TOPIC_sbr10 = "sbr10_controller/command"
TOPIC_sbr09 = "sbr09_controller/command"

TOPIC_sbl08 = "sbl08_controller/command"
TOPIC_sbl07 = "sbl07_controller/command"
TOPIC_sbl06 = "sbl06_controller/command"               

global sfr05_pub





def sfr04(msg):
    print('Front Right 04 %s' %(msg))
    sfr04_pub.publish(msg)

def sfr03(msg):
    print('Front Right 03 %s' %(msg))
    sfr03_pub.publish(msg)

def sfl02(msg):
    sfl02_pub.publish(msg)

def sfl01(msg):
    sfl01_pub.publish(msg)
    
def sfl00(msg):
    sfl00_pub.publish(msg)

def sbr11(msg):
    sbr11_pub.publish(msg)

def sbr10(msg):
    sbr10_pub.publish(msg)

def sbr09(msg):
    sbr09_pub.publish(msg)

def sbl08(msg):
    sbl08_pub.publish(msg)

def sbl07(msg):
    sbl07_pub.publish(msg)
    
def sbl06(msg):
    sbl06_pub.publish(msg)

    

class Dynamixel_Controllers:
    def __init__(self):

        self.DXL_goal_deg = [0 for i in range(12)]
        self.DXL_present_deg = []
        self.DXL_present_POSITION_VALUE = []
        self.DXL_goal_POSITION_VALUE = [0 for i in range(12)]
                             # BR10  11    9    7  BL8   FR3   FR4   FL2   FL0  FL1   FR5
        self._servo_offsets = [150, 150, 150, 150, 150, 140, 150, 150, 150, 150, 150, 150]
       
    def LadianToAngles(self, La):
        # radian to degree
        La *= 180/np.pi
        La = [ [ int(x) for x in y ] for y in La ]

        self._thetas = La
        return self._thetas

    

    def sfr05(self,msg):
        #print('Front Right #FL Shoulder %s' %(msg))
        sfr05_pub.publish(msg)

    def sfr04(self,msg):
        #print('Front Right 04 %s' %(msg))
        sfr04_pub.publish(msg)

    def sfr03(self,msg):
        #print('Front Right 03 %s' %(msg))
        sfr03_pub.publish(msg)

    def sfl02(self,msg):
        sfl02_pub.publish(msg)

    def sfl01(self,msg):
        sfl01_pub.publish(msg)
        
    def sfl00(self,msg):
        sfl00_pub.publish(msg)

    def sbr11(self,msg):
        sbr11_pub.publish(msg)

    def sbr10(self,msg):
        sbr10_pub.publish(msg)

    def sbr09(self,msg):
        sbr09_pub.publish(msg)

    def sbl08(self,msg):
        sbl08_pub.publish(msg)

    def sbl07(self,msg):
        sbl07_pub.publish(msg)
        
    def sbl06(self,msg):
        sbl06_pub.publish(msg)

    def ServoZero(self):
        self.sfr05(0) #FL Shoulder
        self.sfr04(-1.57)
        self.sfr03(1.57)
        self.sfl02(0)
        self.sfl01(1.57)
        self.sfl00(-1.57)
        self.sbr11(0)
        self.sbr10(-1.57)
        self.sbr09(1.57)
        self.sbl08(0)
        self.sbl07(1.57)
        self.sbl06(-1.57)

    def AngleToServo(self, num):

        # for i in range(num):
        #     self.DXL_goal_deg[i] = self._servo_offsets[i] - self._thetas[int(i/3)][int(i%3)]
       
        #FL Lower
        # self.DXL_goal_deg[0] = self._servo_offsets[0] - self._thetas[0][0]
        # # #FL Upper
        # # self.DXL_goal_deg[1] = self._servo_offsets[1] + self._thetas[0][1]
        #FL Shoulder
        self.sfr05(math.radians(-self._thetas[0][0]))
        self.sfr04(math.radians(self._thetas[0][1]))
        self.sfr03(math.radians(self._thetas[0][2]))
        #FR Shoulder
        self.sfl02(math.radians(self._thetas[1][0]))
        self.sfl01(math.radians(-self._thetas[1][1]))
        self.sfl00(math.radians(-self._thetas[1][2])) 

        self.sbr11(math.radians(5)+math.radians(self._thetas[2][0]))
        self.sbr10(math.radians(self._thetas[2][1]))
        self.sbr09(math.radians(self._thetas[2][2]))
        print(self._thetas[2][2])
        #FR Shoulder
        self.sbl08(math.radians(self._thetas[1][0]))
        self.sbl07(math.radians(-self._thetas[3][1]))
        self.sbl06(math.radians(-self._thetas[3][2])) 
        print(self._thetas[3][2])




        #self.DXL_goal_deg[2] = self._servo_offsets[2] - self._thetas[0][0]

        # #FR Lower
        # # self.DXL_goal_deg[3] = self._servo_offsets[3] + self._thetas[1][0]
        # # #FR Upper
        # # self.DXL_goal_deg[4] = self._servo_offsets[4] + self._thetas[1][1]
        # 
        # self.DXL_goal_deg[5] = self._servo_offsets[5] + self._thetas[1][0]

        # #BL Lower
        # # self.DXL_goal_deg[6] = self._servo_offsets[6] - self._thetas[2][0]
        # # #BL Upper
        # # self.DXL_goal_deg[7] = self._servo_offsets[7] - self._thetas[2][1]
        # #BL Shoulder, Formula flipped from the front
        # self.DXL_goal_deg[8] = self._servo_offsets[8] - self._thetas[2][0]

        # #BR Lower.
        # # self.DXL_goal_deg[9] = self._servo_offsets[9] + self._thetas[3][0]
        # # #BR Upper
        # # self.DXL_goal_deg[10] = self._servo_offsets[10] + self._thetas[3][1]
        # #BR Shoulder, Formula flipped from the front
        # self.DXL_goal_deg[11] = self._servo_offsets[11] + self._thetas[3][0]
       
        return self.DXL_goal_deg

    def DegreeToDXLValue(self, Dg):

        self.DXL_goal_POSITION_VALUE = [ int(i / 0.29) for i in Dg ]
        return self.DXL_goal_POSITION_VALUE

    def DXLValueToDegree(self, VL):

        self.DXL_present_deg = [ int(i * 0.29) for i in VL ]
        return self.DXL_present_deg

    

    def SetPosition(self,LegsPosition):
        print(LegsPosition)
        LaDian = kn.initIK(LegsPosition) #radians
        
        # set numbers of motor and ID
        DXLMotor_N = 12
        DXL_ID = [ i + 1 for i in range(DXLMotor_N)]
        # DXL_ID = []

        # calculate DXL_goal_position_value
        print("Angle R/G Thetas")
        print(LaDian)
        thetas = DXL_controller.LadianToAngles(LaDian)
        
        print (thetas)
        Goal_Degree = DXL_controller.AngleToServo(DXLMotor_N)

        Goal_Position_Value = DXL_controller.DegreeToDXLValue(Goal_Degree)
        # DXL_controller.SetSpeed(DXLMotor_N,100)
        # DXL_controller.EnableTorque(DXLMotor_N)

        # write and read DXL_servo
        # DXL_controller.WriteMotor(DXLMotor_N)

        
        # print(Goal_Degree)
        # print(Goal_Position_Value)
        # # DXL_controller.ReadMotor(DXLMotor_N)

if __name__=="__main__":
    # Initialize
    rospy.init_node('robotdog', anonymous=False)

    sfr05_pub = rospy.Publisher(TOPIC_sfr05, Float64, queue_size=1,   latch=True)
    sfr04_pub = rospy.Publisher(TOPIC_sfr04, Float64, queue_size=1,   latch=True)
    sfr03_pub = rospy.Publisher(TOPIC_sfr03, Float64, queue_size=1,   latch=True)

    sfl02_pub = rospy.Publisher(TOPIC_sfl02, Float64, queue_size=1,   latch=True)
    sfl01_pub = rospy.Publisher(TOPIC_sfl01, Float64, queue_size=1,   latch=True)
    sfl00_pub = rospy.Publisher(TOPIC_sfl00, Float64, queue_size=1,   latch=True)

    sbr11_pub = rospy.Publisher(TOPIC_sbr11, Float64, queue_size=1,   latch=True)
    sbr10_pub = rospy.Publisher(TOPIC_sbr10, Float64, queue_size=1,   latch=True)
    sbr09_pub = rospy.Publisher(TOPIC_sbr09, Float64, queue_size=1,   latch=True)

    sbl08_pub = rospy.Publisher(TOPIC_sbl08, Float64, queue_size=1,   latch=True)
    sbl07_pub = rospy.Publisher(TOPIC_sbl07, Float64, queue_size=1,   latch=True)
    sbl06_pub = rospy.Publisher(TOPIC_sbl06, Float64, queue_size=1,   latch=True)

    # setting the DXL_Motor
    DXL_controller = Dynamixel_Controllers()
    # DXL_controller.DynamixelSetting()

    # caculate inverse kinematics
    legPosDown=np.array([[100,-100,87.5,1],[100,-100,-87.5,1],[-100,-100,87.5,1],[-100,-100,-87.5,1]])
    #                                                                     Front
    # x y z   
    legPosSeduto=np.array([[100,-180,87.5,1],[100,-180,-87.5,1],[-100,-130,87.5,1],[-100,-130,-87.5,1]]) 
    legPosZampa=np.array([[120,-140,87.5,1],[100,-180,-87.5,1],[-100,-130,87.5,1],[-100,-130,-87.5,1]])           
    legPosUP =np.array([[100,-180,100,1],[100,-180,-100,1],[-100,-180,100,1],[-100,-180,-100,1]])
    legPosUPM =np.array([[100,-150,100,1],[100,-150,-100,1],[-100,-150,100,1],[-100,-150,-100,1]])
    DXL_controller.SetPosition(legPosDown)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosSeduto)
    time.sleep(5)
    DXL_controller.SetPosition(legPosDown)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUPM)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUPM)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUPM)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUPM)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUP)
    time.sleep(5)
    DXL_controller.SetPosition(legPosUPM)
    time.sleep(5)
    
    #DXL_controller.SetPosition(legPosZampa)
    #DXL_controller.ServoZero()
     # Sleep to give the last log messages time to be sent
    #print(math.radians(90))
    rospy.sleep(1)

 

