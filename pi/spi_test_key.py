

#! /usr/bin/python3
import curses
import time
from spi import *
import copy


stdscr = curses.initscr()
stdscr.refresh()
key = ''
data = []
data1 = [100, 90]
data2 = [100, 80]
data3 = [100, 70]
data4 = [100, 100]
data5 = [100, 110]
data6 = [100, 120]
all_data = [data1,data2,data3,data4,data5,data6]
witch_data = 0

recieved = 0
temp = copy.deepcopy(data)
while key != ord('q'):
    key = stdscr.getch()
    if key ==ord('w'):
        data = copy.deepcopy(all_data[witch_data])
        recieved = motorTransceiver(data)
        witch_data = witch_data + 1
    
curses.endwin()





