import sys, os
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import kinematics as kn
import numpy as np
# import servo_controller
import time



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


    def AngleToServo(self, num):

        # for i in range(num):
        #     self.DXL_goal_deg[i] = self._servo_offsets[i] - self._thetas[int(i/3)][int(i%3)]
       
        #FL Lower
        # self.DXL_goal_deg[0] = self._servo_offsets[0] - self._thetas[0][0]
        # # #FL Upper
        # # self.DXL_goal_deg[1] = self._servo_offsets[1] + self._thetas[0][1]
        # #FL Shoulder
        # self.DXL_goal_deg[2] = self._servo_offsets[2] - self._thetas[0][0]

        # #FR Lower
        # # self.DXL_goal_deg[3] = self._servo_offsets[3] + self._thetas[1][0]
        # # #FR Upper
        # # self.DXL_goal_deg[4] = self._servo_offsets[4] + self._thetas[1][1]
        # #FR Shoulder
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
        print("Angle ")
        print(self._thetas)
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
        thetas = DXL_controller.LadianToAngles(LaDian)
        print("Thetas")
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

    # setting the DXL_Motor
    DXL_controller = Dynamixel_Controllers()
    # DXL_controller.DynamixelSetting()

    # caculate inverse kinematics
    legPosDown=np.array([[100,-100,87.5,1],[100,-100,-87.5,1],[-100,-100,87.5,1],[-100,-100,-87.5,1]])
    #                                                                     Front
    # x y z                                                        DX                     SX
    legPosUP =np.array([[100,-100,100,1],[100,-100,-100,1],[-100,-100,100,1],[-100,-100,-100,1]])
    legPosUP2 =np.array([[100,-120,100,1],[100,-120,-100,1],[-120,-120,180,1],[-120,-120,-180,1]])
    legPosUP2 =np.array([[0,-0,0,1],[0,00,00,1],[0,0,0,1],[0,-0,-0,1]])
    DXL_controller.SetPosition(legPosDown)
 

