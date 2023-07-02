#!/usr/bin/env python3

from bluepy.btle import Scanner, DefaultDelegate

valid_sensors = {
    "a4:c1:38:eb:00:ab" : "lab1"
}

stop_listen_after = 120.0 # stop listening after this many seconds

class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleSensorPacket(self, sensor_mac, data):
#        print("Data length:", len(data))
        data = bytes.fromhex(data)  
#        name = valid_sensors[sensor_mac]
        temperature = int.from_bytes(data[8:10],byteorder='little',signed=True)
        temperature = str(temperature / 100.0)
        humidity = int.from_bytes(data[10:12],byteorder='little',signed=True)
        humidity = humidity
        humidity = str(humidity / 100.0)
        battery = int.from_bytes(data[12:14],byteorder='little',signed=False)
        battery = str(battery / 1000.0)
        battpercent = int.from_bytes(data[14:15], byteorder="little", signed=False)
        count = int.from_bytes(data[15:16], byteorder="little", signed=False)
        
        print("temp: %s , humid: %s , batt: %s, batt_percent: %s, count: %s"%(temperature,humidity, str(battery), str(battpercent), str(count)))
        
    def handleDiscovery(self, dev, isNewDev, isNewData):
        
        if(dev.addr in valid_sensors):
            name = valid_sensors[dev.addr]

            if isNewDev:
                print("Discovered:", name)
            elif isNewData:
                print("New data from:", name)
            else:
                print("Unchanged data from:", name)
            
            for (adtype, desc, value) in dev.getScanData():
#                print("desc:", desc)
                
                if("Service" in desc):
                    self.handleSensorPacket(dev.addr, value)


            
scanner = Scanner().withDelegate(ScanDelegate())

# First argument is timeout in seconds
devices = scanner.scan(stop_listen_after, passive=True)
