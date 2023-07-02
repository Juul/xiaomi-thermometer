Some scripts for talking to Xiaomi thermometers (e.g. LYWSD03MMC) running [pvvx's firmware](https://github.com/pvvx/ATC_MiThermometer).

It seems that most of the hard work for this firmware was originally done by [atc1441](https://github.com/atc1441/ATC_MiThermometer).

Tested with pvvx's firmware version 4.3 and a LYWSD03MMC

These are very rough prototypes but they do work.

# Dependencies

```
sudo apt install python3 python3-pip 
sudo pip3 install bluepy
```

# Get MAC address

To get the MAC address of your thermometer, scan for BLE devices using:

```
sudo hcitool lescan
```
and look for devices where the name begins with `ATC_`.

# listen.py

Passively listen for temperature and humidity announcements. Add your device's MAC address to "valid_sensors" in `listen.py`. 

You might also want to change the timeout.

Must be run as root.

# retrieve.py

Retrieve stored measurements.

Change the `sensor_mac` and `number_of_datapoints` variables toward the top of the file to your liking.

Must be run as root.
