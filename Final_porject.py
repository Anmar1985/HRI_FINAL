import pyaudio
import audioop
import wave
import api
import sys
import time
import os
import struct
from pixy import *
from ctypes import *
from enum import Enum

global Pose

CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
THRESHOLD = 100
snapflag = 1

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

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

if __name__ == "__main__":

  p = pyaudio.PyAudio()
  for i in range(p.get_device_count()):
	dev = p.get_device_info_by_index(i)
	print((i, dev['name'],dev['maxInputChannels']))
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
  FSM = States.NEUTRAL.name
  try: 
   # data = stream.read(CHUNK)
    Accel = 500
    PoseFlag = 0
    walkFlag = 0
    if api.Initialize():
      	print("Initialized")
    else:
      	print("Initialization Failed")
    Walk = False 
    Slack = 0
    hug_flag = 0
    while True: 
     stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)
     data = stream.read(CHUNK)
     rms = audioop.rms(data, 2)
     print "snap flag = ",snapflag
     print("Sound level = ", rms)
     if(rms>THRESHOLD and snapflag == 1):
       snapflag = 2
       Pose ='FIST'
       print "<<<=======Single Tap=====>>>"
     elif(rms>THRESHOLD and snapflag == 2):
       snapflag = 0
       Pose ='FINGER_SPREAD'
       print "<<<======Finger Spread ====>>>"
     elif(rms>THRESHOLD and snapflag == 0):
	snapflag = 1
	Pose = 'Blank'
	print"<<======No Pose=====>>>>>"
     data = '\x00' * CHUNK
     Accel = (api.passAccelData2(1))
     count = pixy_get_blocks(100, blocks)
     print "Accelrometer =  ", Accel

     if count > 0:
        # Blocks found #
        frame += 1
        sawSig1, sawSig2 = False, False
        y1, y3 = 0, 0
        for index in range (0, count):
           #  print('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % \
            #    (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y,blocks[index].width, blocks[index].height))
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
	    print("Working in Neutral")
            if Accel < 550 and Accel > 450 and (Color == 'Red' or Color == 'Blue'):
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
                    print("Stop Walking")
                    api.WalkMove(0)
                    api.Walk(False)
                    walkFlag = 0
                    api.PlayAction(5)# Hug action
		    print("Hug")
		    hug_flag = 1

        # Red Bully
        elif FSM == 'RED_BULLY':
	    print("Working in RED bully")
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
                            api.WalkMove(Speed)
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

        #Blue Bully                
        elif FSM == 'BLUE_BULLY':
	    print "Working in BLUE bully"
            if Color != 'Blue' and Accel < 550 and Accel >450: # Relax
                    Deffence(0)
                    Bullyflag = 1
            if Color == 'Blue' and Accel < 550 and Accel >450:  # Defence
                if Bullyflag == 1:
                    Deffence(1)
                    Bullyflag = 0
                else:
                    pass
            elif Color == 'Red' and Accel < 550 and Accel >450:  #Approach
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
                  if hug_flag == 0:
                    api.WalkMove(0)
                    api.Walk(False)
                    walkFlag = 0
                    api.PlayAction(5)# Hug action
                    print("Hug")
                    hug_flag = 1

        elif FSM == 'BOTH_BULLIES':
	    print "Working in BOTH bullies"
	    if (Color == 'Red' or Color == 'Blue')  and Accel < 550 and Accel >450 and Bullyflag == 1:
			Deffence(1)
			Bullyflag = 0
	    elif Color == 'Else'  and Accel < 550 and Accel >450:
			Deffence(0)
			Bullyflag = 1
			
     else:
        print("Stop Walking end of WHILE")
        api.WalkMove(0)
        api.Walk(False)
        walkFlag = 0
     print "Last color = " , Color
     if (Accel > 590 or Accel < 450 ) and (Accel < 900) and( Color == 'Red' or Color == 'Blue'):
                print("Fall")
                GetUp()
                if Color == 'Red' and FSM == 'NEUTRAL':
                    print("Fall by Red")
                    FSM = States.RED_BULLY.name  # Switch to Red Bully state
                    Red = 1
                elif Color == 'Blue' and FSM == 'NEUTRAL':
                    print("Fall by Blue")
                    FSM = States.BLUE_BULLY.name  # Switch to Blue Bully State
                    Blue = 1
		elif Color == 'Blue' and FSM == 'RED_BULLY':
                    print("Fall by Blue")
                    FSM = States.BOTH_BULLIES.name  # Switch to Both Bullies state
                    Blue = 1
                elif Color == 'Red' and FSM == 'BLUE_BULLY':
                    print("Fall by Red")
                    FSM = States.BOTH_BULLIES.name  # Switch to Both Bullies State
                    Red = 1
                elif Color == 'Red' and FSM == 'RED_BULLY':  # Keep State and hate more
                    print("Fall by Red")
                    Red = Red + 1
                elif Color == 'Blue' and FSM == 'BLUE_BULLY': #Keep state and Hate more
                    print("Fall by Blue")
                    Blue = Blue + 1
                elif Color == 'Red' and FSM == 'BOTH_BULLIES': #Keep state and hate more
                    print("Fall by Red")
                    Red = Red + 1
                elif Color == 'Blue' and FSM == 'BOTH_BULLIES': # keep state and hate more
                    print("Fall by Blue")
                    Blue = Blue + 1
                else:
                    print("Just Fall")
                snapflag = 1
                Pose = 'Blank'
		Bullyflag = 1


     if Pose == 'FIST' and Accel < 590 and Accel >450:  # Break the ice
                print("Break THe Ice")
		if FSM == 'RED_BULLY':
                    if Red == 1:
                        FSM = States.NEUTRAL.name #Switch to neutral
                        print("OK")
                        Deffence(0)
                    else:
                        Red = Red - 1
                        api.PlayAction(38) # Refuse page
                        print("No")
	            snapflag = 1
  	            Pose = 'Blank'
          	    Bullyflag = 1

                elif FSM == 'BOTH_BULLIES':
                    if Red == 1:
                        FSM = States.BLUE_BULLY.name #Switch to Blue Bully
                        print("OK")
                        Deffence(0)
                    else:
                        Red = Red - 1
                        api.PlayAction(38) # Refuse page
                        print("No")
                    snapflag = 1
                    Pose = 'Blank'
                    Bullyflag = 1


     elif Pose == 'FINGER_SPREAD' and Accel < 590 and Accel >450:  # Break the ice
            if FSM == 'BLUE_BULLY':
		if Blue == 1:
                    FSM = States.NEUTRAL.name #Switch to neutral
                    Deffence(0)
                else:
                    Blue = Blue - 1
                    api.PlayAction(38) # Refuse page
            elif FSM == 'BOTH_BULLIES':
                if Blue == 1:
                    FSM = States.RED_BULLY.name #Switch to neutral
		    Deffence(0)
                else:
                    Blue = Blue - 1
                    api.PlayAction(38) # Refuse page
            snapflag = 1
            Pose = 'Blank'
            Bullyflag = 1

     p.close(stream)
     print "Last Pose = ",Pose
     print "Current State = ", FSM
  except (KeyboardInterrupt):
    api.ServoShutdown()
    sys.exit()
    pixy_close(stream)
    p.close(stream)

  except IOError as ex:
	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index = 2,
                frames_per_buffer=CHUNK)
  	data = stream.read(CHUNK)
  except():
    api.ServoShutdown()
    sys.exit()
    pixy_close()
    p.close(stream)
