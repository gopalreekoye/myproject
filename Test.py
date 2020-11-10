import signal
import sys
import RPi.GPIO as GPIO
import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading
import time
import math


#spi bus
spi = busio.SPI(clock =board.SCK, MISO = board.MISO, MOSI=board.MOSI)

#chip select
cs= digitalio.DigitalInOut(board.D5)

#mcp object
mcp =MCP.MCP3008(spi, cs)

#analog input on pin1
chan=AnalogIn(mcp, MCP.P1)
chanLDR=AnalogIn(mcp, MCP.P2)





switch=0

def signal_handler(sig, frame):
	GPIO.cleanup()
	sys.exit(0)

def my_callback(channel):
	
	global switch
	if switch==0:
		switch=1
		print('Runtime       Luminosity      Temp')
		global t0
		global sample_rate
		t0=time.time()
		sample_rate=10
		print_data()
		while True:
			input_state=GPIO.input(5)
			if input_state==False:
				if sample_rate==10:
					sample_rate=5
				elif sample_rate==5:
					sample_rate=1
				else:
					sample_rate=10
			pass
	else:
		sys.exit(0)
	print(str(switch))


def print_data():

	thread=threading.Timer(sample_rate, print_data)
	thread.daemon=True
	thread.start()
	t1=time.time()
	runtime=math.floor(t1-t0)
	ta=(chan.voltage-.5)/0.01
	print(str(runtime)+'s      '+str("{:.1f}".format(chanLDR.voltage*1333))+'        '+str(ta)+'   C')


if __name__ == '__main__':
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	
	

	GPIO.add_event_detect(6, GPIO.FALLING, callback=my_callback, bouncetime=200)

	signal.signal(signal.SIGINT, signal_handler)
	signal.pause()
