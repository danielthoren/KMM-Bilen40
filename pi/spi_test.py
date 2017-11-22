import time
from spi import *

data = [120, 160]
recieved = 0

recieved = motorTransceiver(data)
    
print("recieved data: ", recieved)
'''
time.sleep(5)

data = [120, 90]

recieved = motorTransceiver(data)
    
print("recieved data: ", recieved)
   ''' 
