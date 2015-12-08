
import api
import sys
import time
#import os
#import struct
from pixy import *
from ctypes import *

class Blocks (Structure):
  _fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

if __name__ == "__main__":
  pixy_close()

  pixy_init()
  print( pixy_init())

  blocks = BlockArray(100)
  frame  = 0
  standing = True

  try:
#    if api.Initialize():
#      print("Initialized")
#    else:
#      print("Initialization failed")

    # Servo limits:
    # 3: 350-980
    # 4: 640-60
    while True:
    # api.PlayAction(8)
      count = pixy_get_blocks(100, blocks)
      if count > 0:
        # Blocks found #
        #print('frame %3d:' % (frame))
        frame += 1
        sawSig1, sawSig3 = False, False
        y1, y3 = 0, 0
        for index in range (0, count):
         str_print = ('[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % \
            (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height))
         sys.stdout.write('%s\r' % str_print)
         sys.stdout.flush() 
	 if blocks[index].signature == 1:
            sawSig1 = True
#            y1 = blocks[index].y
#          if blocks[index].signature == 3:
#            sawSig3 = True
#            y3 = blocks[index].y

#        if sawSig1:
#	  api.Walk(True)
#	  print "k"
#	  sawSig1 = False
#	  print "ON   "
 #       if sawSig1 == False:
          #api.SetMotorValue(4, curr4 + diff4)
#	  api.WalkMove(5)
#	  api.WalkMove(2)
#	  api.Walk(False)
#	  print "OFF"
#        time.sleep(0.5)
#          if standing and blocks[index].signature == 1 and blocks[index].x < 150:
#            print("Sitting down")
#            standing = False
#	    api.Walk(True)
           # api.PlayAction(15)
           # time.sleep(2)
#            break
#          elif not standing and blocks[index].signature == 1 and blocks[index].x >= 150:
#           if blocks[index].signature == 3:
#             print("Standing up")
#             standing = True
#             api.PlayAction(8)
#             time.sleep(2)
#             break
  except (KeyboardInterrupt):
    api.ServoShutdown()
    sys.exit()
    pixy_close()
    print(pixy_close())

  except():
    api.ServoShutdown()
    sys.exit()
    pixy_close()
    print(pixy.close())
