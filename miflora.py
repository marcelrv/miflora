#!/usr/bin/python
# -*- mode: python; coding: utf-8 -*-

# Scans for and reads data from Xiaomi flower monitor and publish via MQTT
# Tested on firmware version 2.6.2 &  2.6.6 
# Xiaomi flower protocol & code from https://wiki.hackerspace.pl/projects:xiaomi-flora by emeryth (emeryth at hackerspace.pl)
# Author Marcel Verpaalen

from struct import unpack
import paho.mqtt.publish as publish
from gattlib import DiscoveryService, GATTRequester, GATTResponse

verbose = True

service = DiscoveryService("hci0")
devices = service.discover(5)

baseTopic = "/miflower/"
msgs=[]

for address, name in list(devices.items()):
	if (name == "Flower mate"):
		topic= baseTopic + address.replace(':', '') + '/'
		requester = GATTRequester(address, True)
		#Read battery and firmware version attribute
		data=requester.read_by_handle(0x0038)[0]
		battery, firmware = unpack('<B6s',data)
		msgs.append({'topic': topic + 'battery', 'payload':battery})
		msgs.append({'topic': topic + 'firmware', 'payload':firmware})
		#Enable real-time data reading
		requester.write_by_handle(0x0033, str(bytearray([0xa0, 0x1f])))
		#Read plant data
		data=requester.read_by_handle(0x0035)[0]
		temperature, sunlight, moisture, fertility = unpack('<hxIBHxxxxxx',data)
		msgs.append({'topic': topic + 'temperature', 'payload':temperature/10.})
		msgs.append({'topic': topic + 'sunlight', 'payload':sunlight})
		msgs.append({'topic': topic + 'moisture', 'payload':moisture})
		msgs.append({'topic': topic + 'fertility', 'payload':fertility})
		if (verbose):
			print("name: {}, address: {}".format(name, address))
			print "Battery level:",battery,"%"
			print "Firmware version:",firmware
			print "Light intensity:",sunlight,"lux"
			print "Temperature:",temperature/10.," C"
			print "Soil moisture:",moisture,"%"
			print "Soil fertility:",fertility,"uS/cm"
if (len(msgs) > 0):
	publish.multiple(msgs, hostname="localhost", port=1883, client_id="miflower", keepalive=60,will=None, auth=None, tls=None)
