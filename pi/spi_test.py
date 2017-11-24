
#! /usr/bin/python3
import curses
import time
from spi import *
import copy


stdscr = curses.initscr()
stdscr.refresh()
key = ''

data = [100, 90]
recieved = 0
temp = copy.deepcopy(data)
while key != ord('q'):
    key = stdscr.getch()
    if key ==ord('w'):
        temp[0] = (temp[0] + 10)
        print('Data: ', data)
        print('Temp: ', temp)
        data = copy.deepcopy(temp)
        recieved = motorTransceiver(data)
    elif key ==ord('s'):
        temp[0] = (temp[0] - 10)
        data = copy.deepcopy(temp)
        recieved = motorTransceiver(data)
    elif key ==ord('d'):
        temp[1] = (temp[1] - 10)
        data = copy.deepcopy(temp)
        recieved = motorTransceiver(data)
    elif key ==ord('a'):
        temp[1] = (temp[1] + 10)
        data = copy.deepcopy(temp)
        recieved = motorTransceiver(data)
    print(recieved)

    
curses.endwin()





