# beacon-tracker

## Description
Simple python program to track advertisemets from BLE devices.

Initial scan determins the average advertisment interval and then tracks a specificed device to determine how long it was active for.  Developed to track the battery life of esp32 ble devices

## Global Variables
The global variables should be adjusted to fit your scanning needs.

### TARGET_DEVICE_NAME 
The scans will be filtered from the list of device names. No other device statistics will be tracked.

### TARGET_SERVICE_UUID
This field is passed into the filter of the BLeakScanner constructor to filter based upon specific UUID's

### scan_delay
This is the delay between scans.

### device_timeout_period
This is the period of time after the program has last heard from a device before it is removed from the dictionary and the program exits.

### program_timeout_period
NOT IMPLEMTED YET

### scan_duration
This is the duration which each scan lasts

### advertisement_scan_duration
This is the initial scan which determines the average advertisment interval for a device.  The device must be broadcasting prior to running the program to get an accurate reading.

## Program Output
X's during scanning indicate the device was not found during the scan interval.

.'s during a scan indicates the device was found during the scan interval.

#TODO 
Improve documentation
