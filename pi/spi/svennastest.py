import wiringpi

INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1
mosi = 0
miso = 2
sclk = 3 

wiringpi.wiringPiSetup()

wiringpi.pinMode(mosi, OUTPUT)
wiringpi.pinMode(miso, INPUT)
wiringpi.pinMode(sclk, OUTPUT)

print 'qwerty'

wiringpi.delay(1500) #delay for 1.5 seconds

wiringpi.digitalWrite(mosi, HIGH)
wiringpi.delay(1500)

print 'tjo'

wiringpi.delay(1000)
wiringpi.shiftOut(mosi, sclk, 0, 65)

print 'hejdo'
