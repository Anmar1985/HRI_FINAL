import api
import sys
import time
import os
import struct
from pixy import *
from ctypes import *
from myo import Myo
from vibration_type import VibrationType
from device_listener import DeviceListener
from pose_type import PoseType
from enum import Enum

global Pose

class States(Enum):
	NEUTRAL    = 0
	RED_BULLY  = 1
	BLUE_BULLY = 2
	BOTH_BULLIES = 3
class Actions(Enum):
	GET_UP   = 1
	DEFFEND  = 2
	APPROACH = 3
class Colors(Enum):
	Red  = 1
	Blue = 2
	Blank = 3

def GetUp():
	api.PlayAction(11) #GetUp

def Deffence(flag):
	if flag == 1:
	   old_time = time.clock()
	   api.Walk(True)
	   api.WalkMove(-10)
	   while ((time.clock() - old_time) < 2):
		pass
	   api.PlayAction(6) # Deffence Page
	elif flag == 0:
	   api.PlayAction(8) # WalkReady
class PrintPoseListener(DeviceListener):
	def on_pose(self, pose):
		global Pose
		pose_type = PoseType(pose)
		print(pose_type.name)
                Pose = (pose_type.name)

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

if __name__ == "__main__":
  Color	= Colors.Blank.name 
  OldTime = time.clock()
  Bullyflag = 1
  pixy_init()
  print pixy_init()
  global Pose
  Pose = 'Test'
  blocks = BlockArray(100)
  frame  = 0
  standing = True
  print('Start Myo for Linux')
  listener = PrintPoseListener()
  myo = Myo()	
  FSM = States.NEUTRAL.name
  try: 
    Accel = 500
    PoseFlag = 0
    myo.connect()
    myo.add_listener(listener)
    myo.vibrate(VibrationType.SHORT)
    walkFlag = 0
    if api.Initialize():
      	print("Initialized")
    else:
      	print("Initialization Failed")
    Walk = False 
    Battery = api.BatteryVoltLevel()
    Slack = 0
    hug_flag = 0
    while True: 
     count = pixy_get_blocks(100, blocks)
     myo.run()
     Accel = (api.passAccelData(1))
     if count > 0:
	myo.run()
        Accel = (api.passAccelData(1))
        print Accel
        # Blocks found #
        frame += 1
        sawSig1, sawSig2 = False, False
        y1, y3 = 0, 0
        for index in range (0, count):
             print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % \
                (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y,blocks[index].width, blocks[index].height))
             if blocks[index].signature == 1:
                sawSig2 = True
                X = blocks[index].x
             elif blocks[index].signature == 3:
                sawSig1 = True
                X = blocks[index].x
             if sawSig1:
                 OldTime = time.clock()
                 Color   = Colors.Red.name
		 print ("Color = Red")
             elif (sawSig2):
                 OldTime = time.clock()
                 Color   = Colors.Blue.name
		 print ("Color = Blue")
             else:
		OldTime = time.clock()
		print ("Color = Else")
                Color = Colors.Blank.name
     	#STATES
     	# Neutral
        Time = time.clock() - OldTime
        if FSM == 'NEUTRAL':
	    print("Neutral")
            if Accel < 550 and Accel > 450 and Color == 'Red' or Color == 'Blue':
                if blocks[index].width < 30:
                    if walkFlag == 0:
			hug_flag = 0
			print("Approach")
                        api.Walk(True)
                        for Speed in range(0,10):
                            api.WalkMove(Speed)
                            time.sleep(0.1)
                        walkFlag = 1
                    if X > 220 and blocks[index].width:
                        api.WalkTurn(5)
                    elif X < 180:
                        api.WalkTurn(-5)
                    else:
                    	api.WalkTurn(0)
                else:
		  if hug_flag == 0:
                    print("Stop")
                    api.WalkMove(0)
                    api.Walk(False)
                    walkFlag = 0
                    api.PlayAction(5)# Hug action
		    print("Hug")
		    hug_flag = 1

            elif Accel > 550 and Color == 'Red' or Color == 'Blue':
		print("Fall")
                GetUp()
                if Color == 'Red':
		    print("Fall by Red")
		    FSM = States.RED_BULLY.name  # Switch to Red Bully state
                    Red = 1
                elif Color == 'Blue':
		    print("Fall by Blue")
                    FSM = States.BLUE_BULLY.name  # Switch to Blue Bully State
                    Blue = 1
		else:
		    print("Just Fall")
        # Red Bully
        elif FSM == 'RED_BULLY':
	    print("Red is Bully")
            if Color != 'Red' and Accel < 550 and Accel >450: # Relax
                Deffence(0)
                Bullyflag = 1
		print("Relax")
            if Color == 'Red' and Accel < 550 and Accel >450:  # Defence
                if Bullyflag == 1:
                    Deffence(1)
                    Bullyflag = 0
   		    print("Defend")
            elif Color == 'Blue' and Accel < 550 and Accel >450:  #Approach
		print("Approach")
                if blocks[index].width < 20:
                    if walkFlag == 0:
			hug_flag = 0
                        api.Walk(True)
                        for Speed in range(0,10):
                            api.WalMove(Speed)
                            time.sleep(0.1)
                        walkFlag = 1
                    if X > 220 and blocks[index].width: #Adjust direction
                        api.WalkTurn(5)
                    elif X < 180:
                        api.WalkTurn(-5)
                    else:
                    	api.WalkTurn(0)
                else:
		  if hug_flag == 0:
		    print("Stop")
                    api.WalkMove(0)
                    api.Walk(False)
                    walkFlag = 0
                    api.PlayAction(5)# Hug action
		    print("Hug")
		    hug_flag = 1

            if Pose == 'FIST' and Accel < 550 and Accel >450:  # Break the ice
		    print("Break THe Ice")
                    if Red == 1:
                        FSM = States.NEUTRAL.name #Switch to neutral
			print("OK")
                    else:
                        Red = Red - 1
                        api.PlayAction(38) # Refuse page
			print("No")
            if Accel > 550:  # if pushed
                    GetUp()
                    if Color == 'Blue':
                        FSM = States.BOTH_BULLIES.name  # Both bullies
                        Blue = 1
                    elif Color == 'Red': # Hate more
                        Red = Red + 1
                    else:
                        pass
        #Blue Bully                
        elif FSM == 'BLUE_BULLY':
            if Color != 'Blue': # Relax
                    Deffence(0)
                    Bullyflag = 1
            if Color == 'Blue':  # Defence
                if Bullyflag == 1:
                    Deffence(1)
                    Bullyflag = 0
                else:
                    pass
            elif Color == 'Red':  #Approach
                Deffence(0)
                Bullyflag = 1
                if blocks[index].width < 20:
                    if walkFlag == 0:
                        api.Walk(True)
                        for Speed in range(0,10):
                            api.WalMove(Speed)
                            time.sleep(0.1)
                        walkFlag = 1
                    if X > 220 and blocks[index].width: #Adjust direction
                        api.WalkTurn(3)
                    elif X < 180:
                        api.WalkTurn(-3)
                else:
                    api.WalkMove(0)
                    api.Walk(False)
                    walkFlag = 0
                    api.PlayAction(5)# Hug action

            if Pose == 'FINGERS_SPREAD':  # Break the ice
                if Red == 1:
                    FSM = States.NEUTRAL.name #Switch to neutral
                else:
                    Blue = Blue - 1
                    api.PlayAction(38) # Refuse page
            if Accel > 550:  # if pushed
                GetUp()
                if Color == 'Red':
                    FSM = States.BOTH_BULLIES.name  # Both bullies
                    Red = 1
                elif Color == 'Blue': # Hate more
                    Blue = Blue + 1
                else:
                    pass
        elif FSM == 'BOTH_BULLIES':
	    if Color == 'Red' or Color == 'Blue':
			Deffence(0)
			Bullyflag = 1
            if Pose == 'FINGERS_SPREAD':  # Break the ice
                if Red == 1:
                    FSM = States.BLUE_BULLY.name #Switch to Blue bully
                else:
                    Red = Red - 1
                    api.PlayAction(38) # Refuse page
            elif Pose == 'FIST':  # Break the ice
                if Red == 1:
                    FSM = States.RED_BULLY.name #Switch to Red Bully
                else:
                    Red = Red - 1
                    api.PlayAction(38) # Refuse page
            if Accel >550:  # if pushed
                    GetUp()
                    if Color == 'Blue':
                        Blue = Blue + 1
                    elif Color == 'Red': # Hate more
                        Red = Red + 1
                    else:
                        pass
     else:
        print("Stop")
        api.WalkMove(0)
        api.Walk(False)
        walkFlag = 0
           
        sawSig1, sawSig2 = False, False
	Color = Colors.Blank.name
        if Battery != api.BatteryVoltLevel():
            Battery = api.BatteryVoltLevel()
#            print api.BatteryVoltLevel()
        if int(Battery) < 100 and Battery != -1:
            api.Walk(False)
            api.ServoShutdown()
  except (KeyboardInterrupt):
    api.ServoShutdown()
    sys.exit()
    pixy_close()
    pass
  except ValueError as ex:
        print(ex)
  except():
    api.ServoShutdown()
    sys.exit()
    pixy_close()
  finally:
    myo.safely_disconnect()
    print('Finished.')

