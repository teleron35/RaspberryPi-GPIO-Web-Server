"""
The following Web Server was derived from example code from ws4py.  Specifically code from the example cherrypy_echo_server.py in the ws4py code. 
Copyright (c) 2011-2013, Sylvain Hellegouarch
All rights reserved. 

The rest of the code relies heavily on several different projects.  First the CherryPy project which ws4py runs on top of.  Also a major portion of this project depends on the work of Gordon Henderson and his WiringPi project.  The python wrapper for the WiringPi library was written by Phillip Howard.  Also, Jquery UI was used alot for the web interface.

"""

# -*- coding: utf-8 -*-
import argparse
import random
import os

import cherrypy
import time
from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from gpio_test import labels, GPIO, Names, Phys, Mode, readPins, writePins, setMode, readAnalog, writeAnalog, chgPWM, wp
from subprocess import check_output
import smbus
from gpio_helper import htmlHelper

#setup for wiring pi pinout
wp.wiringPiSetup()
#load required modules
spi = check_output(['gpio','load','spi'])
i2c = check_output(['gpio','load','i2c'])
#setup pin 0 for output to control motor direction and pin 1 for pwm
wp.pinMode(0,1)
wp.pinMode(1,2)
#setup pin6 GPIO25 for button mode
wp.pinMode(6,0)
wp.pullUpDnControl(6, 2) #set pullup
#force pin 0 low and the pwm to 0 
wp.digitalWrite(0,0)
wp.pwmWrite(1,0)
#setup i2c channel,  SMBus channel is zero on rev.1 raspberry pi
bus = smbus.SMBus(0)
address = 0x04


try:
    wp.gertboardAnalogSetup(100)
except:
    print "AD/DA channels already setup.  Try channel 100 or else restart RasPi t clear"




