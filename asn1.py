#!/usr/bin/env python
import roslib
import rospy
from fw_wrapper.srv import *

# -----------SERVICE DEFINITION-----------
# allcmd REQUEST DATA
# ---------
# string command_type
# int8 device_id
# int16 target_val
# int8 n_dev
# int8[] dev_ids
# int16[] target_vals

# allcmd RESPONSE DATA
# ---------
# int16 val
# --------END SERVICE DEFINITION----------

# ----------COMMAND TYPE LIST-------------
# GetMotorTargetPosition
# GetMotorCurrentPosition
# GetIsMotorMoving
# GetSensorValue
# GetMotorWheelSpeed
# SetMotorTargetPosition
# SetMotorTargetSpeed
# SetMotorTargetPositionsSync
# SetMotorMode
# SetMotorWheelSpeed

# wrapper function to call service to get sensor value
def getSensorValue(port):
    rospy.wait_for_service('allcmd')
    try:
	send_command = rospy.ServiceProxy('allcmd', allcmd)
        resp1 = send_command('GetSensorValue', port, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to set a motor target position
def setMotorTargetPositionCommand(motor_id, target_val):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('SetMotorTargetPosition', motor_id, target_val, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to get a motor's current position
def getMotorPositionCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetMotorCurrentPosition', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

# wrapper function to call service to check if a motor is currently moving
def getIsMotorMovingCommand(motor_id):
    rospy.wait_for_service('allcmd')
    try:
        send_command = rospy.ServiceProxy('allcmd', allcmd)
	resp1 = send_command('GetIsMotorMoving', motor_id, 0, 0, [0], [0])
        return resp1.val
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

def HandWave():         # call function to get sensor value
        sensor_reading = getSensorValue(1) # port 1, so DMS sensor
        rospy.loginfo("Sensor value at port %d: %f", 1, sensor_reading)
	if (sensor_reading > 1700):
		stand_up()
        	motor_id = 5
        	target_val = 700
        	# call function to set motor position
        	response = setMotorTargetPositionCommand(5, 700) # parameters are motor_id, target_val
		rospy.sleep(1.) # making a delay
		for waveTurns in range (0, 3):
			response = setMotorTargetPositionCommand(1, 300)
			rospy.sleep(1.)
			response = setMotorTargetPositionCommand(1, 650)
	stand_up()


#this function makes the quadropod lie down and have all four legs extended
def lay_down():
	target_val = 512
	response = setMotorTargetPositionCommand(1, target_val)
	response = setMotorTargetPositionCommand(2, target_val)
	response = setMotorTargetPositionCommand(3, target_val)
	response = setMotorTargetPositionCommand(4, target_val)
	legs = 512
	response = setMotorTargetPositionCommand(5, legs) #8 and 5 move up when target moves up
	response = setMotorTargetPositionCommand(6, legs) #6 and 7 move down when target moves up
	response = setMotorTargetPositionCommand(7, legs)
	response = setMotorTargetPositionCommand(8, legs)

#stand_up function makes the robot turn its legs 90 degrees
def stand_up():
	target_val = 500
	response = setMotorTargetPositionCommand(1, target_val)
	response = setMotorTargetPositionCommand(2, target_val)
	response = setMotorTargetPositionCommand(3, target_val)
	response = setMotorTargetPositionCommand(4, target_val)
	six_seven = 800
	five_eight = 200
	response = setMotorTargetPositionCommand(5, five_eight) #8 and 5 move up when target moves up
	response = setMotorTargetPositionCommand(6, six_seven) #6 and 7 move down when target moves up
	response = setMotorTargetPositionCommand(7, six_seven)
	response = setMotorTargetPositionCommand(8, five_eight)

def HandMotionSensor():
	sensor_reading = getSensorValue(2) # port is 2, so IR sensor
	if (sensor_reading < 50): # a higher sensor_reading means closer
		stand_up()
	else:
		lay_down()

def MoveAllMotors(m1, m2, m3, m4, m5, m6, m7, m8):
	response = setMotorTargetPositionCommand(1, m1)
	response = setMotorTargetPositionCommand(2, m2)
	response = setMotorTargetPositionCommand(3, m3)
	response = setMotorTargetPositionCommand(4, m4)
	response = setMotorTargetPositionCommand(5, m5)
	response = setMotorTargetPositionCommand(6, m6)
	response = setMotorTargetPositionCommand(7, m7)
	response = setMotorTargetPositionCommand(8, m8)

def MoveAllMotorsLeft(m1, m2, m3, m4, m5, m6, m7, m8):
	response = setMotorTargetPositionCommand(1, m2) 
	response = setMotorTargetPositionCommand(2, m4)
	response = setMotorTargetPositionCommand(3, m1)
	response = setMotorTargetPositionCommand(4, m3)
	response = setMotorTargetPositionCommand(5, m6)
	response = setMotorTargetPositionCommand(6, m8)
	response = setMotorTargetPositionCommand(7, m5)
	response = setMotorTargetPositionCommand(8, m7)

def MoveAllMotorsRight(m1,m2,m3,m4,m5,m6,m7,m8):
	response = setMotorTargetPositionCommand(1, m3) 
	response = setMotorTargetPositionCommand(2, m1)
	response = setMotorTargetPositionCommand(3, m4)
	response = setMotorTargetPositionCommand(4, m2)
	response = setMotorTargetPositionCommand(5, m7)
	response = setMotorTargetPositionCommand(6, m5)
	response = setMotorTargetPositionCommand(7, m8)
	response = setMotorTargetPositionCommand(8, m6)

def ReadAllMotors():
	m1 = getMotorPositionCommand(1)
	m2 = getMotorPositionCommand(2)
	m3 = getMotorPositionCommand(3)
	m4 = getMotorPositionCommand(4)
	m5 = getMotorPositionCommand(5)
	m6 = getMotorPositionCommand(6)
	m7 = getMotorPositionCommand(7)
	m8 = getMotorPositionCommand(8)
	rospy.loginfo("Motor positions: %d, %d, %d, %d, %d, %d, %d, %d", m1, m2, m3, m4, m5, m6, m7, m8)
	
	
# Main function
if __name__ == "__main__":
    rospy.init_node('example_node', anonymous=True)
    rospy.loginfo("Starting Group X Control Node...")
    #lay_down()
    MoveAllMotors(341, 605, 692, 365, 159, 817, 854, 179) #stand up position, all legs curled
    # control loop running at 10hz
    r = rospy.Rate(10) # 10hz
    #stand_up()
    while not rospy.is_shutdown():
	#motor_id = 1
	#target_val = 500
	#response = setMotorTargetPositionCommand(motor_id, target_val)
	#stand_up()
	#sensor_reading = getSensorValue(1) # port 1, so DMS sensor
        #rospy.loginfo("Sensor value at port %d: %f", 1, sensor_reading)	

	#MoveAllMotors(369, 619, 645, 367, 221, 808, 840, 212)
	#MoveAllMotors(322, 591, 556, 367, 239, 512, 530, 213)
	#MoveAllMotors(323, 796, 285, 367, 220, 829, 780, 193)
	#MoveAllMotors(323, 528, 553, 365, 477, 828, 831, 497)
	#MoveAllMotors(198, 527, 552, 624, 202, 733, 831, 169)

	#ReadAllMotors()
	# 1 is tLeft, 2 is tRight, 3 is bLeft, 4 is bRight (main motors)
	# 5 is tLeft, 6 is tRight, 7 is bLeft, 8 is bRight (ankles)
	#			 tLeft,tRi, bLef,bRi,tLef,tRig,bLef,bRig)
	MoveAllMotors(198, 516, 840, 500, 159, 817, 857, 180)# put right side forward, left legs out
	MoveAllMotors(198, 747, 840, 500, 159, 720, 857, 180)# right front leg extended
	MoveAllMotors(517, 819, 528, 206, 159, 774, 818, 184)# left side forward, right side extended, 819 is off
	MoveAllMotors(274, 819, 493, 220, 381, 840, 800, 158)# raise left leg halfway
	MoveAllMotors(183, 505, 819, 484, 182, 832, 834, 356)# push back


def MoveRight():
		MoveAllMotors(230,516,840,600,180,817,810,180)
		MoveAllMotors(230,516,840,369,180,817,810,83)
		MoveAllMotors(542,229,1024,297,140,797,806,29) #1024 should be 1234
		MoveAllMotors(542,229,1024,297,140,616,806,29)
		MoveAllMotors(542,396,1024,297,140,616,806,0) #0 should be -47


	#HandMotionSensor() #Behavior one
	#HandWave() #Behavior two
	

        # sleep to enforce loop rate
        r.sleep()

