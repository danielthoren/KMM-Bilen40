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
    
#buf = bytes("gurra","UTF-8")
buf = bytes([116, 117, 114, 110, 101, 114, 0])

print(buf)

retlen, retdata = wiringpi.wiringPiSPIDataRW(0,buf)



print("length ",retlen," data ",retdata, " buf ", buf)
