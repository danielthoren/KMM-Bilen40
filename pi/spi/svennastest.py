import wiringpi

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1
mosi = 0
miso = 2
sclk = 3 

if (wiringpi.wiringPiSPISetup(0,5000) == -1):
    print("error in wiringpi setup. Initialization failed!")

'''
    
number = 13375

number_hex = hex(number).split('x')[-1]

if (len(number_hex) % 2 != 0):
    number_hex = '0' + number_hex

print(number_hex)

hexbuf = bytes.fromhex(number_hex)

print(hexbuf)

print(int.from_bytes(hexbuf, byteorder='big'))

hexbuf += bytes([0, 25, 0])

print(hexbuf)

print(hexbuf[0], hexbuf[1], hexbuf[2], hexbuf[3], hexbuf[4])

print(int.from_bytes(hexbuf, byteorder='big'))
    
'''

buf = bytes([0, 0, 16, 0, 0])

print("sending out databuf: ", buf)

retlen, retdata = wiringpi.wiringPiSPIDataRW(0,buf)
#sends out data which is replaced by data from bus

'''

if isinstance(int.from_bytes(retdata, byteorder='big'), int):
    print ()

if isinstance
retdata.decode("utf-8")

'''

print("|length: ", retlen," | data: ", retdata, " | buf: ", buf, " | int: ", int.from_bytes(retdata, byteorder='big'))
