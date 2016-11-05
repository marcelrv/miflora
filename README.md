# Xiaomi mi flora

Script to read Xiaomi Flora values and publish it via MQTT to be used in Openhab or other home automation

It will scan for all Xiaomi miflora devices and publish the values to the MQTT server.

Paho (mqtt) and gatt libraries are required.

to install :
```
sudo apt-get install python-pip
pip install paho-mqtt
pip install gattlib
```

this requires Bluez 5.37 or higher to be installed as well

To run this as non-root run the following
```
sudo setcap cap_net_raw+eip $(eval readlink -f `which python`)
```

to run this in an automated way every 30 min add to the crontab the script:
```
$ crontab -e
```
add the line:
```
*/30 * * * * /usr/bin/python /home/ubuntu/miflower.py
```
(replace the last part with your file name & path)

Based on the script created by emeryth https://wiki.hackerspace.pl/projects:xiaomi-flora

