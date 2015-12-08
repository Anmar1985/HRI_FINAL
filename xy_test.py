import ctypes
import api
import os
import time
import sys
import struct


def Main():
        #api.ServoShutdown()
        try:
                if api.Initialize():
                        print("Initalized")
                else:
                        print("Intialization failed")
                #api.ServoShutdown()
                api.PlayAction(8)
                #value = int(input("Turn head to"))
                #api.SetMotorValue(20, value)
                Run()
        except (KeyboardInterrupt):
                api.ServoShutdown()
                sys.exit()
        except():
                api.ServoShutdown()
                sys.exit()

def Run():
        command=1
        #api.Walk(True)
        #print("Running...")
        #move foward
        if(command == 1):
		x = int(input("enter X "))
		y = int(input("enter Y "))
                api.Walk(True)
		api.Walking(x,y)
		command = 2
		#api.PlayAction(15)
                #api.WalkMove(0)
                #api.Walk(True)
                #api.WalkMove(20)
        #move back
        elif(command == 2):
                com = input("Enter command")
		if comm == 's':
		  api.Walk(Flase)	
		#print("supposed to move backwards")
        #move right
        elif(command == 8):
                api.WalkMove(0)
                api.WalkTurn(20)
        #move left
        elif(command == 9):
                api.WalkMove(0)
                api.WalkTurn(-20)
        elif(command == 5):
                api.WalkMove(0)
        Run()

if __name__ == "__main__":
  Main()





