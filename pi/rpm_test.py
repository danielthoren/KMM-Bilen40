from spi import *


while 1:
    recieved = motorTransceiver([110,90])
    print(recieved)
