import wiringpi2 as wp
from subprocess import check_output


INPUT = 0
OUTPUT = 1
LOW = 0
HIGH = 1
PUD_DOWN = 1
PUD_UP = 2
PUD_TRI = 3

states = {'INPUT': 0,'OUPUT': 1,'LOW': 0,'HIGH': 1,'PUD_DOWN': 1,'PUD_UP': 2,'PUD_TRI': 3}
labels = ['wiringPi','GPIO','Physical','Name','SetOUT','SetIN','Mode','Value','SetPin','SetPin']
GPIO = ['17','18','21','22','23','24','25','4','0','1','8','7','10','9','11','14','15']
Phys = ['11','12','13','15','16','18','22','7','3','5','24','26','19','21','23','8','10']
Names = ['GPIO 0','GPIO 1','GPIO 2','GPIO 3','GPIO 4','GPIO 5','GPIO 6','GPIO 7','SDA','SCL','CEO','CE1','MOSI','MISO','SCLK','TxD','RxD']
Mode = ['IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','IN','ALTO','ALTO']

def readPins(pin):
	try:
		return wp.digitalRead(pin)
	except:
		return -1

def writePins(pin, value):
	try:
		wp.digitalWrite(pin, value)
		return 0
	except:
		return -1

def setMode(pin, state):
	try:
		wp.pinMode(pin,state)
		return 0
	except:
		return -1

def readAnalog(chan):
	try:
		return wp.analogRead(chan)
	except:
		return -1
def writeAnalog(chan, data):
	try:
		wp.analogWrite(chan, data)
		return 0
	except:
		return -1
def chgPWM(chan, data):
	try:
		wp.pwmWrite(chan, data)
		return 0
	except:
		return -1

if __name__ == '__main__':
	
	for i in range(0,17):
		print readPins(i)
	for i in range(0,8):
		setMode(i,OUTPUT)
		writePins(i,HIGH)
		wp.delay(100)
		writePins(i,LOW)
		
	print "Now the first 8 pins are set to mode OUT"



