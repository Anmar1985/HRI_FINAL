import sys
from enum import Enum

class States(Enum):
        NEUTRAL    = 0
        RED_BULLY  = 1
        BLUE_BULLY = 2
        BOTH_BULLY = 3
class Actions(Enum):
        GET_UP   = 1
        DEFFEND  = 2
        APPROACH = 3


if __name__ == "__main__":
	FSM = States.NEUTRAL.name
	print FSM

