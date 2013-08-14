RaspberryPi-GPIO-Web-Server
===========================

This repo contains a CherryPy based ws4py websocket server to connect a web browser to the RaspberryPi GPIO in realtime.

To use this repo, you must have several things modules and programs installed and have some hardware compatible with the RaspberryPi GPIO.  First you will need to make sure you have the following software:

1.  This project assumes RaspberryPi running raspbian distro.
2.  Python Ver. 2.x
3.  CherryPy Ver. 3.x
4.  ws4py Ver. 1.x
5.  WiringPi2
6.  WiringPi2-Python
7.  Jquery UI, optional to install or could just point to it in script header

This project also assumes that you have certain hardware to connect to the output of the RaspberryPi GPIO.  I have used a Gertboard and have used the following functionality of the Gertboard for demo purposes:

1.  Buffered I/O for LEDs and Buttons.
2.  Analog to Digital Converter MCP3002 to be used on the SPI bus
3.  Digital to Analog Converter MCP4802 to be used on the SPI bus
4.  ATMega328 microcontroller to be used on the i2c bus which controls a servo
5.  H-Bridge L6203-MW to be used with the RaspberryPi onboard PWM pin

With the proper jumper configurations, a Gertboard Version 1, and an off board motor and servo with two different power supplies for each, you could configure this entire project.

The project aim is to test all of the functionality of the RaspberryPi GPIO using the gertboard for IO breakout.  In addition, this has been implemented over WebSocket so as to enable realtime control and feedback.  This will be explained later in this document. 
