# OctoPrint Power Switch

This OctoPrint plugin is designed to run on Rasperry Pi with PowerSwitch Tail II or any other relay. It lets the user to power 3D printer on and off from OctoPrint web interface.

Relay is controled via one of Raspberry Pi's GPIO PINs.

## Setup

Install via the bundled [Plugin Manager] or manually using this URL:

    https://github.com/azhilyakov/OctoPrint-PowerSwitch/archive/master.zip

## Configuration

1. Install pgpio library: http://abyz.co.uk/rpi/pigpio/
```
	wget abyz.co.uk/rpi/pigpio/pigpio.zip
	unzip pigpio.zip
	cd PIGPIO
	make
	sudo make install
	sudo /usr/local/bin/pigpiod -l

	sudo vi /etc/rc.local
	Add line: /usr/local/bin/pigpiod -l
```
2) Connect one of Raspberry Pi's GPIO pins to a relay such as PowerSwitch Tail II

3) Go to PowerSwitch plugin settings and set pin number of the relay connection



