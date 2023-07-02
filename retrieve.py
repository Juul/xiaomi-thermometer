#!/usr/bin/env python3

import time
from datetime import datetime

from bluepy.btle import Scanner, DefaultDelegate, Peripheral

# TODO disconnect properly on error
# TODO retry connection a few times before failing

number_of_datapoints = 100 # how many datapoints to download (max)
sensor_mac = "a4:c1:38:eb:00:ab"

# offset from UTC in seconds
timezoneOffset = -time.localtime().tm_gmtoff

def parseData(data):
    count = int.from_bytes(data[1:3], byteorder='little', signed=False)
    tc = int.from_bytes(data[3:7], byteorder='little', signed=False)
    temp = int.from_bytes(data[7:9], byteorder='little', signed=True) / 100.0
    humid = int.from_bytes(data[9:11], byteorder='little', signed=False) / 100.0
    vbatt = int.from_bytes(data[11:13], byteorder='little', signed=False) / 1000.0
    t = datetime.fromtimestamp(tc + timezoneOffset)
    
    print("Count: %s, Temperature: %s, Humidity: %s, vBatt: %s" % (str(count), str(temp), str(humid), str(vbatt)))
    print("  --time:", t.strftime("%A, %B %d, %Y %I:%M:%S"))

class NotifyDelegate(DefaultDelegate):
    def __init__(self, handle):
        DefaultDelegate.__init__(self)
        self.handle = handle
        
    def handleNotification(self, cHandle, data):

#        print("Handle: %s cHandle: %s" % (str(self.handle), str(cHandle)))
#        print("  data:", data)
        
        blkid = int.from_bytes(data[0:1], byteorder='little', signed=False)
        if blkid == 0x55: # got configuration
            # Request logged temperature/humidity data
            # First byte is the command,
            # second two are the number of samples to request (most significant byte first)
            # TODO catch exception that occurs if no response is received
            char.write(b'\x35\x00\xff', withResponse=True)
        elif blkid == 0x35:
            parseData(data)

device = Peripheral(sensor_mac)
    
service = device.getServiceByUUID(0x1F10)
chars = service.getCharacteristics(0x1F1F)
char = chars[0]
handle = char.getHandle()

device.withDelegate(NotifyDelegate(handle))

time.sleep(1)
# TODO catch exception that occurs if no response is received
char.write(b'\x55', withResponse=True)

while True:
    if device.waitForNotifications(5.0):
        continue

