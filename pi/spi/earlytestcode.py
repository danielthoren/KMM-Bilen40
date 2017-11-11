
'''
number = 1337

number_hex = hex(number).split('x')[-1]

if (len(number_hex) % 2 != 0):
    number_hex = '0' + number_hex

print(number_hex)

number_length = len(number_hex)

print(number_length)

print(number_hex[0])

buffer = bytes([0, 0, ])

hexbuf = bytes.fromhex(number_hex)

print(hexbuf)

print(int.from_bytes(hexbuf, byteorder='big'))

hexbuf += bytes([0, 25, 0])l

print(hexbuf)

print(hexbuf[0], hexbuf[1], hexbuf[2], hexbuf[3], hexbuf[4])

print(int.from_bytes(hexbuf, byteorder='big'))
'''

#buf = bytes([0, 0, 5, 57, 0])

#print("sending out databuf: ", buf)

#retlen, retdata = wiringpi.wiringPiSPIDataRW(0,buf)
#sends out data which is replaced by data from bus

'''

if isinstance(int.from_bytes(retdata, byteorder='big'), int):
    print ()

if isinstance
retdata.decode("utf-8")

'''

#print("|length: ", retlen," | data: ", retdata, " | buf: ", buf, " | int: ", int.from_bytes(retdata, byteorder='big'))
