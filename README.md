# beacon-tracker

## Description
Simple python program to track advertisemets from BLE devices.

Initial scan determins the average advertisment interval and then tracks a specificed device to determine how long it was active for.  Developed to track the battery life of esp32 ble devices

## Installation

Clone the repo:
```
git clone https://github.com/twobit-five/beacon-tracker.git

```

Create a virtual enviroment: (RECOMENDED):
```
cd beacon-tracker
python -m venv .venv
```

Activate the enviroment:

Linux:
```
source .venv/bin/activate
```

Windows:
```
.venv/bin/activate
```

Install the requirements.
```
pip install -r requirements.txt
```

run the program:
```
python app.py
```

## Options
```
usage: app.py [-h] [-s SCAN_DURATION] [-d SCAN_DELAY] [-t DEVICE_TIMEOUT_PERIOD] [-a ADVERTISEMENT_SCAN_DURATION] [-n TARGET_DEVICE_NAME] [-u TARGET_SERVICE_UUID]
              [-p PROGRAM_TIMEOUT_PERIOD]

options:
  -h, --help            show this help message and exit
  -s SCAN_DURATION, --scan_duration SCAN_DURATION
                        Scan duration in seconds
  -d SCAN_DELAY, --scan_delay SCAN_DELAY
                        Scan delay in seconds
  -t DEVICE_TIMEOUT_PERIOD, --device_timeout_period DEVICE_TIMEOUT_PERIOD
                        Device timeout period in minutes
  -a ADVERTISEMENT_SCAN_DURATION, --advertisement_scan_duration ADVERTISEMENT_SCAN_DURATION
                        Advertisement scan duration in seconds
  -n TARGET_DEVICE_NAME, --target_device_name TARGET_DEVICE_NAME
                        Target device name
  -u TARGET_SERVICE_UUID, --target_service_uuid TARGET_SERVICE_UUID
                        Target service UUID
  -p PROGRAM_TIMEOUT_PERIOD, --program_timeout_period PROGRAM_TIMEOUT_PERIOD
                        Program timeout period in minutes
```
## Global Variables
The global variables should be adjusted to fit your scanning needs.

Default Value: 

### scan_duration
This is the duration which each scan lasts

Default Value: 10 (in seconds)

### scan_delay
This is the delay between scans.

Default Value: 30 (in seconds)

### device_timeout_period
This is the period of time after the program has last heard from a device before it is removed from the dictionary and the program exits.

Default Value: 3 (in minutes)

### advertisement_scan_duration
This is the initial scan which determines the average advertisment interval for a device.  The device must be broadcasting prior to running the program to get an accurate reading.

Default Value: 30 (in seconds)

### TARGET_DEVICE_NAME 
The scans will be filtered from the list of device names. No other device statistics will be tracked.

Default Value: 'Dangerous-Vehicle'

### TARGET_SERVICE_UUID
This field is passed into the filter of the BLeakScanner constructor to filter based upon specific UUID's

Default Value: '6362b48b-130c-4e9e-9e48-c068f959084b'

### program_timeout_period
NOT IMPLEMTED YET

Default Value: N/A

## Program Output
X's during scanning indicate the device was not found during the scan interval.

.'s during a scan indicates the device was found during the scan interval.

``` Sample Output
******************************************************************
Starting program...
Press Ctrl+C to exit

******************************************************************
******************************************************************
Program Start time:  2023-06-08 14:00:00.234387
Program Timeout:  1  minutes (LOGIC NOT IMPLEMENTED)
Target Device Name: Dangerous-Vehicle
Target Service UUID: 6362b48b-130c-4e9e-9e48-c068f959084b
Scan Duration: 10 seconds
Scan Delay: 30 seconds
Device Timeout: 3 minutes
Advertisement Scan Duration: 30 seconds
******************************************************************

Performing Initial scan to determine advertising interval...
/home/kali/src/beacon-tracker/beacon-tracker/app.py:38: FutureWarning: This method will be removed in a future version of Bleak. Use the detection_callback of the BleakScanner constructor instead.
  scanner.register_detection_callback(detection_callback)
Advertisng Report for 34:85:18:07:0A:D2:
    Advertising count: 3 over 30 seconds
    Avg Adv Interval: 10.0 seconds

Device registered:  2023-06-08 14:00:40.407405
{'34:85:18:07:0A:D2': {'device_name': 'Dangerous-Vehicle', 'advertisement_count': 3, 'first_heard': datetime.datetime(2023, 6, 8, 14, 0, 1, 949109), 'last_heard': datetime.datetime(2023, 6, 8, 14, 0, 40, 407309)}}
...................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................XXXX

Device 34:85:18:07:0A:D2 report:
  Device name: Dangerous-Vehicle
  First heard: 2023-06-08 14:00:01.949109
  Last heard: 2023-06-08 21:20:00.677218
  Active time: 7:19:58.728109 (approximately 7.33 hours)
```

## Future Work
- [X] Add command line options
- [ ] Update Deprecated detection_callback method to register callback (Use constructor instead)
- [ ] Improve documentation
- [ ] Add verbose flag which prints each received beacon.