class ChatWebSocketHandler(WebSocket):
    def received_message(self, m):
	 # respond to text input

	 if(m.data.split(":")[0] == "TextBox"):
		 #cherrypy.engine.publish('websocket-broadcast', m)
		 try:
			 p =  check_output(m.data.split(":")[1].strip().split(" "))
			 cherrypy.engine.publish('websocket-broadcast', TextMessage(p))
		 except Exception as e:
			 print e
			 print m.data.split(":")[1].strip().split(" ")
			 cherrypy.engine.publish('websocket-broadcast', TextMessage("Did not work"))
	 # respond to Slider input

	 if(m.data.split(":")[0][0:6] == "Slider"):
		 #cherrypy.engine.publish('websocket-broadcast', m)
		 if m.data.split(":")[0][6:] == "1":
			 writeAnalog(100, int(m.data.split(":")[1].strip()))
			 data=str(readAnalog(100))
			 cherrypy.engine.publish('websocket-broadcast', TextMessage("Ana1: " + data))
			 #cherrypy.engine.publish('websocket-broadcast', m)

		 elif m.data.split(":")[0][6:] == "2":
		 	 writeAnalog(101, int(m.data.split(":")[1].strip()))
			 data=str(readAnalog(101))
			 cherrypy.engine.publish('websocket-broadcast', TextMessage("Ana2: " + data))
			 #cherrypy.engine.publish('websocket-broadcast', m)

		 elif m.data.split(":")[0][6:] == "3":
		 	 cherrypy.engine.publish('websocket-broadcast', m)

		 elif m.data.split(":")[0][6:] == "4":
			 cherrypy.engine.publish('websocket-broadcast', m)

		 else:
		 	 pass

	 if(m.data.split(":")[0][0:4] == "Mode"):
		 #cherrypy.engine.publish('websocket-broadcast', m)
		 try:
			 setMode(int(m.data.split(":")[0][4:]), int(m.data.split(":")[1].strip()))
		 except:
		 	 pass


	 # respond to button input

	 if(m.data.split(":")[0][0:3] == "Pin"):
	 	 if readPins(int(m.data.split(":")[0][3:])) == 0:
		 	 writePins(int(m.data.split(":")[0][3:]), 1)
		 else:
		 	 writePins(int(m.data.split(":")[0][3:]), 0)

	 # respond to pwm signals, this has been setup for outputs 0 (for direction control) and 1 for pwm signal

	 if(m.data.split(":")[0]== "PWM"):
		 chgPWM(1, int(m.data.split(":")[1].strip()))
		 cherrypy.engine.publish('websocket-broadcast', TextMessage("PWM: " + m.data.split(":")[1].strip()))

	 # respond to status input

	 if(m.data.split(":")[0]== "Status"):
		 #cherrypy.engine.publish('websocket-broadcast', TextMessage("clearText"))
		 s = check_output(['sudo','gpio','readall'])
		 t = s.split("\n")
		 for i in range(3,20):
			 q = "Stat:" + t[i].split("|")[1].strip() + ":" + t[i].split("|")[5].strip() + ":" + t[i].split("|")[6].strip()
			 cherrypy.engine.publish('websocket-broadcast', TextMessage(q))
		 #cherrypy.engine.publish('websocket-broadcast', TextMessage(s))

	 # respond to analogRead input

	 if(m.data.split(":")[0] == "Analog"):
		 #cherrypy.engine.publish('websocket-broadcast', m)
		 data=str(readAnalog(100))
		 cherrypy.engine.publish('websocket-broadcast', TextMessage("Ana1: " + data))
		 data=str(readAnalog(101))
		 cherrypy.engine.publish('websocket-broadcast', TextMessage("Ana2: " + data))

	 if(m.data.split(":")[0] == "Servo"):
		 """
		 if (m.data.split(":")[1].strip() == "1"):
		 	bus.write_byte(address, 1)
		 elif (m.data.split(":")[1].strip() == "10"):
		 	bus.write_byte(address, 10)
		 elif (m.data.split(":")[1].strip() == "20"):
		 	bus.write_byte(address, 20)
		 elif (m.data.split(":")[1].strip() == "30"):
		 	bus.write_byte(address, 30)
		 elif (m.data.split(":")[1].strip() == "40"):
		 	bus.write_byte(address, 40)
		 elif (m.data.split(":")[1].strip() == "50"):
		 	bus.write_byte(address, 50)
		 elif (m.data.split(":")[1].strip() == "60"):
		 	bus.write_byte(address, 60)
		 elif (m.data.split(":")[1].strip() == "70"):
		 	bus.write_byte(address, 70)
		 elif (m.data.split(":")[1].strip() == "80"):
		 	bus.write_byte(address, 80)
		 elif (m.data.split(":")[1].strip() == "90"):
		 	bus.write_byte(address, 90)
		 elif (m.data.split(":")[1].strip() == "100"):
		 	bus.write_byte(address, 100)
		 elif (m.data.split(":")[1].strip() == "110"):
		 	bus.write_byte(address, 110)
		 elif (m.data.split(":")[1].strip() == "120"):
		 	bus.write_byte(address, 120)
		 elif (m.data.split(":")[1].strip() == "130"):
		 	bus.write_byte(address, 130)
		 elif (m.data.split(":")[1].strip() == "140"):
		 	bus.write_byte(address, 140)
		 elif (m.data.split(":")[1].strip() == "150"):
		 	bus.write_byte(address, 150)
		 elif (m.data.split(":")[1].strip() == "160"):
		 	bus.write_byte(address, 160)
		 elif (m.data.split(":")[1].strip() == "170"):
		 	bus.write_byte(address, 170)
		 elif (m.data.split(":")[1].strip() == "180"):
		 	bus.write_byte(address, 180)
		 else:
		 	pass
		 """
		 bus.write_byte(address, int(m.data.split(":")[1].strip()))
		 time.sleep(0.015)
		 cherrypy.engine.publish('websocket-broadcast', TextMessage("Servo: " + m.data.split(":")[1].strip()))
		

    def closed(self, code, reason="A client left the room without a proper explanation."):
        cherrypy.engine.publish('websocket-broadcast', TextMessage(reason))

class Root(object):
    def __init__(self, host, port, ssl=False):
        self.host = host
        self.port = port
        self.scheme = 'wss' if ssl else 'ws'
	self.connection = { 'scheme':self.scheme, 'host':self.host, 'port':self.port }


    @cherrypy.expose
    def index(self):
	    return htmlHelper(self.connection)

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

if __name__ == '__main__':
    import logging
    from ws4py import configure_logger
    configure_logger(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='GPIO RaspberryPi CherryPy Server')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('-p', '--port', default=9000, type=int)
    parser.add_argument('--ssl', action='store_true')
    args = parser.parse_args()

    cherrypy.config.update({'server.socket_host': args.host,
                            'server.socket_port': args.port,
                            'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__) , 'static'))})

    if args.ssl:
        cherrypy.config.update({'server.ssl_certificate': './server.crt',
                                'server.ssl_private_key': './server.key'})

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(Root(args.host, args.port, args.ssl), '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': ChatWebSocketHandler
            },
        '/js': {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': 'js'
            },
	'/img': {
	      'tools.staticdir.on': True,
	      'tools.staticdir.dir': 'img'
	    },
	'/css': {
	      'tools.staticdir.on': True,
	      'tools.staticdir.dir': 'css'
	    }
        }
    )
