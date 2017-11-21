from main import *

currVal = 0 #Input, avrage distance from the walls
pGain = 0.5 #Random value
dGain = 0.1 #Random value
old_dGain = 0 #Used in the pidloop
setVal = 0 #This is the goal.
currOutVal = main.angle #Output, the angle we want to turn

def pidLoop():
    pTerm = 0
    dTerm = 0

    errorVal = setVal - currVal

    pTerm = pGain * errorVal
    dTerm = dGain * (old_dGain - errorVal)
    old_dGain = dTerm

    main.angle = currOutVal - (pTerm + dTerm)
