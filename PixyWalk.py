import api
import sys
import time
#import os
#import struct
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
	BOTH_BULLY = 3
class Actions(Enum):
	GET_UP   = 1
	DEFFEND  = 2
	APPROACH = 3
class Colors(Enum)
	Red  = 1
	Blue = 2
	None = 3

def GetUp():
	api.PlayAction() #GetUp

def Deffence(flag):
	if flag == 1:
	   old_time = time.clock()
	   api.Walk(True)
	   api.WalkMove(-10)
	   while ((time.clock - old_time) < 2):
		pass
	   api.PlayAction() # Deffence Page
	   return 1
	if flag == 0:
	   api.PlayAction() # WalkReady
	   return 0
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
    PoseFlag = 0
    myo.connect()
    myo.add_listener(listener)
    myo.vibrate(VibrationType.SHORT)
    if api.Initialize():
      print("Initialized")
    else:
      print("Initialization Failed")
    Walk = False 
    Battery = api.BatteryVoltLevel()
    Slack = 0
    while True: 
     count = pixy_get_blocks(100, blocks)
     myo.run()
     Accel = (api.passAccelData(1))
     if Accel > 0 :
	print Accel
     if count > 0:
        # Blocks found #
        #print('frame %3d:' % (frame), count)
        frame += 1
        sawSig1, sawSig2 = False, False
        y1, y3 = 0, 0
        for index in range (0, count):
         print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % \
            (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height))
         if blocks[index].signature == 1:
            sawSig2 = True
            y2 = blocks[index].y        
	 elif blocks[index].signature == 4:
            sawSig1 = True
            y1 = blocks[index].y
         if sawSig1:
	     OldTime = time.clock()
	     Color   = Colors.Red.name
         elif (sawSig2): #and Slack > 5 : #blocks[index].width > 50:
	     OldTime = time.clock()
	     Color   = Colors.Blue.name
     #STATES
     # Neutral
     Time = time.clock - OldTime
     if FSM == 'NEUTRAL':
	if Color = 'Red' and Time < 2:
	  api.Walk(True)
	  api.WalMove(10)
	if blocks[index].x > 220 and blocks[index].width:
	  api.WalkTurn(3)
	elif blocks[index].x < 180:
	  api.WalkTurn(-3)
        
     elif FSM == 'RED_BULLY':
     elif FSM == 'BLUE_BULLY':
     elif FSM == 'BOTH_BULLY':
    	      
	sawSig1, sawSig2 = False, False 
	if Battery != api.BatteryVoltLevel():
	   Battery = api.BatteryVoltLevel()
	   print api.BatteryVoltLevel()
           if int(Battery) < 100 and Battery != -1:
	     api.Walk(False)
	     api.ServoShutdown()
	 #print Slack
     #Slack = Slack + 1
     elif count < 1 and Walk == True and Slack > 50 :
	api.WalkMove(0)
	api.Walk(False)
	print "Stop if not seeing anything"
	Slack = 0
	Walk = False
     #time.sleep(0.1)
     Slack = Slack + 1
     #print count < 1 , Walk == True ,Slack > 50
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
